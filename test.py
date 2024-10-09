from mock import patch
import sys
from sys import stdout

#example test function
def to_test():
    name = input("Please enter name")
    print(f"Hello, {name}!")
    age = input("How old are you?")
    print(f"{age} is soooo old!")

#test io
input_overflow = "Too many input calls"

test_inputs = [["Ada","39"],["Bob","12"]]
test_iter : iter
expected_outputs = ["Hello, Ada!\n39 is soooo old!","Hello, Bob!\n12 is soooo old!"]

def next_input():
    this_input = next(test_iter, input_overflow)
    if this_input == input_overflow:
        print(input_overflow)
    return this_input

def run_tests(code : function, test_in, expected_out):
    global test_iter 
    test_iter = iter(test_in)
    with patch("builtins.input", side_effect = next_input), patch("sys.stdout", new=io.StringIO()) as fake_out:
        code()
    print(expected_out)
    print(fake_out)

for i in range(len(test_inputs)):
    run_tests(to_test, test_inputs[i],expected_outputs[i])

