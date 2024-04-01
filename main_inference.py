import os
import yaml
import shutil

from src import PARAMETERS_DIR, INFERENCE_REPORTS_DIR
from src.evaluate.inference_sft import inference


def main():

    parameters_file_name = 'inference_sft_parameters.yaml'
    parameters_file_path = os.path.join(PARAMETERS_DIR, parameters_file_name)

    with open(parameters_file_path) as file:
        parameters_inf = yaml.load(file, yaml.FullLoader)

    model_dir = parameters_inf["model_dir"]
    save_dir = parameters_inf.get("report_dir", INFERENCE_REPORTS_DIR)
    dataset_path = parameters_inf["dataset_path"]

    parameters_path = os.path.join(model_dir, 'train_sft_parameters.yaml')

    if os.path.isfile(parameters_path):
        with open(parameters_path) as file:
            parameters_train = yaml.load(file, yaml.FullLoader)
    else:
        parameters_train = {}

    report_dir = os.path.join(save_dir, f'{os.path.splitext(os.path.basename(model_dir))[0]}_{os.path.splitext(os.path.basename(dataset_path))[0]}')
    os.makedirs(report_dir, exist_ok=True)
    shutil.copy(parameters_file_path, os.path.join(report_dir, parameters_file_name))

    inference(parameters_inf, parameters_train, model_dir, report_dir, dataset_path)


if __name__ == "__main__":
    main()
