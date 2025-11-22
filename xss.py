import requests

payload = "<script>alert(1)</script>"

def test_xss(url):
    results = []

    if "?" not in url:
        return results

    try:
        test_url = url.replace("=", "=" + payload)
        resp = requests.get(test_url, timeout=5)

        # If payload appears in response → reflected XSS exists
        if payload in resp.text:
            results.append({
                "url": url,
                "payload": payload,
                "issue": "Reflected XSS Found"
            })

    except:
        pass

    return results
