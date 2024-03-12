import time
import requests

def send_request():
    res = requests.get("http://127.0.0.1:8000/heartbeat")
    print(res.text)



if __name__ == "__main__":
    while True:
        send_request()
        time.sleep(9)