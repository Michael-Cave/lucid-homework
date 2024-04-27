import requests

def main():
    try:
        response = requests.get('http://localhost:8280/cache/info')
        print(response.text)
    except requests.exceptions.RequestException as e:
        print(e)