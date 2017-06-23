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
 *
 */
int verlet(float *pos, float *vel, float **fza, float **fza_aux, int n, float L, float h);

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
int nueva_pos(float *pos, float *vel, float *fza, int n, float h);

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
float energia(float *pos, float *vel, int n);

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

#endif
