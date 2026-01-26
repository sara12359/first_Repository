import requests

year = 2024
country = 'US'
url = f'https://date.nager.at/api/v3/PublicHolidays/{year}/{country}'

try:
    response = requests.get(url, timeout=10)
    print(f"Status Code: {response.status_code}")
    if response.status_code == 200:
        print(f"Response: {response.text[:500]}")
    else:
        print(f"Error Response: {response.text}")
except Exception as e:
    print(f"Error: {e}")
