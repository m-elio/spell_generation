import yaml
import os
import shutil

from src import PARAMETERS_DIR
from src.train.train_sft import train


def main():

    parameters_file_name = 'train_sft_parameters.yaml'
    parameters_file_path = os.path.join(PARAMETERS_DIR, parameters_file_name)

    with open(parameters_file_path) as file:
        parameters = yaml.load(file, yaml.FullLoader)

    save_directory = parameters['new_model_path']

    os.makedirs(save_directory, exist_ok=True)
    shutil.copy(parameters_file_path, os.path.join(save_directory, parameters_file_name))
    
    train(parameters, save_directory)


if __name__ == "__main__":
    main()
