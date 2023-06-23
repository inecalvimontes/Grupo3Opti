from gurobipy import GRB, Model, quicksum
from datos import Ca, A, T, MM, k, b, m, z, D, d, J, f, alpha, s, h

model = Model()

# VARIABLES
x = model.addVars(A, Ca, T, vtype=GRB.BINARY, name='x_act')
g = model.addVars(A, Ca, T, vtype=GRB.BINARY, name='g_act')
y = model.addVars(A, Ca, T, vtype=GRB.CONTINUOUS, lb=0, name='y_act')
n = model.addVars(Ca, vtype=GRB.BINARY, name='n_c')
w = model.addVars(A, Ca, vtype=GRB.BINARY, name='w_ac')
M = model.addVars(T, Ca, vtype=GRB.CONTINUOUS, lb=0, name='M_tc')
r = model.addVars(A, Ca, T, vtype=GRB.BINARY, name='r_act')
v = model.addVars(Ca, vtype=GRB.CONTINUOUS, lb=0, name='v_c')
q = model.addVars(A, Ca, T, vtype=GRB.CONTINUOUS, lb=0, name='q_act')
model.update()

# RESTRICCIONES
# (1) La cantidad de agua reciclada debe ser menor a la capacidad del estanque
# en cada momento t:
model.addConstrs((M[t, c] <= m[c] for t in T for c in Ca), name='R1')

# (2)La cantidad de agua almacenada en el estanque en el periodo t (inventario):
model.addConstrs((M[t, c] == M[t-1, c] + quicksum(x[a, c, t]*k[a] for a in A)
                 - quicksum(q[a, c, t] for a in A) for t in T for c in
                 Ca if t >= 2), name='R2')

# (3)Cantidad inicial del estanque:
model.addConstrs((M[1, c] == 0 for c in Ca), name='R3')

# (4) No se puede realizar la actividad a con agua reciclada del estanque si
# es que este no posee suficiente agua:
model.addConstrs((M[t - 1, c] >= r[a, c, t]*k[a] for a in A for c in Ca for t in T if t>=2), name='R4')

# (5) El agua solo se puede reciclar si tiene un grado alfa de calidad:
model.addConstrs((x[a, c, t] <= s[a] for a in A for c in Ca for t in T), name='R5')

# (6) Solo se puede utilizar el agua del estanque si la actividad no requiere
# una calidad sobre alfa para ser realizada: 
model.addConstrs((r[a, c, t] <= h[a] for a in A for c in Ca for t in T), name='R6')

# (7) No se puede reciclar el agua de la actividad a si esta no se realiza:
model.addConstrs((x[a, c, t] <= g[a, c, t] for a in A for c in Ca for t in T), name='R7')

# (8) La cantidad de presupuesto utilizado en mantenciones y agua por cada casa debe ser menor al 
# presupuesto total destinado por la familia: 
model.addConstrs((n[c]*J + quicksum(quicksum(y[a, c, t]*d for t in T) for a in A) <= D[c] for c in Ca), name='R8')

# (9) Si se decide realizar mantenimiento, las fugas disminuyen en un factor f.
model.addConstrs((n[c]*z[c]*f + (1 - n[c])*z[c] == v[c] for c in Ca), name='R9')

# (10) Las actividades se realizan la cantidad mínima de veces necesarias:
model.addConstrs((quicksum(g[a, c, t] for t in T) >= b[a] for a in A for c in Ca), name='R10')

# (11) La suma entre el agua reciclada utilizada para una actividad y el agua de la llave utilizada 
# para la misma, es igual a la cantidad mínima necesaria de agua para esa actividad, si es que se realiza:
model.addConstrs((q[a, c, t] + y[a, c, t] == g[a, c, t]*k[a] for a in A for c in Ca for t in T), name='R11')

# (12) Si no se utiliza agua reciclada del estanque para la actividad a, entonces el agua reciclada 
# para esa actividad es 0:
model.addConstrs((MM*r[a, c, t] >= q[a, c, t] for a in A for c in Ca for t in T), name='R12')

# (13)  Si no se realiza la actividad entonces la cantidad consumida de la llave debe ser 0:
model.addConstrs((y[a, c, t] <= MM*g[a, c, t] for a in A for c in Ca for t in T), name='R13')

model.update()
objetivo = quicksum(quicksum(y[a, c, t] - q[a, c, t] for a in A for t in T) + v[c] for c in Ca)
model.setObjective(objetivo, GRB.MINIMIZE)  # FUNCIÓN OBJETIVO
model.optimize()

# Solución óptima
model.printAttr('X')

print("Valor óptimo de la función objetivo: ", model.objVal)