import requests
import os

url = 'https://www.ufc-bets.com/wp-json/jwt-auth/v1/token'
password  = os.environ.get('wp_pass')

# WordPress login credentials
credentials = {
    'username': 'admin',
    'password': password
}

response = requests.post(url, data=credentials)
response_data = response.json()

if 'token' in response_data:
    print("JWT Token:", response_data['token'])
else:
    print("Failed to generate JWT token. Error:", response_data)
