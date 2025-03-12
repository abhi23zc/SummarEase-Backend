import requests

payload = { 'api_key': 'b2cd891913a261a35c4b577b1b74524a', 'url': 'https://httpbin.org/' }
r = requests.get('https://api.scraperapi.com/', params=payload)
print(r.text)
