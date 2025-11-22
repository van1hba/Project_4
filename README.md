# Project_4
**1. Project Overview**

AutoWebVulnScanner is a Python-based automated security assessment tool designed to scan websites for common vulnerabilities and generate a structured, professional-grade PDF report.
The project combines web crawling, input manipulation, vulnerability testing, and reporting, aligning closely with industry practices in web application security evaluation.

This tool is suitable for academic research, final-year engineering projects, and cybersecurity demonstrations.

**2. Objectives**

The primary objectives of AutoWebVulnScanner are:

To automate the process of discovering and testing web application vulnerabilities.

To detect common OWASP Top 10 issues such as SQL Injection, Cross-Site Scripting (XSS), and missing security headers.

To generate a clear, organized PDF report summarizing findings.

To provide both a command-line interface (CLI) and an optional GUI using CustomTkinter.

To demonstrate practical cybersecurity skills using Python and industry libraries.

**3. Features**

Automated website crawler

Multi-parameter URL injection testing

SQL Injection detection

Reflected Cross-Site Scripting (XSS) detection

Security header analysis

Professional PDF report generation

GUI interface for ease of use

Modular and extensible architecture

**4. Technologies Used**
Component	Technology
Programming Language	Python
Web Crawling	requests, BeautifulSoup4
Vulnerability Detection	Custom Python logic
PDF Report Generation	reportlab
GUI Framework (optional)	CustomTkinter
URL Parsing	urllib.parse
5. Project Structure
AutoWebVulnScanner/
│
├── webscanner.py                 # Main CLI-based scanner
├── gui_runner.py              # GUI version (CustomTkinter)
│
└── scanner/
    ├── __init__.py
    ├── site_crawler.py           # Web crawler module
    ├── sqli.py                   # SQL Injection tests
    ├── xss.py                    # XSS tests
    ├── headers.py                # Security header analysis
    ├── reporter.py               # PDF report generator

**6. How the System Works**
**6.1 Input**

The user provides a target URL.

**6.2 Crawling**

The crawler identifies internal links and extracts URLs with parameters.

**6.3 Vulnerability Testing**

For each discovered URL:

SQL Injection payloads are injected into parameters.

XSS payloads are injected and reflected output is analyzed.

Response headers are examined for important security headers.

**6.4 Reporting**

All results are compiled into a single PDF report containing:

Vulnerabilities detected

Affected URLs

Payloads used

Missing security controls

Summary analysis

The output file is generated as:

Security_Report.pdf

**7. Setup and Installation**
Step 1: Install Dependencies
pip install requests beautifulsoup4 reportlab customtkinter

Step 2: Run the CLI Version
python webscanner.py -u http://testphp.vulnweb.com/

Step 3: Run the GUI Version
python gui_no_browse.py

**8. Vulnerabilities Detected**
SQL Injection

Common payloads used:

' OR '1'='1

' OR 1=1 --

" OR "1"="1

Detection relies on error-based SQL responses.

Reflected XSS

Payload used:

<script>alert(1)</script>


The scanner checks whether the payload is reflected in the server response.

Missing Security Headers

The tool checks for the presence of headers such as:

Content-Security-Policy

X-Frame-Options

Strict-Transport-Security

X-XSS-Protection

**9. Testing**

The scanner has been tested on multiple intentionally vulnerable applications:

DVWA (Damn Vulnerable Web Application)

OWASP Juice Shop

testphp.vulnweb.com

Local practice environments

**10. Authors and Contributions**

This project was collaboratively developed by:

Abhinav Roll No. 22010203002
Arushita Roll No. 22010203012

Both team members contributed to design, development, testing, and documentation.

**11. Disclaimer**

This tool is intended strictly for educational purposes and authorized security testing.
Scanning any system without explicit permission is illegal and unethical.

**12. Contact Information**

For academic reference or project-related queries:

Abhinav – CSE Department  Roll No. 22010203002
Arushita – CSE Department Roll No. 22010203012
