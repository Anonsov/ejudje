import subprocess
import os
import random
import sys
import logging
from typing import List



__all__ = [
    "IntGen",
    "ArrayGen",
    "QueriesGen",
    "StrGen",
    "MatrixGen",
    "PermutationGen",
    "SetGen",
    "GraphGen",
    "TreeGen",
    
    "Task"
]




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
    def __init__(self, name: str, size: IntGen | int, lo: int, hi: int, sorted=False):
        self.name = name
        self.size = size
        self.lo = lo
        self.hi = hi
        self.sorted = sorted
                
    def generate(self, values):
        if isinstance(self.size, IntGen):
            size = values[self.size.name]
        else:
            size = self.size
        arr = [random.randint(self.lo, self.hi) for _ in range(size)]
        if self.sorted:
            return sorted(arr)
        else:
            return arr

class ValuesWithSpaces:
    def __init__(self, name, quantity_vars, lo, hi, sorted=False, unique=False):
        self.name = name
        self.quantity_vars = quantity_vars
        self.lo = lo
        self.hi = hi
        self.sorted = sorted
        self.unique = unique
        
    def generate(self, values=None):
        quantity_vars = self.quantity_vars
        if self.unique:
            arr = set()
            while len(arr) < quantity_vars:
                arr.add(random.randint(self.lo, self.hi))
        else:
            arr = [random.randint(self.lo, self.hi) for _ in range(quantity_vars)]
        
        if self.sorted:
           return sorted(arr)
        else:
            return arr
        
class QueriesGen:
    def __init__(self, name: str, q_var: IntGen | int, query_types: List[str] | str, constraints: dict):
        """ 
        Attributes:\n
        name -> it's just the name of our Query\n
        q_var -> means, what exactly variable are we giving, usually it's "q", and our q will have this: IntGen("q", 1, 50) meaning the amount of queries we have
        query_types -> usually its the type of our query, i have only two right now: pref_sum and update.\n
        constraints: it will take a dict that will look like this: constraints={"n": n} where our n is equal: n = IntGen("n", 1, 100)
        """
        self.name = name
        self.q_var = q_var
        self.query_types = query_types  
        self.constraints = constraints
    
    def generate(self, values):
        q = values[self.q_var.name]
        queries = []
        for _ in range(q):
            q_type = random.choice(self.query_types)
            if q_type == "pref_sum":
                l = random.randint(1, values["n"])
                r = random.randint(l, values["n"])
                queries.append(f"{l} {r}")
            elif q_type == "update":
                i = random.randint(1, values["n"])
                x = random.randint(1, 1000)
                queries.append(f"{i} {x}")
        return queries

class StrGen:
    """
    Attributes:\n
    length -> means what will be the length of our random string, it can be even inherited from IntGen class\n
    chars_allowed -> means, there could be some problems that could be limited in char includings\n
    has_uppercase -> by default it's False, it means our string can have some uppercases\n
    only_uppercase -> by default it's False, it means our string is full of uppercases\n
    """
    def __init__(self, name: str, length: IntGen | int, chars_allowed: List | str | None, has_uppercase=False, only_uppercase=False):
        self.name = name
        self.length = length
        self.has_uppercase = has_uppercase
        self.only_uppercase = only_uppercase
        self.chars_allowed = chars_allowed
        if has_uppercase and only_uppercase:
            print("Аттрибуты has_uppercase и only_uppercase не могу быть одновременно быть True")
    def generate(self, values):
        """
        This function gives one parameter called: values \n
        Type(values) -> dict\n
        Example: {'n': 3, 'a':[1,2,3], and etc}\n\n
        
        using the random choice of ascii code:\n
        <b>97-122 -> a-z\n
        65-90 -> A-Z\n<b/>
        
        """
        if isinstance(self.length, IntGen):
            size = values[self.length.name]
        elif isinstance(self.length, int):
            size = self.length
        result = ""
        if self.chars_allowed is None:
            if self.only_uppercase:
                for _ in range(size):
                    result += chr(random.randint(65, 90))
            elif self.has_uppercase:
                for _ in range(size):
                    result += chr(
                        random.choice(
                            [random.randint(65,90), random.randint(97, 122)]
                            )
                        )
            else:
                for _ in range(size):
                    result += chr(random.randint(97,122))
            
        else:
            for _ in range(size):
                result += random.choice(self.chars_allowed)
        
        return result
                
            

class MatrixGen:
    def __init__(self, name: str, nm: ValuesWithSpaces | List[int], lo: int, hi: int, only_chars=False, square=False):
        self.name = name
        self.nm = nm
        self.lo = lo
        self.hi = hi
        self.only_chars = only_chars
        self.square = square
        
    def generate(self, values):
        if isinstance(self.nm, ValuesWithSpaces):
            n = values[self.nm.name][0]
            if self.square:
                values[self.nm.name][1] = n
                m = values[self.nm.name][1]
            else:
                m = values[self.nm.name][1]
        elif isinstance(self.nm, list):
            n = self.nm[0]
            if self.square:
                values[self.nm.name][1] = n
                m = values[self.nm.name][1]
            else:
                m = self.nm[1]
            
        matrix = []
        for i in range(n):
            row = []
            for j in range(m):
                row.append(random.randint(self.lo, self.hi))
            matrix.append(row)
        
        return matrix
        
    
class PermutationGen:
    pass

class SetGen:
    def __init__(self, name: str, size: IntGen | int, lo: int, hi: int, sorted=False):
        self.name = name 
        self.size = size
        self.lo = lo
        self.hi = hi
        self.sorted = sorted
    
    def generate(self, values=None):
        if isinstance(self.size, IntGen):
            size = values[self.size.name]
        else:
            size = self.size

        arr = set()
        while len(arr) < size:
            arr.add(random.randint(self.lo, self.hi))
        
        if self.sorted:
            return sorted(arr)
        else:
            return arr
        
class NonWeightedGraphGen:
    def __init__(self, name: str, uv: ValuesWithSpaces | List[int], lo: int, hi: int):
        self.name = name 
        self.uv = uv
        self.lo = lo
        self.hi = hi

    def generate(self, values):
        if isinstance(self.uv, ValuesWithSpaces):
            n = values[self.uv.name][0]
            m = values[self.uv.name][1]
            
        elif isinstance(self.uv, list):
            n = self.uv[0]
            m = self.uv[1]
        
        if n <= 0:
            logging.warning(f"Number of vertices must be positive, got {n}")
            n = 1
            if isinstance(self.uv, ValuesWithSpaces):
                values[self.uv.name][0] = n
        
        max_edges = max(0, n * (n - 1) // 2)
        
        if m > max_edges:
            logging.warning(f"Too many edges requested: {m} for {n} vertices. Max is {max_edges}")
            m = max_edges
            if isinstance(self.uv, ValuesWithSpaces):
                values[self.uv.name][1] = m
        all_edges = []
        for i in range(1, n + 1):
            for j in range(i + 1, n + 1):
                all_edges.append((i, j))
        
        selected_edges = []
        if m > 0:
            selected_edges = random.sample(all_edges, m)
        return [[u, v] for u, v in selected_edges]

class WeightedGraph:
    def __init__(self):
        # self.head
        pass
    
    
    def generate(self, values):
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
            elif isinstance(val, StrGen):
                values[val.name] = val.generate(values)
            elif isinstance(val, MatrixGen):
                values[val.name] = val.generate(values)
            elif isinstance(val, ValuesWithSpaces):
                values[val.name] = val.generate(values)
            elif isinstance(val, SetGen):
                values[val.name] = val.generate(values)
            elif isinstance(val, NonWeightedGraphGen):
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
                elif isinstance(var_value[0], list):
                    for name in var_value:
                        lines.append(" ".join(map(str, name)))
                else:
                    raise ValueError(f"Unsupported list type in {var_name}")
            else:
                lines.append(str(var_value))
        # print(lines)
        input_str = "\n".join(lines)
        print(input_str)
        # print(input_str)
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