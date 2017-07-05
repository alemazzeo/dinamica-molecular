#!/usr/bin/env python
# -*- coding: utf-8 -*-
# file: md_main.py

from md_class import md
import numpy as np
import matplotlib.pyplot as plt

import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-N', type=int, default=32)
parser.add_argument('-rho', type=float, default=0.8)
parser.add_argument('-start', type=float, default=2.0)
parser.add_argument('-stop', type=float, default=0.2)
parser.add_argument('-step', type=float, default=0.02)
parser.add_argument('-termalizacion', type=int, default=500)
parser.add_argument('-plot', action='store_true')

params = parser.parse_args()

start = params.start
stop = params.stop
step = params.step

N = params.N
rho = params.rho

termalizacion = params.termalizacion

n_temps = int(abs((start - stop) / step))

md1 = md(N=N, T=start, rho=rho)
md1.n_pasos(termalizacion) # termalizacion

temps = np.linspace(start, stop, n_temps)
energia = np.zeros(n_temps, dtype=float)
presion = np.zeros(n_temps, dtype=float)
std_energia = np.zeros(n_temps, dtype=float)
std_presion = np.zeros(n_temps, dtype=float)

for i, T in enumerate(temps):
    print "%3d/%3d" % (i, n_temps)
    md1._rescaling(T)
    md1.n_pasos(50)
    e, p = md1.muestreo()
    energia[i] = e[0]
    std_energia[i] = e[1]
    presion[i] = p[0]
    std_presion = p[1]

if params.plot:
    plt.ion()
    fig, axs = plt.subplots(2)
    axs[0].errorbar(temps, energia, yerr=std_energia)
    axs[1].errorbar(1/temps, presion, yerr=std_presion)
