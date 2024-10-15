import unittest
from unittest.mock import patch
from io import StringIO
from inspect import signature

#test io
def test_io(func, test_cases):
    results = []
    for case in test_cases:
        with patch("builtins.input", side_effect=case["inputs"]), patch("sys.stdout", new=StringIO()) as fake_out:
            try:
                func()
            except StopIteration: #catches exception raised by running out of inputs
                print("Too many input calls")
                
        result = {
            "inputs": case["inputs"],
            "expected_output": case["expected_output"].strip(),
            "actual_output": fake_out.getvalue().strip(),
            "passed": fake_out.getvalue().strip() == case["expected_output"].strip()
        }
        results.append(result)
    return results
#test function with return
def test_func(func, test_cases):
    results = []
    for case in test_cases:
        result = {
            "params" : case["params"],
            "expected" : case["expected"]
        }
        if func.__code__.co_argcount == len(case["params"]):
            actual = func(*case["params"])
            result["actual"] = actual
            result["passed"] = actual == case["expected"]

        else:
            result["actual"] = "Error wrong number of parameters"
            result["passed"] = False
        results.append(result)
    return results


if __name__ == '__main__':
    #example test data
    io_test_cases = [
        {
            "inputs": ["Ada", "39"], #put inputs in list even if only 1 input
            "expected_output": "Hello, Ada!\n39 is soooo old!\n"
        },
        {
            "inputs": ["Bob", "12"], #put inputs in list even if only 1 input
            "expected_output": "Hello, Bob!\n12 is soooo old!\n"
        }
    ]
    func_test_cases = [
        {
            "params" : [3,5], #put params in list even if only 1 param
            "expected" : 15 
        },
        {
            "params" : [2.2,10], #put params in list even if only 1 param
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

    
    results = test_func(func_to_test, func_test_cases)
    for result in results:
        if result["passed"]:
            print("Test passed")
        else:
            for key, value in result.items():
                print(key,":", value)
            
    results = test_io(io_to_test, io_test_cases)
    for result in results:
        if result["passed"]:
            print("Test passed")
        else:
            for key, value in result.items():
                print(key,":", value)

def html_results_table(data): 
    """
    requires data to be a list of dictionaries with at minimum the keys for "test name" and "passed"
    """
    html = "<style>table,th,td {border-collapse: collapse; border: 1px solid;text-align: center;}td, th{padding:5px;}</style>"
    html += "<table>"
    html += "<tr><th>Test Name</th><th>Outcome</th><tr>"
    for d in data:
        html += "<tr >"
        html += f"<td> {d['test name']}</td>"
        html += "<td "
        html += 'style = "background-color:Aquamarine;">' if d["passed"] else 'style = "background-color:LightCoral;">' 
        html += "pass </td>" if d["passed"] else "fail </td>"
        html += "</tr>"
    html += "</table>"
    return html
