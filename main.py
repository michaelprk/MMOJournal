import json
import os

# Path to the file where we'll save Pokémon data
DATA_FILE = "data/pokemon.json"

# This dictionary will hold all Pokémon categories while the app is running
pokemon_list = {
    "pvp": [],
    "shiny": []
}

def load_data():
    """Load saved pokémon data from JSON file, if it exists"""
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as file:
            return json.load(file)
    return []

def save_data():
    """Save current Pokémon list to JSON file."""
    with open(DATA_FILE, "w") as file:
        json.dump(pokemon_list, file, indent=2)

def add_pvp_pokemon():
    """Add a competitive (PvP) Pokémon with validated inputs."""
    print("\n--- Add PvP Pokémon ---")

    # === Name ===
    name = input("Enter Pokémon name: ").strip().title()
    while not name.replace(" ", "").isalpha():
        print("❌ Only letters allowed.")
        name = input("Enter Pokémon name: ").strip().title()

    # === Tier Selection from Dropdown ===
    tier_options = {
        "1": "OU",
        "2": "UU",
        "3": "NU",
        "4": "DOUBLES/VGC",
        "5": "UT"
    }

    print("\nChoose a tier:")
    for num, tier in tier_options.items():
        print(f"{num}. {tier}")

    while True:
        tier_choice = input("Select tier number: ").strip()
        if tier_choice in tier_options:
            tier = tier_options[tier_choice]
            break
        print("❌ Invalid choice. Please choose a number from the list.")

    # === Moves ===
    moves = []
    print("Enter up to 4 moves (press Enter to skip a move):")
    for i in range(4):
        move = input(f"Move {i + 1}: ").strip().title()
        if move:
            if not move.replace(" ", "").isalpha():
                print("❌ Moves must be letters only.")
                continue
            moves.append(move)

    # === IVs ===
    ivs = {}
    print("\nEnter IVs (0 to 31):")
    stats = ["HP", "ATK", "DEF", "SPATK", "SPDEF", "SPEED"]
    for stat in stats:
        while True:
            try:
                value = int(input(f"{stat}: "))
                if 0 <= value <= 31:
                    ivs[stat] = value
                    break
                else:
                    print("❌ Must be between 0 and 31.")
            except ValueError:
                print("❌ Please enter a number.")

    # === Nature ===
    while True:
        nature = input("Enter nature (e.g., Jolly, Modest): ").strip().title()
        if nature.replace(" ", "").isalpha():
            break
        print("❌ Nature must contain letters only.")

    # === Owned ===
    while True:
        owned_input = input("Do you own this Pokémon? (yes/no): ").strip().lower()
        if owned_input in ["yes", "no", "y", "n"]:
            owned = owned_input.startswith("y")
            break
        print("❌ Please enter yes or no.")

    # === Final Pokémon Entry ===
    pokemon = {
        "name": name,
        "tier": tier,
        "moves": moves,
        "ivs": ivs,
        "nature": nature,
        "owned": owned
    }

    pokemon_list["pvp"].append(pokemon)
    print(f"\n✅ {name} added to your PvP list!")


def add_shiny_pokemon():
    """Add a shiny hunt entry to your wishlist/checklist."""
    print("\n--- Add Shiny Pokémon Hunt ---")

    # === Name ===
    name = input("Enter Pokémon name: ").strip().title()
    while not name.replace(" ", "").isalnum():
        print("❌ Name should only include letters or numbers.")
        name = input("Enter Pokémon name: ").strip().title()

    # === Method Dropdown ===
    method_options = {
        "1": "Single",
        "2": "Horde 3x",
        "3": "Horde 5x",
        "4": "Safari",
        "5": "Lures",
        "6": "Egg Hunt",
        "7": "Honey Tree",
        "8": "Alpha Hunt"
    }

    print("\nChoose a hunting method:")
    for num, method in method_options.items():
        print(f"{num}. {method}")

    while True:
        method_choice = input("Select method number: ").strip()
        if method_choice in method_options:
            method = method_options[method_choice]
            break
        print("❌ Invalid choice. Please choose a number from the list.")

    # === Phases ===
    while True:
        try:
            phases = int(input("How many phases so far? (0 if none): "))
            if phases >= 0:
                break
            else:
                print("❌ Phases can't be negative.")
        except ValueError:
            print("❌ Please enter a valid number.")

    # === Phase Pokémon (Optional) ===
    phase_pokemon = []
    if phases > 0:
        print("Enter shiny Pokémon you got during earlier phases (one per line, press Enter to finish):")
        while True:
            poke = input("Phase Pokémon: ").strip().title()
            if not poke:
                break
            elif not poke.replace(" ", "").isalpha():
                print("❌ Use letters only.")
            else:
                phase_pokemon.append(poke)

    # === Obtained? ===
    while True:
        obtained_input = input("Have you obtained this shiny yet? (yes/no): ").strip().lower()
        if obtained_input in ["yes", "no", "y", "n"]:
            obtained = obtained_input.startswith("y")
            break
        print("❌ Please enter yes or no.")

    # === Final Shiny Entry ===
    shiny_entry = {
        "name": name,
        "method": method,
        "phases": phases,
        "phase_pokemon": phase_pokemon,
        "obtained": obtained
    }

    pokemon_list["shiny"].append(shiny_entry)
    print(f"\n✅ {name} hunt added to your shiny checklist!")


def main_menu():
    while True:
        print("\n=== MMOJournal Main Menu ===")
        print("1. Add PvP Pokémon")
        print("2. Add Shiny Hunt Entry")
        print("3. View PvP Pokémon")
        print("4. View Shiny Hunts")
        print("5. Remove Entry")
        print("6. Edit Entry")
        print("7. Filter/Search Entries")
        print("8. Save & Exit")

        choice = input("Choose an option (1–6): ").strip()

        if choice == "1":
            add_pvp_pokemon()
        elif choice == "2":
            add_shiny_pokemon()
        elif choice == "3":
            view_pvp()
        elif choice == "4":
            view_shiny()
        elif choice == "5":
            remove_entry()
        elif choice == "6":
            edit_entry()    
        elif choice == "7":
            filter_entries()    
        elif choice == "8":
            save_data()
            print("✅ Data saved. Goodbye!")
            break
        else:
            print("❌ Invalid choice. Try again.")


def view_pvp():
    """View all PvP Pokémon entries."""
    if "pvp" not in pokemon_list or not pokemon_list["pvp"]:
        print("No PvP Pokémon saved yet.")
        return

    print("\n--- PvP Pokémon ---")
    for p in pokemon_list["pvp"]:
        print(f"{p['name']} ({p['tier']}) | Nature: {p['nature']} | Owned: {'Yes' if p['owned'] else 'No'}")
        print(f"Moves: {', '.join(p['moves'])}")
        print(f"IVs: {p['ivs']}")
        print("-" * 40)

def view_shiny():
    """View all shiny wishlist/hunt entries."""
    if "shiny" not in pokemon_list or not pokemon_list["shiny"]:
        print("No shiny hunts saved yet.")
        return

    print("\n--- Shiny Hunts ---")
    for s in pokemon_list["shiny"]:
        print(f"{s['name']} | Method: {s['method']} | Phases: {s['phases']}")
        if s["phase_pokemon"]:
            print(f"Phases obtained: {', '.join(s['phase_pokemon'])}")
        print(f"Obtained: {'Yes' if s['obtained'] else 'No'}")
        print("-" * 40)

def remove_entry():
    print("\n--- Remove Entry ---")
    print("1. Remove PvP Pokémon")
    print("2. Remove Shiny Hunt")

    choice = input("Choose a category (1 or 2): ").strip()

    if choice == "1" and pokemon_list["pvp"]:
        print("\nPvP Pokémon List:")
        for idx, p in enumerate(pokemon_list["pvp"], start=1):
            print(f"{idx}. {p['name']} ({p['tier']})")

        index = input("Enter number to remove (or press Enter to cancel): ").strip()
        if index.isdigit() and 1 <= int(index) <= len(pokemon_list["pvp"]):
            removed = pokemon_list["pvp"].pop(int(index) - 1)
            print(f"✅ Removed {removed['name']} from PvP list.")
        else:
            print("❌ Invalid selection or cancelled.")

    elif choice == "2" and pokemon_list["shiny"]:
        print("\nShiny Hunt List:")
        for idx, s in enumerate(pokemon_list["shiny"], start=1):
            print(f"{idx}. {s['name']} ({s['method']})")

        index = input("Enter number to remove (or press Enter to cancel): ").strip()
        if index.isdigit() and 1 <= int(index) <= len(pokemon_list["shiny"]):
            removed = pokemon_list["shiny"].pop(int(index) - 1)
            print(f"✅ Removed {removed['name']} from shiny list.")
        else:
            print("❌ Invalid selection or cancelled.")
    else:
        print("❌ No entries to remove in that category.")

def edit_entry():
    print("\n--- Edit Entry ---")
    print("1. Edit PvP Pokémon")
    print("2. Edit Shiny Hunt")
    choice = input("Choose a category (1 or 2): ").strip()

    if choice == "1" and pokemon_list["pvp"]:
        print("\nPvP Pokémon List:")
        for idx, p in enumerate(pokemon_list["pvp"], start=1):
            print(f"{idx}. {p['name']} ({p['tier']})")

        index = input("Enter number to edit (or press Enter to cancel): ").strip()
        if index.isdigit() and 1 <= int(index) <= len(pokemon_list["pvp"]):
            p = pokemon_list["pvp"][int(index) - 1]

            print("\nPress Enter to keep existing value.")
            p["name"] = input(f"Name [{p['name']}]: ").strip().title() or p["name"]
            p["tier"] = input(f"Tier [{p['tier']}]: ").strip().upper() or p["tier"]
            p["nature"] = input(f"Nature [{p['nature']}]: ").strip().title() or p["nature"]

            print("Owned? (yes/no or press Enter to skip)")
            owned_input = input(f"Currently {'Yes' if p['owned'] else 'No'}: ").strip().lower()
            if owned_input in ["yes", "no", "y", "n"]:
                p["owned"] = owned_input.startswith("y")

            # Moves: Enter new list or skip
            print("Enter moves separated by commas (or press Enter to keep existing):")
            move_input = input(f"Moves [{', '.join(p['moves'])}]: ").strip()
            if move_input:
                p["moves"] = [m.strip().title() for m in move_input.split(",") if m.strip()]

            # IVs: Optional update
            for stat in p["ivs"]:
                new_val = input(f"{stat} IV [{p['ivs'][stat]}]: ").strip()
                if new_val.isdigit() and 0 <= int(new_val) <= 31:
                    p["ivs"][stat] = int(new_val)

            print(f"\n✅ {p['name']} updated!")

    elif choice == "2" and pokemon_list["shiny"]:
        print("\nShiny Hunt List:")
        for idx, s in enumerate(pokemon_list["shiny"], start=1):
            print(f"{idx}. {s['name']} ({s['method']})")

        index = input("Enter number to edit (or press Enter to cancel): ").strip()
        if index.isdigit() and 1 <= int(index) <= len(pokemon_list["shiny"]):
            s = pokemon_list["shiny"][int(index) - 1]

            print("\nPress Enter to keep existing value.")
            s["name"] = input(f"Name [{s['name']}]: ").strip().title() or s["name"]
            s["method"] = input(f"Method [{s['method']}]: ").strip().title() or s["method"]

            phase_input = input(f"Phases [{s['phases']}]: ").strip()
            if phase_input.isdigit():
                s["phases"] = int(phase_input)

            phase_poke_input = input(f"Phase Pokémon [{', '.join(s['phase_pokemon'])}]: ").strip()
            if phase_poke_input:
                s["phase_pokemon"] = [p.strip().title() for p in phase_poke_input.split(",") if p.strip()]

            obtained_input = input(f"Obtained? (yes/no) [Currently {'Yes' if s['obtained'] else 'No'}]: ").strip().lower()
            if obtained_input in ["yes", "no", "y", "n"]:
                s["obtained"] = obtained_input.startswith("y")

            print(f"\n✅ {s['name']} updated!")

    else:
        print("❌ Invalid category or no entries available.")

def filter_entries():
    print("\n--- Filter/Search ---")
    print("1. Filter PvP Pokémon")
    print("2. Filter Shiny Hunts")
    choice = input("Choose category (1 or 2): ").strip()

    if choice == "1" and pokemon_list["pvp"]:
        print("\nFilter by:")
        print("1. Tier")
        print("2. Nature")
        f_choice = input("Choose filter (1 or 2): ").strip()

        if f_choice == "1":
            tier = input("Enter tier to search (OU, UU, NU, DOUBLES/VGC, UT): ").strip().upper()
            results = [p for p in pokemon_list["pvp"] if p["tier"] == tier]
        elif f_choice == "2":
            nature = input("Enter nature to search: ").strip().title()
            results = [p for p in pokemon_list["pvp"] if p["nature"] == nature]
        else:
            print("❌ Invalid filter.")
            return

        print(f"\nFound {len(results)} Pokémon:")
        for p in results:
            print(f"- {p['name']} ({p['tier']}), Nature: {p['nature']}, Owned: {'Yes' if p['owned'] else 'No'}")

    elif choice == "2" and pokemon_list["shiny"]:
        print("\nFilter by:")
        print("1. Method")
        print("2. Obtained (yes/no)")
        f_choice = input("Choose filter (1 or 2): ").strip()

        if f_choice == "1":
            method = input("Enter shiny method: ").strip().title()
            results = [s for s in pokemon_list["shiny"] if s["method"] == method]
        elif f_choice == "2":
            owned_input = input("Show obtained only? (yes/no): ").strip().lower()
            if owned_input in ["yes", "y"]:
                results = [s for s in pokemon_list["shiny"] if s["obtained"]]
            elif owned_input in ["no", "n"]:
                results = [s for s in pokemon_list["shiny"] if not s["obtained"]]
            else:
                print("❌ Invalid input.")
                return
        else:
            print("❌ Invalid filter.")
            return

        print(f"\nFound {len(results)} shiny hunts:")
        for s in results:
            status = "✅ Obtained" if s["obtained"] else "🔄 Still Hunting"
            print(f"- {s['name']} ({s['method']}) – {status}")

    else:
        print("❌ Invalid category or no entries available.")


# Load data from file and start the menu
loaded_data = load_data()
pokemon_list = loaded_data if loaded_data else {"pvp": [], "shiny": []}

main_menu()

