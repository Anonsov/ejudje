# import random
# s = "{}[]()"
# for i in range(100):
#     print(random.choice(s))

import random
arr = set()
size = 10
while len(arr) < size:
    arr.add(random.randint(1, 100))

arr = sorted(arr)

print(arr)        