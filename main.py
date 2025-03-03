"""
curl -X 'PUT' \
  'http://5.63.153.31:5051/v1/account/44f1f333-270b-4b41-8f53-cf28a4d5b639' \
  -H 'accept: text/plain'
"""
import pprint

import requests

# url = 'http://5.63.153.31:5051/v1/account'
# headers = {
#     'accept': '*/*',
#     'Content-Type': 'application/json',
# }
# json = {
#     "login": "Pakhomov",
#     "email": "Pakhomov@mail.ru",
#     "password": "12345"
# }
#
# response = requests.post(
#     url=url,
#     headers=headers,
#     json=json
# )

url = 'http://5.63.153.31:5051/v1/account/44f1f333-270b-4b41-8f53-cf28a4d5b639'
headers = {
    'accept': 'text/plain'
}

response = requests.put(
    url=url,
    headers=headers
)

print(response.status_code)
pprint.pprint(response.json())
response_json = response.json()
print(response_json['resource']['rating']['quantity'])