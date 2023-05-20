from gurobipy import GRB, Model, quicksum
from random import randint, seed, uniform
seed(100)
Ca = range(10)  # Construcciones
A = range(8)  # Localizaciones

# PARAMS
p = [randint(0, 100) for i in Ca]
print(p)