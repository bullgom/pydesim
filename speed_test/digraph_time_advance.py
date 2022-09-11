import random as rnd
import datetime as dt

def a(value: dict[int,int]) -> list[int]:
    minval = min(value.values())
    return list(filter(lambda x: value[x]==minval, value))

def b(value: dict[int, int]) -> list[int]:
    minval = min(value.values())
    return [k for k, v in value.items() if v==minval]

def c(value: dict[int, int]) -> list[int]:
    minval = float("inf")
    mins = []
    for k, v in value.items():
        if v < minval:
            minval = v
            mins = [k]
        
        elif v == minval:
            mins.append(k)

    return mins    

def generate(n: int, low: int, high: int) -> dict[int, int]:
    value = {}
    for i in range(n):
        k = rnd.randint(low, high)
        v = rnd.randint(low, high)
        value[k] = v
    
    return value

repeats = 1000000
n = 10
low = 0
high = 1000

targets = {
    "a":a,
    "b":b,
    "c":c
}

for name, f in targets.items():
    value = []
    case = generate(n, low, high)
    start = dt.datetime.now()
    for _ in range(repeats):
        f(case)
    end = dt.datetime.now()
    elapsed = (end-start).total_seconds()
    print(f"{name} took {elapsed}")



