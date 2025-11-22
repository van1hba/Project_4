# webscanner.py

import argparse
from scanner.site_crawler import get_links
from scanner.sqli import test_sqli
from scanner.xss import test_xss
from scanner.headers import check_headers
from scanner.reporter import generate_pdf
from urllib.parse import urlparse


def normalize_url(url):
    """Ensure URL starts with http:// or https://"""
    if not url.startswith(("http://", "https://")):
        return "http://" + url
    return url


def main():
    parser = argparse.ArgumentParser(description="Automated Web Vulnerability Scanner")
    parser.add_argument("-u", "--url", required=True, help="Target website URL")
    args = parser.parse_args()

    target = normalize_url(args.url)

    print("\n[+] Starting scan on:", target)

    # ---- CRAWLING ----
    print("\n[+] Crawling website…")
    links = get_links(target)
    print(f"[+] Found {len(links)} pages to test")

    sqli_results = []
    xss_results = []
    header_results = []

    # ---- TESTING ----
    print("\n[+] Testing vulnerabilities…")
    for link in links:
        print(f"    -> Testing: {link}")

        try:
            sqli_results.extend(test_sqli(link))
            xss_results.extend(test_xss(link))

            missing = check_headers(link)
            if missing:
                header_results.append({"url": link, "missing": missing, "issue": "Missing Security Headers"})

        except Exception as e:
            print(f"[Error testing] {link} -> {e}")

    # ---- FINAL RESULTS ----
    final = {
        "SQL Injection": sqli_results,
        "Cross-Site Scripting": xss_results,
        "Missing Security Headers": header_results
    }

    # ---- REPORT ----
    print("\n[+] Generating Report…")
    generate_pdf("Security_Report.pdf", final)
    print("[+] Report saved as Security_Report.pdf\n")


if __name__ == "__main__":
    main()
