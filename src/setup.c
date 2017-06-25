#include <stdlib.h>
#include <stdio.h>
#include <time.h>
#include <math.h>

#include "setup.h"

int llenar (float *pos, float N, float L){
    int n,i,j,k,s;
    float p,a;
    p = pow(N, (double)1/3); //raiz cubica del numero de particulas
    n = floor(p); // parte entera de p.
    a = L/N; // Distancia entre particulas
    float r = p - n; // r es la parte decimal de p
    // si r < 0.5 acomodo las particulas en la caja y las que sobra las distribuyo después.
    if (r < 0.5) {
        s = N - n*n*n; //cantidad de particulas que sobran
        //Acomodo las particulas. El for en i es para la coordenada x, el de j para y y el de k para z.
        for (k=0;k<n;k++){
            for (j=0;j<n;j++){
                for (i=0;i<n;i++){
                    pos [3*i + (3*n)*j + (3*n*n)*k] = (a/2) + i*a;
                    pos [1 + 3*i + (3*n)*j + (3*n*n)*k] = (a/2) + j*a;
                    pos [2 + 3*i + (3*n)*j + (3*n*n)*k] = (a/2) + k*a;
                }
            }
        }

  //Veo los casos de las particulas que sobran
  // s<=n: Entran en un eje
        if (s<=n) {
            for (i=0;i<s;i++) {
                pos [3*(n*n*n) + 3*i] = a + i*a;
                pos [1 + 3*(n*n*n) + 3*i] = a;
                pos [2 + 3*(n*n*n) + 3*i] = a ;
            }
        }

//s>n y s<n*n entran en un plano intercaladas entre las demas particulas.
        int v = floor (s/n); //límite para j
        if (s>n && s<n*n) {
            for (j=0;j<v;j++) {
                for (i=0;i<n;i++) {
                    pos [3*(n*n*n) + 3*i + 3*n*j] = a + i*a;
                    pos [1 + 3*(n*n*n) + 3*i + 3*n*j] = a + j*a;
                    pos [2 + 3*(n*n*n) + 3*i + 3*n*j] = a ;
                }
            }
        }
        int vv = floor (s/n*n); //límite para k
         // s>n*n y s<n*n*n las voy acomodando en distintos planos.
        if (s>n*n && s<n*n*n) {
            for (k=0;k<vv;k++){
                for (j=0;j<v;j++) {
                    for (i=0;i<n;i++) {
                        pos [3*(n*n*n) + 3*i + 3*n*j + 3*(n*n)*k] = a + i*a;
                        pos [1 + 3*(n*n*n) + 3*i + 3*n*j + 3*(n*n)*k] = a + j*a;
                        pos [2 + 3*(n*n*n) + 3*i + 3*n*j + 3*(n*n)*k] = a + k*a ;
                    }
                }
            }
        }
    }  else {
        // si r>0.5 pongo mas sobre cada eje, n+1 y que queden libres los últimos espacios.
        n = n+1;
        for (k=0;k<n;k++){
            for (j=0;j<n;j++){
                for (i=0;i<n;i++) {
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
            vels += (rand()/RAND_MAX - 0.5)*2*sigma*sqrt(3*k);
        }
        vels /= k;
        vel[i] = vels;
    }

    // Resto velocidad promedio
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
