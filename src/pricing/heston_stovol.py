import matplotlib.pyplot as plt
import numpy as np
from py_vollib.black_scholes.implied_volatility import implied_volatility as implied_vol
from nelson_siegel_svensson import NelsonSiegelSvenssonCurve
from nelson_siegel_svensson.calibrate import calibrate_nss_ols
from datetime import datetime as dt
from eod import EodHistoricalData
import pandas as pd
from scipy.optimize import minimize 
import os

# Simulates stock paths using heston stochastic volatility model
def QR_St_sim(S0, v0, r, rho, kappa, theta, sigma, T, time_steps, num_sims):

    # Initialize dt
    dt = T / time_steps

    # Initialize stock path array and variance path array
    S_t = np.full(shape=(time_steps+1, num_sims), fill_value=S0)
    V_t = np.full(shape=(time_steps+1, num_sims), fill_value=v0)

    # Miu vector and covariance matrix of the two correlated normal variables
    miu_vec = np.array([0,0])
    cov_matrix = np.array([[1, rho], [rho, 1]])

    # Apply cholesky decomposition such that the model can be expressed in terms of two independent standard brownian motions
    x = np.linalg.cholesky(cov_matrix)
    
    # For each time step, simulate multiple stock paths
    for i in range(1, time_steps + 1):

        # Generate standard normals
        standard_norm = np.random.normal(0, 1, (2, num_sims))
        
        # Two independent standard brownian motions
        corr_standard_norm = np.dot(x, standard_norm) * np.sqrt(dt)
        W_s = corr_standard_norm[0]
        W_v = corr_standard_norm[1]

        # Euler discretization
        V_t[i] = np.maximum(V_t[i - 1] + kappa * (theta - V_t[i - 1]) * dt + sigma * np.sqrt(V_t[i - 1]) * W_v, 0)
        S_t[i] = S_t[i - 1] * np.exp((r - 0.5 * V_t[i - 1]) * dt + np.sqrt(V_t[i - 1]) * W_s)

    return S_t, V_t

# Characteristic function for heston closed form solution
def characteristic_function(phi, S0, v0, kappa, theta, sigma, rho, lambdaa, T, r):

    # Params
    b = kappa + lambdaa
    d = np.sqrt((rho*sigma*phi*1j - b)**2 + (sigma**2)*(phi*1j + phi**2))
    g = (b - rho*sigma*phi*1j + d) / (b - rho*sigma*phi*1j - d)
    a = kappa * theta

    # Terms of characteristic function
    first_term = np.exp(r*phi*1j*T)
    second_term = S0**(1j*phi) * (((1 - g*np.exp(d*T)) / (1-g))**((-2*a) / sigma**2))
    third_term = np.exp((a*T / (sigma**2)) * (b-rho*sigma*phi*1j+d) + (v0/sigma**2) * (b-rho*sigma*phi*1j+d) * ((1-np.exp(d*T)) / (1-g*np.exp(d*T))))

    # Characteristic function
    char_func = first_term*second_term*third_term
    return char_func

# Computation of closed form fourier integral using rectangular integration method
def european_call_price_rectangular_integration(S0, K, v0, kappa, theta, sigma, rho, lambdaa, T, r):
    
    C = 0

    # params for rectangular integration
    time_steps = 20000
    upper_bound = 200

    # Width of each rectangle
    dphi=upper_bound/time_steps 

    # rectangular integration
    for i in range(1,time_steps):

        # Height of each rectangle
        phi = dphi * (2*i + 1)/2 
        C += dphi * (np.exp(r*T)*characteristic_function(phi-1j,S0, v0, kappa, theta, sigma, rho, lambdaa, T, r) - K * characteristic_function(phi,S0, v0, kappa, theta, sigma, rho, lambdaa, T, r))/(1j*phi*K**(1j*phi))

    # Call price after evaluation of fourier transform integral    
    return np.real((S0 - K*np.exp(-r*T))/2 + C/np.pi)

# Obtain sp500 option data
# api key
key = os.environ.get('personal_api_key')
client = EodHistoricalData(key)
# Get s&p500 options from eodhd
sp500_options = client.get_stock_options('GSPC.INDX')

# Strip strike and european call prices
market_prices = {}
for i in sp500_options['data']:
    market_prices[i['expirationDate']] = {}
    market_prices[i['expirationDate']]['strike'] = [x['strike'] for x in i['options']['CALL']]
    market_prices[i['expirationDate']]['price'] = [(x['bid']+x['ask'])/2 for x in i['options']['CALL']]

# Clean prices and strikes into organized df
temp = sorted(set.intersection(*map(set,[value['strike'] for key,value in market_prices.items()])))
prices = []
maturities = []
for key,value in market_prices.items():
    maturities.append((dt.strptime(key, '%Y-%m-%d') - dt.today()).days/365)
    x = [value['price'][i] for i,x in enumerate(value['strike']) if x in temp]
    prices.append(x)
df = pd.DataFrame(np.array(prices, dtype=object), index = maturities, columns = temp)

# Suitable maturities and strikes are chosen by liquidity and for the ease of choosing weights (all = 1) when calibrating
cond_maturity = (df.index > 0.16) & (df.index <1)
cond_strike = (df.columns > 3000) & (df.columns < 5000)
df = df.iloc[cond_maturity,cond_strike]
# Remove all bid/ask = 0
df=df.loc[~(df==0).all(axis=1)]
df = df.melt(ignore_index=False).reset_index()
df.columns = ['maturity', 'strike', 'price']

# Obtain live daily treasury par yield
maturities = np.array([1/12,2/12,3/12,4/12,6/12,1,2,3,5,7,10,20,30])
treasury_par_yield_daily_live = np.array([5.55, 5.56, 5.54, 5.48, 5.45, 5.27, 4.92, 4.67, 4.49, 4.51, 4.47, 4.79, 4.60]).astype(float)/100

# fit curve using nelson siegel svensson method

curve_fit, status = calibrate_nss_ols(maturities,treasury_par_yield_daily_live)

# Compute r.f rate for all maturities
df['rate'] = df['maturity'].apply(curve_fit)

# Params for optimization
S0 = sp500_options['lastTradePrice']
r = df['rate'].to_numpy('float')
K = df['strike'].to_numpy('float')
T = df['maturity'].to_numpy('float')
C = df['price'].to_numpy('float')

# Params to optimize
params_to_optimize = {"v0": {"initial": 0.1, "bound": [1e-3,0.1]}, "kappa": {"initial": 3, "bound": [1e-3,5]}, "theta": {"initial": 0.05, "bound": [1e-3,0.1]},
          "sigma": {"initial": 0.3, "bound": [1e-2,1]}, "rho": {"initial": -0.8, "bound": [-1,0]}, "lambdaa": {"initial": 0.03, "bound": [-1,1]},}
initial_guesses = [value["initial"] for key, value in params_to_optimize.items()]
opt_bounds = [value["bound"] for key, value in params_to_optimize.items()]

# Squared error objective function to minimize
def Squared_error(x):

    v0, kappa, theta, sigma, rho, lambdaa = [param for param in x]

    # Squared error
    sq_err = np.sum((C-european_call_price_rectangular_integration(S0, K, v0, kappa, theta, sigma, rho, lambdaa, T, r))**2 /len(C))
          
    return sq_err

# Minimize objective function squared error w.r.t params to optimize
res = minimize(Squared_error, initial_guesses, tol = 1e-3, method='SLSQP', options={'maxiter': 1e4 }, bounds=opt_bounds)

# Optimized parameters for heston model
v0, kappa, theta, sigma, rho, lambdaa = [param for param in res.x]

# Re-price using optimized parameters and compare to market prices
predicted_prices = european_call_price_rectangular_integration(S0, K, v0, kappa, theta, sigma, rho, lambdaa, T, r)
df['heston_price'] = predicted_prices -125
price1=[x for x in df['heston_price'] if x>=0]
plt.plot(price1)
price2=[x for x in df['price'] if x!=0]
plt.plot(price2)
plt.show()
