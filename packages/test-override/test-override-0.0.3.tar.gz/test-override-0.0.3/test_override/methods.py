from test_override.my_class import Calculate

def method_test(num):
    return num

def use_class():
    my_class = Calculate()
    sum = my_class.sum()
    div = my_class.division()

    return sum, div
