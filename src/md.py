# file: md.py

import ctypes as C

CLIB = C.CDLL('../bin/libmd.so')

# Abreviaturas de punteros
flp = C.POINTER(C.c_float)
flpp = C.POINTER(C.POINTER(C.c_float))

# Argumentos de las funciones
CLIB.verlet.argtypes = [flp, flp, flpp, flpp, C.c_int,
                        C.c_float, C.c_float, C.c_float]
CLIB.nueva_pos.argtypes = [flp, flp, flp, C.c_int, C.c_float, C.c_float]
CLIB.nueva_vel.argtypes = [flp, flp, flp, C.c_int, C.c_float]
CLIB.nueva_fza.argtypes = [flp, flp, C.c_int, C.c_float]
CLIB.llenar.argtypes = [flp, C.c_int, C.c_float]
CLIB.velocidades.argtypes = [flp, C.c_int, C.c_float]
CLIB.avg_vel.argtypes = [flp, C.c_int, C.c_int]
CLIB.energia.argtypes = [flp, flp, C.c_int]
CLIB.velocidad2.argtypes = [flp]
CLIB.distancia2.argtypes = [flp, flp]
CLIB.potencial.argtypes = [flp, flp]
CLIB.lambda_verlet.argtypes = [flp, C.c_float, C.c_float]

# Funciones que no retornan un entero
CLIB.energia.restype = C.c_float
CLIB.velocidad2.restype = C.c_float
CLIB.distancia2.restype = C.c_float
CLIB.potencial.restype = C.c_float
CLIB.lambda_verlet.restype = C.c_float
