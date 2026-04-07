import requests
from config import BASE_URL


def call_api(method, endpoint, path_params=None, json=None):
    url = BASE_URL + endpoint

    if path_params:
        for k, v in path_params.items():
            url = url.replace(f"{{{k}}}", str(v))

    response = requests.request(method, url, json=json, timeout=30)

    try:
        data = response.json()
        print(data)
        return {
            "status_code": response.status_code,
            "data": data
        }
    except Exception:
        data = response.text
        print(data)
        return {
            "status_code": response.status_code,
            "data": data
        }