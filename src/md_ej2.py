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
import matplotlib.pyplot as plt
import numpy as np
import os
from scipy.interpolate import griddata
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
ls_cycler = cycler('ls', ['-', '--', ':'])
plt.rc('axes', prop_cycle=lc_cycler * lw_cycler * ls_cycler)

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
    energia.append(dato[4])
    std_energia.append(dato[5])

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


def plot_lindemann_array(i=0, j=-1, ax=None, errorbar=True):
    if ax is None:
        fig, ax = plt.subplots(1)

    x = np.arange(100) * 50
    y, yerr = np.load(lds_list[i][1][j])
    str_rho_ld = r'$\rho$ ' + '%-6.2f' % float(lds_list[i][1][j].split('_')[2])
    str_temp_ld = r'$T=$ ' + '%-6.2f' % float(lds_list[i][1][j].split('_')[4])

    if errorbar:
        ax.errorbar(x, y, yerr=yerr, marker='.', label='LD - ' + str_temp_ld,
                    elinewidth=0.5, errorevery=2, ls=' ', color='k')
    else:
        ax.plot(x, y, label='LD - ' + str_temp_ld)

    ax.set_xlabel('Pasos')
    ax.set_ylabel('Coef. de Lindemann (' + str_rho_ld + ')')
    ax.annotate(str_temp_ld, xy=(x[-1], y[-1]), xytext=(x[-1] + 100, y[-1]),
                fontsize=14)
    ax.set_xlim([-50, x[-1] + 1000])


t1 = [1.05, 1.20, 0.95, 0.90, 0.80, 0.65, 0.43]
t1e = [0.05, 0.10, 0.05, 0.05, 0.02, 0.05, 0.01]
t2 = [0.36, 0.31, 0.33, 0.36, 0.34, 0.33, 0.31]
t2e = [0.01, 0.01, 0.02, 0.03, 0.01, 0.02, 0.01]


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
    fig.savefig(ruta_figuras + 'energia_rho_' + str_rho + '_fig.png')
    plt.close()

for i, r in enumerate(rho):
    str_rho = '%3.1f' % r
    fig, ax = plt.subplots(1)
    plot_presion(i=i, ax=ax, errorbar=True)
    fig.savefig(ruta_figuras + 'presion_rho_' + str_rho + '_fig.png')
    plt.close()

for i, r in enumerate(rho):
    str_rho = '%3.1f' % r
    fig, ax = plt.subplots(1)
    plot_lindemann(i=i, ax=ax, errorbar=True)
    fig.savefig(ruta_figuras + 'lindemann_rho_' + str_rho + '_fig.png')
    plt.close()

for i, r in enumerate(rho):
    str_rho = '%3.1f' % r
    fig, ax = plt.subplots(1)
    plot_temperatura(i=i, ax=ax, errorbar=True)
    fig.savefig(ruta_figuras + 'temp_rho_' + str_rho + '_fig.png')
    plt.close()
