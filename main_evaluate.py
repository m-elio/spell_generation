from src.evaluate.evaluate import main as eval_main


def main():

    eval_dict = {

        "bleu": {},

        "bertscore": {
            "nthreads": 1, 
            "batch_size":1,
            "lang": "en"
        }
    }

    eval_main(eval_dict)


if __name__ == "__main__":
    main()
