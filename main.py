from gurobipy import GRB, Model, quicksum
from random import randint, seed, uniform

seed(300000)
model = Model()

# SETS
Ca = range(10)  # 10 Casas
A =  range(11) 
#  ['WC', 'Ducha', 'Lavado manos', 'Lavado dientes', 'Riego', 'Beber', 'Cocina','limpieza', 'Lavado platos', 'Lavado ropa', 'Lavado auto' ]  # 11 Actividades
T = range(1, 25)  # 24 Horas del día
# PARAMS
MM = 10 ** 10  # mm >> 0
k = [randint(3, 20) for a in A]
b = [randint(1, 10) for a in A]
m = [randint(0, 1000) for c in Ca]
z = [uniform(0, 2) for c in Ca]  
D = [randint(1000, 2000) for c in Ca]
d = 2
J = 50000
f = 0.7
Co = [randint(10000, 100000) for a in A]
alpha = 0.8
s = [0, 1, 1, 1, 0, 0, 0, 0, 1, 0, 0]
h = [1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0]
N = [uniform(0, 1) for a in A]
# Coloque aca sus variables
x = model.addVars(A, Ca, T, vtype=GRB.BINARY, name='x_act')
g = model.addVars(A, Ca, T, vtype=GRB.BINARY, name='g_act')
y = model.addVars(A, Ca, T, vtype=GRB.CONTINUOUS, name='y_act')
n = model.addVars(Ca, vtype=GRB.BINARY, name='n_c')
w = model.addVars(A, Ca, vtype=GRB.BINARY, name='w_ac')
M = model.addVars(T, Ca, vtype=GRB.CONTINUOUS, name='M_tc')
r = model.addVars(A, Ca, T, vtype=GRB.BINARY, name='r_act')
v = model.addVars(Ca, vtype=GRB.CONTINUOUS, name='v_c')
q = model.addVars(A, Ca, T, vtype=GRB.CONTINUOUS, name='q_act')
model.update()

# Coloque aca sus restricciones
# (1) La cantidad de agua reciclada debe ser menor a la capacidad del estanque
# en cada momento t:
model.addConstrs((M[t, c] <= m[c] for t in T for c in Ca), name='R1')

# (2)La cantidad de agua almacenada en el estanque en el periodo t (inventario):
model.addConstrs((M[t, c] == M[t-1, c] + quicksum(x[a, c, t]*k[a] for a in A)
                 - quicksum(r[a, c, t]*k[a] for a in A) for t in T for c in
                 Ca if t >= 2), name='R2')

# (3)Cantidad inicial del estanque: 
model.addConstrs((M[1, c] == 0 for c in Ca), name='R3')

# (4) No se puede realizar la actividad a con agua reciclada del estanque si
# es que este no posee suficiente agua:
model.addConstrs((M[t, c] >= r[a, c, t]*k[a] for a in A for c in Ca for t in T), name='R4')

# (5) El agua solo se puede reciclar si tiene un grado alfa de calidad:
model.addConstrs((x[a, c, t] <= s[a] for a in A for c in Ca for t in T), name='R5')

# (6) Solo se puede utilizar el agua del estanque si la actividad no requiere
# una calidad sobre alfa para ser realizada: 
model.addConstrs((r[a, c, t] <= h[a] for a in A for c in Ca for t in T), name='R6')

# (7) No se puede reciclar el agua de la actividad a si esta no se realiza:
model.addConstrs((x[a, c, t] <= g[a, c, t] for a in A for c in Ca for t in T), name='R7')

# (8) La cantidad de agua utilizada por cada casa debe ser menor al presupuesto destinado por la familia:
model.addConstrs((n[c]*J + quicksum(y[a, c, t]*d + w[a, c]*Co[a] for a in A for t in T) <= D[c] for c in Ca), name='R8')

# (9) La adquisición de nuevas tecnologías para llevar a cabo una actividad debe
# traer una reducción del agua consumida en comparación a la tecnología anterior:
# OJOOOOO ACAAA ARREGLAR ESTO, ESTA RARO
model.addConstrs((w[a, c]*k[a]*N[a] + (1-w[a,c])*k[a]== y[a, c, t] + q[a, c, t] for a in A for c in Ca for t in T), name='R9')

# (10) Si se decide realizar mantenimiento, las fugas disminuyen en un factor f.
model.addConstrs((n[c]*z[c]*f + (1 - n[c])*z[c] == v[c] for c in Ca ), name='R10')

# (11) Las actividades se realizan la cantidad mínima de veces necesarias:
model.addConstrs((quicksum(g[a, c, t] for t in T) >= b[a] for a in A for c in Ca), name='R11')

# (12) Las actividades se realizan la cantidad mínima de veces necesarias:
model.addConstrs((MM*r[a, c, t] >= q[a, c, t] for a in A for c in Ca for t in T), name='R12')

# model.addConstrs((q[a, c, t] >= x[a, c, t] for a in A for c in Ca for t in T), name='R12')

model.update()
objetivo = quicksum((y[a, c, t] + v[c] - x[a, c, t]*k[a]) for a in A for c in Ca for t in T)
model.setObjective(objetivo, GRB.MINIMIZE)  # Colocar la FO
model.optimize()

# Solución óptima
model.printAttr('X')

print("Valor óptimo de la función objetivo: ", model.objVal)


