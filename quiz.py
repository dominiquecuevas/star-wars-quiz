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

    # get 2 random planets NOT in film
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

def opening_crawl_in_film():
    url = "https://swapi.co/api/films/"
    response = requests.get(url)
    data = response.json()

    films = data['results']
    rando_film = choice(films)
    title = rando_film['title']

    opening_crawl = rando_film['opening_crawl']
    opening_crawl_snippet = " ".join(opening_crawl.split()[:10])+"...."

    titles_false = []
    while len(titles_false) < 2:
        rando_title = choice(films)['title']
        if rando_title != title and rando_title not in titles_false:
            titles_false.append(rando_title)
    
    return {'titles_false': titles_false,
            'title': title,
            'opening_crawl': opening_crawl_snippet
            }

def film_year():
    url = "https://swapi.co/api/films/"
    response = requests.get(url)
    data = response.json()

    films = data['results']
    rando_film = choice(films)
    title = rando_film['title']

    year = rando_film['release_date'][:4]

    return {
            'title': title,
            'year': year
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
    answer = input(f"""Which planet is {name} from?
> """)
    if answer.lower().strip() == homeworld_.lower().strip():
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

    choices = {
                'A': planet_name_all[0],
                'B': planet_name_all[1],
                'C': planet_name_all[2]
                }

    answer = input(f"""Which planet was in the film, "{title}"? 
A. {planet_name_all[0]}
B. {planet_name_all[1]}
C. {planet_name_all[2]}
> """)

    if choices.get(answer.upper().strip()) == planet_name_true or (
        answer.lower().strip() == planet_name_true.lower().strip()):
        print("Correct!")
        return 1
    else:
        print(f"Wrong! The answer is {planet_name_true}")
        return 0

def q_opening_crawl():
    opening_crawl = opening_crawl_in_film()
    title = opening_crawl['title']
    all_titles = opening_crawl['titles_false'] + [title]
    shuffle(all_titles)
    choices = {
                'A': all_titles[0],
                'B': all_titles[1],
                'C': all_titles[2]
                }
    answer = input(f"""Which movie does this opening crawl belong to? 
"{opening_crawl['opening_crawl']}"
A. {choices['A']}
B. {choices['B']}
C. {choices['C']}
> """)

    # answer given as letter or full title
    if choices.get(answer.upper().strip()) == title or answer.lower().strip() == title.lower().strip():
        print("Correct!")
        return 1
    else:
        print(f"Wrong! The answer is {title}")
        return 0

def q_film_year():
    film_year_ = film_year()
    title = film_year_['title']
    year = film_year_['year']

    answer = input(f"""Which year was "{title}" released?
> """)

    if answer.strip() == year:
        print("Correct!")
        return 1
    else:
        print(f"Wrong! The answer is {year}")
        return 0

def quiz():


    questions = [q_opening_crawl(), q_planet(), q_film_year(), q_homeworld(), 
                q_planet(), q_homeworld(), q_planet(), q_homeworld(), q_planet(), 
                q_planet()]
    score = 0
    for question in questions:
        score += question
    sleep(1)
    print()
    total = len(questions)
    percent = score/total
    print(f"Your score: {score}/{total}")
    if percent < .6:    
        print("Your rank: Protocol Droid")
        print('''"Oh. They've encased him in Carbonite. He should be quite well protected. If he survived the freezing process, that is."
    - C-3PO''')
    if .6 <= percent < .7:
        print("Your rank: Nerf Herder")
        print('''"Who’s scruffy-looking?"
    - Han Solo''')
        return
    if .7 <= percent < .8:
        print("Your rank: Padawan")
        print('''"I don't like sand."
    - Anakin Skywalker''')
        return
    if .8 <= percent < .9:
        print("Your rank: Sith Lord")
        print('''"Brave of you, boy."
    - Count Dooku''')
        return
    if .9 <= percent < 1:
        print("Your rank: Jedi Master")
        return
    if percent == 1:
        print("Your rank: The Senate")
        print('''"Did you ever hear the tragedy of Darth Plagueis The Wise?"
    - Darth Sidious''')
        return

if __name__ == "__main__":
    print("Hello, there!")
    print("Star Wars quiz")
    print("Loading transmissions...")
    api_people_urls = get_api_people_urls(api_people_urls = [], 
                                        url = 'https://swapi.co/api/people/')
    print("Loading transmissions...")
    api_planet_urls = get_api_planet_urls(api_planet_urls = [], 
                                        url = "https://swapi.co/api/planets/")
    print()
    quiz()
