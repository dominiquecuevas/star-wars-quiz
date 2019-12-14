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

def people():

    url = "https://swapi.co/api/people/"
    response = requests.get(url)
    data = response.json()

    rando_person = choice(data['results'])

    attributes = ['hair_color', 'eye_color', 'homeworld']
    rando_attribute = choice(attributes)

    if rando_attribute == 'homeworld':
        url_homeworld = rando_person['homeworld']
        response_homeworld = requests.get(url_homeworld)
        data_homeworld = response_homeworld.json()
        homeworld = data_homeworld['name']
        attribute_value = homeworld
    else: 
        attribute_value = rando_person[rando_attribute]

    return {'name': rando_person['name'], 
            rando_attribute: attribute_value
            }

def people_all(data = [], url = 'https://swapi.co/api/people/'):
    """Get all pages of API endpoint results with recursion"""

    if url == None:
        return

    response = requests.get(url)
    data_new = response.json()
    data.extend(data_new['results'])
    sleep(2)
    people_all_recursion(data, data_new['next'])

    return data