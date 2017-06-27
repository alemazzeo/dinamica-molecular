#ifndef LENNARDJONES_H
#define LENNARDJONES_H

/*
 * Funcion: lennardjones_lut
 * ---------------
 * Crea una Lookup-table para el potencial de Lennard-Jones. Lo trunca en r=rc,
 * lo mueve para arriba y suaviza la curva cerca de rc.
 *
 * LJ_LUT: (float *) Vector de dimension k con el potencial de Lennard-Jones.
 * k: (int) Tamano de la Lookup-table
 * rc: (float) Distancia de corte para el potencial
 *
 */
int lennardjones_lut(float *LJ_LUT, int k, float rc);

/*
 * Funcion: lennardjones
 * ---------------
 * Evalua analiticamente el potencial de Lennard-Jones.
 *
 * r: (float) Distancia entre dos particulas.
 *
 */
float lennardjones(float r);

/*
 * Funcion: spline
 * ---------------
 * Introduce un spline en el potencial para suavizar la derivada cerca de rc
 *
 * LJ_LUT: (float *) Vector de dimension k con el potencial de Lennard-Jones.
 * k: (int) Tamano de la Lookup-table
 * vec_pos: (float *) Vector de dimension k con los valores de la distancia.
 * rc: (float) Distancia de corte para el potencial
 *
 */
int spline(float *LJ_LUT, int k, float *vec_pos, float rc);

/*
 * Funcion: t
 * ---------------
 * Funcion auxiliar para facilitar el calculo del spline.
 *
 * x: (float) Distancia actual.
 * x1: (float) Posicion donde empieza el spline
 * x2: (float) Posicion donde termina el spline
 *
 */
float t(float x, float x1, float x2);

/*
 * Funcion: fuerza_lut
 * ---------------
 * Crea una Lookup-table de la fuerza haciendo la derivada de Lennard-Jones
 * usando la LUT ya creada y usando diferencia finita.
 *
 * FZA_LUT: (float *) Lookup-table de la fuerza de dimension k.
 * LJ_LUT: (float *) Vector de dimension k con el potencial de Lennard-Jones.
 * k: (int) Tamano de la Lookup-table
 * rc: (float) Distancia de corte para el potencial
 *
 */
int fuerza_lut(float *FZA_LUT, float *LJ_LUT, int k, float rc);

int indice_lut(int g, float r);
float lookup(float *LUT, int g, float r);

#endif
