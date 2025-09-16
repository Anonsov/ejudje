import os
from path_generator_slash import path_generator_slash
import logging

# Настройка логгера
logging.basicConfig(
    level=logging.INFO,
    filename='ejudje.log',
    format='%(asctime)s - %(levelname)s - %(message)s'
)

PROBLEMS_PATH = "ejudje/problems/"


def create_file(file_path, content=""):
    """Создает файл с указанным содержимым"""
    try:
        with open(file_path, 'w') as f:
            f.write(content)
        logging.info(f"Successfully created file: {file_path}")
        print(f"Файл {file_path} успешно создан")
    except Exception as e:
        logging.exception(f"Error creating file: {e}")
        print(f"Ошибка при создании файла {file_path}: {e}")


def main() -> None:
    """ Функция самая важная то есть main """
    logging.info("Starting main function")
    print("1. Новый урок")
    print("2. Новая задача в существующую папку")
    try:
        a = int(input("Выберите действие: "))
        logging.info(f"User input: {a}")
    except ValueError:
        logging.error("Invalid input. Please enter a number.")
        print("Ошибка: Введите число.")
        return

    if a == 1:
        print("1. Новую папку")
        print("2. ")
        logging.info("Creating a new lesson")
    elif a == 2:
        logging.info("Creating a new task in an existing folder") 
        print("По какой теме будет задача: ")
        try:
            list_dirs = os.listdir(PROBLEMS_PATH)
            for num, theme in enumerate(list_dirs):
                print(f"{num + 1}. {theme}")

            num_theme = int(input("Выберите тему: "))
            logging.info(f"User selected theme number: {num_theme}")

            if 1 <= num_theme <= len(list_dirs):
                selected_theme = list_dirs[num_theme - 1]
                print(f"Вы выбрали тему: {selected_theme}")
            else:
                logging.warning(f"Invalid theme number: {num_theme}")
                print("Неверный номер темы.")
                return

            new_path = path_generator_slash(PROBLEMS_PATH[:-1], selected_theme)
            print("Как назовем папку (желательно по названию задачи)")
            name_task = input("Введите название папки: ")
            logging.info(f"Task folder name: {name_task}")

            full_path = new_path + name_task
            os.makedirs(full_path, exist_ok=True)
            print("Успешно создано ", full_path)
            logging.info(f"Successfully created folder: {full_path}")

            statement_path = path_generator_slash(full_path, "statement.md")
            try:
                with open(statement_path[:-1], 'w') as f:
                    statement = input("Напишите условие задачи: ")
                    f.write(statement)
                print("Файлик", statement_path, "успешно создан")
                logging.info(f"Successfully created statement file: {statement_path}")
            except Exception as e:
                logging.exception(f"Error creating statement file: {e}")
                print(f"Ошибка при создании файла statement: {e}")
                return

            tests_path = path_generator_slash(full_path, "tests")
            os.makedirs(tests_path, exist_ok=True)
            print("Успешно создан: ", tests_path)
            logging.info(f"Successfully created tests folder: {tests_path}")


            generator_path = path_generator_slash(full_path, "generator.py")
            etalon_solution_path = path_generator_slash(full_path, "etalon_solution.py")
            user_solution_path = path_generator_slash(full_path, "user_solution.py")

            create_file(generator_path[:-1], "# Code generator")
            create_file(etalon_solution_path[:-1], "# Etalon solution")
            create_file(user_solution_path[:-1], "# User solution")


        except FileNotFoundError:
            logging.error(f"Problems path not found: {PROBLEMS_PATH}")
            print(f"Ошибка: Путь к задачам не найден: {PROBLEMS_PATH}")
        except ValueError:
            logging.error("Invalid input. Please enter a number.")
            print("Ошибка: Введите число.")
        except Exception as e:
            logging.exception(f"An unexpected error occurred: {e}")
            print(f"Произошла непредвиденная ошибка: {e}")
    else:
        logging.warning(f"Invalid action number: {a}")
        print("Неверный номер действия.")

    logging.info("Ending main function")

if __name__ == "__main__":
    main()
















    
