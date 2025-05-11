import os
import random

FILENAME_POKEDEX = "pokemon_database.txt"
FILENAME_MYPOKEMON = "my_pokemons.txt"

def input_validator(min, max, prompt):
    user_input = input(prompt)
    keepGoing = True

    while keepGoing:
        if not user_input.isdigit():
            print("Invalid input. Please enter a numeric value.")
            user_input = input(prompt)
        elif int(user_input) < min or int(user_input) > max:
            print(f"Choose a valid option from {min} to {max}")
            user_input = input(prompt)
        else:
            keepGoing = False
    return int(user_input)


def load_pokedex_database(FILENAME_POKEDEX):
    pokedex = {}
    if not os.path.exists(FILENAME_POKEDEX):
        print(f"Error: The file '{FILENAME_POKEDEX}' was not found.")
        return pokedex

    with open(FILENAME_POKEDEX) as file:
        for line in file:
            name, area, type1, type2, species, catch_rate, isCaught = line.strip().split(',')
            pokedex[name] = {
                "area": area,
                "type1": type1,
                "type2": type2,
                "species": species,
                "captureRate": int(catch_rate),
                "isCaught": int(isCaught)  # 1 -> not seen, 2 -> encountered, 3 -> caught
            }
    return pokedex

def load_my_pokemon_database(FILENAME_MYPOKEMON):
    myPokemon = {}
    if not os.path.exists(FILENAME_MYPOKEMON):
        print(f"Error: The file '{FILENAME_MYPOKEMON}' was not found.")
        return myPokemon

    with open(FILENAME_MYPOKEMON) as file:
        for line in file:
            name, rock, bait, turns = line.strip().split(',')
            myPokemon[name] = {
                "rocksThrown" : rock,
                "baitsThrown" : bait,
                "turns" : turns
            }
    return myPokemon

def update_pokedex_database(pokedex, FILENAME_POKEDEX):
    lines = []
    for name, data in pokedex.items():
        line = f"{name},{data['area']},{data['type1']},{data['type2']},{data['species']},{data['captureRate']},{data['isCaught']}"
        lines.append(line)

    with open(FILENAME_POKEDEX, 'w') as file:
        file.write("\n".join(lines))

def update_my_pokemon_database(selectedPokemon, rock, bait, turns):
    line = f"{selectedPokemon},{rock},{bait},{turns}"

    with open(FILENAME_MYPOKEMON, 'a') as file:
        file.write(line + "\n")

def remove_data_my_pokemon(filename, key_name):
    with open(filename, "r") as file:
        rows = file.readlines()  # Read all rows into a list

    with open(filename, "w") as file:
        for row in rows:
            if not row.startswith(key_name + ","):  # Skip the row to delete
                file.write(row)

def view_pokedex():
    pokedex = load_pokedex_database(FILENAME_POKEDEX)

    print("{:<15} {:<15} {:<15} {:<15} {:<15} {:<15}".format(
        "Name", "Area", "Type 1", "Type 2", "Species", "Capture Rate"
    ))
    print("=" * 90)

    for name, data in pokedex.items():
        status = data["isCaught"]
        if status == 1:
            print("{:<15} {:<15} {:<15} {:<15} {:<15} {:<15}".format(
                name, "???", "???", "???", "???", "???"
            ))
        elif status == 2:
            print("{:<15} {:<15} {:<15} {:<15} {:<15} {:<15}".format(
                name, data["area"], "???", "???", "???", "???"
            ))
        elif status == 3:
            print("{:<15} {:<15} {:<15} {:<15} {:<15} {:<15}".format(
                name,
                data["area"],
                data["type1"],
                data["type2"],
                data["species"],
                data["captureRate"],
            ))
    print("=" * 90)
    print()

def view_my_pokemon():
    myPokemon = load_my_pokemon_database(FILENAME_MYPOKEMON)
    print("{:<15} {:<15} {:<15} {:<15}".format(
        "Name", "Rocks Thrown", "Baits Thrown", "Turns"
    ))
    print("=" * 70)

    for name, data in myPokemon.items():
        print("{:<15} {:<15} {:<15} {:<15} ".format(
            name,
            data["rocksThrown"],
            data["baitsThrown"],
            data["turns"],
        ))
    print("=" * 70)
    print()

def remove_pokemon():
    view_my_pokemon()
    print()
    choice = input("Type the name of pokemon you want to release: ")
    remove_data_my_pokemon(FILENAME_MYPOKEMON, choice)

def sort_pokemon():
    pokedex = load_pokedex_database(FILENAME_POKEDEX)
    areas = {
        "grass": [],
        "plain": [],
        "water": [],
        "tallGrass": []
    }
    for pokemon, data in pokedex.items():
        if data["area"].lower() == "grass":
            areas["grass"].append(pokemon)
        elif data["area"].lower() == "plain":
            areas["plain"].append(pokemon)
        elif data["area"].lower() == "water":
            areas["water"].append(pokemon)
        elif data["area"].lower() == "tall grass":
            areas["tallGrass"].append(pokemon)

    return areas

def create_safari_zone():
    areas = sort_pokemon()

    grid = [
        ['[g]', '[g]', '[g]', '[p]', '[p]', '[p]'],
        ['[g]', '[g]', '[g]', '[p]', '[p]', '[p]'],
        ['[g]', '[g]', '[g]', '[p]', '[p]', '[p]'],
        ['[w]', '[w]', '[w]', '[t]', '[t]', '[t]'],
        ['[w]', '[w]', '[w]', '[t]', '[t]', '[t]'],
        ['[w]', '[w]', '[w]', '[t]', '[t]', '[t]'],
    ]

    coordinates = []
    for i in range(len(grid)): # flatten grid
        for j in range(len(grid[i])):
            coordinates.append((i, j))

    randomSpots = random.sample(coordinates, 5)

    pokemon_spawns = []
    for num, (x, y) in enumerate(randomSpots, start=1):
        area_key = grid[x][y][1]  # get area type
        if area_key == 'g':
            pokemon = random.choice(areas["grass"])
        elif area_key == 'p':
            pokemon = random.choice(areas["plain"])
        elif area_key == 'w':
            pokemon = random.choice(areas["water"])
        elif area_key == 't':
            pokemon = random.choice(areas["tallGrass"])

        grid[x][y] = f"[{num}]"
        pokemon_spawns.append((num, pokemon))

    for row in grid:
        print(' '.join(row))

    return pokemon_spawns

def get_capture_rate(pokemonSpawns, choice):
    pokedex = load_pokedex_database(FILENAME_POKEDEX)
    chosenPokemons = pokemonSpawns
    chosen = int(choice)
    selectedPokemon = chosenPokemons[chosen - 1][1]

    captureRate = 0

    for name, data in pokedex.items():
        if selectedPokemon == name:
            captureRate = int(data["captureRate"])

    return captureRate

def change_status(pokemonSpawns, choice, captured):
    pokedex = load_pokedex_database(FILENAME_POKEDEX)
    chosenPokemons = pokemonSpawns
    chosen = int(choice)
    selectedPokemon = chosenPokemons[chosen - 1][1]

    for name, data in pokedex.items():
        if selectedPokemon == name:
            if data["isCaught"] == 1:
                data["isCaught"] = 2
            elif captured == True:
                data["isCaught"] = 3

    update_pokedex_database(pokedex, FILENAME_POKEDEX)

def simulate_turn(captureRate, runChance):
    catch_roll = random.randint(1, 255)
    is_caught = catch_roll <= captureRate

    run_roll = random.randint(1, 100)
    has_run = run_roll <= runChance

    if is_caught:
        return "caught"
    elif has_run:
        return "ran away"
    else:
        return "still there"

def play_safari_zone():
    keepGoing = True
    pokemonSpawns = create_safari_zone()
    captureRate = 0
    print()
    while keepGoing:
        selectedPokemon = ""
        recordedAction = [0, 0] # rock, bait, turn
        stats = [captureRate, 0]
        print("Options")
        print("\t[1-5] : Interact with a pokemon")
        print("\t[0] : Refresh spawn area")
        print("\t[r] : Return")
        print()

        choice = input("Choice: ")
        print()

        if choice.isdigit() and choice in ('1','2','3','4','5'):
            stats[0] = get_capture_rate(pokemonSpawns, choice)
            change_status(pokemonSpawns, choice, False)
            match choice:
                case '1':
                    print(f"You've encountered {pokemonSpawns[0][1]}")
                    selectedPokemon = pokemonSpawns[0][1]
                case '2':
                    print(f"You've encountered {pokemonSpawns[1][1]}")
                    selectedPokemon = pokemonSpawns[1][1]
                case '3':
                    print(f"You've encountered {pokemonSpawns[2][1]}")
                    selectedPokemon = pokemonSpawns[2][1]
                case '4':
                    print(f"You've encountered {pokemonSpawns[3][1]}")
                    selectedPokemon = pokemonSpawns[3][1]
                case '5':
                    print(f"You've encountered {pokemonSpawns[4][1]}")
                    selectedPokemon = pokemonSpawns[4][1]
                case _:
                    print("Choose a valid option")

            for turn in range(1, 5 + 1):
                print(f"Capture Rate: {stats[0]}")
                print(f"Run Chance: {stats[1]}")
                print(f"Turn {turn}")
                print()
                print("OPTIONS"
                      "\n\t[1] : Safari Ball"
                      "\n\t[2] : Throw Rock"
                      "\n\t[3] : Safari Bait"
                      "\n\t[4] : Run")

                takenAction = input_validator(1, 4, "Choose: ")
                print()
                if turn == 4:
                    stats[1] = 100
                elif turn == 5:
                    print(f"{selectedPokemon} ran away!")
                    break

                if takenAction == 1:
                    result = simulate_turn(stats[0], stats[1])
                    if result == "caught":
                        print(f"You caught {selectedPokemon}")
                        update_my_pokemon_database(selectedPokemon, recordedAction[0], recordedAction[1], turn)
                        change_status(pokemonSpawns, choice, True)
                        break
                    elif result == "ran away":
                        print(f"{selectedPokemon} ran away!")
                        break
                    else:
                        print("The Pokémon is still there. Try again!")
                elif takenAction == 2:
                    recordedAction[0] += 1
                    stats[0] = int(round(stats[0] + (stats[0] * .05)))
                    stats[1] += 5
                elif takenAction == 3:
                    recordedAction[1] += 1
                    stats[0] = int(round(stats[0] - (stats[0] * .05)))
                    stats[1] -= 5
                elif takenAction == 4:
                    break

                if turn < 4:
                    stats[1] += 10

        elif choice == '0':
            pokemonSpawns = create_safari_zone()
            print()
        elif choice == 'r':
            keepGoing = False

def my_pokemon():
    print("OPTIONS"
          "\n\t[1] : View My Pokemon"
          "\n\t[2] : Release a Pokemon")

    choice = int(input("Choose: "))
    print()
    match choice:
        case 1:
            view_my_pokemon()
        case 2:
            remove_pokemon()

def main():

    while True:
        print("~*" * 35)
        print("{:^70}".format("MAIN MENU"))
        print("~*" * 35)
        print("\t[1] : View Pokedex")
        print("\t[2] : My Pokemon")
        print("\t[3] : Play Safari Zone")
        print("\t[4] : Exit")
        print()

        choice = input_validator(1, 4, "Watcha wanna do?: ")
        print()

        match choice:
            case 1:
                view_pokedex()
            case 2:
                my_pokemon()
            case 3:
                play_safari_zone()
            case 4:
                print("Saved Progress. You've Exited the Game")
                break


main()