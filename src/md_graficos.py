#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
import matplotlib.pyplot as plt
from cycler import cycler

# CONFIGURACIONES POR DEFECTO

# Figura (tamaño)
plt.rc('figure', figsize=(8, 6))

# Lineas (color)
plt.rc('lines', color='0.0')

# Ticks (tamaño de la fuente)
plt.rc(('xtick', 'ytick'), labelsize=14)

# Bordes de la figura (visibles o no)
plt.rc('axes.spines', left=True, bottom=True, top=False, right=False)

# Leyenda (tamaño de la fuenta y ubicación)
plt.rc('legend', fontsize=14, loc='best')

# Ejes (tamaño de la fuente)
plt.rc('axes', labelsize=14)

# Ejes (autoestilo para múltiples curvas)
lw_cycler = cycler('lw', [2, 1])
ls_cycler = cycler('ls', ['-', '-.', '--', ':'])
plt.rc('axes', prop_cycle=lw_cycler * ls_cycler)


# EJEMPLO DE PRUEBA

# Valores de prueba
x = np.linspace(0, 5, 100)
y = [np.exp(-x / 8) * np.sin(x + i / 4) for i in range(8)]

# Crea el gráfico interactivo
plt.ion()
# Crea los subplots necesarios
fig, ax = plt.subplots(1)

# Nombre de los ejes (reconoce fórmulas de Latex)
ax.set_xlabel(r'$T$')
ax.set_ylabel(r'$\rho$')

# Grilla (sólo si es útil)
ax.grid(ls=':')

# Grafica las curvas
for i in range(8):
    # Al graficar añadir un label a las curvas
    ax.plot(x, y[i], label='Curva %d' % i)

# Grafica la leyenda (puede tener múltiples columnas)
ax.legend(loc='best', ncol=2)
