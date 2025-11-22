# scanner/headers.py

import requests

required = [
    "content-security-policy",
    "x-frame-options",
    "strict-transport-security",
    "x-xss-protection"
]

def check_headers(url):
    missing = []
    try:
        resp = requests.get(url, timeout=5)

        # convert all headers to lowercase for case-insensitive checking
        response_headers = {k.lower(): v for k, v in resp.headers.items()}

        for header in required:
            if header not in response_headers:
                missing.append(header)

    except Exception:
        # If request fails → consider all required headers missing
        return required

    return missing
