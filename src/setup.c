#include <stdlib.h>
#include <stdio.h>
#include <time.h>
#include <math.h>

#include "setup.h"

int llenar (float *pos, float N, float L){
    int n,i,j,k;
    float p,a;
    p = pow(N, (double)1/3); //raiz cubica del numero de particulas
    n = ceil(p);
    printf("%d\n", n);
    a = L/n; // Distancia entre particulas

    //Acomodo las particulas. El for en i es para la coordenada x, el de j para y y el de k para z.
    for (k=0;k<n;k++){
        for (j=0;j<n;j++){
            for (i=0;i<n;i++){

                //Chequea si me pase de las particulas que tengo disponibles
                if(k*n*n + j*n + i < N) {
                    pos [3*i + (3*n)*j + (3*n*n)*k] = (a/2) + i*a;
                    pos [1 + 3*i + (3*n)*j + (3*n*n)*k] = (a/2) + j*a;
                    pos [2 + 3*i + (3*n)*j + (3*n*n)*k] = (a/2) + k*a;
                }
            }
        }
    }

    return 0;

}


int velocidades(float *vel, int N, float T){
    float sigma = sqrt(T);
    float vels;
    int k = 20;
    int i,j;

    // Genero distribucion de velocidades
    for(i=0; i<3*N; i++){
        vels = 0;
        for(j=0; j<k; j++){
            vels += ((float)rand()/RAND_MAX - 0.5)*2*sigma*sqrt(3*k);
        }
        vels /= k;
        vel[i] = vels;
    }

    //Resto velocidad promedio
    for(i=0; i<3; i++){
        float promedio = avg_vel(vel, N, i);
        for(j=0; j<3*N; j=j+3){
            vel[j+i] -= promedio;
        }
    }

    return 0;
}

float avg_vel(float *vel, int N, int coordenada){
    float promedio = 0;
    for(int i=0; i<3*N; i=i+3){
        promedio += vel[i+coordenada];
    }
    return promedio/N;
}
