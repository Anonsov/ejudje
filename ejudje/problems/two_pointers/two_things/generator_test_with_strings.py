import logging
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..')))
from scripts.DSL import IntGen, ArrayGen, Task, QueriesGen, StrGen
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
tests_dir = os.path.join(BASE_DIR, 'tests')
lists_tests = [f for f in os.listdir(tests_dir) if os.path.isfile(os.path.join(tests_dir, f))]


def tests_folder_maker():
    if len(lists_tests) < 21:
        os.makedirs(tests_dir, exist_ok=True)
        for i in range(1, 21):
            with open(os.path.join(tests_dir, f"input{i}.txt"), 'w') as f:
                pass
        print("Папка tests успешно создана и содержит 20 тестов.")
    else:
        print("Папка tests уже содержит 20 тестов или больше.")
        


def generator_of_tests():
    n = IntGen(name="n", lo=1, hi=40)
    s = StrGen(
        name="s",
        length=n,
        chars_allowed=None,
        has_uppercase=False,
        only_uppercase=False
    )
    task = Task(
        variables=[n, s],
        order=["n", "s"],
        solution_file=os.path.join(BASE_DIR, "etalon_solution.py"),
        file_path_tests=tests_dir
    )
    for i in range(1, 21):
        task.generate(i)
        
def main_generator():
    tests_folder_maker()
    generator_of_tests()
    
main_generator()