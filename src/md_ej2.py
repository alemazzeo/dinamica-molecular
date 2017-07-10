#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
import matplotlib.pyplot as plt
import os
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

# CARGA DE ARCHIVOS

ruta = '../datos/maps/n512/'
archivos = os.listdir(ruta)

temps = np.load(ruta + 'temps.npy')
rhos = np.load(ruta + 'rhos.npy')

avg_energia = [[int(a.split('_')[2]), a] for a in archivos
               if a.startswith('avg_energia')]
avg_energia.sort()
avg_energia = [np.load(ruta + a) for i, a in avg_energia]
avg_energia = np.concatenate(avg_energia).T

std_energia = [[int(a.split('_')[2]), a] for a in archivos
               if a.startswith('std_energia')]
std_energia.sort()
std_energia = [np.load(ruta + a) for i, a in std_energia]
std_energia = np.concatenate(std_energia).T

avg_presion = [[int(a.split('_')[2]), a] for a in archivos
               if a.startswith('avg_presion')]
avg_presion.sort()
avg_presion = [np.load(ruta + a) for i, a in avg_presion]
avg_presion = np.concatenate(avg_presion).T

std_presion = [[int(a.split('_')[2]), a] for a in archivos
               if a.startswith('std_presion')]
std_presion.sort()
std_presion = [np.load(ruta + a) for i, a in std_presion]
std_presion = np.concatenate(std_presion).T

#np.save(ruta + 'avg_energia', avg_energia)
#np.save(ruta + 'std_energia', std_energia)
#np.save(ruta + 'avg_presion', avg_presion)
#np.save(ruta + 'std_presion', std_presion)


ejes = [rhos[0], rhos[-1], temps[-1], temps[0]]

fig, ax1 = plt.subplots(1)


cax = ax1.imshow(avg_energia, origin='upper',
                 extent=ejes, aspect=0.5, cmap='hot')
ax1.set_xlabel(r'$\rho*$')
ax1.set_ylabel(r'$T*$')
fig.colorbar(cax)

plt.show()

fig, ax2 = plt.subplots(1)

cax = ax2.imshow(avg_presion, origin='upper',
                 extent=ejes, aspect=0.5, cmap='hot')
ax2.set_xlabel(r'$\rho*$')
ax2.set_ylabel(r'$T*$')
fig.colorbar(cax)

plt.show()
