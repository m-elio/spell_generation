import os
import json
import random

import numpy as np

from src import PROCESSED_DATA_DIR


def main(num_instances: int):
    
    input_file_path = os.path.join(PROCESSED_DATA_DIR, 'spells_processed_and_formatted.jsonl')
    output_file_path_train = os.path.join(PROCESSED_DATA_DIR, 'spells_processed_and_formatted_train.jsonl')
    output_file_path_test = os.path.join(PROCESSED_DATA_DIR, 'spells_processed_and_formatted_test.jsonl')

    random.seed(42)
    np.random.seed(42)
    instances_idxs = np.arange(0, num_instances)
    instances_idxs_test = np.random.choice(instances_idxs, 50, replace=False)
    instances_idxs_test = set(instances_idxs_test)

    with open(output_file_path_train, 'w', encoding='utf8') as f_out_train:
        with open(output_file_path_test, 'w', encoding='utf8') as f_out_test:
            with open(input_file_path, 'r', encoding='utf8') as f_in:
                
                num_train_instances = 0
                num_test_instances = 0

                print("-" * 24)
                print(f"SPLITTING DATASET: {input_file_path}")

                for i, l in enumerate(f_in):
                    data = json.loads(l)
                    if i in instances_idxs_test:
                        json.dump(data, f_out_test)
                        f_out_test.write('\n')
                        num_test_instances += 1
                    else:
                        json.dump(data, f_out_train)
                        f_out_train.write('\n')
                        num_train_instances += 1
                
                print(f"Total number of instances for train set: {num_train_instances}")
                print(f"Total number of instances for test set: {num_test_instances}")

                print("-" * 24)
            
            print("COMPLETED!")


if __name__ == "__main__":

    main()