class Employee:
    def __init__(self, first_name, last_name):
        self.first = first_name
        self.last = last_name

    @classmethod
    def from_more_params(cls, param_dict):
        return cls(dict['first'], dict['last'])

    @staticmethod
    def calc_len():
        pass

    def __len__(self):
        return 6

    def __eq__(self, other):
        return self.first == other.first and self.last == other.last

    def __hash__(self):
        pass

    def __repr__(self):
        pass

    def __str__(self):
        pass

    def __call__(self, *args, **kwargs):
        pass


if __name__ == '__main__':
    emp1 = Employee('add', 'cdd')
    emp2_dict = dict({'first': 'add', 'last': 'c3d'})
    emp2 = Employee.from_more_params(emp2_dict)

    print(emp1 == emp2)
