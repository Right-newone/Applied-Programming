import os
from get_args import get_arguments
from annotation_header import create_annotation_header
from scrapper import run_scraper
from iterator_files import test_iterators

def main() -> None:
    """
    Основная функция, объединяющая все этапы программы.
    """
    args = get_arguments()
    
    user_rate = args.rating.capitalize()
    save_directory = args.dir
    annotation_file = args.annotation

    os.makedirs(save_directory, exist_ok=True)
    create_annotation_header(annotation_file)

    print(f"Ищем книги с рейтингом: {user_rate}")
    print(f"Сохраняем в папку: {save_directory}")

    run_scraper(user_rate, save_directory, annotation_file)

    test_iterators(save_directory, annotation_file)

if __name__ == "__main__":
    main()