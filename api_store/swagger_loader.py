import requests

def load_swagger(url: str):
    res = requests.get(url, timeout=10)
    res.raise_for_status()
    return res.json()