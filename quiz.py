import requests
from random import choice
from time import sleep

def search(search):
    
    payload = {'search': search}
    # add parameter for translation into wookiee
    # 'format': 'wookiee'

    url = "https://swapi.co/api/"

    response = requests.get(url, params=payload)

    data = response.json()

    return data

def people_search(search):

    payload = {'search': search}

    url = "https://swapi.co/api/people/"

    response = requests.get(url, params=payload)

    data = response.json()

    return data

def people_all(data = [], url = 'https://swapi.co/api/people/'):
    """Get all pages of API endpoint results with recursion"""

    if url == None:
        return

    response = requests.get(url)
    data_new = response.json()
    data.extend(data_new['results'])
    sleep(3)
    people_all(data, data_new['next'])

    return data

def homeworld(people_data):

    rando_person = choice(people_data)

    url = rando_person['homeworld']
    response = requests.get(url)
    data = response.json()
    homeworld = data['name']

    return {
            'name': rando_person['name'],
            'homeworld': homeworld
            }

if __name__ == "__main__":
    people_data = people_all(data = [], url = 'https://swapi.co/api/people/')
    homeworld_data = homeworld(people_data)
    print(homeworld_data)