#!/usr/bin/env python
# -*- coding: utf-8 -*-
# file: md_ej2.py

import matplotlib

try:
    matplotlib.use('Qt5Agg')
except:
    try:
        matplotlib.use('qt4Agg')
    except:
        print('No fue posible configurar Qt5Agg o qt4Agg')
        print('Se utilizará', matplotlib.get_backend())

from md_class import md
import argparse
from cycler import cycler
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
from matplotlib.collections import PolyCollection
import numpy as np
import os
from scipy.interpolate import InterpolatedUnivariateSpline as spline
import sys

######################
# PARÁMETROS EXTERNOS
######################

parser = argparse.ArgumentParser()
parser.add_argument('-ruta', type=str, default='../datos/corrida2/n512/')

args_params = parser.parse_args()
ruta = args_params.ruta

###############################################
# CONFIGURACIONES POR DEFECTO PARA LAS FIGURAS
###############################################

# Figura (tamaño)
plt.rc('figure', figsize=(8, 6))

# Figura (subplot)
plt.rc('figure.subplot', left=0.15)

# Ticks (tamaño de la fuente)
plt.rc(('xtick', 'ytick'), labelsize=14)

# Bordes de la figura (visibles o no)
plt.rc('axes.spines', left=True, bottom=True, top=False, right=False)

# Leyenda (tamaño de la fuenta y ubicación)
plt.rc('legend', fontsize=14, loc='best')

# Ejes (tamaño de la fuente)
plt.rc('axes', labelsize=14)

# Errorbar
plt.rc('errorbar', capsize=2.0)

# Ejes (autoestilo para múltiples curvas)
lc_cycler = cycler('color', ['0.0', '0.5'])
lw_cycler = cycler('lw', [2, 1])
ls_cycler = cycler('ls', ['-', '--', ':', '-.'])
plt.rc('axes', prop_cycle=lw_cycler * ls_cycler)

####################
# CARGA DE ARCHIVOS
####################

archivos = os.listdir(ruta)

N = int(ruta.split('/')[-2][1:])

configs = [[float(a.split('_')[1]), np.load(ruta + a)] for a in archivos
           if a.endswith('config.npy')]
configs.sort()

datos = [[float(a.split('_')[1]), np.load(ruta + a)] for a in archivos
         if a.endswith('data.npy')]
datos.sort()

mds_list = [[float(a.split('_')[1]), np.load(ruta + a)] for a in archivos
            if a.endswith('mds.npy')]
mds_list.sort()

lds_list = [[float(a.split('_')[1]), np.load(ruta + a)] for a in archivos
            if a.endswith('lds.npy')]
lds_list.sort()

rho = []
array_pasos = []
temp = []
temp_real = []
std_temp = []
energia = []
std_energia = []
presion = []
std_presion = []
ld_avg = []
ld_std = []
volumen = []

for r, dato in datos:
    rho.append(r)
    array_pasos.append(dato[0])
    temp.append(dato[1])
    temp_real.append(dato[2])
    std_temp.append(dato[3])
    energia.append(dato[4] / 1000)
    std_energia.append(dato[5] / 1000)

    vol = N / r
    presion_corregida = (dato[6] / vol + 1) * r * dato[2]
    std_corregida = dato[7] * r * dato[2] / vol

    presion.append(presion_corregida)
    std_presion.append(std_corregida)
    ld_avg.append(dato[8])
    ld_std.append(dato[9])
    volumen.append(np.repeat(vol, len(dato[0])))

##########################
# FUNCIONES PARA GRAFICAR
##########################


def plot_temperatura(i=0, ax=None, errorbar=True):
    str_rho = '%3.1f' % rho[i]
    if ax is None:
        fig, ax = plt.subplots(1)

    if errorbar:
        ax.errorbar(array_pasos[i], temp_real[i], yerr=std_temp[i],
                    elinewidth=0.5, ls=' ', marker='o', alpha=0.5,
                    label=r'Temperatura (<v²>) ($\rho$ ' + str_rho + ')')
    else:
        ax.plot(array_pasos[i], temp_real[i], marker='o',
                label=r'Temperatura (<v²>) ($\rho$ ' + str_rho + ')')

    ax.plot(array_pasos[i], temp[i], ls='--', label='Temperatura buscada')
    ax.set_xlabel('Muestras')
    ax.set_ylabel(r'Temperatura')
    ax.legend(loc='best')


def plot_energia(i=0, ax=None, errorbar=True):
    str_rho = '%3.1f' % rho[i]
    if ax is None:
        fig, ax = plt.subplots(1)

    if errorbar:
        ax.errorbar(temp_real[i], energia[i],
                    xerr=std_temp[i], yerr=std_energia[i],
                    label=r'Energía ($\rho$: ' + str_rho + ')',
                    ls=' ', marker='o', elinewidth=0.5)
    else:
        ax.plot(temp_real[i], energia[i], label='Energía')

    ax.set_xlabel('Temperatura')
    ax.set_ylabel(r'Energía')
    ax.legend(loc='best')


def plot_presion(i=0, ax=None, errorbar=True):
    str_rho = '%3.1f' % rho[i]
    if ax is None:
        fig, ax = plt.subplots(1)

    if errorbar:
        ax.errorbar(temp_real[i], presion[i],
                    xerr=std_temp[i], yerr=std_presion[i],
                    label=r'Presión ($\rho$: ' + str_rho + ')',
                    ls=' ', marker='o', elinewidth=0.5)
    else:
        ax.plot(temp_real[i], presion[i], label='Presión')
    ax.set_xlabel(r'Temperatura')
    ax.set_ylabel(r'Presión')
    ax.legend(loc='best')


def plot_presion_exceso(i=0, ax=None, errorbar=True):
    str_rho = '%3.1f' % rho[i]
    if ax is None:
        fig, ax = plt.subplots(1)

    p_exceso = presion[i] / (temp_real[i] * rho[i]) - 1
    std_exceso = std_presion[i] * (temp_real[i] * rho[i])
    if errorbar:
        ax.errorbar(1 / temp_real[i], p_exceso,
                    xerr=std_temp[i] / temp_real[i]**2, yerr=std_exceso,
                    label=r'Presión de exceso ($\rho$: ' + str_rho + ')',
                    ls=' ', marker='o', elinewidth=0.5)
    else:
        ax.plot(temp_real[i], presion[i], label='Presión')
    ax.set_xlabel(r'1/T')
    ax.set_ylabel(r'Presión')
    ax.legend(loc='best')


def plot_presion_vs_V(i=0, ax=None, errorbar=True):
    str_temp = '%3.1f' % temp_real[0][i]
    if ax is None:
        fig, ax = plt.subplots(1)

    vol = N / np.asarray(rho)
    p = np.asarray(presion).T[i]

    if errorbar:
        ax.errorbar(vol, p,
                    yerr=np.asarray(std_presion).T[i],
                    label=r'Presión ($T$: ' + str_temp + ')',
                    ls=' ', marker='o', elinewidth=0.5)
    else:
        ax.plot(vol, p, marker='o',
                label=r'Presión ($T$: ' + str_temp + ')')
    ax.set_xlabel(r'Volumen')
    ax.set_ylabel(r'Presión')
    ax.legend(loc='best')


def plot_lindemann(i=0, ax=None, errorbar=True):
    str_rho = '%3.1f' % rho[i]
    if ax is None:
        fig, ax = plt.subplots(1)

    if errorbar:
        ax.errorbar(energia[i], ld_avg[i],
                    xerr=std_energia[i], yerr=ld_std[i],
                    label=r'Coef. de Lindemann ($\rho$: ' + str_rho + ')',
                    ls=' ', marker='o', elinewidth=0.5)
    else:
        ax.errorbar(energia[i], ld_avg[i],
                    label=r'Coef. de Lindemann ($\rho$: ' + str_rho + ')')

    ax.set_xlabel('Energía')
    ax.set_ylabel(r'Coef. de Lindemann')
    ax.legend(loc='best')


def plot_lindemann_vs_T(i=0, ax=None, errorbar=True):
    str_rho = '%3.1f' % rho[i]
    if ax is None:
        fig, ax = plt.subplots(1)

    if errorbar:
        ax.errorbar(temp_real[i], ld_avg[i],
                    xerr=std_temp[i], yerr=ld_std[i],
                    label=r'Coef. de Lindemann ($\rho$: ' + str_rho + ')',
                    ls=' ', marker='o', elinewidth=0.5)
    else:
        ax.errorbar(temp_real[i], ld_avg[i],
                    label=r'Coef. de Lindemann ($\rho$: ' + str_rho + ')')

    ax.set_xlabel('Temperatura')
    ax.set_ylabel(r'Coef. de Lindemann')
    ax.annotate(r'$\rho$: ' + str_rho, xy=(temp_real[i][0], ld_avg[i][0]),
                xytext=(temp_real[i][0] + 0.1, ld_avg[i][0]), fontsize=14,
                verticalalignment='center')
    ax.set_xlim([0, 2.3])


def plot_lindemann_array(i=0, j=-1, ax=None, errorbar=True):
    if ax is None:
        fig, ax = plt.subplots(1)

    x = np.arange(100) * 50
    y, yerr = np.load(lds_list[i][1][j])
    str_rho_ld = r'$\rho$ ' + '%3.1f' % float(lds_list[i][1][j].split('_')[2])
    str_temp_ld = r'$T=$ ' + '%3.1f' % float(lds_list[i][1][j].split('_')[4])

    if errorbar:
        ax.errorbar(x, y, yerr=yerr, marker='.', label='LD - ' + str_temp_ld,
                    elinewidth=0.5, errorevery=2, ls=' ', color='k')
    else:
        ax.plot(x, y, label='LD - ' + str_temp_ld)

    ax.set_xlabel('Pasos')
    ax.set_ylabel('Coef. de Lindemann (' + str_rho_ld + ')')
    ax.annotate(str_temp_ld, xy=(x[-1], y[-1]), xytext=(x[-1] + 100, y[-1]),
                fontsize=14, verticalalignment='center')
    ax.set_xlim([-50, x[-1] + 1000])


def plot_energia_waterfall(i=slice(None, None, None)):
    plt.ion()
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1, projection='3d')

    xs = temp_real[i]
    ys = energia[i]
    zs = rho[i]

    xmin, ymin = [], []
    xmax, ymax = [], []

    verts = []
    for i, z in enumerate(zs):
        ys[i][0], ys[i][-1] = -3.2, -3.2
        verts.append(list(zip(xs[i], ys[i])))
        xmin.append(min(xs[i]))
        ymin.append(min(ys[i]))
        xmax.append(max(xs[i]))
        ymax.append(max(ys[i]))

    poly = PolyCollection(verts, facecolors=(1, 1, 1, 1),
                          edgecolors=(0, 0, 0, 0))
    poly.set_alpha(0.9)

    ax.add_collection3d(poly, zs=zs, zdir='y')

    ax.set_xlim3d(min(xmin), max(xmax))
    ax.set_ylim3d(min(zs), max(zs))
    ax.set_zlim3d(min(ymin), max(ymax))

    ax.set_xlabel('\nTemperatura', linespacing=3)
    ax.set_ylabel('\nDensidad', linespacing=3)
    ax.set_zlabel('\nEnergía', linespacing=3)

    return fig, ax


def plot_presion_waterfall(i=slice(None, None, None)):
    plt.ion()
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1, projection='3d')

    xs = temp_real[i]
    ys = presion[i]
    zs = N / np.asarray(rho[i])

    xmin, ymin = [], []
    xmax, ymax = [], []

    verts = []
    for i, z in enumerate(zs):
        ys[i][0], ys[i][-1] = -0.2, -0.2
        verts.append(list(zip(xs[i], ys[i])))
        xmin.append(min(xs[i]))
        ymin.append(min(ys[i]))
        xmax.append(max(xs[i]))
        ymax.append(max(ys[i]))

    poly = PolyCollection(verts, facecolors=(1, 1, 1, 1),
                          edgecolors=(0, 0, 0, 0))
    poly.set_alpha(0.9)

    ax.add_collection3d(poly, zs=zs, zdir='y')

    ax.set_xlim3d(min(xmin), max(xmax))
    ax.set_ylim3d(min(zs), max(zs))
    ax.set_zlim3d(min(ymin), max(ymax))

    ax.set_xlabel('\nTemperatura', linespacing=3)
    ax.set_ylabel('\nDensidad', linespacing=3)
    ax.set_zlabel('\nPresión', linespacing=3)


###########################
# GRÁFICOS PARA EL INFORME
###########################

plt.ioff()

ruta_figuras = ruta + '/figuras/'
os.makedirs(ruta_figuras, exist_ok=True)


for i, r in enumerate(rho):
    str_rho = '%3.1f' % r
    fig, ax = plt.subplots(1)
    plot_energia(i=i, ax=ax, errorbar=True)
    # fig.savefig(ruta_figuras + 'energia_rho_' + str_rho + '_fig.png')
    plt.close()


for i, r in enumerate(rho):
    str_rho = '%3.1f' % r
    fig, ax = plt.subplots(1)
    plot_presion(i=i, ax=ax, errorbar=True)
    # fig.savefig(ruta_figuras + 'presion_rho_' + str_rho + '_fig.png')
    plt.close()


for i, r in enumerate(rho):
    str_rho = '%3.1f' % r
    fig, ax = plt.subplots(1)
    plot_presion_exceso(i=i, ax=ax, errorbar=True)
    # fig.savefig(ruta_figuras + 'p_exceso_rho_' + str_rho + '_fig.png')
    plt.close()


for i, r in enumerate(rho):
    str_rho = '%3.1f' % r
    fig, ax = plt.subplots(1)
    plot_lindemann(i=i, ax=ax, errorbar=True)
    # fig.savefig(ruta_figuras + 'lindemann_rho_' + str_rho + '_fig.png')
    plt.close()


for i, r in enumerate(rho):
    str_rho = '%3.1f' % r
    fig, ax = plt.subplots(1)
    plot_temperatura(i=i, ax=ax, errorbar=True)
    # fig.savefig(ruta_figuras + 'temp_rho_' + str_rho + '_fig.png')
    plt.close()


fig, ax = plt.subplots(1)
for i in range(9):
    plot_lindemann_array(i=6, j=0 + 8 * i, ax=ax)
str_rho = '%3.1f' % rho[6]
#fig.savefig(ruta_figuras + 'ld_array_rho_' + str_rho + '_fig.png')
plt.close()


fig, ax = plt.subplots(1)
for i in range(9):
    plot_lindemann_array(i=5, j=40 + 4 * i, ax=ax)
str_rho = '%3.1f' % rho[5]
fig.savefig(ruta_figuras + 'ld_array_rho_' + str_rho + '_fig2.png')
plt.close()

fig, ax = plt.subplots(2, sharex='all')
fig.subplots_adjust(hspace=0.025)
str_rho = '%3.1f' % rho[2]
ax[0].set_xlabel(' ')
ax[0].axvline(0.965, color='k', ls=':')
ax[0].axvline(0.34, color='k', ls=':')
plot_energia(i=2, ax=ax[0], errorbar=True)
ax[1].axvline(0.965, color='k', ls=':')
ax[1].axvline(0.34, color='k', ls=':')
plot_presion(i=2, ax=ax[1], errorbar=True)
fig.savefig(ruta_figuras + 'energia_presion_rho_' + str_rho + '_fig.png')
plt.close()

fig, ax = plt.subplots(2, sharex='all')
fig.subplots_adjust(hspace=0.025)
str_rho = '%3.1f' % rho[3]
ax[0].set_xlabel(' ')
ax[0].axvline(0.90, color='k', ls=':')
ax[0].axvline(0.365, color='k', ls=':')
plot_energia(i=3, ax=ax[0], errorbar=True)
ax[1].axvline(0.90, color='k', ls=':')
ax[1].axvline(0.365, color='k', ls=':')
plot_presion(i=3, ax=ax[1], errorbar=True)
fig.savefig(ruta_figuras + 'energia_presion_rho_' + str_rho + '_fig.png')
plt.close()

fig, ax = plt.subplots(2, sharex='all')
fig.subplots_adjust(hspace=0.025)
str_rho = '%3.1f' % rho[4]
ax[0].set_xlabel(' ')
ax[0].axvline(0.82, color='k', ls=':')
ax[0].axvline(0.34, color='k', ls=':')
plot_energia(i=4, ax=ax[0], errorbar=True)
ax[1].axvline(0.82, color='k', ls=':')
ax[1].axvline(0.34, color='k', ls=':')
plot_presion(i=4, ax=ax[1], errorbar=True)
fig.savefig(ruta_figuras + 'energia_presion_rho_' + str_rho + '_fig.png')
plt.close()

fig, ax = plt.subplots(2, sharex='all')
fig.subplots_adjust(hspace=0.025)
str_rho = '%3.1f' % rho[5]
ax[0].set_xlabel(' ')
ax[0].axvline(0.640, color='k', ls=':')
ax[0].axvline(0.345, color='k', ls=':')
plot_energia(i=5, ax=ax[0], errorbar=True)
ax[1].axvline(0.640, color='k', ls=':')
ax[1].axvline(0.345, color='k', ls=':')
plot_presion(i=5, ax=ax[1], errorbar=True)
fig.savefig(ruta_figuras + 'energia_presion_rho_' + str_rho + '_fig.png')
plt.close()

fig, ax = plt.subplots(2, sharex='all')
fig.subplots_adjust(hspace=0.025)
str_rho = '%3.1f' % rho[6]
ax[0].set_xlabel(' ')
ax[0].axvline(0.435, color='k', ls=':')
ax[0].axvline(0.315, color='k', ls=':')
plot_energia(i=6, ax=ax[0], errorbar=True)
ax[1].axvline(0.435, color='k', ls=':')
ax[1].axvline(0.315, color='k', ls=':')
plot_presion(i=6, ax=ax[1], errorbar=True)
fig.savefig(ruta_figuras + 'energia_presion_rho_' + str_rho + '_fig.png')
plt.close()


t1 = [1.05, 1.20, 0.965, 0.90, 0.80, 0.64, 0.435]
t1e = [0.05, 0.10, 0.05, 0.05, 0.02, 0.05, 0.01]

t2 = [0.36, 0.31, 0.33, 0.365, 0.34, 0.345, 0.315]
t2e = [0.01, 0.01, 0.02, 0.03, 0.01, 0.02, 0.01]

fig, ax = plot_energia_waterfall(slice(0, 6))
ax.plot([1.32, 0.66], [rho[0], rho[5]], [0.35, -1.78], ls='--', lw=2)
ax.plot([0.36, 0.33], [rho[0], rho[5]], [-2.5, -2.8], ls='--', lw=2)
plt.close()
