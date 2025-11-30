import requests
import json

# Test the import endpoint
url = "http://localhost:8000/api/import/resume-data/"

try:
    response = requests.post(url, headers={"Content-Type": "application/json"})
    print("Status Code:", response.status_code)
    print("Response:", response.text)
except Exception as e:
    print("Error:", str(e))