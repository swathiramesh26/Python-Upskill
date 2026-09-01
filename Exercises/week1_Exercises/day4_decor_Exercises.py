# Retry Decorator
def retry(func):

    def wrapper():
        for attempt in range(3):
            try:
                func()
                return
            except Exception:
                print(f"Attempt {attempt + 1} failed. Retrying...")

    return wrapper


# Login Test Step
@retry
def login():
    raise Exception("Login Failed")
print("Login Failed")

@retry
def logout():
    raise Exception("Logout Failed")
print("Logout Failed")


# Run Login
login()
logout()


# Test Results
test_results = ["Pass", "Fail", "Pass", "Fail", "Pass"]


# Filter failed tests using list comprehension
failed_tests = [result for result in test_results if result == "Fail"]

# Count failed tests
failed_count = len(failed_tests)

print("\nFailed Tests:", failed_tests)
print("Failed Test Count:", failed_count)