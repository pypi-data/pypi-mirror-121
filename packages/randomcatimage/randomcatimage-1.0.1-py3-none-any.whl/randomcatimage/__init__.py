import requests

def getCat(mime='png'):
    if mime == 'png':
        response = requests.get('https://api.thecatapi.com/v1/images/search?mime_types=png', headers={"x-api-key": "cc0eb636-fcc2-4522-ad8a-f2319898a5c3"})
        data = response.json()
    elif mime == 'jpg':
        response = requests.get('https://api.thecatapi.com/v1/images/search?mime_types=jpg', headers={"x-api-key": "cc0eb636-fcc2-4522-ad8a-f2319898a5c3"})
        data = response.json()
    elif mime == 'gif':
        response = requests.get('https://api.thecatapi.com/v1/images/search?mime_types=gif', headers={"x-api-key": "cc0eb636-fcc2-4522-ad8a-f2319898a5c3"})
        data = response.json()
    return data[0]['url']
