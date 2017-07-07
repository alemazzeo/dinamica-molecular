#!/usr/bin/env python
# -*- coding: utf-8 -*-
# file: md_map.py

from md_class import md
import time
import numpy as np
import matplotlib.pyplot as plt

import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-path', type=str, default='../datos/maps/n125/')
parser.add_argument('-N', type=int, default=125)
parser.add_argument('-T_start', type=float, default=2.0)
parser.add_argument('-T_stop', type=float, default=0.22)
parser.add_argument('-T_step', type=float, default=0.02)
parser.add_argument('-rho_start', type=float, default=0.02)
parser.add_argument('-rho_stop', type=float, default=0.1)
parser.add_argument('-rho_step', type=float, default=0.02)
parser.add_argument('-preterm', type=int, default=500)
parser.add_argument('-term', type=int, default=50)
parser.add_argument('-m', type=int, default=200)
parser.add_argument('-dc', type=int, default=50)
parser.add_argument('-plot', action='store_true')

params = parser.parse_args()

path = params.path

N = params.N

T_start = params.T_start
T_stop = params.T_stop
T_step = params.T_step

rho_start = params.rho_start
rho_stop = params.rho_stop
rho_step = params.rho_step

term = params.term
preterm = params.preterm

m = params.m
dc = params.dc

n_rhos = int(abs((rho_start - rho_stop) / rho_step)) + 1
n_temps = int(abs((T_start - T_stop) / T_step)) + 1

rhos = np.linspace(rho_start, rho_stop, n_rhos, endpoint=True)
temps = np.linspace(T_start, T_stop, n_temps, endpoint=True)

avg_energia = np.zeros((n_rhos, n_temps), dtype=float)
avg_presion = np.zeros((n_rhos, n_temps), dtype=float)
std_energia = np.zeros((n_rhos, n_temps), dtype=float)
std_presion = np.zeros((n_rhos, n_temps), dtype=float)

time_start = time.time()
for i, rho in enumerate(rhos):

    for j, T in enumerate(temps):

        str_rho = 'Rho: %3d/%-3d (%6.3f)' % (i + 1, n_rhos, rho)
        str_T = 'T: %3d/%-3d (%6.3f)' % (j + 1, n_temps, T)
        str_progreso = ' - ' + str_rho + ', ' + str_T + ' - '
        str_nuevo_rho = '%-35s' % 'Termalizando para nuevo rho'
        str_rescaling = '%-35s' % 'Termalizando para nueva T'
        str_muestra = '%-35s' % 'Promediando muestra'
        str_guardar = '%-35s' % 'Guardando estado actual'

        if j > 0:
            elapsed = time.gmtime(time.time() - time_start)
            str_elapsed = time.strftime('%X', elapsed)
            print(str_elapsed + str_progreso + str_rescaling)
            mdsys.rescaling(T)
            mdsys.n_pasos(preterm)

        else:
            elapsed = time.gmtime(time.time() - time_start)
            str_elapsed = time.strftime('%X', elapsed)
            print(str_elapsed + str_progreso + str_nuevo_rho)
            mdsys = md(N=N, T=T_start, rho=rho)
            mdsys.n_pasos(term)

        elapsed = time.gmtime(time.time() - time_start)
        str_elapsed = time.strftime('%X', elapsed)
        print(str_elapsed + str_progreso + str_muestra)
        e, p = mdsys.tomar_muestra(m, dc)

        avg_energia[i][j] = e[0]
        std_energia[i][j] = e[1]
        avg_presion[i][j] = p[0]
        std_presion[i][j] = p[1]

        elapsed = time.gmtime(time.time() - time_start)
        str_elapsed = time.strftime('%X', elapsed)
        print(str_elapsed + str_progreso + str_guardar)

        nombre_md = 'md_' + str(N) + '_r_%5.3f' % rho + '_T_%5.3f' % T + '.npy'
        mdsys.save(nombre=nombre_md, ruta=path)

intervalo = 'rho_%5.3f_a_%5.3f' % (rho_start, rho_stop)
np.save(path + intervalo + '_avg_energia', avg_energia)
np.save(path + intervalo + '_std_energia', std_energia)
np.save(path + intervalo + '_avg_presion', avg_presion)
np.save(path + intervalo + '_std_presion', std_presion)


if params.plot:
    plt.ion()
    fig, axs = plt.subplots(2, 2)

    axs[0][0].imshow(avg_energia.T)
    axs[0][1].imshow(avg_presion.T)
    axs[1][0].imshow(std_presion.T)
    axs[1][1].imshow(std_presion.T)

    #axs[0].errorbar(temps, avg_energia, yerr=std_energia)
    #axs[1].errorbar(1 / temps, avg_presion, yerr=std_presion)
