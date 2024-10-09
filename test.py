import unittest
from unittest.mock import patch
from io import StringIO
from inspect import signature

#test data
io_test_cases = [
    {
        "inputs": ["Ada", "39"],
        "expected_output": "Hello, Ada!\n39 is soooo old!\n"
    },
    {
        "inputs": ["Bob", "12"],
        "expected_output": "Hello, Bob!\n12 is soooo old!\n"
    }
]
results = []
func_test_cases = [
    {
        "params" : [3,5],
        "expected" : 15 
    },
    {
        "params" : [2.2,10],
        "expected" : 22 
    }
]
#example test functions
def io_to_test():
    name = input("Please enter name")
    print(f"Hello, {name}!")
    age = input("How old are you?")
    print(f"{age} is soooo old!")
def func_to_test(a,b):
    return a* b

#test io
def test_io(func):
    for case in io_test_cases:
        with patch("builtins.input", side_effect=case["inputs"]), patch("sys.stdout", new=StringIO()) as fake_out:
            try:
                func()
            except StopIteration:
                print("Too many input calls")
                
        result = {
            "inputs": case["inputs"],
            "expected_output": case["expected_output"].strip(),
            "actual_output": fake_out.getvalue().strip(),
            "passed": fake_out.getvalue().strip() == case["expected_output"].strip()
        }
        results.append(result)
#test function with return
def test_func(func):
    for case in func_test_cases:
        if func.__code__.co_argcount == len(case["params"]):
            actual = func(*case["params"])
            result = {
                "params" : case["params"],
                "expected" : case["expected"],
                "actual" : actual,
                "passed" : actual == case["expected"]
            }
            results.append(result)
        else:
            result = {
                "params" : case["params"],
                "expected" : case["expected"],
                "actual" : "Error wrong number of parameters",
                "passed" : False
            }
            results.append(result)


if __name__ == '__main__':
    test_func(func_to_test)
    for result in results:
        for key, value in result.items():
            print(key,":", value)