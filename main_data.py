from src.data.processing.spell_processor import main as processor_main
from src.data.processing.spell_formatter import main as formatter_main
from src.data.splitting.spell_train_test_split import main as train_test_split_main
from src.data.processing.spell_test_formatter import main as formatter_test_main


def main():

    processor_main()
    num_instances = formatter_main()
    train_test_split_main(num_instances)
    formatter_test_main(20)


if __name__ == "__main__":
    main()