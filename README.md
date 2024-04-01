# Dungeons & Dragons 5th Edition Spell Generation using Large Language Models

Welcome! This is the codebase for the paper "Leveraging Large Language Models for Spell-Generation in Dungeons & Dragons" accepted at the [Games and NLP 2024 Workshop](https://gamesandnlp.com/) of the [LREC/Coling 2024](https://lrec-coling-2024.org/) conference. 
This repo contains the code to reproduce the experiments described in the work, in particular the code does the following:

- Obtain the dataset
- Fine-tune a Large Language Model for spell generation
- Evaluate the quality of the generated spells using BLEU and Bert Score

## Requirements

To reproduce the experiments, create a Python 3.10 virtual environment and install the requirements listed in the [requirements file](requirements.txt).

Alternatively, you can also build a container, for the experiments, Singularity 3.9 Pro was used starting from this [Docker image]([nvidia/cuda:12.1.0-cudnn8-devel-ubuntu20.04](https://hub.docker.com/layers/nvidia/cuda/12.1.0-cudnn8-devel-ubuntu20.04/images/sha256-da5f69611ae7526fbd23f8f8edb06d1818a782f1bbed7b6508efca1cd8d87777?context=explore)).

Finally, to smoothly run the scripts, **set the working directory to the root of this project**.

## Dataset & Models

The first step is to obtain the datasets and the base models that were used. To do so, first download the Kaggle dataset consisting of 554 official spells and unzip its contents into [raw data directory](data/raw/).

Then, download the base models, you can do so by running the following command for a given mdoel:

    git lfs install
    git clone git@hf.co:<MODEL ID>

Finally, run the scraping process to obtain homebrew 5th edition D&D spells by executing the following command:

    python3.10 -m main_scraper

After doing all of this, you are now ready to process the dataset. To do so, execute the following command:

    python3.10 -m main_data

This will generate the train and test processed splits in the [processed data directory](data/processed/).

## Fine-Tuning for Spell Generation

To fine-tune a model, modify the [train parameters file](parameters/train_sft_parameters.yaml). By default, this file contains an example of the parameters used for one of the models. The most important parameters to set are:

- **original_model_path**: the path to the model to be fine-tuned
- **new_model_path**: the path where the fine-tuned model will be saved
- **dataset_path**: the path to the dataset to use, if you followed the previous section the path should be "data/processed/spells_processed_and_formatted_train.jsonl"

You can now run the fine-tune process by executing the following command:

    python3.10 -m main_train

The script can also be easily launched with the accelerate library as well in combination with deepspeed / fsdp for parallelism.

## Inference & Evaluation

The inference procedure follows a similar pipeline to the one used for fine-tuning. Modify the [inference parameters file](parameters/inference_sft_parameters.yaml) according to your needs. By default, this file contains an example of the parameters used for one of the models. The most important parameters to set are:

- **model_dir**: the path to the fine-tuned model directory saved by the HuggingFace trainer
- **dataset_path**: the path to the dataset to use, if you followed the previous section the path should be "data/processed/spells_processed_and_formatted_eval.jsonl"

You can now run the inference process by executing the following command:

    python3.10 -m main_inference

This will generate a directory in the [inference reports directory](reports/inference/) (the name will be a concatenation of the model and dataset name) which will contain a "report.jsonl" file with the generated output.

To evaluate the generated output, you can execute the following command:

    python3.10 -m main_evaluate

This will generate a directory in the [evaluation reports directory](reports/evaluate/) for each inference output (the names of these directories will match the ones in the inference directory) which will contain a "report_blue.jsonl" and a "report_bertscore.jsonl" file with the metric output from the [evaluate]() library.
