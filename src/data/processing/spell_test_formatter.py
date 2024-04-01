import os
import json

from src import PROCESSED_DATA_DIR


def main(words_threshold: int):
    
    input_file_path = os.path.join(PROCESSED_DATA_DIR, 'spells_processed_and_formatted_test.jsonl')
    output_file_path = os.path.join(PROCESSED_DATA_DIR, 'spells_processed_and_formatted_eval.jsonl')

    with open(input_file_path, 'r', encoding='utf8') as f_in:
        with open(output_file_path, 'w', encoding='utf8') as f_out:

            i = 0
                        
            print("-" * 24)
            print(f"PROCESSING DATASET: {input_file_path}")

            for l in f_in:

                words_added = 0

                line_data = json.loads(l)
                line_data, desc_text = line_data['response'].split('Description:')

                is_word = False
                for character_num, character in enumerate(list(desc_text)):

                    if words_added == words_threshold:
                        break
                    
                    if character.isalnum():
                        is_word = True
                    else:

                        if is_word:
                            words_added += 1

                        is_word = False

                desc_to_keep = desc_text[0:character_num]
                desc_reference = desc_text[character_num:-1]

                processed_data = {}
                processed_data['input'] = line_data + 'Description:' + desc_to_keep
                processed_data['response'] = desc_reference

                json.dump(processed_data, f_out)
                f_out.write('\n')

                i += 1
                
            print(f"Total number of instances: {i}")

            print("-" * 24)
    
    print("COMPLETED!")


if __name__ == "__main__":

    words_threshold = 20
    main(words_threshold)