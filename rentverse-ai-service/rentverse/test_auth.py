import requests

BASE_URL = "http://127.0.0.1:8000"

# Test /auth/login
resp_login = requests.post(f"{BASE_URL}/auth/login")
print("POST /auth/login response:", resp_login.json())

# Test /auth/verify-otp
resp_otp = requests.post(f"{BASE_URL}/auth/verify-otp")
print("POST /auth/verify-otp response:", resp_otp.json())
