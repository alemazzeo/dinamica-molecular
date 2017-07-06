#ifndef ENERGIA_H
#define ENERGIA_H

float cinetica(float *vel, int N);
/*
* Función: cinetica
* ----------------
* Calcula la energia cinetica.
*
* pos: (float *) Vector de dimensión 3N para las posiciones.
* n: Cantidad de particulas
*/

float potencial(float *pos, int N, float L, float *LJ_LUT, int g, float rc);
/*
* Función: potencial
* ----------------
* Calcula la energia potencial mediante el potencial de Lennard-Jones.
*
* pos: (float *) Vector de dimensión 3N para las posiciones.
* N: Cantidad de particulas
* LJ_LUT: (float *) Lookup-table del potencial de Lennard-Jones
* g: (int) Precision de la Lookup-table
* rc: Distancia de corte para el potencial
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


float potencial_exacto(float *pos, int N, float L, float rc);
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

float distrib_radial(float *distrad, float *pos, float n, float L, float rho, float Q);

float build_rij(float *arr_rij, float *pos, float N);

#endif
