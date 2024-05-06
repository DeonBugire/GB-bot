import requests


def dog():
    url = 'https://random.dog/woof.json'
    response = requests.get(url)
    if response.status_code:
        data = response.json()
        image = data.get('image')
        return image


if __name__ == '__main__':
    print(dog())