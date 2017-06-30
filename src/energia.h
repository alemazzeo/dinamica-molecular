#ifndef ENERGIA_H
#define ENERGIA_H


float energia(float *pos, float *vel, int n, float *LJ_LUT, int g, float rc);
/*
 * Función: energia
 * ----------------
 * Calcula la energia mediante el hamiltoniano.
 *
 * pos: (float *) Vector de dimensión 3N para las posiciones.
 * vel: (float *) Vector de dimensión 3N para las velocidades.
 * n: Cantidad de particulas
 */


float velocidad2(float *vel);
/*
 * Función: velocidad2
 * -------------------
 * Calcula la velocidad al cuadrado.
 *
 * vel: (float *) Vector de dimensión 3 para la velocidad.
 *
 * return: (float) Módulo cuadrado de la velocidad.
 */


float distancia2(float *pos_i, float *pos_j);
/*
 * Función: distancia2
 * -------------------
 * Calcula la distancia al cuadrado.
 *
 * pos_i: (float *) Vector de dimensión 3 para la posición de la partícula i.
 * pos_j: (float *) Vector de dimensión 3 para la posicion de la partícula j.
 *
 * return: (float) Módulo de la distancia al cuadrado
 */


float potencial(float *pos_i, float *pos_j);
/*
 * Función: potencial
 * ------------------
 * Calcula la interacción de dos particulas i, j.
 *
 * pos_i: (float *) Vector de dimensión 3 para la posición de la partícula i.
 * pos_j: (float *) Vector de dimensión 3 para la posicion de la partícula j.
 *
 * return: (float) Módulo de la distancia al cuadrado
 */


float lambda_verlet (float *pos, float N, float L);
float Hboltzmann (float *vel, float N, float T);
float funcionH (float vel, float T);

#endif
