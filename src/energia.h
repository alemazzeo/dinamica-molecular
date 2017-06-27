#ifndef ENERGIA_H
#define ENERGIA_H

#define M      1.0
#define EPS    1.0
#define GAMMA  1.0

/*
 * Función: energia
 * ----------------
 * Calcula la energia mediante el hamiltoniano.
 *
 * pos: (float *) Vector de dimensión 3N para las posiciones.
 * vel: (float *) Vector de dimensión 3N para las velocidades.
 * n: Cantidad de particulas
 */
float energia(float *pos, float *vel, int n, float *LJ_LUT, int g, float rc);

/*
 * Función: velocidad2
 * -------------------
 * Calcula la velocidad al cuadrado.
 *
 * vel: (float *) Vector de dimensión 3 para la velocidad.
 *
 * return: (float) Módulo cuadrado de la velocidad.
 */
float velocidad2(float *vel);

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
float distancia2(float *pos_i, float *pos_j);

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
float potencial(float *pos_i, float *pos_j);
float lambda_verlet (float *pos, float N, float L);
float Hboltzmann (float *vel, float N, float T);
float funcionH (float vel, float T);

#endif
