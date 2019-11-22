import requests

url = "https://api.linkedin.com/v2/me"

headers = {
    'Authorization': "Bearer AQU6cmq8aX_yPNC63dd5LsYzy2juf6CWf5Qrm5QHf5VwF3X0_PkfThBRqgI9-J1VLyp8VxKEOb45q4QAQkhLOS1Y20cfl3RJ7tTIzue6WcvTuZaIwVR8MgsGnlSEL8p9aHHFXOKdPuf4QRIZS7vJ4XK9laZR5Orb84Uh6w9pP7jBt2e0YtJywBBSCs4q1RjDFMfI7BixRc6NW3-ziLAutudfKZn_dXeqZFtVAvjJVkMTw9lhs9_2n6wDmdkLX8zR_ZAP1uSWJT5_VSDv-f9VrsXuu-Ce4e5dUaEC-Adu2nkqi9a_ISik07apncgcdmim9fubxGwF8dEA2-kIxM4EUVrJ8pJoLw",
    }

response = requests.request("GET", url, headers=headers)
import json
print(response.json())
obj = response.json()
print(obj['firstName']['localized']['en_US'],obj['lastName']['localized']['en_US'])