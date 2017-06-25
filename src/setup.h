#ifndef SETUP_H
#define SETUP_H


/*
 * Funcion: llenar
 * ---------------
 * Llena la caja con las N partiuclas en una configuracion de red simple.
 *
 * pos: (float *) Vector de dimension 3N para las posiciones.
 * N: (int) Cantidad de particulas
 * L: (float) Tamano de la caja
 *
 */
int llenar (float *pos, float N, float L);

/*
 * Funcion: velocidades
 * ---------------
 * Asigna velocidades a cada particula siguiendo la distribucion de
 * Maxwell-Boltzman para una dada temperatura.
 *
 * vel: (float *) Vector de dimension 3N para las velocidades.
 * N: (int) Cantidad de particulas
 * T: (float) Temperatura
 *
 */
int velocidades(float *vel, int N, float T);

/*
 * Funcion: avg_vel
 * ---------------
 * Calcula la velocidad promedio de todas las particulas para una
 * dada coordenada.
 *
 * vel: (float *) Vector de dimension 3N para las velocidades.
 * N: (int) Cantidad de particulas
 * coordenada: (int) Coordenada elegida donde x=0, y=1 y z=2.
 *
 */
float avg_vel(float *vel, int N, int coordenada);

#endif
