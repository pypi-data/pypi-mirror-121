from .class import Calculate

def method_test(self, num):
    return num

def use_class(self):
    my_class = Calculate()
    sum = my_class.sum()
    div = my_class.division()

    return sum, div
