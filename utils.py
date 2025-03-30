import string
import requests
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

BASE_URL = "https://zxgbhnz8ox.voorivex-lab.online/"
HEADERS = {"User-Agent": "Mozilla/5.0"}
VERIFY = False
PROXIES = {
    "http": "http://127.0.0.1:8080",
    "https": "http://127.0.0.1:8080",
}

charset = string.ascii_letters + string.digits + "_-" # {}@!#$%&*()=+<>

def send(payload):
    params = {"id": payload}
    res = requests.get(
        BASE_URL, 
        params=params, 
        headers=HEADERS, 
        verify=VERIFY,
        proxies=PROXIES,
    )
    return res.text