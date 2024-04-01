import os
import re
import json

from src import RAW_DATA_DIR, INTERIM_DATA_DIR
from src.utils.data_iter import CsvDataProcessor, JsonDataProcessor


VALID_CLASSES = set([
    'Barbarian', 'Bard', 'Cleric', 'Druid', 'Fighter', 'Monk', 'Paladin', 'Ranger', 'Rogue', 'Sorcerer', 'Warlock', 'Wizard', 'Artificer', 'Blood Hunter'
])


class HomebrewDataProcessor(JsonDataProcessor):

    def process_single_data_line(self, data: dict):

        processed_data = dict()

        data_keys = set(data.keys())
        mandatory_keys = set(["classes", "components", "casting_time", "range", "duration"])

        # check that all the mandatory keys for the spell are present in the data instance, otherwise skip
        if len(data_keys.intersection(mandatory_keys)) != len(mandatory_keys):
            return None
        
        spell_classes = set(data["classes"])
        spell_classes = sorted(spell_classes.intersection(VALID_CLASSES))

        # check that at least one of the classes is an official class of the game
        if len(spell_classes) == 0:
            return None

        spell_description = data["description"]
        spell_description = spell_description[:-1]

        # remove number of votes for spell that may be found at the end of the spell description
        spell_description_length = len(spell_description)

        spell_description = re.sub('\d.\d\d \(\d votes\)?', '', spell_description)

        if spell_description_length == len(spell_description):
            spell_description = re.sub('\d.\d\d \(one vote\)?', '', spell_description)

        if spell_description[-1] == "\n":
            spell_description = spell_description[:-1]

        # extract level and school of the spell from header
        header = data["header"]
        level_info = re.findall('([0-9])[a-z][a-z]-level', header)

        if len(level_info) == 0:
            level = 0
            school = re.findall('(.*) cantrip', header)

            if len(school) == 0:
                return None
            else:
                school = school[0]
        else:
            level = int(level_info[0])
            school = re.findall('[0-9][a-z][a-z]-level (.*)', header)[0]
        
        components = data["components"]

        materials = re.findall('\((.*)\)', components)
        components = re.sub('\(.*\)', '', components)

        # skip cases in which it is impossible to correctly retrieve the components
        if len(components) > 8:
            return None

        processed_data["name"] = data["spell_name"]
        processed_data["classes"] = ', '.join(data["classes"])
        processed_data["level"] = int(level)
        processed_data["school"] = school.title()
        processed_data["cast_time"] = data["casting_time"].title()
        processed_data["range"] = data["range"].title()
        processed_data["duration"] = data["duration"].title()
        processed_data["verbal"] = 1 if "V" in components else 0
        processed_data["somatic"] = 1 if "S" in components else 0
        processed_data["material"] = 1 if "M" in components else 0
        processed_data["material_cost"] = materials[0] if materials else None
        processed_data["description"] = spell_description

        return processed_data


class OfficialDataProcessor(CsvDataProcessor):

    def process_single_data_line(self, data: dict):

        processed_data = dict()

        spell_description = data["description"]

        if spell_description[-1] == "\n":
            spell_description = spell_description[:-1]

        processed_data["name"] = data["name"]
        processed_data["classes"] = data["classes"]
        processed_data["level"] = int(data["level"])
        processed_data["school"] = data["school"]
        processed_data["cast_time"] = data["cast_time"]
        processed_data["range"] = data["range"]
        processed_data["duration"] = data["duration"]
        processed_data["verbal"] = int(data["verbal"])
        processed_data["somatic"] = int(data["somatic"])
        processed_data["material"] = int(data["material"])
        processed_data["material_cost"] = data["material_cost"] if data["material_cost"] else None
        processed_data["description"] = spell_description

        return processed_data


def main():
    
    input_data_processors = [
        HomebrewDataProcessor(os.path.join(RAW_DATA_DIR, 'spells_homebrew.jsonl')),
        OfficialDataProcessor(os.path.join(RAW_DATA_DIR, 'dnd-spells.csv'))
    ]
    
    output_file_path = os.path.join(INTERIM_DATA_DIR, 'spells_processed.jsonl')

    with open(output_file_path, 'w', encoding='utf8') as f_out:

        for data_p in input_data_processors:

            i = 0
                    
            print("-" * 24)
            print(f"PROCESSING DATASET: {data_p.file_path}")

            for processed_data in data_p:
                if processed_data:
                    json.dump(processed_data, f_out)
                    f_out.write('\n')
                    i += 1
            
            print(f"Total number of instances: {i}")

            print("-" * 24)
    
    print("COMPLETED!")


if __name__ == "__main__":
    main()
