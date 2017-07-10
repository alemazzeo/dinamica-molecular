import numpy as np
import matplotlib.pyplot as plt
from md_class import md

mdsys = md(N=64, T=2.0, rho=0.4)

print('Reduciendo T a 1.2')
mdsys.nueva_T(1.6)

print('Calculando coeficientes de Lindemann')

puntos = 25
pasos = 1000
dT = 0.04
ld_avg = np.zeros((puntos, pasos), dtype=float)
ld_std = np.zeros((puntos, pasos), dtype=float)
T = np.zeros(puntos, dtype=float)


for i in range(puntos):
    print('%3d/%-3d' % (i, puntos), end='\r')
    for j in range(4):
        mdsys.rescaling(mdsys.T - dT / 4)
        mdsys.n_pasos(100)
    T[i] = mdsys.T
    ld_avg[i], ld_std[i] = mdsys.lindemann(pasos, 50)

print('Hecho.' + ' ' * 20 + '\n')

plt.ion()
fig, ax = plt.subplots(1)
ax.plot(T, ld_avg[:, -1], label='Coeficiente de Lindemann')
ax.set_xlabel('$T$')
ax.set_ylabel('Coeficiente de Lindemann')
ax.legend()
