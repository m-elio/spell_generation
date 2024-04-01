import os
import json
import datasets

from datasets import load_dataset
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline
from transformers.utils import logging
from transformers.trainer_utils import enable_full_determinism, set_seed

from src import DATA_DIR, HF_CACHE_DIR
from src.utils import POSSIBLE_DTYPES, available_formats


def inference(parameters_inf: dict, parameters_train: dict, model_path: str, report_dir: str, dataset_path: str):

    logging.set_verbosity_info()
    logger = logging.get_logger("transformers")

    logger.info(f"MODEL PATH: {model_path}")
    
    dataset_extension = dataset_path.split('.')[-1]

    if dataset_extension == "jsonl":
        dataset_extension = "json"

    # https://github.com/huggingface/datasets/issues/1785#issuecomment-1305872400
    datasets.builder.has_sufficient_disk_space = lambda needed_bytes, directory='.': True
    dataset = load_dataset(dataset_extension, data_files=os.path.join(DATA_DIR, dataset_path))['train']

    pretrained_parameters = parameters_inf.get("pretrained_parameters", {})
    generation_parameters = parameters_inf.get("generation_parameters", {})
    batch_size = parameters_inf.get("batch_size", 8)

    padding_side = parameters_inf.get("padding_side", None)
    cut_dataset = parameters_inf.get("cut_dataset", None)

    logger.info(f"Dataset cut: {cut_dataset}")
    logger.info(f"Padding side: {padding_side}")
    logger.info(f"Batch size: {batch_size}")

    if cut_dataset:
        dataset = dataset.select(range(cut_dataset))
    
    if "torch_dtype" in pretrained_parameters:
        pretrained_parameters["torch_dtype"] = POSSIBLE_DTYPES[pretrained_parameters["torch_dtype"]]
    
    if "torch_dtype" in generation_parameters:
        generation_parameters["torch_dtype"] = POSSIBLE_DTYPES[generation_parameters["torch_dtype"]]

    training_parameters = parameters_train.get("training_arguments", {})

    logger.info("Setting seed")

    seed = training_parameters.get("seed", 42)
    full_determinism = training_parameters.get("full_determinism", False)

    if full_determinism:
        enable_full_determinism(seed)
    else:
        set_seed(seed)

    model = AutoModelForCausalLM.from_pretrained(
        model_path,
        quantization_config=None,
        device_map="auto",
        cache_dir=HF_CACHE_DIR,
        **pretrained_parameters
    )

    model.eval()
    model = model.bfloat16()

    tokenizer = AutoTokenizer.from_pretrained(model_path, use_fast=False, add_eos_token=True, trust_remote_code=True, cache_dir=HF_CACHE_DIR)

    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token

    if padding_side:
        tokenizer.padding_side = padding_side

    input_format = parameters_inf.get('input_format', 'raw')
    logger.info(f'Selected input format: {input_format}')

    input_format_parameters = parameters_inf.get('input_format_parameters', {'text_field': 'prompt'})
    logger.info(f'Input format parameters: {input_format_parameters}')

    input_formatter = available_formats[input_format](**input_format_parameters)
    formatting_func = lambda x: input_formatter.get_prompt(x, is_train=False)

    logger.info(formatting_func(dataset[0]))

    logger.info("Applying input formatter to dataset")
    dataset = dataset.map(lambda x: {'input': formatting_func(x)})

    pipe = pipeline(task="text-generation", model=model, tokenizer=tokenizer, device_map="auto", return_full_text=False, **generation_parameters)
    outs = pipe(dataset['input'], batch_size=batch_size)
    
    logger.info("Generation completed, starting report")

    with open(os.path.join(report_dir, 'report.jsonl'), 'w', encoding='utf8') as f_out:

        for i in range(len(dataset['input'])):

                original_prompt = dataset['input'][i]
                generated_answer = outs[i][0]['generated_text']

                data = {
                    'original_prompt': original_prompt,
                    'generated_answer': generated_answer
                }

                json.dump(data, f_out)
                f_out.write('\n')
