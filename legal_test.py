import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from dotenv import load_dotenv
import os
import json
import time

# Load environment variables from .env
load_dotenv()

def get_robots_txt(domain):
    url = urljoin(domain, "/robots.txt")
    try:
        r = requests.get(url, timeout=5)
        if r.status_code == 200:
            content = r.text.strip()
            if "Disallow: /" in content:
                status = "Blocked all"
            elif "Disallow:" not in content or "Disallow: " in content:
                status = "Allowed (no restrictions)"
            else:
                status = "Partially allowed"
            return status, content
        else:
            return "No robots.txt", ""
    except Exception as e:
        return f"Error: {e}", ""

def find_terms_url(domain):
    common_paths = [
        "/terms", "/terms-of-service", "/terms-and-conditions",
        "/privacy-policy", "/legal", "/policy"
    ]
    for path in common_paths:
        full_url = urljoin(domain, path)
        try:
            r = requests.get(full_url, timeout=5)
            if r.status_code == 200 and "html" in r.headers.get("Content-Type", ""):
                return full_url
        except:
            continue
    try:
        r = requests.get(domain, timeout=5)
        soup = BeautifulSoup(r.text, "html.parser")
        links = soup.find_all('a', href=True)
        for link in links:
            href = link['href'].lower()
            if any(term in href for term in ['terms', 'conditions', 'legal', 'policy', 'privacy']):
                return urljoin(domain, link['href'])
    except:
        return None
    return None

def get_terms_text(url):
    try:
        r = requests.get(url, timeout=10)
        soup = BeautifulSoup(r.text, 'html.parser')
        return soup.get_text(separator="\n").strip()
    except:
        return ""

def is_login_required(domain):
    try:
        r = requests.get(domain, timeout=5)
        return any(x in r.text.lower() for x in ['login', 'sign in', 'authentication'])
    except:
        return False

def check_response_headers(domain):
    try:
        r = requests.get(domain, timeout=5)
        headers = r.headers
        suspicious = {k: v for k, v in headers.items() if 'robot' in k.lower() or 'policy' in k.lower()}
        return suspicious
    except:
        return {}

def check_for_api_docs(domain):
    possible_paths = ['/api', '/api-docs', '/swagger', '/openapi.json']
    for path in possible_paths:
        try:
            r = requests.get(urljoin(domain, path), timeout=5)
            if r.status_code == 200:
                return urljoin(domain, path)
        except:
            continue
    return None

def openai_terms_analysis(domain, robots_txt, terms_text):
    prompt = f"""
You are a legal AI. Analyze whether scraping the website "{domain}" is LEGAL or POTENTIALLY ILLEGAL.

Evaluate:
1. robots.txt rules:
{robots_txt}

2. Terms of Service / Privacy Policy:
--- START ---
{terms_text[:7000]}
--- END ---

Answer:
- LEGAL or POTENTIALLY ILLEGAL
- A clear explanation why.
- Write in a professional tone, suitable for a legal document.
- write in short 5-6 bullet points.
"""
    try:
        api_key = os.getenv("OPENAI_API_KEY", "").strip()
        if not api_key:
            return "OpenAI Error: API key not set."
        print(f"Using OpenAI API key: {api_key[:8]}...")

        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }

        payload = {
            "model": "gpt-4o",
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.2
        }

        response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload, timeout=30)

        if response.status_code != 200:
            return f"OpenAI API Error {response.status_code}: {response.text}"

        response_json = response.json()
        return response_json['choices'][0]['message']['content'].strip()

    except Exception as e:
        return f"OpenAI Error: {str(e)}"

def check_website_legality(domain):
    print(f"Checking legality for: {domain}\n")

    robots_status, robots_content = get_robots_txt(domain)
    print(f"Robots.txt Status: {robots_status}\n")

    terms_url = find_terms_url(domain)
    print(f"Terms/Policy URL Found: {terms_url if terms_url else 'Not found'}\n")
    terms_text = get_terms_text(terms_url) if terms_url else ""

    suspicious_headers = check_response_headers(domain)
    if suspicious_headers:
        print("Suspicious HTTP Headers:")
        for k, v in suspicious_headers.items():
            print(f"  {k}: {v}")
        print()

    login_required = is_login_required(domain)
    print(f"Login Required: {'Yes' if login_required else 'No'}\n")

    api_docs = check_for_api_docs(domain)
    print(f"API Docs Found: {api_docs if api_docs else 'None'}\n")

    if not terms_text:
        print("Could not read the terms/policy content. Proceeding with caution.\n")
    else:
        print("Terms/Policy Content (Preview):\n" + "-" * 40)
        print(terms_text[:1000] + "\n... [truncated]")
        print("-" * 40 + "\n")

    print("Sending content to OpenAI for analysis...\n")
    result = openai_terms_analysis(domain, robots_content, terms_text)
    print("OpenAI Legal Analysis:\n" + "=" * 40)
    print(result)
    print("=" * 40 + "\n")

#use your own domain or url
if __name__ == "__main__":
    check_website_legality("https://www.yourdomain.com")
