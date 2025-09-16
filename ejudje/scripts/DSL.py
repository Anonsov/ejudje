import subprocess
import os
import random
import sys
import logging
from typing import List
logging.basicConfig(
    level=logging.DEBUG,
    filename='dsl.log',
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class IntGen:
    def __init__(self, name: str, lo: int, hi: int):
        self.name = name
        self.lo = lo
        self.hi = hi

    def generate(self):
        return random.randint(self.lo, self.hi)


class ArrayGen:
    def __init__(self, name: str, size: IntGen | int, lo: int, hi: int):
        self.name = name
        self.size = size
        self.lo = lo
        self.hi = hi
        
    def generate(self, values):
        if isinstance(self.size, IntGen):
            size = values[self.size.name]
        else:
            size = self.size
        return [random.randint(self.lo, self.hi) for _ in range(size)]

class QueriesGen:
    def __init__(self, name, q_var: IntGen, query_types, constraints):
        self.name = name
        self.q_var = q_var
        self.query_types = query_types  
        self.constraints = constraints
    
    def generate(self, values):
        q = values[self.q_var.name]
        queries = []
        for _ in range(q):
            q_type = random.choice(self.query_types)
            if q_type == "sum":
                l = random.randint(1, values["n"])
                r = random.randint(l, values["n"])
                queries.append(f"{l} {r}")
            elif q_type == "update":
                i = random.randint(1, values["n"])
                x = random.randint(1, 1000)
                queries.append(f"{i} {x}")
        return queries


class StrGen:
    pass

class MatrixGen:
    pass

class PermutationGen:
    pass

class SetGen:
    pass

class GraphGen:
    pass

class TreeGen:
    pass

class Task:
    def __init__(
            self, 
            variables: List[IntGen | ArrayGen], 
            order: List[str], 
            solution_file: str, 
            file_path_tests: str
        ):
        self.variables = {var.name: var for var in variables}
        self.order = order
        self.solution_file = solution_file
        self.file_path_tests = file_path_tests
    
    def generate(self, test_number):
        values = {}
        for val in self.variables.values():
            if isinstance(val, IntGen):
                values[val.name] = val.generate()
            elif isinstance(val, ArrayGen):
                values[val.name] = val.generate(values)
            elif isinstance(val, QueriesGen):
                values[val.name] = val.generate(values)
            else:
                logging.warning(f"Unsupported variable type for {val.name}")
                raise NotImplementedError(f"Generation for {type(val)} is not implemented.")
            
        logging.info(f"Generated values for test {test_number}: {values}")
        
        lines = []
        for var_name in self.order:
            var_value = values[var_name]
            if isinstance(var_value, list):
                if all(isinstance(x, int) for x in var_value):
                    lines.append(" ".join(map(str, var_value)))
                elif all(isinstance(x, str) for x in var_value):
                    lines.extend(var_value)
                else:
                    raise ValueError(f"Unsupported list type in {var_name}")
            else:
                lines.append(str(var_value))

        input_str = "\n".join(lines)

        input_file = os.path.join(self.file_path_tests, f"input{test_number}.txt")
        with open(input_file, 'w') as f:
            f.write(input_str)
        logging.info(f"Wrote input file: {input_file}")
        
        etalone_outputs = subprocess.run(
            ["python3", self.solution_file],
            input=input_str,
            text=True,
            capture_output=True
        )
        if etalone_outputs.returncode != 0:
            logging.error(f"Solution script error for test {test_number}: {etalone_outputs.stderr}")
            raise RuntimeError(f"Solution script failed with error: {etalone_outputs.stderr}")
        output_file = os.path.join(self.file_path_tests, f"output{test_number}.txt")
        with open(output_file, 'w') as f:
            f.write(etalone_outputs.stdout)
        logging.info(f"Wrote output file: {output_file}")