import os
import requests

model_url = 'https://huggingface.co/mistralai/Mistral-7B-v0.1'
api_url = model_url + '/raw/main/config.json'

token = os.environ.get('HUGGINGFACE_HUB_TOKEN')
if not token:
    print('HUGGINGFACE_HUB_TOKEN not set in environment')
    raise SystemExit(1)

headers = {'Authorization': f'Bearer {token}'}
print('Checking access to', api_url)
resp = requests.get(api_url, headers=headers, timeout=10)
print('status:', resp.status_code)
print('headers:', resp.headers.get('content-type'))
print('body (first 400 chars):')
print(resp.text[:400])
