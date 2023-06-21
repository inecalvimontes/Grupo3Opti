from random import randint, seed, uniform

seed(300000)

# SETS
Ca = range(10)  # 10 Casas
A = range(10)  # 10 Actividades
#  ['WC', 'Ducha', 'Lavado manos', 'Lavado dientes', 'Riego', 'Beber', 'Cocina',
# 'Lavado platos', 'Lavado ropa', 'Lavado auto' ]  
T = range(1, 25)  # 24 Horas del día

# PARAMS
# En cientos de litros
MM = 10 ** 100  # mm >> 0
k = [10, 150, 8, 8, 8, 2, 8, 150, 150, 400]
b = [8, 4, 8, 8, 1, 4, 1, 8, 1, 0]
m = [randint(100, 1000) for c in Ca]
z = [uniform(0, 3) for c in Ca]
D = [randint(50000, 60000) for c in Ca]
d = 1.5
J = 43000
f = 0.7
Co = [randint(333, 3333) for a in A]
alpha = 0.8
s = [0, 1, 1, 1, 0, 0, 0, 0, 1, 0, 0]
h = [1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0]
N = [uniform(0, 1) for a in A]