import os
import json
import evaluate

import numpy as np

from src import PROCESSED_DATA_DIR, EVALUATE_REPORTS_DIR, INFERENCE_REPORTS_DIR


def main(metrics: dict):

    for metric_to_load, metric_args in metrics.items():

        metric = evaluate.load(metric_to_load, module_type="metric")

        for x in os.listdir(INFERENCE_REPORTS_DIR):
            
            # skip hidden files
            if x[0] == '.':
                continue

            report_file = os.path.join(INFERENCE_REPORTS_DIR, x, "report.jsonl")

            predictions = []
            gold_references = []

            with open(report_file, 'r', encoding='utf8') as f_predict:
                with open(os.path.join(PROCESSED_DATA_DIR, 'spells_processed_and_formatted_eval.jsonl'), 'r', encoding='utf8') as f_ref:

                    for l_pred, l_ref in zip(f_predict, f_ref):

                        line_data_pred = json.loads(l_pred)
                        generated_answer = line_data_pred['generated_answer']

                        line_data_ref = json.loads(l_ref)
                        reference = line_data_ref['response']

                        predictions.append(generated_answer)
                        gold_references.append(reference)

            result = metric.compute(predictions=predictions, references=gold_references, **metric_args)
            to_add = {}
            
            for result_name, result_value in result.items():
                if isinstance(result_value, list):
                    to_add[f"{result_name}_mean"] = np.mean(result_value)

            result = {**to_add, **result}
            os.makedirs(os.path.join(EVALUATE_REPORTS_DIR, x), exist_ok=True)

            with open(os.path.join(EVALUATE_REPORTS_DIR, x, f"report_{metric_to_load}.jsonl"), 'w', encoding='utf8') as f:

                json.dump(result, f)
                f.write('\n')


if __name__ == "__main__":

    main()