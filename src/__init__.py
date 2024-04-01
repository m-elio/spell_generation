import os

THIS_DIR = os.path.dirname(os.path.realpath(__file__))
ROOT_DIR = os.path.abspath(os.path.join(THIS_DIR, '..'))

DATA_DIR = os.path.join(ROOT_DIR, 'data')
MODELS_DIR = os.path.join(ROOT_DIR, 'models')
REPORTS_DIR = os.path.join(ROOT_DIR, 'reports')
PARAMETERS_DIR = os.path.join(ROOT_DIR, 'parameters')

INFERENCE_REPORTS_DIR = os.path.join(REPORTS_DIR, 'inference')
EVALUATE_REPORTS_DIR = os.path.join(REPORTS_DIR, 'evaluate')

PROCESSED_DATA_DIR = os.path.join(DATA_DIR, 'processed')
INTERIM_DATA_DIR = os.path.join(DATA_DIR, 'interim')
RAW_DATA_DIR = os.path.join(DATA_DIR, 'raw')

CACHE_DIR = os.path.join(ROOT_DIR, 'cache')
HF_CACHE_DIR = os.environ.get("HF_CACHE_DIR", os.path.join(CACHE_DIR, 'hf_cache'))
os.environ['TRANSFORMERS_CACHE'] = HF_CACHE_DIR
os.environ["HF_DATASETS_OFFLINE"] = "1"
os.environ["TRANSFORMERS_OFFLINE"] = "1"
