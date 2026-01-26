import requests
import os

api_key = '894eb47ad7744a9a858465f88540962e'
url = f'https://holidays.abstractapi.com/v1/'

params = {
    'api_key': api_key,
    'country': 'US',
    'year': '2024',
}

try:
    response = requests.get(url, params=params, timeout=10)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.text[:500]}")
except Exception as e:
    print(f"Error: {e}")
