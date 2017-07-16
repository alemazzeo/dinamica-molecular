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

for r, dato in datos:
    rho.append(r)
    array_pasos.append(dato[0])
    temp.append(dato[1])
    temp_real.append(dato[2])
    std_temp.append(dato[3])
    energia.append(dato[4])
    std_energia.append(dato[5])
    presion.append(dato[6])
    std_presion.append(dato[7])
    ld_avg.append(dato[8])
    ld_std.append(dato[9])
