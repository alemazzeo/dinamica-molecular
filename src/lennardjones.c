/* Crea una Lookup-table para el potencial de Lennard-Jones. Esta ya tiene la
forma truncada, con el shift para que coincida V(rc)=0 y con la suaviazacion
de la derivada alrededor de rc. */

#include "stdio.h"
#include "stdlib.h"
#include "math.h"

#include "lennardjones.h"


int lennardjones_lut(float *LJ_LUT, int k, float rc){
    // Genera un vector con las posiciones reales a evaluar
    float *vec_pos = malloc(k*sizeof(float));

    for(int i=0;i<k;i++){
        vec_pos[i] = (i+1) * (rc/k);
    }

    // LUT de Lennard-Jones con el shift
    for(int i=0; i<k; i++){
        LJ_LUT[i] = lennardjones(vec_pos[i]) - lennardjones(rc);
    }

    // Crea la spline alrededor de rc
    spline(LJ_LUT, k, vec_pos, rc);

    free(vec_pos);

    return 0;
}


float lennardjones(float r){
    /* Evalua el potencial de Lennard-Jones de forma analitica. */
    return 4*(pow(r, -12) - pow(r, -6));
}


int spline(float *LJ_LUT, int k, float *vec_pos, float rc){
    /* Introduce el spline para suavizar la curva */
    int p = k/10; // Pasos anteriores a rc donde empieza el spline
    float x1 = vec_pos[k-p]; // posicion donde empieza el spline
    float x2 = rc; // posicion donde termina el spline
    float y1 = LJ_LUT[k-p]; // valor en x1
    float k1 = (LJ_LUT[k-p+1]-LJ_LUT[k-p])/(vec_pos[k-p+1]-vec_pos[k-p]); // Derivada en x1
    float a = k1*(x2-x1) + y1;
    float b = -y1;

    for(int i=k-p; i<k; i++){
        LJ_LUT[i] = (1-t(vec_pos[i], x1, x2))*y1 +
                t(vec_pos[i], x1, x2)*(1-t(vec_pos[i], x1, x2))*
                (a*(1-t(vec_pos[i], x1, x2))+b*t(vec_pos[i], x1, x2));
    }

    return 0;
}


float t(float x, float x1, float x2){
    // Funcion auxiliar para facilitar el calculo del spline
    return (x-x1)/(x2-x1);
}


int fuerza_lut(float *FZA_LUT, float *LJ_LUT, int k, float rc){
    float delta_r = rc/k;
    for(int i=0; i<k; i++){
        // Caso aparte para el ultimo elemento de la fuerza
        if(i == k-1){
            FZA_LUT[i] = LJ_LUT[i]/delta_r;
        }
        // Fuerza mediante diferencia finita.
        else{
            FZA_LUT[i] = -(LJ_LUT[i+1]-LJ_LUT[i])/delta_r;
        }
    }

    return 0;
}


int indice_lut(int g, float r){
    // Devuelve el indice a donde mirar en la LUT
    return floor(r*g);
}


float lookup(float *LUT, int g, float r){
    // Calcula el valor en una LUT segun la distancia r
    int indice = indice_lut(g, r);

    // Version simple, agarra el valor de la izquierda
    return LUT[indice];
}
