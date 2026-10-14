import urllib.request
import json
import re

# 1. Fetch homepage to retrieve CSRF token and session cookies
url_home = 'http://127.0.0.1:5000/'
req_home = urllib.request.Request(url_home)
with urllib.request.urlopen(req_home) as resp_home:
    html = resp_home.read().decode('utf-8')
    cookie = resp_home.headers.get('Set-Cookie', '')
    match = re.search(r'name="csrf-token"\s+content="([^"]+)"', html)
    csrf_token = match.group(1) if match else ''

print(f"Retrieved CSRF Token: {csrf_token[:16]}... Cookie present: {bool(cookie)}")

# 2. Submit valid contact inquiry
url_contact = 'http://127.0.0.1:5000/contact'
payload = json.dumps({
    'name': 'Hiring Team Lead',
    'email': 'lead@recruiting.org',
    'subject': 'Full-Time / Internship Role',
    'message': 'Hello Jayaprakash, we reviewed your portfolio, Glint portal, and data analytics work. We would like to connect with you.',
    'hp_website': '',
    'csrf_token': csrf_token
}).encode('utf-8')

headers = {
    'Content-Type': 'application/json',
    'X-CSRFToken': csrf_token,
    'X-Requested-With': 'XMLHttpRequest'
}
if cookie:
    headers['Cookie'] = cookie

req_post = urllib.request.Request(url_contact, data=payload, headers=headers, method='POST')
try:
    with urllib.request.urlopen(req_post) as resp_post:
        res_data = json.loads(resp_post.read().decode('utf-8'))
        print(f"Status Code: {resp_post.status}")
        print(f"Response Body: {res_data}")
        assert resp_post.status == 200
        assert res_data['success'] is True
        print("\nLIVE CONTACT FORM SUBMISSION TEST PASSED WITH 200 OK!")
except urllib.error.HTTPError as e:
    print(f"HTTPError {e.code}: {e.read().decode('utf-8')}")
