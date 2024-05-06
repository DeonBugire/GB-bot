import requests


def kitten():
    url = 'http://www.randomkittengenerator.com/cats/queued/random/'
    response = requests.get(url)
    if response.status_code:
        data = response.json()
        image = data.get('image')
        return image


if __name__ == '__main__':
    print(kitten())