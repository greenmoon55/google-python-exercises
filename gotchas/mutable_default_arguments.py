# A new list is created once when the function is defined
def append_to(element, to=[]):
    to.append(element)
    return to

my_list = append_to(12)
print my_list

my_other_list = append_to(42)
print my_other_list
