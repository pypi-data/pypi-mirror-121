# Husteblume API

import base64
import requests

HEADERS = {
    'user-agent': 'okhttp/4.4.0'
}


def api(method: str, url: str, data: dict = None, user=None) -> requests.Response:
    headers = HEADERS
    if user:
        headers = headers | {
            'authorization': 'Basic ' + (base64.b64encode(f"{user.appId}:{user.password}".encode('ascii'))).decode('ascii')
        }
    m = getattr(requests, method)
    r = m(url, headers=headers, data=data)
    r.raise_for_status()
    return r
