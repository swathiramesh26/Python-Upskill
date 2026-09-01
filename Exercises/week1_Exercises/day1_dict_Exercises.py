# Dictionary
test_cases = [
    {"id": 1, "expected": 200, "actual": 200},
    {"id": 2, "expected": 200, "actual": 404},
    {"id": 3, "expected": 500, "actual": 500}
]

def test_testcases():
    # For loop to capture dictionary values
    for test in test_cases:
        if test["expected"] == test["actual"]:
            print(f"Test Case {test['id']} : PASS")
        else:
            print(f"Test Case {test['id']} : FAIL")


