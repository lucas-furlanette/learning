import requests
from colorama import Fore, Style

base_url = 'https://pogoapi.net/api/v1/pokemon_stats.json'


def get_pokemon(name):
    response = requests.get(base_url)
    if response.status_code == 200:
        data = response.json()
        for poke in data:
            if poke['pokemon_name'].lower() == name.lower():
                return poke
    return None


def get_evolutions(pokemon_id):
    evolutions_url = f"https://pogoapi.net/api/v1/pokemon_evolutions.json"
    response = requests.get(evolutions_url)
    if response.status_code == 200:
        data = response.json()
        for poke in data:
            if poke['pokemon_id'] == pokemon_id:
                return poke['evolutions']
    return None


def get_max_cp(pokemon_id):
    max_cp_url = f"https://pogoapi.net/api/v1/pokemon_max_cp.json"
    response = requests.get(max_cp_url)
    if response.status_code == 200:
        data = response.json()
        for poke in data:
            if poke['pokemon_id'] == pokemon_id:
                return poke['max_cp']
    return None


def get_mega_evolution(pokemon_id):
    mega_url = f"https://pogoapi.net/api/v1/mega_pokemon.json"
    response = requests.get(mega_url)
    if response.status_code == 200:
        data = response.json()
        mega_evolution = []
        for poke in data:
            if poke['pokemon_id'] == pokemon_id:
                mega_evolution.append(poke['mega_name'])
        return mega_evolution
    return None


def get_damage_multipliers():
    url = "https://gist.githubusercontent.com/agarie/2620966/raw/6d950a9757033e0b230f5eb7dd456b5682fac811/type-chart" \
          ".json"
    response = requests.get(url)
    return response.json()


def get_pokemon_type(pokemon_name):
    pokemon_name = pokemon_name.lower()
    url = f"https://pokeapi.co/api/v2/pokemon/{pokemon_name}/"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        types = []
        for type_data in data["types"]:
            types.append(type_data["type"]["name"])
        return types
    else:
        print("Error: ", response.status_code)


def get_type_advantages(types, multipliers):
    strengths = []
    weaknesses = []
    for attack_type in multipliers:
        for defense_type in types:
            if multipliers[attack_type][defense_type] > 1:
                strengths.append(attack_type)
            elif multipliers[attack_type][defense_type] < 1:
                weaknesses.append(attack_type)
    return strengths, weaknesses


def start_app(poke_name):
    pokemon = get_pokemon(poke_name)
    if not pokemon:
        print(Fore.RED + f"Pokemon {poke_name} not found." + Style.RESET_ALL)
        return

    print(Fore.CYAN + "Name: ", str(pokemon["pokemon_name"]) + Style.RESET_ALL)
    print(Fore.CYAN + "ID: ", str(pokemon["pokemon_id"]) + Style.RESET_ALL)
    print(Fore.CYAN + "Base Attack: ", pokemon["base_attack"], "Base Defense: ", pokemon["base_defense"],
          "Base Stamina: ",
          str(pokemon["base_stamina"]) + Style.RESET_ALL)

    max_cp = get_max_cp(pokemon["pokemon_id"])
    if not max_cp:
        print(Fore.RED + "Max CP data not available for this Pokemon." + Style.RESET_ALL)
    else:
        print(Fore.CYAN + "Max CP: ", str(max_cp) + Style.RESET_ALL)

    evolutions = get_evolutions(pokemon["pokemon_id"])
    if not evolutions:
        print(Fore.RED + "Evolutions not found." + Style.RESET_ALL)
    else:
        for evolution in evolutions:
            print(Fore.YELLOW + "Evolves into: ", evolution["pokemon_name"], "with", evolution["candy_required"],
                  "candy" + Style.RESET_ALL)

    mega_evolution = get_mega_evolution(pokemon["pokemon_id"])
    if not mega_evolution:
        print(Fore.RED + "This Pokemon does not have a Mega Evolution." + Style.RESET_ALL)
    else:
        for mega in mega_evolution:
            if 'Mega Charizard X' in mega:
                print(Fore.BLUE + "Mega Evolution: " + mega + Style.RESET_ALL)
            elif 'Mega Charizard Y' in mega:
                print(Fore.GREEN + "Mega Evolution: " + mega + Style.RESET_ALL)
            else:
                print(Fore.YELLOW + "Mega Evolution: " + mega + Style.RESET_ALL)
    types = get_pokemon_type(pokemon["pokemon_name"])
    damage_multipliers = get_damage_multipliers()
    print(Fore.CYAN + "Type Advantages: " + Style.RESET_ALL)
    for poke_type in types:
        if poke_type == 'normal':
            print(Fore.WHITE + f'{poke_type.capitalize()} type:' + Style.RESET_ALL)
        elif poke_type == 'fire':
            print(Fore.RED + f'{poke_type.capitalize()} type:' + Style.RESET_ALL)
        elif poke_type == 'water':
            print(Fore.BLUE + f'{poke_type.capitalize()} type:' + Style.RESET_ALL)
        elif poke_type == 'grass':
            print(Fore.GREEN + f'{poke_type.capitalize()} type:' + Style.RESET_ALL)
        elif poke_type == 'electric':
            print(Fore.YELLOW + f'{poke_type.capitalize()} type:' + Style.RESET_ALL)
        elif poke_type == 'ice':
            print(Fore.CYAN + f'{poke_type.capitalize()} type:' + Style.RESET_ALL)
        elif poke_type == 'fighting':
            print(Fore.MAGENTA + f'{poke_type.capitalize()} type:' + Style.RESET_ALL)
        elif poke_type == 'poison':
            print(Fore.RED + f'{poke_type.capitalize()} type:' + Style.RESET_ALL)
        elif poke_type == 'ground':
            print(Fore.YELLOW + f'{poke_type.capitalize()} type:' + Style.RESET_ALL)
        elif poke_type == 'flying':
            print(Fore.CYAN + f'{poke_type.capitalize()} type:' + Style.RESET_ALL)
        elif poke_type == 'dragon':
            print(Fore.LIGHTYELLOW_EX + f'{poke_type.capitalize()} type:' + Style.RESET_ALL)
        for target_type, multipliers in damage_multipliers[poke_type].items():
            if multipliers > 1:
                print(Fore.GREEN + f'\t Strong against {target_type} x{multipliers}' + Style.RESET_ALL)
            elif multipliers < 1:
                print(Fore.RED + f'\t Weak against {target_type} x{multipliers}' + Style.RESET_ALL)
            else:
                print(Fore.YELLOW + f'\t Neutral against {target_type} x{multipliers}' + Style.RESET_ALL)


while True:
    search_input = input("Enter Pokemon name: ")
    if search_input.lower() == "exit":
        break
    start_app(search_input.lower())
