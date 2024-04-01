import os
import torch

from src.utils.input_formatter.format import AlpacaFormat, RawFormat


def is_abstract(cls):
    return bool(getattr(cls, "__abstractmethods__", False))


def print_on_main(to_print):
    if os.environ.get('RANK', '0') == '0' and os.environ.get('LOCAL_RANK', '0') == '0':
        print(to_print)


def all_subclasses(cls):
    return set(cls.__subclasses__()).union(
        [s for c in cls.__subclasses__() for s in all_subclasses(c) if not is_abstract(c)])


def print_trainable_parameters(model):
    trainable_params = 0
    all_param = 0
    for _, param in model.named_parameters():
        all_param += param.numel()
        if param.requires_grad:
            trainable_params += param.numel()
    print_on_main(
        f"trainable params: {trainable_params} || all params: {all_param} || trainable%: {100 * trainable_params / all_param:.2f}"
    )


POSSIBLE_DTYPES = {
    "f32": torch.float32,
    "f16": torch.float16,
    "bf16": torch.bfloat16,
    "auto": "auto"
}

available_formats = {
    'alpaca': AlpacaFormat,
    'raw': RawFormat
}
