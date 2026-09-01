"""
config.py
Central place for environment-driven settings. Reads BASE_URL, BROWSER,
and HEADLESS from a .env file (via python-dotenv) so the same test suite
can run against different environments/browsers without updates in the test code.
"""
import os
from dotenv import load_dotenv

load_dotenv()

# def _str_to_bool(value: str) -> bool:
#     return value.strip().lower() in ("1", "true", "yes", "on")

BASE_URL = os.getenv("BASE_URL")
BROWSER = os.getenv("BROWSER")
HEADLESS =os.getenv("HEADLESS")
#HEADLESS = _str_to_bool(os.getenv("HEADLESS", "true"))

if __name__ == "__main__":
    print(f"BASE_URL = {BASE_URL}")
    print(f"BROWSER  = {BROWSER}")
    print(f"HEADLESS = {HEADLESS}")