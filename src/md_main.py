#!/usr/bin/env python
# -*- coding: utf-8 -*-
# file: md_main.py

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
import sys

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


################
# DOCUMENTACIÓN
################

def doc():
    print('\nCaracterísticas disponibles\n' + '-' * 27)
    print('\nFunciones para graficar:\n')
    print('    plot_temperatura(ax=None)')
    print('    plot_energia(ax=None)')
    print('    plot_presion(ax=None)')
    print('    plot_lindemann(ax=None)')
    print('    plot_lindemann_array(index=-1, ax=None, errorbar=True)\n')
    print('    (por defecto se grafican en figuras independientes)\n')
    print('    plot_main()')
    print('\nFunciones para manipular o ver estados:\n')
    print('    list_md()')
    print('    load_md(index=-1)\n')
    print('    mdsys.ver_pos(plot_vel=False, size=30)')
    print('    mdsys.dist_radial(n=100, m=100)')
    print('    mdsys.lindemann(m=10, subm=100, k=50, plot=False, ax=None)')
    print('    mdsys.ver_pos(plot_vel=False, size=30)')
    print('    mdsys.animacion(frames=1000, n_pasos=2)')


######################
# PARÁMETROS EXTERNOS
######################

parser = argparse.ArgumentParser()
parser.add_argument('-ruta', type=str, default='../datos/temp/')
parser.add_argument('-N', type=int, default=512)
parser.add_argument('-rho', type=float, default=0.4)
parser.add_argument('-T', type=float, default=2.0)
parser.add_argument('-dT', type=float, default=-0.025)
parser.add_argument('-pasos', type=int, default=76)
parser.add_argument('-pterm', type=int, default=5000)
parser.add_argument('-term', type=int, default=1000)
parser.add_argument('-m', type=int, default=30)
parser.add_argument('-subm', type=int, default=30)
parser.add_argument('-dc', type=int, default=150)
parser.add_argument('-k', type=int, default=50)
parser.add_argument('-actual', type=int, default=0)
parser.add_argument('-plot', action='store_true')

args_params = parser.parse_args()

ruta = args_params.ruta
N = args_params.N
rho = args_params.rho
T = args_params.T
dT = args_params.dT
pasos = args_params.pasos
pterm = args_params.pterm
term = args_params.term
m = args_params.m
subm = args_params.subm
dc = args_params.dc
k = args_params.dc
actual = args_params.actual


str_n = '%03d' % N
str_rho = '%06.3f' % rho
if not ruta[-1] == '/':
    ruta += '/'
ruta += 'n' + str_n + '/'

nombre_datos = ruta + 'r_' + str_rho + '_data.npy'
nombre_cfg = ruta + 'r_' + str_rho + '_config.npy'
nombre_lds = ruta + 'r_' + str_rho + '_lds.npy'
nombre_mds = ruta + 'r_' + str_rho + '_mds.npy'

os.makedirs(ruta, exist_ok=True)
os.makedirs(ruta + '/mds/', exist_ok=True)
os.makedirs(ruta + '/lds/', exist_ok=True)

mds = []

array_pasos = np.arange(pasos)
temp = array_pasos * dT + T
temp_real = np.zeros(pasos, dtype=float)
energia = np.zeros(pasos, dtype=float)
presion = np.zeros(pasos, dtype=float)
std_temp = np.zeros(pasos, dtype=float)
std_energia = np.zeros(pasos, dtype=float)
std_presion = np.zeros(pasos, dtype=float)
ld_avg = np.zeros(pasos, dtype=float)
ld_std = np.zeros(pasos, dtype=float)

ld_array_avg = np.zeros(100, dtype=float)
ld_array_std = np.zeros(100, dtype=float)

mdsys = md(N=N, T=T, rho=rho)
int_params = [N, pasos, pterm, term, m, subm, dc, k, actual]
float_params = [rho, T, dT]
mds = []
lds = []


if os.path.isfile(nombre_cfg) and os.path.isfile(nombre_mds):
    print('\nYa existe una simulación en la ubicación dada:')
    print('"' + nombre_cfg + '"')
    rta = input('[C]argar, [R]eemplazar, [S]alir: ').upper()
    while rta not in ('C', 'R', 'S'):
        rta = input('[C]argar, [R]eemplazar, [S]alir: ').upper()

    if rta == 'C':
        int_params, float_params = np.load(nombre_cfg)
        N, pasos, pterm, term, m, subm, dc, k, actual = int_params
        rho, T, dT = float_params

        datos = np.load(nombre_datos)
        array_pasos = datos[0]
        temp = datos[1]
        temp_real = datos[2]
        std_temp = datos[3]
        energia = datos[4]
        std_energia = datos[5]
        presion = datos[6]
        std_presion = datos[7]
        ld_avg = datos[8]
        ld_std = datos[9]

        lds = np.load(nombre_lds).tolist()
        mds = np.load(nombre_mds).tolist()
        mdsys = md.load(mds[-1])

        print('Simulación cargada.')

        doc()

    elif rta == 'R':
        msj = 'Esta acción no puede deshacerse. ¿Continuar? (S/N): '
        rta2 = input(msj).upper()
        while rta2 not in ('SI', 'NO', 'S', 'N'):
            rta2 = input(msj).upper()
        if rta2 in ('SI', 'S'):
            np.save(nombre_cfg, [int_params, float_params])
            np.save(nombre_lds, lds)
            np.save(nombre_mds, mds)
        else:
            sys.exit()

    elif rta == 'S':
        sys.exit()

    else:
        sys.exit()


############
# FUNCIONES
############


def corregir(T, mensaje=''):
    t_avg, t_std = mdsys.medir_temp(m=m, subm=subm, dc=dc)

    while (t_avg + t_std / 2 < T or T < t_avg - t_std / 2):
        str_t = '%06.3f +/-%-06.3f' % (t_avg, t_std / 2)
        str_dif = 'Ta: ' + str_t + 'Td: %-6.3f' % T
        print(mensaje + 'Corrigiendo', str_dif)
        mdsys.rescaling(T_deseada=T, T_actual=t_avg)
        mdsys.n_pasos(term)
        t_avg, t_std = mdsys.medir_temp(m=m, subm=subm, dc=dc)
    str_t = '%06.3f +/-%-06.3f' % (t_avg, t_std / 2)
    print(mensaje + 'Temp. estabilizada en ' + str_t)


def siguiente_paso(paso):
    actual = paso
    str_actual = "%3d/%3d - " % (paso + 1, pasos)

    print('\n' + str_actual + 'Tomando muestra')
    t_m, e_m, p_m = mdsys.tomar_muestra(m=m, subm=subm, dc=dc, k=k)

    print(str_actual + 'Calculando Lindemann')
    ld_m = mdsys.lindemann(m=10, subm=100, k=50)

    temp_real[paso] = t_m[0]
    std_temp[paso] = t_m[1]
    energia[paso] = e_m[0]
    std_energia[paso] = e_m[1]
    presion[paso] = p_m[0]
    std_presion[paso] = p_m[1]

    ld_avg[paso] = ld_m[0][-1]
    ld_std[paso] = ld_m[1][-1]

    if paso + 1 < pasos:
        print(str_actual + 'Rescaleando y verificando')
        mdsys.rescaling(T_deseada=temp[paso + 1], T_actual=t_m[0])
        mdsys.n_pasos(term)

        corregir(temp[paso + 1], mensaje=str_actual)

    datos = [array_pasos, temp, temp_real, std_temp, energia, std_energia,
             presion, std_presion, ld_avg, ld_std]

    lindemann = [ld_m[0], ld_m[1]]

    str_temp = '%06.3f' % temp_real[paso]
    nombre_md = 'n' + str_n + '_r_' + str_rho + '_t_' + str_temp + '_md.npy'
    nombre_ld = 'n' + str_n + '_r_' + str_rho + '_t_' + str_temp + '_ld.npy'

    int_params[-1] = actual + 1
    mds.append(ruta + 'mds/' + nombre_md)
    lds.append(ruta + 'lds/' + nombre_ld)

    mdsys.save(nombre=nombre_md, ruta=ruta + 'mds/')
    np.save(lds[-1], lindemann)

    np.save(nombre_cfg, [int_params, float_params])
    np.save(nombre_datos, datos)
    np.save(nombre_lds, lds)
    np.save(nombre_mds, mds)


def plot_temperatura(ax=None, errorbar=True):
    if ax is None:
        fig, ax = plt.subplots(1)

    if errorbar:
        ax.errorbar(array_pasos, temp_real, yerr=std_temp, elinewidth=0.5,
                    label='Temperatura (<v²>)', ls=' ', marker='o')
    else:
        ax.plot(array_pasos, temp_real, label='Temperatura (<v²>)',
                marker='o')

    ax.plot(array_pasos, temp, ls='--', marker=' ',
            label='Temperatura buscada')
    ax.set_xlabel('Muestras')
    ax.set_ylabel(r'Temperatura ($\rho$' + str_rho + ')')
    ax.legend(loc='best')


def plot_energia(ax=None, errorbar=True):
    if ax is None:
        fig, ax = plt.subplots(1)

    if errorbar:
        ax.errorbar(temp_real, energia, xerr=std_temp, yerr=std_energia,
                    label='Energía', ls=' ', marker='o', elinewidth=0.5)
    else:
        ax.plot(temp_real, energia, label='Energía', ls=' ', marker='o')

    ax.set_xlabel('Temperatura')
    ax.set_ylabel(r'Energía ($\rho$' + str_rho + ')')
    ax.legend(loc='best')


def plot_presion(ax=None, errorbar=True):
    if ax is None:
        fig, ax = plt.subplots(1)

    inv_temp = 1 / temp_real
    inv_std_temp = inv_temp**2 * std_temp
    if errorbar:
        ax.errorbar(inv_temp, presion, xerr=inv_std_temp, yerr=std_presion,
                    label='Presión', ls=' ', marker='o', elinewidth=0.5)
    else:
        ax.plot(inv_temp, presion, label='Presión', ls=' ', marker='o')
    ax.set_xlabel(r'$1/T$')
    ax.set_ylabel(r'Presión ($\rho$' + str_rho + ')')

    ax.legend(loc='best')


def plot_lindemann(ax=None, errorbar=True):
    if ax is None:
        fig, ax = plt.subplots(1)

    ax.errorbar(energia, ld_avg, xerr=std_energia, yerr=ld_std[-1],
                label='Coef. de Lindemann', ls=' ', marker='o',
                elinewidth=0.5)
    ax.set_xlabel('Energía')
    ax.set_ylabel(r'Coef. de Lindemann ($\rho$' + str_rho + ')')
    ax.legend(loc='best')


def plot_lindemann_array(index=-1, ax=None, errorbar=True):
    if ax is None:
        fig, ax = plt.subplots(1)

    x = np.arange(100) * 50
    y, yerr = np.load(lds[index])
    str_rho_ld = r'$\rho$ ' + '%-6.3f' % float(lds[index].split('_')[2])
    str_temp_ld = r'$T$ ' + '%-6.3f' % float(lds[index].split('_')[4])

    if errorbar:
        ax.errorbar(x, y, yerr=yerr, marker='.', label='LD - ' + str_temp_ld,
                    elinewidth=0.5)
    else:
        ax.plot(x, y, label='LD - ' + str_temp_ld)
    ax.set_xlabel('Pasos')
    ax.set_ylabel('Coef. de Lindemann (' + str_rho_ld + ')')
    ax.legend(loc='best', ncol=2)


def plot_main():
    plt.ion()
    fig, axs = plt.subplots(2, 2)
    plot_temperatura(axs[0][0])
    plot_energia(axs[0][1])
    plot_presion(axs[1][0])
    plot_lindemann(axs[1][1])
    plot_lindemann_array(-1)


def list_md():
    for i, name in enumerate(mds):
        flt_rho = float(name.split('_')[2])
        flt_temp = float(name.split('_')[4])
        print('%3d, %-6.3f, %-6.3f -> %40s' % (i, flt_rho, flt_temp, name))


def load_md(index=-1):
    global mdsys
    mdsys = md.load(mds[index])


#####################
# PROGRAMA PRINCIPAL
#####################

continuar = True
if 0 < actual < pasos:
    print('\nQuedan %d pasos pendientes,' % (pasos - actual), end='')
    rta = input('¿Continuar hasta terminar? (S/N): ').upper()
    while rta not in ('S', 'N', 'SI', 'NO'):
        rta = input('¿Continuar hasta terminar? (S/N): ').upper()
    if rta in ('S', 'SI'):
        continuar = True
        actual -= 1
    else:
        continuar = False

if actual < pasos and continuar:
    print('\nPreparando la configuración')
    mdsys.n_pasos(pterm)
    corregir(T)

    print('')

    for i in range(actual, pasos):
        siguiente_paso(i)

    print('Simulación finalizada\n')
    doc()

if args_params.plot:
    plot_main()
