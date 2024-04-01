import os
import json

from src import INTERIM_DATA_DIR, PROCESSED_DATA_DIR


def format_data(data: dict):

    ## format spell according to the attributes that are present in the data
    
    formatted_data = dict()
    formatted_data["instruction"] = "Write a spell for the 5th edition of the Dungeons & Dragons game."

    spell_name = data["name"]
    spell_level = data["level"]
    spell_school = data["school"]
    spell_classes = data["classes"]
    spell_cast_time = data["cast_time"]
    spell_range = data["range"]
    spell_duration = data["duration"]

    spell_components = []

    if data["verbal"] == 1:
        spell_components.append("V")
    
    if data["somatic"] == 1:
        spell_components.append("S")
    
    if data["material"] == 1:
        spell_components.append("M")
    
    spell_components = ', '.join(spell_components)
    if len(spell_components) == 0:
        spell_components  = "None"

    spell_description = data["description"]
    spell_material_cost = data["material_cost"]
    spell_material_cost_str = f"Material cost: {spell_material_cost}\n" if spell_material_cost else ""

    formatted_data["response"] = \
        f"Name: {spell_name}\n" \
        f"Level: {spell_level}\n" \
        f"School: {spell_school}\n" \
        f"Classes: {spell_classes}\n" \
        f"Casting time: {spell_cast_time}\n" \
        f"Range: {spell_range}\n" \
        f"Duration: {spell_duration}\n" \
        f"Components: {spell_components}\n"\
        f"{spell_material_cost_str}" \
        f"Description: {spell_description}"

    return formatted_data


def main():
    
    input_file_path = os.path.join(INTERIM_DATA_DIR, 'spells_processed.jsonl')
    output_file_path = os.path.join(PROCESSED_DATA_DIR, 'spells_processed_and_formatted.jsonl')

    num_instances = 0

    with open(output_file_path, 'w', encoding='utf8') as f_out:
        with open(input_file_path, 'r', encoding='utf8') as f_in:

            print("-" * 24)
            print(f"FORMATTING DATASET: {input_file_path}")

            for processed_data in f_in:
                processed_data = json.loads(processed_data)
                formatted_data = format_data(processed_data)
                json.dump(formatted_data, f_out)
                f_out.write('\n')
                num_instances += 1

            print("-" * 24)
    
    print("COMPLETED!")

    return num_instances


if __name__ == "__main__":
    main()
