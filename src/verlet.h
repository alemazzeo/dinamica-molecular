#ifndef VERLET_H
#define VERLET_H

#define M      1.0
#define EPS    1.0
#define GAMMA  1.0

/*
 * Función: verlet
 * ---------------
 * Realiza los pasos del algoritmo de Verlet:
 *    Calcula la posición con la velocidad y la fuerza
 *    Calcula la fuerza con las posiciones
 *    Calcula la velocidad con la fuerza anterior y nueva
 *
 * pos: (float *) Vector de dimensión 3N para las posiciones.
 * vel: (float *) Vector de dimensión 3N para las velocidades.
 * fza: (float **) Puntero al vector de dimensión 3N para las fuerzas.
 * fza_aux: (float **) Puntero a un vector auxiliar de dimensión 3N.
 * n: (int) Cantidad de particulas
 * L: (float) Tamaño de la caja
 * h: (float) Tamaño del paso de Verlet
 * rc: (float) Distancia de corte
 *
 */
int verlet(float *pos, float *vel, float **fza, float **fza_aux, int n, float L, float h, float rc);

/*
 * Función: nueva_pos
 * ------------------
 * Calcula la nueva posición.
 *
 * pos: (float *) Vector de dimensión 3N para las posiciones.
 * vel: (float *) Vector de dimensión 3N para las velocidades.
 * fza: (float *) Puntero al vector de dimensión 3N para las fuerzas.
 * n: (int) Cantidad de particulas
 * h: (float) Tamaño del paso de Verlet
 *
 */
int nueva_pos(float *pos, float *vel, float *fza, int n, float h, float L);

/*
 * Función: nueva_vel
 * ------------------
 * Calcula la nueva posición.
 *
 * vel: (float *) Vector de dimensión 3N para las velocidades.
 * fza: (float *) Puntero al vector de dimensión 3N para las fuerza nueva.
 * fza0: (float *) Puntero al vector de dimensión 3N para las fuerza anterior.
 * n: (int) Cantidad de particulas
 * h: (float) Tamaño del paso de Verlet
 */
int nueva_vel(float *vel, float *fza, float *fza0, int n, float h);

/*
 * Función: energia
 * ----------------
 * Calcula la energia mediante el hamiltoniano.
 *
 * pos: (float *) Vector de dimensión 3N para las posiciones.
 * vel: (float *) Vector de dimensión 3N para las velocidades.
 * n: Cantidad de particulas
 */


int c_cont(float *pos, int N, float L);
int nueva_fza(float *pos, float *fza, int n, float rc);

#endif
