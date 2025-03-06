import requests
import time
import random

URL = "http://127.0.0.1:5000/update_crowd"
while True:
    for gate in ["Gate A", "Gate B"]:
        data={"gate":gate, "count":random.randint(50,500)}
        response=requests.post(URL,json=data)
        print(f"Sent data: {data}, Response:{response.status_code}")
    time.sleep(1)