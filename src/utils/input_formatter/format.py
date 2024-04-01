from abc import ABC, abstractmethod

from src.utils.decorators import classproperty


class Format(ABC):

    @classmethod
    @abstractmethod
    def format_name(cls):
        raise NotImplementedError

    @classmethod
    @classproperty
    @abstractmethod
    def format_dict(cls):
        raise NotImplementedError

    @abstractmethod
    def get_prompt(self, example: dict, is_train: bool) -> str:
        raise NotImplementedError


class RawFormat(Format):

    def __init__(self, text_field: str):
        self.text_field = text_field
    
    @classmethod
    def format_name(cls):
        return "raw"

    def get_prompt(self, example: dict, is_train: bool) -> str:
        text = example[self.text_field]
        return text


class InstructionFormat(Format):

    def __init__(self, instruction_field: str, response_field: str, lang: str = "en"):        
        self.lang = lang
        self.instruction_field = instruction_field
        self.response_field = response_field

    @classmethod
    @abstractmethod
    def format_name(cls):
        raise NotImplementedError

    @classmethod
    @classproperty
    @abstractmethod
    def format_dict(cls):
        raise NotImplementedError

    @abstractmethod
    def get_prompt(self, example: dict, is_train: bool) -> str:
        raise NotImplementedError


class AlpacaFormat(InstructionFormat):

    def __init__(self, instruction_field: str, response_field: str, context_field: str = None, lang: str = "en"):
        super().__init__(instruction_field, response_field, lang)
        self.context_field = context_field
    
    @classmethod
    def format_name(cls):
        return "alpaca"

    @classmethod
    @classproperty
    def format_dict(cls):
        
        f_dict = {

            "en": {

                "with_input": "Below is an instruction that describes a task, paired with an input that provides further context. "
                              "Write a response that appropriately completes the request.\n\n"
                              "### Instruction:\n{instruction}\n\n### Input:\n{context}\n\n### Response:\n{response}",

                "no_input": "Below is an instruction that describes a task. "
                            "Write a response that appropriately completes the request.\n\n"
                            "### Instruction:\n{instruction}\n\n### Response:\n{response}"
            },
            
        }

        return f_dict

    def get_prompt(self, example: dict, is_train: bool) -> str:
        instruction = example[self.instruction_field]
        response = example[self.response_field] if is_train else ""
        context = example.get(self.context_field, "") if self.context_field else ""

        if context != "":

            return self.format_dict[self.lang]["with_input"].format(
                instruction=instruction,
                context=context,
                response=response)

        else:

            return self.format_dict[self.lang]["no_input"].format(
                instruction=instruction,
                response=response
            )
