from gurobipy import GRB, Model, quicksum
from random import randint, seed, uniform

seed(10)
m = Model()

# SETS
Ca = range(10)  # Construcciones
A = range(8)  # Localizaciones

# PARAMS
p = 
k = 
R = 
m = [randint(0, 1000) for i in Ca]
Cmax = 20000
h = [uniform(0, 1) for i in A]
f = 0.1
t = 
d = 2
D = 
z =
J = 200000
g =
s =
N = 
Co = [randint(10000, 100000) for i in A]
v =

# Coloque aca sus variables
x = m.addVars(A, A, vtype=GRB.BINARY, name='x_ab')
y = m.addVars(A, Ca, vtype=GRB.CONTINUOUS, name='y_ac')
u = m.addVars(A, Ca, vtype=GRB.CONTINUOUS, name='u_ac')
v = m.addVars(A, vtype=GRB.CONTINUOUS, name='v_a')
n = m.addVar(Ca, vtype=GRB.BINARY, name='n_c')
w = m.addVar(A, vtype=GRB.BINARY, name='w_a')
m.update()
# Coloque aca sus restricciones
# (1): 
m.addConstrs((quicksum(u[a, c] for a in A) <= m[c] for c in Ca), name='R1')

# (2): 
m.addConstrs((y[a, c] >= k[a] * p[c] for a in A for c in Ca), name='R2')

# (3): 
m.addConstr((quicksum(y[a, c] for a in A for c in Ca) <= Cmax), name='R3')

# (4): 
m.addConstr((quicksum(n[c] * z[c] for c in Ca) <= f * Cmax), name='R4')

# (5): 
m.addConstrs((x[a, b] * s[a] >= h[b] for a in A for b in A if a != b), name='R5')
# (6): 
m.addConstrs((abs(n[c] - 1) * J + quicksum(y[a, c] * d + w[a] * Co[a] for a in A) <= D[c] for c in Ca), name='R6')
# (7): 
m.addConstrs((y[a, c] >= u[a, c] for a in A for c in Ca), name='R7')
# (8): 
m.addConstrs((w[a] * k[a] * N <= k[a] for a in A), name='R8')

m.update()
objetivo = quicksum((y[a, c] + (n[c] * z[c]) - u[a, c]) for a in A for c in Ca)
m.setObjective(objetivo, GRB.MINIMIZE)  # Colocar la FO
m.optimize()

# Solución óptima
m.printAttr('X')

print("Valor óptimo de la función objetivo: ", m.objVal)
