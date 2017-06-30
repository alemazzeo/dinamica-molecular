# file: md.py

import ctypes as C
import numpy as np

import matplotlib.pyplot as plt
import matplotlib.animation as animation
from mpl_toolkits.mplot3d import Axes3D

CLIB = C.CDLL('../bin/libmd.so')

# Abreviaturas
flp = C.POINTER(C.c_float)

# Funciones de C
CLIB.primer_paso.argtypes = [flp, flp, flp, C.c_int, C.c_float]
CLIB.nueva_fza.argtypes = [flp, flp, C.c_int, C.c_float, C.c_float,
                           flp, C.c_int]
CLIB.ultimo_paso.argtypes = [flp, flp, C.c_int, C.c_float]
CLIB.c_cont.argtypes = [flp, C.c_int, C.c_float]
CLIB.lennardjones_lut.argtypes = [flp, C.c_int, C.c_float]
CLIB.fuerza_lut.argtypes = [flp, flp, C.c_int, C.c_float]
CLIB.energia.argtypes = [flp, flp, C.c_int, flp, C.c_int, C.c_float]

CLIB.energia.restype = C.c_float

##############################
# Paso completo de MD
##############################


def paso(pos, vel, fza, N, L, h, rc, FZA_LUT, g):
    """ Da un paso en la simulacion. """
    p_pos = pos.ctypes.data_as(flp)
    p_vel = vel.ctypes.data_as(flp)
    p_fza = fza.ctypes.data_as(flp)
    p_FZA_LUT = FZA_LUT.ctypes.data_as(flp)

    CLIB.primer_paso(p_pos, p_vel, p_fza, N, h)
    CLIB.nueva_fza(p_pos, p_fza, N, L, rc, p_FZA_LUT, g)
    CLIB.ultimo_paso(p_vel, p_fza, N, h)
    CLIB.c_cont(p_pos, N, L)

def calc_energia(pos, vel, N, lj_lut, g, rc):
    p_pos = pos.ctypes.data_as(flp)
    p_vel = vel.ctypes.data_as(flp)
    p_lj_lut = LJ_LUT.ctypes.data_as(flp)
    # print pos[0], pos[3], pos[6]
    # print CLIB.energia(p_pos, p_vel, N, p_lj_lut, g, rc)

    return CLIB.energia(p_pos, p_vel, N, p_lj_lut, g, rc)

##############################
# Funciones auxiliares
##############################

def transforma_1D(x, y, z):
    ''' Recibe las coordenadas X, Y, Z y las convierte al 3N de C. '''
    assert x.size == y.size == z.size
    return np.array([x, y, z]).T.reshape(x.size * 3)


def transforma_xyz(vector):
    ''' Recibe el vector 3N mezclado y lo convierte en X, Y, Z. '''
    assert vector.ndim == 1
    N = vector.size
    assert N % 3 == 0
    aux = np.reshape(vector, (N // 3, 3)).T
    return aux[0], aux[1], aux[2]


def llenar_pos(N, L):
    ''' Setup para las posiciones y velocidades iniciales. '''

    # Toma la parte entera de la raiz cubica de N
    lado = int(N**(1.0 / 3.0))
    # Calcula el numero de lugares generados
    particulas = lado ** 3
    # Si las particulas no entran en la caja de lado M aumenta su tamano
    if particulas < N:
        lado += 1

    # Calcula la mitad de la separacion entre particulas
    s = L / lado / 2

    # Genera un vector
    aux = np.linspace(s, L - s, lado, dtype=float)
    x, y, z = np.meshgrid(aux, aux, aux, indexing='ij')
    pos = transforma_1D(x, y, z)

    return pos[0:3 * N].astype(C.c_float)


def llenar_vel(N, T):
    ''' Setup para las velocidades '''
    vel = np.random.normal(loc=0, scale=T**0.5, size=3 * N)
    vel -= np.mean(vel)

    return vel.astype(C.c_float)


def ver_pos(pos, vel=None, L=None, ax=None):
    if ax is None:
        plt.ion()
        fig, ax = plt.subplots(subplot_kw=dict(projection='3d'))

    if L is not None:
        ax.set_xlim([0, L])
        ax.set_ylim([0, L])
        ax.set_zlim([0, L])

    x, y, z = transforma_xyz(pos)
    scatter = ax.scatter(x, y, z)

    if vel is not None:
        vx, vy, vz = transforma_xyz(vel)
        quiver = ax.quiver(x, y, z, vx, vy, vz)
    else:
        quiver = None

    return fig, ax, scatter, quiver

##############################
# Configuracion
##############################


# Parametros externos
N = 512
rho = 0.8442
h = 0.001
T = 2.0
g = 1000
niter = 5000

# Parametros internos
L = (N / rho)**(1.0 / 3.0)
rc = 0.5 * L
long_lut = int(g*rc)

# Configuracion inicial de posiciones y velocidades
pos = llenar_pos(N, L)
vel = llenar_vel(N, T)

# Memoria para las fuerzas
fza = np.zeros(3 * N, dtype=C.c_float)

# Memoria para las LUT
LJ_LUT = np.zeros(int(g * rc), dtype=C.c_float)
FZA_LUT = np.zeros(int(g * rc), dtype=C.c_float)

print LJ_LUT

# Memoria para la energia
energia = np.zeros(niter, dtype=float)

# Llenar las LUT
p_lj_lut = LJ_LUT.ctypes.data_as(flp)
p_fza_lut = FZA_LUT.ctypes.data_as(flp)
CLIB.lennardjones_lut(p_lj_lut, long_lut, rc)
CLIB.fuerza_lut(p_fza_lut, p_lj_lut, long_lut, rc)

print LJ_LUT


##############################
# Animacion provisoria
##############################

for i in range(niter):
    paso(pos, vel, fza, N, L, h, rc, FZA_LUT, g)
    energia[i] = calc_energia(pos, vel, N, LJ_LUT, g, rc)

fig, ax = plt.subplots(1)
ax.plot(energia, '.')
plt.show()
