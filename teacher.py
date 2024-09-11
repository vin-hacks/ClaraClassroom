import requests
import time
import json
import os

TOKEN = "fd0dfef2a3c2c358446125688051a2fb10046ff45f87f11ad80e813b3e0c2150"
CSRFTOK = "e8e1a4d2ccc825cdfa5b0bd6e4adc37a87d3871df516ded2f25a8dcace195431"



while True:

    url = 'http://localhost:8081/pending'

    headers = {
        'Accept': 'application/json'
    }

    cookies = {
        'token': TOKEN
    }

    params = {
        'csrftok': CSRFTOK
    }
    # Get waiting users
    response = requests.get(url, headers=headers, cookies=cookies)

    data = json.loads(response.text)
    waitingUsers = data['students']

    #Denying users
    for user in waitingUsers:
        path = f"deny/{user}"

        #Simulating the traversal made by the browser:
        normalized_path = os.path.normpath(path)
        try:
            requests.post(url, params=params, headers=headers, cookies=cookies)
            print(url)
        except:
            print("invalid path")
        
        requests.post(url, params=params, headers=headers, cookies=cookies)
        print(url)
        time.sleep(2)

    #print(response.status_code)

    #print(response.text)

# Wait 1 min until denying again
    time.sleep(60)
