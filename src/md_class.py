#!/usr/bin/env python
# -*- coding: utf-8 -*-
# file: md_class.py

import ctypes as C
import numpy as np

import matplotlib.pyplot as plt
import matplotlib.animation as animation
from mpl_toolkits.mplot3d import Axes3D

import os

CLIB = C.CDLL('../bin/libmd.so')

# Abreviaturas
flp = C.POINTER(C.c_float)

# Funciones de C
CLIB.primer_paso.argtypes = [flp, flp, flp, C.c_int, C.c_float]
CLIB.nueva_fza.argtypes = [flp, flp, C.c_int, C.c_float, C.c_float,
                           flp, C.c_int]
CLIB.nueva_fza_exacto.argtypes = [flp, flp, C.c_int, C.c_float, C.c_float]
CLIB.ultimo_paso.argtypes = [flp, flp, C.c_int, C.c_float]
CLIB.c_cont.argtypes = [flp, C.c_int, C.c_float]
CLIB.lennardjones_lut.argtypes = [flp, C.c_int, C.c_float]
CLIB.fuerza_lut.argtypes = [flp, flp, C.c_int, C.c_float]

CLIB.cinetica.argtypes = [flp, C.c_int]
CLIB.potencial.argtypes = [flp, C.c_int, C.c_float, flp, C.c_int, C.c_float]
CLIB.potencial_exacto.argtypes = [flp, C.c_int, C.c_float, C.c_float]

CLIB.distrib_radial.argtypes = [flp, flp, C.c_float, C.c_float, C.c_float, C.c_float]

# Return types
CLIB.cinetica.restype = C.c_float
CLIB.potencial.restype = C.c_float
CLIB.nueva_fza.restype = C.c_float


class md():

<<<<<<< HEAD
    def __init__(self, N=512, rho=0.8442, h=0.001, T=2, lut_precision=10000, Q=400):
=======
    def __init__(self, N=512, rho=0.8442, h=0.001, T=2.0, lut_precision=10000):
>>>>>>> 4d2fce855c4cf68cddf14ba601be7facdfcd53d5

        # Almacena los parámetros recibidos
        self._N = N
        self._rho = rho
        self._h = h
        self._T = T
        self._g = lut_precision
        self._Q = Q

        # Calcula otros parámetros internos
        self._L = (N / rho)**(1.0 / 3.0)
        self._rc = 0.5 * self._L
        self._long_lut = int(lut_precision * self._rc)

        # Cantidad de pasos realizados

        self._cant_pasos = 0

        # Prepara las posiciones y velocidades con sus punteros
        self._pos = self.llenar_pos()
        self._vel = self.llenar_vel()
        self._p_pos = self._pos.ctypes.data_as(flp)
        self._p_vel = self._vel.ctypes.data_as(flp)

        # Prepara la memoria para almacenar la fuerza con su puntero
        self._fza = np.zeros(3 * N, dtype=C.c_float)
        self._p_fza = self._fza.ctypes.data_as(flp)

        # Prepara la memoria para almacenar la funcion de distribucion radial y su puntero
        self._distrad = np.zeros(self._Q, dtype=C.c_float)
        self._p_distrad = self._distrad.ctypes.data_as(flp)

        # Calcula la LUT para el potencial de Lennard-Jones
        self._LJ_LUT = np.zeros(self._long_lut, dtype=C.c_float)
        self._p_LJ_LUT = self._LJ_LUT.ctypes.data_as(flp)
        CLIB.lennardjones_lut(self._p_LJ_LUT, self._long_lut, self._rc)

        # Calcula la LUT para las fuerzas
        self._FZA_LUT = np.zeros(self._long_lut, dtype=C.c_float)
        self._p_FZA_LUT = self._FZA_LUT.ctypes.data_as(flp)
        CLIB.fuerza_lut(self._p_FZA_LUT, self._p_LJ_LUT,
                        self._long_lut, self._rc)

        # Modo configurado para calculos
        self._exacto = False

        # Tiempo de termalizacion
        self._t_termalizacion = 1000

        # Presion de exceso
        self._p_exceso = 0.0

    @property
    def N(self):
        return self._N

    @property
    def rho(self):
        return self._rho

    @property
    def h(self):
        return self._h

    @property
    def T(self):
        return self._T

    @property
    def lut_precision(self):
        return self._g

    @property
    def rc(self):
        return self._rc

    @property
    def L(self):
        return self._L

    @property
    def cant_pasos(self):
        return self._cant_pasos

    @classmethod
    def transforma_1D(cls, x, y, z):
        '''
        Recibe las coordenadas X, Y, Z y las convierte al 3N de C
        '''
        assert x.size == y.size == z.size
        return np.array([x, y, z]).T.reshape(x.size * 3)

    @classmethod
    def transforma_xyz(cls, vector):
        '''
        Recibe el vector 3N mezclado de C y lo convierte en X, Y, Z
        '''
        assert vector.ndim == 1
        N = vector.size
        assert N % 3 == 0
        aux = np.reshape(vector, (N // 3, 3)).T
        return aux[0], aux[1], aux[2]

    def llenar_pos(self):
        '''
        Setup para las posiciones y velocidades iniciales
        '''
        N = self._N
        L = self._L

        # Toma la parte entera de la raiz cubica de N
        lado = int(N**(1.0 / 3.0))
        # Calcula el numero de lugares generados
        particulas = lado ** 3
        # Si las particulas no entran en la caja de lado M aumenta su tamano
        if particulas < N:
            lado += 1

        # Calcula la mitad de la separacion entre particulas
        s = L / lado / 2

        # Genera un vector para la grilla
        aux = np.linspace(s, L - s, lado, dtype=float)
        # Genera las posiciones con la grilla en 3D
        x, y, z = np.meshgrid(aux, aux, aux, indexing='ij')
        # Transforma las coordenadas xyz al vector 3N que usan las func. de C
        pos = self.transforma_1D(x, y, z)

        # Devuelve la cantidad de posiciones pedidas como vector de c_floats
        return pos[0:3 * N].astype(C.c_float)

    def llenar_vel(self):
        '''
        Setup para las velocidades
        '''
        N = self._N
        T = self._T

        # Genera una distribucion normal de velocidades
        vel = np.random.normal(loc=0, scale=T**0.5, size=3 * N)
        # Resta el promedio para evitar que Pt sea igual a cero
        vel -= np.mean(vel)

        # Devuelve las velocidades como vector de c_floats
        return vel.astype(C.c_float)

    def ver_pos(self, plot_vel=False, ax=None, size=30):
        '''
        Grafica las posiciones y velocidades (opcional)
        '''
        if ax is None:
            plt.ion()
            fig, ax = plt.subplots(subplot_kw=dict(projection='3d'))

        x, y, z = self.transforma_xyz(self._pos)
        scatter = ax.scatter(x, y, z, s=size, alpha=0.7)

        ax.set_xlim([0, self._L])
        ax.set_ylim([0, self._L])
        ax.set_zlim([0, self._L])

        if plot_vel:
            vx, vy, vz = self.transforma_xyz(self._vel)
            quiver = ax.quiver(x, y, z, vx, vy, vz)
        else:
            quiver = None

        return fig, ax, scatter, quiver

    def paso(self):
        """
        Da un paso en la simulacion usando las LUT o exacto
        """
        # Llama a la función que da medio paso de velocidad y uno de posición
        CLIB.primer_paso(self._p_pos, self._p_vel,
                         self._p_fza, self._N, self._h)

        # Calcula la nueva fuerza en el modo configurado
        if self._exacto:
            CLIB.nueva_fza_exacto(self._p_pos, self._p_fza,
                                  self._N, self._L, self._rc)
        else:
            # Al calcular la nueva fuerza actualiza la presión de exceso
            self._p_exceso = CLIB.nueva_fza(self._p_pos, self._p_fza, self._N,
                                            self._L, self._rc, self._p_FZA_LUT,
                                            self._g)

        # Da el ultimo medio paso de velocidad
        CLIB.ultimo_paso(self._p_vel, self._p_fza, self._N, self._h)

        # Aplica condiciones de contorno
        CLIB.c_cont(self._p_pos, self._N, self._L)

        self._cant_pasos += 1

    def n_pasos(self, n=5000):
        '''
        Realiza sucesivos pasos sin almacenar información
        '''
        for i in range(n):
            self.paso()

    def calc_energia_cinetica(self):
        '''
        Calcula la suma de la energia cinética.
        '''
        ecin = CLIB.cinetica(self._p_vel, self._N)
        return ecin

    def calc_energia_potencial(self):
        '''
        Calcula la suma de la energia potencial en el modo configurado.
        '''
        epot = CLIB.potencial(self._p_pos, self._N, self._L,
                              self._p_LJ_LUT, self._g, self._rc)

        if self._exacto:
            epot = CLIB.potencial(self._pos, self._N, self._L, self._rc)

        return epot

    def calc_energia(self):
        '''
        Calcula la suma de la energia cinética y potencial.
        '''
        return self.calc_energia_cinetica() + self.calc_energia_potencial()

    def calc_presion(self):
        '''
        Calcula el observable P / (rho*T) - 1
        '''
        return self._p_exceso / 3

    def rescaling(self, T):
        '''
        Realiza el rescaling de velocidades
        '''
        self._vel *= np.sqrt(T / self._T)

    def nueva_T(self, T, dT=0.01):
        '''
        Realiza los rescaling y n_pasoses necesarios para llegar a T
        '''

        # Corrige el signo de dT si es necesario
        if T < self.T:
            dT = -abs(dT)
        else:
            dT = abs(dT)

        while abs(T - self._T) > 0:

            # Corrige dT si es mayor a la diferencia de temperaturas
            if dT > T - self._T:
                dT = T - self._T

            self.rescaling(self._T + dT)
            self.n_pasos()

    def llenar_vectores(self, m, plot=False):
        '''
        Promedia m valores de energia y presion
        '''
        energia = np.zeros(m, dtype=float)
        presion = np.zeros(m, dtype=float)

        for i in range(m):
            self.paso()
            energia[i] = self.calc_energia()
            presion[i] = self.calc_presion()

        if plot:
            fig, ax = plt.subplots(2)
            ax[0].plot(energia)
            ax[1].plot(presion)
            plt.show()

        return energia, presion

    def prueba_piloto(self, precision, m_piloto=20, dc=100):
        '''
        Estima para la precision deseada la cantidad de promedios a considerar
        '''
        x = np.zeros(m_piloto, dtype=float)

        for i in range(m_piloto):
            energia, presion = self.llenar_vectores(dc)
            x[i] = np.mean(energia)

        var_piloto = np.var(x)

        return int(m_piloto * var_piloto / (precision**2)), var_piloto**0.5

    def tomar_muestra(self, m=50, dc=100):
        '''
        Toma n muestras promediando 'm' grupos de 'dc' pasos
        '''
        energia = np.zeros(m, dtype=float)
        presion = np.zeros(m, dtype=float)

        for i in range(m):
            e, p = self.llenar_vectores(dc)
            energia[i] = np.mean(e)
            presion[i] = np.mean(p)

        avg_energia = np.average(energia)
        std_energia = np.std(energia)
        avg_presion = np.average(presion)
        std_presion = np.std(presion)

        return [avg_energia, std_energia], [avg_presion, std_presion]

    def dist_radial(self, n=100, m=100):
        '''
        Calcula la  funcion de distribucion radial promediando los resultados n pasos totales,
        donde entre cada paso se realizan m pasos de Verlet
        '''

        for i in range(n):
            CLIB.distrib_radial(self._p_distrad, self._p_pos, self._N, self._L, self._rho, self._Q)
            self.n_pasos(m)

        self._distrad = [i/(n * 0.5 * self._N) for i in self._distrad]
        return self._distrad

    def save(self, nombre='temp.npy', ruta='../datos/'):
        '''
        Almacena el estado actual de la simulación
        '''
        os.makedirs(ruta, exist_ok=True)

        params = [self.N,
                  self.rho,
                  self.h,
                  self.T,
                  self.lut_precision,
                  self.cant_pasos]

        particulas = [self._pos,
                      self._vel]

        np.save(ruta + nombre, [params, particulas])

    @classmethod
    def load(cls, nombre='temp.npy', ruta='../datos/'):
        '''
        Recupera el estado de una simulación almacenada
        '''
        params, particulas = np.load(ruta + nombre)

        N, rho, h, T, lut_precision, cant_pasos = params

        md_load = cls(N, rho, h, T, lut_precision)
        md_load._cant_pasos = cant_pasos

        md_load._pos = np.asarray(particulas[0], dtype=C.c_float)
        md_load._vel = np.asarray(particulas[1], dtype=C.c_float)

        md_load._p_pos = md_load._pos.ctypes.data_as(flp)
        md_load._p_vel = md_load._vel.ctypes.data_as(flp)

        md_load._p_exceso = CLIB.nueva_fza(md_load._p_pos, md_load._p_fza,
                                           md_load._N, md_load._L,
                                           md_load._rc, md_load._p_FZA_LUT,
                                           md_load._g)

        return md_load
