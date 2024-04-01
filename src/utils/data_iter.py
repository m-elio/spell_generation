import csv
import json

from abc import ABC, abstractmethod
from typing import Iterator


class DataProcessor(ABC):

    def __init__(self, file_path: str):
        self.file_path = file_path
    
    @abstractmethod
    def create_file_iter(self) -> Iterator[dict]:
        raise NotImplementedError

    @abstractmethod
    def process_single_data_line(self, data: dict) -> dict:
        raise NotImplementedError
    
    def __iter__(self):
        for data in self.create_file_iter():
            yield data


class JsonDataProcessor(DataProcessor):

    def create_file_iter(self) -> Iterator[dict]:

        with open(self.file_path, 'r', encoding='utf8') as f:

            for l in f.readlines():
                
                line_data = json.loads(l)
                processed_data = self.process_single_data_line(line_data)

                if processed_data:
                    yield processed_data


class CsvDataProcessor(DataProcessor):

    def create_file_iter(self) -> Iterator[dict]:

        with open(self.file_path, newline='', encoding='utf-8') as f:
            reader = csv.reader(f)
            for i, row in enumerate(reader):
                if i == 0:
                    header_row = row
                else:
                    line_data = dict(zip(header_row, row))
                    processed_data = self.process_single_data_line(line_data)

                    if processed_data:
                        yield processed_data
