#include <stdlib.h>
#include <stdio.h>
#include <time.h>
#include <math.h>

#include "setup.h"
#include "verlet.h"
#include "energia.h"

int main(int argc, char **argv) {
    int N = 8; // Nr de particulas
    float rho = 0.8442; //Densidad
    float L = N/rho; // Longitud de la caja (el doble de rc)
    float rc = 0.5*L; // Maxima influencia del potencial
    float h = 0.001; // Intervalo de tiempo entre simulaciones
    int niter = 2000; // Nro de veces que se deja evolucionar
    float T = 1.5; // Temperatura 0.728
    int i; // Indices para loopear

    // Aloja memoria para los vectores
    float *pos = (float *)malloc(3*N*sizeof(float));
    float *vel = (float *)malloc(3*N*sizeof(float));
    float *fza = (float *)malloc(3*N*sizeof(float));
    float *fza_aux = (float *)malloc(3*N*sizeof(float));
    float *lambda = (float *)malloc(niter*sizeof(float));

    // Inicializa la caja con las N partiuclas
    llenar(pos, N, L);
    velocidades(vel, N, T);

    for(i=0;i<niter;i++){
        verlet(pos, vel, &fza, &fza_aux, N, L, h, rc);
        if(i % 10 == 0) {
            for(int k = 0; k < N; k ++) {
                printf("%f\t%f\t%f\n", pos[3*k],pos[3*k + 1],pos[3*k + 2]);
            }
        }
        // printf("%f\t%f\t%f\n", pos[6],pos[7],pos[8]);
        lambda[i] = lambda_verlet (pos, N, L);
    }

    // printf("\n\nlambda values\n\n");
    //
    // for (i=0;i<niter;i++) {
    //     printf("%f\n", lambda[i]);
    // }

    free(pos);
    free(vel);
    free(fza);
    free(fza_aux);
    free(lambda);

}
