from gurobipy import GRB, Model, quicksum
from random import randint, seed, uniform

seed(10)
m = Model()

# SETS
I = range(10)  # Construcciones
J = range(8)  # Localizaciones

# PARAMS
t = {(i, j): uniform(6, 15) for i in I for j in J}
c = [randint(10, 20) for i in I]
b1 = randint(3, 7)
b2 = randint(3, 7)
p = randint(3, 7)
n = 3
alpha = 10
beta = 8


# Coloque aca sus variables
x = m.addVars(I, J, vtype=GRB.BINARY, name='x_ij')
y = m.addVars(J, vtype=GRB.BINARY, name='y_j')
v = m.addVars(I, vtype=GRB.BINARY, name='v_i')
w = m.addVars(I, vtype=GRB.BINARY, name='w_i')
z1 = m.addVar(vtype=GRB.CONTINUOUS, name='z1')
z2 = m.addVar(vtype=GRB.CONTINUOUS, name='z2')
m.update()
# Coloque aca sus restricciones
# (2): Cada construccion sea asignada a exactamente una companıa de bomberos.
m.addConstrs((quicksum(x[i, j] for j in J) == 1 for i in I), name='R2')

# (3): Cantidad de companıas a localizar.
m.addConstr(quicksum(y[j] for j in J) == n, name='R3')

# (4): Una construccion solo puede ser asignada a un lugar donde se encuentre
# una companıa localizada.
m.addConstrs((x[i, j] <= y[j] for i in I for j in J), name='R4')

# (5): Cada construccion es asignada a la companıa mas cercana
# (o de menor tiempo).
m.addConstrs((x[i, j] >= y[j] - quicksum(y[k] for k in J if t[i, k] < t[i, j])
             for i in I for j in J), name='R5')

# (6): Una construcci ́on puede ser cubierta siempre y cuando exista una
# companıa a 10 minutos o menos.
m.addConstrs((v[i] <= quicksum(y[j] for j in J if t[i, j] <= alpha)
             for i in I), name='R6')
# (7): Una llamada puede ser correctamente atendida siempre y cuando exista
# una companıa a 8 minutos o menos.
m.addConstrs((w[i] <= quicksum(y[j] for j in J if t[i, j] <= beta)
             for i in I), name='R7')
# (8): Se debe cubrir al menos el 85 % de las construcciones.
m.addConstr(quicksum(v[i] for i in I)/len(I) == 0.85 + z1, name='R8')
# (9): Se debe atender correctamente al menos el 90 % de las llamadas.
denominador = quicksum(c[i] for i in I)
numerador = quicksum((w[i]*c[i]) for i in I)
m.addConstr(numerador == denominador * (0.9 + z2), name='R9')

m.update()
objetivo = b1*z1 + b2*z2 - p * quicksum((t[i, j] - alpha)*x[i, j] for i in I
                                        for j in J if t[i, j] > alpha)
m.setObjective(objetivo, GRB.MAXIMIZE)  # Colocar la FO
m.optimize()

# Solución óptima
m.printAttr('X')

print("Valor óptimo de la función objetivo: ", m.objVal)
