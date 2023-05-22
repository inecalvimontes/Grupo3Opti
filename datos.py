from random import randint, seed, uniform

seed(300000)

# SETS
Ca = range(10)  # 10 Casas
A =  range(11)  # 11 Actividades
#  ['WC', 'Ducha', 'Lavado manos', 'Lavado dientes', 'Riego', 'Beber', 'Cocina','limpieza', 
# 'Lavado platos', 'Lavado ropa', 'Lavado auto' ]  
T = range(1, 25)  # 24 Horas del día

# PARAMS
MM = 10 ** 10  # mm >> 0
k = [randint(3, 20) for a in A]
b = [randint(1, 10) for a in A]
m = [randint(100, 1000) for c in Ca]
z = [uniform(0, 2) for c in Ca]  
D = [randint(5000, 6000) for c in Ca]
d = 1.5
J = 60000/30
f = 0.7
Co = [randint(333, 3333) for a in A]
alpha = 0.8
s = [0, 1, 1, 1, 0, 0, 0, 0, 1, 0, 0]
h = [1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0]
N = [uniform(0,1) for a in A]