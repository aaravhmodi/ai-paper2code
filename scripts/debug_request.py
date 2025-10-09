import requests
import json

url = 'http://127.0.0.1:8000/generate'
payload = {'query': 'test query to debug response'}
try:
    r = requests.post(url, json=payload, timeout=15)
except Exception as e:
    print('Request failed:', e)
    raise SystemExit(1)

print('Status:', r.status_code)
print('OK:', r.ok)
print('Content-Type:', r.headers.get('content-type'))
print('--- Response text (first 2000 chars) ---')
print(r.text[:2000])
print('--- End response text ---')

try:
    print('\nAttempting to parse JSON...')
    data = r.json()
    print('Parsed JSON:', json.dumps(data, indent=2)[:2000])
except Exception as e:
    print('JSON parse error:', e)
    # If it's an HTML error page or empty, show some diagnostics
    if not r.text:
        print('Response body is empty')
    elif r.text.strip().startswith('<'):
        print('Response appears to be HTML (likely a server error page)')
    else:
        print('Response is text but not JSON')

# Exit with non-zero code if non-2xx so CI/automation can detect failures
if not r.ok:
    raise SystemExit(2)
