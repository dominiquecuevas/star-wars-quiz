import requests
from random import choice, shuffle
from time import sleep

def get_api_people_urls(api_people_urls = [], 
                        url = 'https://swapi.co/api/people/'):
    """Get all pages of API endpoint results with recursion"""

    if url == None:
        return

    api_people_urls.append(url)
    response = requests.get(url)
    data = response.json()
    api_url = data['next']
    
    get_api_people_urls(api_people_urls, api_url)

    return api_people_urls

def get_api_planet_urls(api_planet_urls = [], 
                        url = "https://swapi.co/api/planets/"):

    if url == None:
        return

    api_planet_urls.append(url)
    response = requests.get(url)
    data = response.json()
    next_api_url = data['next']

    get_api_planet_urls(api_planet_urls, next_api_url)

    return api_planet_urls

def planet_in_film(api_planet_urls):

    url = "https://swapi.co/api/films/"
    response = requests.get(url)
    data = response.json()
    films = data['results']
    rando_film = choice(films)
    title = rando_film['title']

    planets_true = rando_film['planets']

    planets_false = []
    while len(planets_false) < 2:
        url_p = choice(api_planet_urls)
        response_p = requests.get(url_p)
        data_p = response_p.json()
        for result in data_p['results']:
            if result['url'] not in planets_true and result['url'] not in planets_false:
                planets_false.append(result['url'])
            if len(planets_false) >= 2:
                break

    return {
            'title': title,
            'planets_true': planets_true,
            'planets_false': planets_false,
            }

def homeworld(api_people_urls):
    # random person and their homeworld

    while True:
        url = choice(api_people_urls)
        response = requests.get(url)
        data = response.json()

        rando_person = choice(data['results'])

        url_h = rando_person['homeworld']
        response_h = requests.get(url_h)
        data_h = response_h.json()
        homeworld_h = data_h['name']
        if homeworld_h != 'unknown':
            break
        # print(rando_person['name'])
        # print(homeworld_h)

    return {
            'name': rando_person['name'],
            'homeworld': homeworld_h
            }


def q_homeworld():
    homeworld_data = homeworld(api_people_urls)
    name = homeworld_data['name']
    homeworld_ = homeworld_data['homeworld']
    answer = input(f"Which planet is {name} from? ")
    if answer.lower() == homeworld_.lower():
        print('Correct!')
        return 1
    else:
        print(f"Wrong! The answer is {homeworld_}")
        return 0

def q_planet():
    rando_film = planet_in_film(api_planet_urls)
    title = rando_film['title']
    url_planet = choice(rando_film['planets_true'])
    response_planet = requests.get(url_planet)
    data_planet = response_planet.json()
    planet_name_true = data_planet['name']

    planet_name_all = [planet_name_true]

    planets_false = rando_film['planets_false']
    for url_planet in planets_false:
        response_planet = requests.get(url_planet)
        data_planet = response_planet.json()
        planet_name_all.append(data_planet['name'])

    shuffle(planet_name_all)

    planets_string = f"{planet_name_all[0]}, {planet_name_all[1]}, or {planet_name_all[2]}"


    planet = input(f"""Which planet was in the film, {title}? {planets_string}
""")

    if planet.lower() == planet_name_true.lower():
        print("Correct!")
        return 1
    else:
        print(f"Wrong! The answer is {planet_name_true}")
        return 0

def quiz():

    score = (
            q_homeworld() +
            q_planet() +
            q_homeworld() +
            q_planet() +
            q_planet()
            )
    print(f"Your score is {score}")

if __name__ == "__main__":
    print("Loading people data...")
    api_people_urls = get_api_people_urls(api_people_urls = [], 
                                        url = 'https://swapi.co/api/people/')
    print("Loading planet data...")
    api_planet_urls = get_api_planet_urls(api_planet_urls = [], 
                                        url = "https://swapi.co/api/planets/")
    print("Star Wars quiz")
    print("Welcome")

    quiz()
