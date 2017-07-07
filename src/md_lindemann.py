import numpy as np
import matplotlib.pyplot as plt
from md_class import md

mdsys = md(N=125, T=2.0, rho=0.4)

print('Reduciendo T a 1.2')
mdsys.nueva_T(1.2)

print('Calculando coeficientes de Lindemann')

puntos = 100
dT = 0.01
a = np.zeros(100, dtype=float)
T = np.zeros(puntos, dtype=float)

for i in range(puntos):
    print('%3d/%-3d' % (i, puntos), end='\r')
    mdsys.rescaling(mdsys.T - 0.01)
    mdsys.n_pasos(100)
    T[i] = mdsys.T
    a[i], b = mdsys.lindemann(1000, 1)

print('Hecho.' + ' ' * 20 + '\n')

fig, ax = plt.subplots(1)
ax.plot(T, a, label='Coeficiente de Lindemann')
ax.set_xlabel('$T$')
ax.set_ylabel('Coeficiente de Lindemann')
ax.legend()
