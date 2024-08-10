"""
scheduling utility functions
ex. isBusDay, bump_date
"""
import datetime
import holidays


def isBusDay(d: datetime.date,
             calendar: str = "nyse") -> bool:
    holidays_ = holidays.country_holidays(calendar.upper())
    return (d not in holidays_) and (d.weekday() not in [5, 6])


def getHoliday(d: datetime.date,
               calendar: str = "nyse") -> str:
    holidays_ = holidays.country_holidays(calendar.upper())
    return holidays_.get(d)


if __name__ == "__main__":
    my_date = datetime.date(2023, 9, 4)
    # my_date.weekday()
    print(isBusDay(my_date, "US"))
    # holidays_ = holidays.country_holidays("NYSE")
    print(getHoliday(my_date))
