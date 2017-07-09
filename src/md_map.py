#!/usr/bin/env python
# -*- coding: utf-8 -*-
# file: md_map.py

from md_class import md
import os
import time
import numpy as np
import matplotlib.pyplot as plt

import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-etapa', type=int, default=1)
parser.add_argument('-n_etapas', type=int, default=6)
parser.add_argument('-path', type=str, default='../datos/maps/')
parser.add_argument('-N', type=int, default=512)
parser.add_argument('-T_start', type=float, default=2.0)
parser.add_argument('-T_stop', type=float, default=0.02)
parser.add_argument('-T_step', type=float, default=0.02)
parser.add_argument('-rho_start', type=float, default=0.01)
parser.add_argument('-rho_stop', type=float, default=1.0)
parser.add_argument('-rho_step', type=float, default=0.01)
parser.add_argument('-preterm', type=int, default=500)
parser.add_argument('-term', type=int, default=50)
parser.add_argument('-m', type=int, default=200)
parser.add_argument('-dc', type=int, default=50)
parser.add_argument('-plot', action='store_true')

params = parser.parse_args()

etapa = params.etapa
n_etapas = params.n_etapas

N = params.N

path = params.path + '/n%d/' % N
os.makedirs(path, exist_ok=True)

T_start = params.T_start
T_stop = params.T_stop
T_step = params.T_step

rho_start = params.rho_start
rho_stop = params.rho_stop
rho_step = params.rho_step

assert rho_start < 1.5
assert rho_stop < 1.5

term = params.term
preterm = params.preterm

m = params.m
dc = params.dc

n_rhos = int(abs((rho_start - rho_stop) / rho_step)) + 1
n_temps = int(abs((T_start - T_stop) / T_step)) + 1

rhos = np.linspace(rho_start, rho_stop, n_rhos, endpoint=True)
temps = np.linspace(T_start, T_stop, n_temps, endpoint=True)

np.save(path + 'rhos', rhos)
np.save(path + 'temps', temps)

with open(path + 'params.txt', 'w') as f:
    f.write('T_start:  %6.3f\n' % T_start)
    f.write('T_stop:   %6.3f\n' % T_stop)
    f.write('T_step:   %6.3f\n' % T_step)
    f.write('rho_start %6.3f\n' % rho_start)
    f.write('rho_stop: %6.3f\n' % rho_stop)
    f.write('rho_step: %6.3f\n' % rho_step)
    f.write('term:     %6d\n' % term)
    f.write('preterm:  %6d\n' % preterm)
    f.write('m:        %6d\n' % m)
    f.write('dc:       %6d\n' % dc)

# DIVISIÓN DEL TRABAJO PARA PROCESOS SIMULTÁNEOS

division = np.array_split(rhos, n_etapas)
rhos = division[etapa - 1]

print('Esquema de trabajo:\n')
for i in range(n_etapas):
    if i == etapa - 1:
        print('Desde %6.3f hasta %6.3f (asignado)' %
              (division[i][0], division[i][-1]))
    else:
        print('Desde %6.3f hasta %6.3f' %
              (division[i][0], division[i][-1]))

rho_start = rhos[0]
rho_stop = rhos[-1]
n_rhos = len(rhos)

np.save(path + 'rhos_%d_%d' % (etapa, n_etapas), rhos)

avg_energia = np.zeros((n_rhos, n_temps), dtype=float)
avg_presion = np.zeros((n_rhos, n_temps), dtype=float)
std_energia = np.zeros((n_rhos, n_temps), dtype=float)
std_presion = np.zeros((n_rhos, n_temps), dtype=float)

time_start = time.time()
str_total = '--:--:--'

print('\nSimulación iniciada\n')

for i, rho in enumerate(rhos):

    for j, T in enumerate(temps):

        str_rho = 'Rho: %3d/%-3d (%6.3f)' % (i + 1, n_rhos, rho)
        str_T = 'T: %3d/%-3d (%6.3f)' % (j + 1, n_temps, T)
        str_progreso = ' - ' + str_rho + ', ' + str_T + ' - '
        str_nuevo_rho = '%-35s' % 'Nuevo Rho'
        str_rescaling = '%-35s' % 'Nueva T'
        str_muestra = '%-35s' % 'Muestreando'
        str_guardar = '%-35s' % 'Guardando'
        str_listo = '%-35s' % 'Listo.'

        if j > 0:
            elapsed = time.gmtime(time.time() - time_start)
            str_elapsed = time.strftime('%X', elapsed) + ' / ' + str_total
            print('\r' + str_elapsed + str_progreso + str_rescaling, end='')
            mdsys.rescaling(T)
            mdsys.n_pasos(preterm)

        else:
            elapsed = time.gmtime(time.time() - time_start)
            str_elapsed = time.strftime('%X', elapsed) + ' / ' + str_total
            print('\r' + str_elapsed + str_progreso + str_nuevo_rho, end='')
            mdsys = md(N=N, T=T_start, rho=rho)
            mdsys.n_pasos(term)

        elapsed = time.gmtime(time.time() - time_start)
        str_elapsed = time.strftime('%X', elapsed) + ' / ' + str_total
        print('\r' + str_elapsed + str_progreso + str_muestra, end='')
        e, p = mdsys.tomar_muestra(m, dc)

        avg_energia[i][j] = e[0]
        std_energia[i][j] = e[1]
        avg_presion[i][j] = p[0]
        std_presion[i][j] = p[1]

        elapsed = time.gmtime(time.time() - time_start)
        str_elapsed = time.strftime('%X', elapsed) + ' / ' + str_total
        print('\r' + str_elapsed + str_progreso + str_guardar, end='')

        nombre_md = 'md_' + str(N) + '_r_%5.3f' % rho + '_T_%5.3f' % T + '.npy'
        mdsys.save(nombre=nombre_md, ruta=path + '/estados/')

        np.save(path + 'avg_energia_%d_%d' % (etapa, n_etapas), avg_energia)
        np.save(path + 'std_energia_%d_%d' % (etapa, n_etapas), std_energia)
        np.save(path + 'avg_presion_%d_%d' % (etapa, n_etapas), avg_presion)
        np.save(path + 'std_presion_%d_%d' % (etapa, n_etapas), std_presion)

        elapsed = time.gmtime(time.time() - time_start)
        str_elapsed = time.strftime('%X', elapsed) + ' / ' + str_total
        print('\r' + str_elapsed + str_progreso + str_listo)

    total = (time.time() - time_start) * (n_rhos / (i + 1))
    str_total = time.strftime('%X', time.gmtime(total))

if params.plot:
    plt.ion()
    fig, axs = plt.subplots(2, 2)

    ejes = [rho_start, rho_stop, T_stop, T_start]

    axs[0][0].imshow(avg_energia.T, origin='upper', extent=ejes, cmap='hot')
    axs[0][1].imshow(avg_presion.T, origin='upper', extent=ejes, cmap='hot')
    axs[1][0].imshow(std_presion.T, origin='upper', extent=ejes, cmap='hot')
    axs[1][1].imshow(std_presion.T, origin='upper', extent=ejes, cmap='hot')
