import json, requests
from dataclasses import asdict 
from entities import SimpleCard, TypeData
from datetime import date

def get_creature_type_data_from_deck(deck: str) -> list[TypeData]:
    with open("decklist\\" + deck, "r", encoding="utf-8") as f:
        # Strip the leading number from the decklist txt file
        card_names = [line.strip().split(' ', 1)[1] for line in f if line.strip()]
        
        # Return all creatures from card_names
        creatures : list[SimpleCard] = get_creatures_from_card_names(card_names)
        
        # Grabs all creature type data from creature cards
        creature_type_counts = get_creature_type_counts(creatures)
    return creature_type_counts 

def get_creature_type_counts(cards : list[SimpleCard]) -> list[TypeData]:
    types : list[TypeData] = []
    type_names : list[str] = [t.type_name for t in types]
    for card in cards:
        for sub in card.subtype:
            if sub in type_names:
                for t in types:
                    if sub == t.type_name:
                        t.count += 1
                        t.card_names.append(card.name)
            else:
                type_names.append(sub)
                types.append(
                    TypeData(
                        sub,
                        1,
                        [card.name]
                    )
                )
    return sorted(types, key=lambda x:(-x.count, x.type_name))

def get_creatures_from_card_names(cards : list[str]) -> list[SimpleCard]:
    creatures: list[SimpleCard] = []
    with open("data\\simple_card_info.json", "r", encoding="utf-8") as f:
        all_simples = json.load(f)
        all_creatures = [SimpleCard.from_simple(item) for item in all_simples if 'Creature' in item.get('supertype', [])]
        for card in cards:
            for creature in all_creatures:
                if card == creature.name:
                    creatures.append(creature)
    return list(set(creatures))

def convert_cards(input_filename: str, output_filename: str):
    with open(input_filename, "r", encoding="utf-8") as f:
        # You can modify this if your JSON file is a JSON array instead of newline-delimited
        try:
            card_data = json.load(f)
        except json.decoder.JSONDecodeError:
            # fallback to line-by-line reading (newline-delimited JSON)
            f.seek(0)
            card_data = [json.loads(line) for line in f]

    simple_cards = [SimpleCard.from_dict(card) for card in card_data]

    # Convert dataclasses to dicts for JSON serialization
    simplified_dicts = [asdict(card) for card in simple_cards]

    with open(output_filename, "w", encoding="utf-8") as out_f:
        json.dump(simplified_dicts, out_f, indent=2)

def update_card_info():
    #Oracle Text for cards, smallest bulk data
    url = "https://api.scryfall.com/bulk-data/27bf3214-1271-490b-bdfe-c0be6c23d02e"
    unique_card_path = "data\\unique_all_card_info.json"

    response = requests.get(url)
    if (response.ok):
        data = json.loads(response.content.decode("utf-8"))

        data_uri = data["download_uri"]
        data_response = requests.get(data_uri, stream=True)
        if (data_response.ok):
            with open(unique_card_path, 'wb') as f:
                for chunk in data_response.iter_content(chunk_size=8192):
                    f.write(chunk)
            convert_cards(unique_card_path, "data\\simple_card_info.json")
            return
        else:    
            print(f"There was an error with the request: {data_response.status_code}")
            return
    print(f"There was an error with the request: {response.status_code}")

def run_deck_analysis(deck_name: str, download_latest: bool = False) -> list[TypeData]:
    if download_latest:
        update_card_info()
    type_data = get_creature_type_data_from_deck(deck_name)
    return type_data