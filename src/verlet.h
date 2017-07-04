#ifndef VERLET_H
#define VERLET_H

#define M      1.0
#define EPS    1.0
#define GAMMA  1.0

int primer_paso(float *pos, float *vel, float *fza, int N, float h);
/*
 * Función: primer_paso
 * ---------------
 * Realiza medio paso de verlet correspondiente a
 *   evolucionar medio paso la velocidad
 *     v(t+h/2) = v(t) + a * h/2
 *   evolucionar un paso entero la posición
 *     x(t+h) = x(t) + v(t+h/2) * h
 *
 * pos: (float *) Vector de dimensión 3N para las posiciones.
 * vel: (float *) Vector de dimensión 3N para las velocidades.
 * fza: (float **) Puntero al vector de dimensión 3N para las fuerzas.
 * N: (int) Cantidad de particulas
 * h: (float) Tamaño del paso de Verlet
 *
 */

float nueva_fza(float *pos, float *fza, int n, float L, float rc, float *FZA_LUT, int g);
/*
 * Función: nueva_fza
 * ------------------
 * Calcula la nueva fuerza usando la Lookup-table.
 *
 * pos: (float *) Vector de dimensión 3N para las posiciones.
 * fza: (float *) Vector de dimensión 3N para las fuerzas.
 * n: (int) Cantidad de particulas
 * L: (float) Tamano de la caja
 * rc: (float) Distancia de corte para el potencial
 * FZA_LUT: (float *) Lookup-table de la fuerza
 * g: (int) Precision de la Lookup-table
 *
 * return: (float) Presion de exceso
 */

int nueva_fza_exacto(float *pos, float *fza, int n, float L, float rc);
/*
 * Función: nueva_fza_exacto
 * ------------------
 * Calcula la nueva fuerza de forma exacta.
 *
 * pos: (float *) Vector de dimensión 3N para las posiciones.
 * fza: (float *) Vector de dimensión 3N para las fuerzas.
 * n: (int) Cantidad de particulas
 * L: (float) Tamano de la caja
 * rc: (float) Distancia de corte para el potencial
 */

int ultimo_paso(float *vel, float *fza, int N, float h);
/*
 * Función: ultimo_paso
 * ---------------
 * Realiza medio paso de verlet restante para la velocidad
 *   v(t+h/2) = v(t) + a * h/2
 *
 * vel: (float *) Vector de dimensión 3N para las velocidades.
 * fza: (float **) Puntero al vector de dimensión 3N para las fuerzas.
 * N: (int) Cantidad de particulas
 * h: (float) Tamaño del paso de Verlet
 *
 */

int c_cont(float *pos, int N, float L);
/*
 * Función: c_cont
 * ----------------
 * Aplica las condiciones de contorno periodicas a todas las partículas.
 *
 * pos: (float *) Vector de dimensión 3N para las posiciones.
 * N: (int) Cantidad de particulas
 * L: (float) Tamano de la caja
 *
 */

#endif
