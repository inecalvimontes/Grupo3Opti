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
m.addConstrs((quicksum(u[a, c] for a in A) <= m for c in Ca), name='R1')

# (2): 
m.addConstrs(y[a][c] >= k * p for a in A for c in Ca, name='R2')

# (3): 
m.addConstrs((x[i, j] <= y[j] for i in I for j in J), name='R3')

# (4): 
m.addConstrs((x[i, j] >= y[j] - quicksum(y[k] for k in J if t[i, k] < t[i, j])
             for i in I for j in J), name='R4')

# (5): 
m.addConstrs((v[i] <= quicksum(y[j] for j in J if t[i, j] <= alpha)
             for i in I), name='R5')
# (6): 
m.addConstrs((w[i] <= quicksum(y[j] for j in J if t[i, j] <= beta)
             for i in I), name='R6')
# (7): 
m.addConstr(quicksum(v[i] for i in I)/len(I) == 0.85 + z1, name='R7')
# (8): 
denominador = quicksum(c[i] for i in I)
numerador = quicksum((w[i]*c[i]) for i in I)
m.addConstr(numerador == denominador * (0.9 + z2), name='R8')

m.update()
objetivo = quicksum(y[a][c] + (n[c] * z[c]) - u[a][c] for a in A for c in Ca)
m.setObjective(objetivo, GRB.MINIMIZE)  # Colocar la FO
m.optimize()

# Solución óptima
m.printAttr('X')

print("Valor óptimo de la función objetivo: ", m.objVal)
