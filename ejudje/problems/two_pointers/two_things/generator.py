import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..')))

from scripts.DSL import IntGen, ArrayGen, Task


BASE_DIR = os.path.abspath(os.path.dirname(__file__))
tests_dir = os.path.join(BASE_DIR, 'tests')




os.makedirs(tests_dir, exist_ok=True)

n = IntGen("n", 1, 100)
a = ArrayGen("a", n, 1, 1000)

task = Task(
    variables=[n, a],
    order=["n", "a"],
    solution_file=os.path.join(BASE_DIR, "etalon_solution.py"),
    file_path_tests=tests_dir
)

for i in range(1, 6):
    task.generate(i)