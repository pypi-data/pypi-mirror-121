import numpy as np

def foo():
    print("foo", np.array)
    

def bar():
    print("bar", np.ones(3))
    

def hello(name: str) -> str:
    greeting = "Hello, {}".format(name)
    print(greeting)
    return greeting
