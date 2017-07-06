#include <stdlib.h>
#include <stdio.h>
#include <time.h>
#include <math.h>

#include "setup.h"
#include "verlet.h"
#include "energia.h"
#include "lennardjones.h"

int main(int argc, char **argv) {
    int N = 512; // Nr de particulas
    float rho = 0.6; //Densidad
    float L = pow(N/rho, 1.0/3); // Longitud de la caja
    float rc = 0.5*L; // Maxima influencia del potencial
    float h = 0.001; // Intervalo de tiempo entre simulaciones
    int niter = 5000; // Nro de veces que se deja evolucionar
    float T = 0.5; // Temperatura
    int g = 1000; // Precision de LUT (1/g)
    int i; // Indices para loopear
    // int Q = 400; // presicion para la funcion g(r)

    // NO CAMBIAR ESTO:
    int long_lut = floor(g*rc); // Tamano de la Lookup-table

    // Aloja memoria para los vectores
    float *LJ_LUT = (float *)malloc(long_lut*sizeof(float));
    float *FZA_LUT = (float *)malloc(long_lut*sizeof(float));
    float *pos = (float *)malloc(3*N*sizeof(float));
    float *vel = (float *)malloc(3*N*sizeof(float));
    float *fza = (float *)malloc(3*N*sizeof(float));
    float *lambda = (float *)malloc(niter*sizeof(float));
    // float *distrad = (float *)malloc(Q*sizeof(float));

    srand(time(NULL));

    // Creo las LUT para el potencial y para la fuerza
    lennardjones_lut(LJ_LUT, long_lut, rc);
    fuerza_lut(FZA_LUT, LJ_LUT, long_lut, rc);

    // Inicializa la caja con las N partiuclas
    llenar(pos, N, L);
    velocidades(vel, N, T);


    for(i=0;i<niter;i++){
        primer_paso(pos, vel, fza, N, h);
        // nueva_fza(pos, fza, N, L, rc, FZA_LUT, g);
        nueva_fza_exacto(pos, fza, N, L, rc);
        ultimo_paso(vel, fza, N, h);
        c_cont(pos, N, L);
    }


    free(LJ_LUT);
    free(FZA_LUT);
    free(pos);
    free(vel);
    free(fza);
    free(lambda);

}
