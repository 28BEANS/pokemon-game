import os
import random

FILENAME_POKEDEX = "pokemon_database.txt"
FILENAME_MYPOKEMON = "my_pokemons.txt"

def input_validator(min, max, prompt, active): # utility function used to validate user inputs
    user_input = input(prompt)
    keepGoing = True

    while keepGoing:
        if user_input in ("r", "c") and active == True:
            return user_input
        if not user_input.isdigit():
            print("Invalid input.")
            user_input = input(prompt)
        elif int(user_input) < min or int(user_input) > max:
            print(f"Choose a valid option from {min} to {max}")
            user_input = input(prompt)
        else:
            keepGoing = False
    return int(user_input)

def create_default_pokedex_database(FILENAME_POKEDEX): # creates default pokemon database if there is none
    with open (f"{FILENAME_POKEDEX}", "w") as file:
        file.write("Charmander,Plain,Fire,None,Lizard,45,1\n"
                   "Bulbasaur,Grass,Grass,Poison,Seed,45,1\n"
                   "Pikachu,Tall Grass,Electric,None,Mouse,190,1\n"
                   "Pidgey,Plain,Normal,Flying,Tiny Bird,255,1\n"
                   "Rattata,Plain,Normal,None,Mouse,255,1\n"
                   "Jigglypuff,Plain,Normal,Fairy,Balloon,170,1\n"
                   "Vulpix,Tall Grass,Fire,None,Fox,190,1\n"
                   "Zubat,Grass,Poison,Flying,Bat,255,1\n"
                   "Diglett,Plain,Ground,None,Mole,255,1\n"
                   "Psyduck,Water,Water,None,Duck,190,1\n"
                   "Abra,Tall Grass,Psychic,None,Psi,200,1\n"
                   "Ponyta,Plain,Fire,None,Fire Horse,190,1\n"
                   "Geodude,Plain,Rock,Ground,Rock,255,1\n"
                   "Doduo,Plain,Normal,Flying,Twin Bird,190,1\n"
                   "Haunter,Grass,Ghost,Poison,Gas,90,1\n"
                   "Onix,Plain,Rock,Ground,Rock Snake,45,1\n"
                   "Drowzee,Grass,Psychic,None,Hypnosis,190,1\n"
                   "Voltorb,Plain,Electric,None,Ball,190,1\n"
                   "Cubone,Plain,Ground,None,Lonely,190,1\n"
                   "Chansey,Tall Grass,Normal,None,Egg,30,1\n"
                   "Staryu,Water,Water,None,Star Shape,225,1\n"
                   "Eevee,Grass,Normal,None,Evolution,45,1\n"
                   "Mewtwo,Plain,Psychic,None,Genetic,3,1\n"
                   "Exeggcute,Grass,Grass,Psychic,Egg,90,1\n"
                   "Magnemite,Plain,Electric,Steel,Magnet,190,1\n")

def create_default_my_pokemon_database(FILENAME_MYPOKEMON): # creates default 'my_pokemon' database if there is none
    with open(f"{FILENAME_MYPOKEMON}", "w") as file:
        file.write("")

def load_pokedex_database(FILENAME_POKEDEX): # retrieves data from "pokemon_database" and stores it into dictionary
    pokedex = {}
    if not os.path.exists(FILENAME_POKEDEX):
        print(f"Error: The file '{FILENAME_POKEDEX}' was not found.")
        print("Default file was created instead")
        create_default_pokedex_database(FILENAME_POKEDEX)

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

def load_my_pokemon_database(FILENAME_MYPOKEMON): # retrieves data from "my_pokemon" database and stores it into 2d list
    myPokemon = []

    if not os.path.exists(FILENAME_MYPOKEMON):
        print(f"Error: The file '{FILENAME_MYPOKEMON}' was not found.")
        print("Default File was created instead")
        create_default_my_pokemon_database(FILENAME_MYPOKEMON)
        return myPokemon

    with open(FILENAME_MYPOKEMON) as file:
        lines = [line.strip() for line in file if line.strip()]
        if not lines:
            return myPokemon
        for line in lines:
            name, rock, bait, turns = line.split(',')
            myPokemon.append([name, rock, bait, turns])

    return myPokemon

def update_pokedex_database(pokedex, FILENAME_POKEDEX): # update whole pokemon databasse
    lines = []
    for name, data in pokedex.items():
        line = f"{name},{data['area']},{data['type1']},{data['type2']},{data['species']},{data['captureRate']},{data['isCaught']}"
        lines.append(line)

    with open(FILENAME_POKEDEX, 'w') as file:
        file.write("\n".join(lines))

def update_my_pokemon_database(selectedPokemon, rock, bait, turns): # adds captured pokemon to "my_pokemon" database
    line = f"{selectedPokemon},{rock},{bait},{turns}"

    with open(FILENAME_MYPOKEMON, 'a') as file:
        file.write(line + "\n")

def remove_data_my_pokemon_by_index(filename, index_to_remove): #removes selected pokemon from "my_pokemon" database
    with open(filename, "r") as file:
        rows = file.readlines()

    with open(filename, "w") as file:
        for idx, row in enumerate(rows):
            if idx != index_to_remove:
                file.write(row)

def view_pokedex(): # displays whole pokemo database
    pokedex = load_pokedex_database(FILENAME_POKEDEX)
    print("{:^90}".format(">> POKEDEX <<"))
    print()

    print("=" * 95)
    print("{:<15} {:<15} {:<15} {:<15} {:<15} {:<15}".format(
        "Name", "Area", "Type 1", "Type 2", "Species", "Capture Rate"
    ))
    print("=" * 95)

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

def view_my_pokemon(): # displays captured pokemons
    myPokemon = load_my_pokemon_database(FILENAME_MYPOKEMON)
    print("{:<15} {:<15} {:<15} {:<15}".format(
        "Name", "Rocks Thrown", "Baits Thrown", "Turns"
    ))
    print("=" * 70)

    if len(myPokemon) == 0:
        print("{:^70}".format(">> NO POKEMONS CAPTURED <<"))

    else:
        for data in myPokemon:
            name, rock, bait, turns = data
            print("{:<15} {:<15} {:<15} {:<15}".format(name, rock, bait, turns))

    print("=" * 70)
    print()


def remove_pokemon(): # gives index-based list of captured pokemon for easy removal
    with open(FILENAME_MYPOKEMON, "r") as file:
        rows = file.readlines()

    myPokemon = []
    for i, line in enumerate(rows):
        name, rock, bait, turns = line.strip().split(',')
        myPokemon.append([i, name, rock, bait, turns])

    print("{:<5} {:<15} {:<15} {:<15} {:<15}".format("ID", "Name", "Rocks Thrown", "Baits Thrown", "Turns"))
    print("=" * 75)
    if len(myPokemon) == 0:
        print("{:^70}".format(">> NO POKEMONS CAPTURED <<"))
        print()
    else:
        for entry in myPokemon:
            idx, name, rock, bait, turns = entry
            print("{:<5} {:<15} {:<15} {:<15} {:<15}".format(idx, name, rock, bait, turns))
    print("=" * 75)

    while True:
        if len(myPokemon) == 0:
            break

        else:
            choice = input_validator(0,len(rows),"Enter the ID of the Pokémon to release [c to cancel]: ", True)
            if choice == "c":
                break
            elif 0 <= choice < len(rows):
                remove_data_my_pokemon_by_index(FILENAME_MYPOKEMON, choice)
                print("Pokémon released.")
                break



def sort_pokemon(): #sort pokemons by their area
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

def create_safari_zone(): # creates the playing field and also randomizes pokemon spawns
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

def get_capture_rate(pokemonSpawns, choice): # getter function for a certain pokemon's capture rate
    pokedex = load_pokedex_database(FILENAME_POKEDEX)
    chosenPokemons = pokemonSpawns
    chosen = int(choice)
    selectedPokemon = chosenPokemons[chosen - 1][1]

    captureRate = 0

    for name, data in pokedex.items():
        if selectedPokemon == name:
            captureRate = int(data["captureRate"])

    return captureRate

def change_status(pokemonSpawns, choice, captured): # change a certain's pokemon 'isCaught' status
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

def simulate_turn(captureRate, runChance): # determines the 'fate' of the pokemon if user chose to capture them
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

def play_safari_zone(): # where the user interacts with pokemon and the 'playing zone'
    keepGoing = True
    captureRate = 0

    while keepGoing:
        pokemonSpawns = create_safari_zone()
        print()
        selectedPokemon = ""
        recordedAction = [0, 0] # rock, bait, turn
        stats = [captureRate, 0]
        print("OPTIONS")
        print("\t[1-5] : Interact with a pokemon")
        print("\t[0] : Refresh spawn area")
        print("\t[r] : Return")
        print()

        choice = input_validator(0, 5, "Choose: ", True)
        print()

        if choice in (1, 2, 3, 4, 5):
            stats[0] = get_capture_rate(pokemonSpawns, choice)
            change_status(pokemonSpawns, choice, False)
            if choice == 1:
                print(f"You've encountered {pokemonSpawns[0][1]}")
                selectedPokemon = pokemonSpawns[0][1]
            elif choice == 2:
                print(f"You've encountered {pokemonSpawns[1][1]}")
                selectedPokemon = pokemonSpawns[1][1]
            elif choice == 3:
                print(f"You've encountered {pokemonSpawns[2][1]}")
                selectedPokemon = pokemonSpawns[2][1]
            elif choice == 4:
                print(f"You've encountered {pokemonSpawns[3][1]}")
                selectedPokemon = pokemonSpawns[3][1]
            elif choice == 5:
                print(f"You've encountered {pokemonSpawns[4][1]}")
                selectedPokemon = pokemonSpawns[4][1]

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

                takenAction = input_validator(1, 4, "Choose: ", False)
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

def my_pokemon(): # initiates my_pokemon sub-function
    keepGoing = True

    while keepGoing:
        print("OPTIONS"
              "\n\t[1] : View My Pokemon"
              "\n\t[2] : Release a Pokemon"
              "\n\t[r] : Return")
        print()

        choice = input_validator(1, 2, "Choose: ", True)
        print()
        if choice == 1:
            view_my_pokemon()
        elif choice == 2:
            remove_pokemon()
        elif choice == "r":
            keepGoing = False

def reset_database(FILENAME_POKEDEX, FILENAME_MYPOKEMON): # reset both database into their default state
    while True:
        choice = input_validator(0, 1, "Are you sure? [0] yes [1] no: ", False)
        if choice == 0:
            create_default_pokedex_database(FILENAME_POKEDEX)
            create_default_my_pokemon_database(FILENAME_MYPOKEMON)
            print("Progress Reset")
            break
        elif choice == 1:
            break

def main(): # main block where main options will be displayed to user

    while True:
        print("~*" * 25)
        print("{:^50}".format("MAIN MENU"))
        print("~*" * 25)
        print("\t[1] : View Pokedex")
        print("\t[2] : My Pokemon")
        print("\t[3] : Play Safari Zone")
        print("\t[4] : Reset Progress")
        print("\t[5] : Exit")
        print()

        choice = input_validator(1, 5, "Watcha wanna do?: ", False)
        print()

        if choice == 1:
            view_pokedex()
        elif choice == 2:
            my_pokemon()
        elif choice == 3:
            play_safari_zone()
        elif choice == 4:
            reset_database(FILENAME_POKEDEX, FILENAME_MYPOKEMON)
        elif choice == 5:
            print("Saved Progress. You've Exited the Game")
            break


main()
