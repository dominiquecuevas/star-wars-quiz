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

def get_api_species_urls(api_species_urls = [], 
                        url = "https://swapi.co/api/species/"):

    if url == None:
        return

    api_species_urls.append(url)
    response = requests.get(url)
    data = response.json()
    next_api_url = data['next']

    get_api_species_urls(api_species_urls, next_api_url)

    return api_species_urls

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

    return {
            'name': rando_person['name'],
            'homeworld': homeworld_h
            }

def people_eye_color(api_people_urls):

    while True:
        url = choice(api_people_urls)
        response = requests.get(url)
        data = response.json()

        rando_person = choice(data['results'])
        name = rando_person['name']
        eye_color = rando_person['eye_color']
        if eye_color != "unknown":
            break

    return {
            'name': name,
            'eye_color': eye_color
            }

def people_species(api_people_urls, api_species_urls):

    while True: 
        url = choice(api_people_urls)
        response = requests.get(url)
        data = response.json()

        rando_person = choice(data['results'])
        name = rando_person['name']

        url_species_list = rando_person['species']
        if url_species_list:
            break
    url_species = choice(url_species_list)
    response_species = requests.get(url_species)
    data_species = response_species.json()
    species = data_species['name']

    species_false = []
    while len(species_false) < 2:
        url_species_false = choice(api_species_urls)
        response_species_false = requests.get(url_species_false)
        data_species_false = response_species_false.json()
        results_species_list = data_species_false['results']

        rando = choice(results_species_list)
        rando_species_url = rando['url']
        rando_species_false = rando['name']

        if rando_species_url not in url_species_list and rando_species_false not in species_false:
            species_false.append(rando_species_false)

    return {
            'name': name,
            'species': species,
            'species_false': species_false
            }

def q_homeworld():
    print()
    homeworld_data = homeworld(api_people_urls)
    name = homeworld_data['name']
    homeworld_ = homeworld_data['homeworld']
    answer = input(f"""Which planet is {name} from?
> """)
    if answer.lower().strip() == homeworld_.lower().strip():
        print('Correct!')
        return 1
    else:
        print(f"Wrong! The answer is {homeworld_}.")
        return 0

def q_planet():
    print()
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
        print(f"Wrong! The answer is {planet_name_true}.")
        return 0

def q_opening_crawl():
    print()
    opening_crawl = opening_crawl_in_film()
    title = opening_crawl['title']
    all_titles = opening_crawl['titles_false'] + [title]
    shuffle(all_titles)
    choices = {
                'A': all_titles[0],
                'B': all_titles[1],
                'C': all_titles[2]
                }
    answer = input(f"""Which movie is this opening crawl from? 
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
        print(f"Wrong! The answer is {title}.")
        return 0

def q_film_year():
    print()
    film_year_ = film_year()
    title = film_year_['title']
    year = film_year_['year']

    answer = input(f"""Which year was "{title}" released?
> """)

    if answer.strip() == year:
        print("Correct!")
        return 1
    else:
        print(f"Wrong! The answer is {year}.")
        return 0

def q_eye_color():
    print()
    eye_color_dict = people_eye_color(api_people_urls)
    name = eye_color_dict['name']
    eye_color = eye_color_dict['eye_color']
    answer = input(f"""What color are {name}'s eyes?
> """)

    if answer.lower().strip() == eye_color.lower():
        print("Correct!")
        return 1
    else:
        print(f"Wrong! The answer is {eye_color}.")
        return 0

def q_species():
    print()
    species_dict = people_species(api_people_urls, api_species_urls)
    name = species_dict['name']
    species = species_dict['species']
    species_false = species_dict['species_false']

    all_species = species_false + [species]
    shuffle(all_species)
    choices = {
                'A': all_species[0],
                'B': all_species[1],
                'C': all_species[2],
                }

    answer = input(f'''What species is {name}?
A. {choices['A']}
B. {choices['B']}
C. {choices['C']}
> ''')
    if choices.get(answer.upper().strip()) == species or answer.lower().strip() == species.lower().strip():
        print("Correct!")
        return 1
    else:
        print(f"Wrong! The answer is {species}.")
        return 0

def q_species_t_f():
    print()
    species_dict = people_species(api_people_urls, api_species_urls)
    name = species_dict['name']
    species = species_dict['species']
    species_false = species_dict['species_false'][0]

    choices = {
                species: 'True',
                species_false: 'False'
                }
    rando_choice = choice(list(choices.keys()))

    answer = input(f'''True/False: {name}'s species is {rando_choice}
> ''')
    if answer.title().strip() == choices[rando_choice]:
        print("Correct!")
        if choices[rando_choice] == 'False':
            print(f"{name} is {species}.")
        return 1
    else:
        print(f"Wrong! The answer is {choices[rando_choice]}.")
        if choices[rando_choice] == 'False':
            print(f"{name} is {species}.")
        return 0

def quiz(play_again = ""):
    if play_again == "N":
        print("May the force be with you.")
        r2_ascii()
        return
    elif play_again =="Y":
        print("Hello, there!")

    questions = [q_species_t_f(), q_species(), q_homeworld(), q_homeworld(),
                q_planet(), q_species(), q_species_t_f(), q_film_year(), q_eye_color(), 
                q_opening_crawl()]
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
        print('''   "Oh. They've encased him in Carbonite. He should be quite well protected. If he survived the freezing process, that is."
    - C-3PO''')
    elif .6 <= percent < .7:
        print("Your rank: Nerf Herder")
        print('''   "Who’s scruffy-looking?"
    - Han Solo''')
    elif .7 <= percent < .8:
        print("Your rank: Padawan")
        print('''   "I don't like sand."
    - Anakin Skywalker''')
    elif .8 <= percent < .9:
        print("Your rank: Sith Lord")
        print('''   "Brave of you, boy."
    - Count Dooku''')
    elif .9 <= percent < 1:
        print("Your rank: Jedi Master")
        print('''   "Wars not make one great."
    - Yoda''')
    elif percent == 1:
        print("Your rank: The Senate")
        print('''   "Did you ever hear the tragedy of Darth Plagueis The Wise?"
    - Darth Sidious''')

    while True:
        play_again = input("""Would you like to play again? Y/N 
> """)
        if play_again.upper().strip() != "Y" and play_again.upper().strip() != "N":
            print("Not an option!")
        else:
            break

    quiz(play_again.upper().strip())

def r2_ascii():
    print("         _____")
    print("       .'/L|__`.")
    print("      / =[_]O|` \ ")
    print('      |"+_____":|')
    print("    __:='|____`-:__")
    print("   ||[] ||====| []||")
    print("   ||[] | |=| | []||")
    print("   |:||_|=|U| |_||:|")
    print("   |:|||]_=_ =[_||:|")
    print("   | |||] [_][]C|| |")
    print('''   | ||-'"""""`-|| |''')
    print("   /|\\\_\_|_|_/_//|\ ")
    print("  |___|   /|\   |___| ")
    print("  `---'  |___|  `---' ")
    print("         `---'")
    print()
    print("This ASCII pic can be found at https://asciiart.website/index.php?art=movies/star%20wars")


if __name__ == "__main__":
    print("        _________________.   ___      .______")
    print("       /                 |  /   \     |   _  \ ")
    print("      |   (------|  |----` /  ^  \    |  |_)  |")
    print("       \   \     |  |     /  /_\  \   |      /")
    print(".-------)   |    |  |    /  _____  \  |  |\  \----.")
    print("|__________/     |__|   /__/     \__\ | _| `._____|")
    print("                    Q  U  I  Z                    ")
    print("___    __    ___   ___      .______        _______.")
    print("\  \  /  \  /  /  /   \     |   _  \      /       |")
    print(" \  \/    \/  /  /  ^  \    |  |_)  |    |   (----`")
    print("  \          /  /  /_\  \   |      /      \   \    ")
    print("   \   /\   /  /  _____  \  |  |\  \-------)   |   ")
    print("    \_/  \_/  /__/     \__\ | _| `.___________/    ")
    print()
    print("Loading...")
    api_people_urls = get_api_people_urls(api_people_urls = [], 
                                        url = 'https://swapi.co/api/people/')
    print("Loading...")
    api_planet_urls = get_api_planet_urls(api_planet_urls = [], 
                                        url = "https://swapi.co/api/planets/")
    print("Loading...")
    api_species_urls = get_api_species_urls(api_species_urls = [], 
                        url = "https://swapi.co/api/species/")
    quiz()