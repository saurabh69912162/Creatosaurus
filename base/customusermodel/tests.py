import requests

url = "https://api.linkedin.com/v2/me"

headers = {
    'Authorization': "Bearer xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
    }

response = requests.request("GET", url, headers=headers)
import json
print(response.json())
obj = response.json()
print(obj['firstName']['localized']['en_US'],obj['lastName']['localized']['en_US'])
