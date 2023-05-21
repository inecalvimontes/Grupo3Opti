from gurobipy import GRB, Model, quicksum
from random import randint, seed, uniform

seed(30)
m = Model()

# SETS
Ca = range(10)  # Construcciones
A = range(8)  # Localizaciones
T = range(24)
# PARAMS
p = [randint(1, 10) for c in Ca]
k = 
m = [randint(0, 1000) for c in Ca]
h = [uniform(0, 1) for a in A]
z =   
d = 2
J = 100000
Co = [randint(10000, 100000) for i in A]
alpha = 0.8
s = 
N = [uniform(0, 1) for a in A]

# Coloque aca sus variables
x = m.addVars(A, Ca, T, vtype=GRB.BINARY, name='x_act')
g = m.addVars(A, Ca, T, vtype=GRB.BINARY, name='g_act')
y = m.addVars(A, Ca, vtype=GRB.CONTINUOUS, name='y_ac')
u = m.addVars(A, Ca, vtype=GRB.CONTINUOUS, name='u_ac')
n = m.addVars(Ca, vtype=GRB.BINARY, name='n_c')
w = m.addVars(A, Ca, vtype=GRB.BINARY, name='w_ac')
Cal = m.addVars(T, Ca, vtype=GRB.CONTINUOUS, name='Cal_tc')
M = m.addVars(T, vtype=GRB.CONTINUOUS, name='M_t')
r = m.addVars(A, Ca, T, vtype=GRB.BINARY, name='r_act')
m.update()
# Coloque aca sus restricciones
# (1) La cantidad de agua reciclada debe ser menor a la capacidad del estanque:
m.addConstrs((M[t, c] <= m[c] for t in T for c in Ca), name='R1')

# (2)La cantidad de agua almacenada en el estanque en el periodo t (inventario): 
m.addConstrs((M[t, c] == M[t-1, c] + quicksum(x[a, c, t] * k[a] for a in A)
              - quicksum(r[a, c, t] * k[a] for a in A) for t in T for c in Ca), name='R2')

# (3)Cantidad inicial del estanque: 
m.addConstr((M[1, c] == 0 for c in Ca), name='R4')

# (4)Cada actividad cuenta con la cantidad mínima de agua necesaria:
m.addConstr((y[a, c] >= k[a] * p[c] for a in A for c in Ca), name='R3')

# (5)El agua solo se puede reciclar si tiene un grado alfa de calidad: 
m.addConstrs((x[a, c, t] <= s[a] for a in A for c in Ca for t in T), name='R5')
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
