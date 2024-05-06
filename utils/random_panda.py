import requests


def panda():
    url = 'https://some-random-api.ml/img/panda'
    response = requests.get(url)
    if response.status_code:
        data = response.json()
        image = data.get('image')
        return image


if __name__ == '__main__':
    print(panda())