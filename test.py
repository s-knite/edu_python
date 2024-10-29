import unittest
from unittest.mock import patch
from io import StringIO
from inspect import signature
import pandas as pd
from IPython import get_ipython

# example_cases = [
#     {
#       "test_name": "A",
#       "inputs": ["Ada"],
#       "e_out": "Hello, Ada!",
#     },
#     {
#       "test_name": "B",
#       "inputs": ["Bob"],
#       "e_out": "Hello, Bob!",
#     },
#     {
#       "test_name": "C",
#       "inputs": [""],
#       "e_out": "Hello, !",
#     },
# ]

# def example_function():
#   name = input("Enter name")
#   print(f"Hello, {name}!")

def run_test(f,test):
  """
    Runs a test simulating inputs and capturing print statements,
    compares expected outputs and expected returns if they exist
    Test case must include at lease one of expected return or expected out
  """
  result = test.copy() #mainly used for debugging
  sig = signature(f)
  if len(sig.parameters) != len(test["params"]):
    print("Number of paramaters does not match expected\nAborting Tests")
    result["passed"] = False
    return result
  with patch("builtins.input", side_effect=test["inputs"]), patch("sys.stdout", new=StringIO()) as fake_out:
    try:
      a_return = f(*test["params"])
    except StopIteration: #catches exception raised by running out of inputs
      a_return = StopIteration
  if a_return == StopIteration:
    print("Too many input calls")
  result["a_return"] = a_return
  result["a_out"] = fake_out.getvalue().strip()
  result["passed"] = True
  #will only test against outputs if expected output in test case
  #otherwise will ignore outputs
  if "e_out" in test.keys() and test["e_out"] != result["a_out"]:
    result["passed"] = False
  #will only test against return if expected return in test case
  #otherwise will ignore return value
  if "e_return" in test.keys() and a_return != test["e_return"]:
    result["passed"] = False   
  return result

def pre_test(f_name):
    """Checks if a function with the given name exists in the user's namespace."""
    user_ns = get_ipython().user_ns
    if f_name in user_ns and callable(user_ns[f_name]):
        print("Function found\n")
        return user_ns[f_name]
    else:
        print(f"Function not found with name {f_name}")
        print("\033[1;31mAborting tests\033[0;30m")

def run_tests(f,tests):
  """Loops through all test cases, tests should be a list of dictionaries"""
  results = []
  for test in tests:
    if "params" not in test.keys():
      test["params"] = [] #adds empty list for cases that don't use params
    if "inputs" not in test.keys():
      test["inputs"] = [] #adds empty list for cases that don't use input
    results.append(run_test(f,test))
  return results

def post_test(results):
  """uses pandas to style results table"""
  df = pd.DataFrame(results, columns=["test_name","passed"])
  styled_df = df.style.map(highlight_passed, subset=['passed'])
  return styled_df

def highlight_passed(val):
  """Highlights 'passed' column: green for True, red for False."""
  color = 'green' if val else 'red'
  return f'background-color: {color}'

def run_all(f_name,test_cases):
  """
    To display results styled_results must be declared in the global scope
    before calling run all and must be the final line of code in a colab cell
    not in a code block (e.g. not in an if statement)

    e.g.
    styled_results = None
    run_all("Calculate",Tests)
    styled_results
  """
  global styled_results
  func = pre_test(f_name)
  if func:
    results = run_tests(func,test_cases)
    # for result in results:
    #   print(result)
    styled_results = post_test(results)

# styled_results = None
# run_all("example_function", example_cases)
# styled_results

# def html_results_table(data): 
#     """
#     requires data to be a list of dictionaries with at minimum the keys for "test name" and "passed"
#     """
#     html = "<style>table,th,td {border-collapse: collapse; border: 1px solid;text-align: center;}td, th{padding:5px;}</style>"
#     html += "<table>"
#     html += "<tr><th>Test Name</th><th>Outcome</th><tr>"
#     for d in data:
#         html += "<tr >"
#         html += f"<td> {d['test name']}</td>"
#         html += "<td "
#         html += 'style = "background-color:Aquamarine;">' if d["passed"] else 'style = "background-color:LightCoral;">' 
#         html += "pass </td>" if d["passed"] else "fail </td>"
#         html += "</tr>"
#     html += "</table>"
#     return html
