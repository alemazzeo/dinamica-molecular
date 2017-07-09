o#include <math.h>
#include <stdlib.h>
#include <stdio.h>

#include "energia.h"
#include "lennardjones.h"

float cinetica(float *vel, int N){
    float cinetica = 0;
    for(int i=0; i<N; i++){
    	// suma la energía cinética
    	cinetica += velocidad2(&vel[i*3]) / 2;
    }

    return cinetica;
}

float potencial(float *pos, int N, float L, float *LJ_LUT, int g, float rc){
    float potencial=0;
    float rij2, rij;
    float dr[3];

    // Calcula la energia potencial de las n particulas
    for(int i=0; i<N; i++){
        // i<j para no repetir la misma interacción
        for (int j=i+1; j<N; j++)
        {
            rij2 = 0;

            for(int k=0; k<3; k++){
                // calcula los dk con k = (x, y, z)
                dr[k] = pos[i*3+k] - pos[j*3+k];

                // condiciones de contorno para dk
                if(dr[k] > L/2){
                    dr[k] -= L;
                }
                if(dr[k] < -L/2){
                    dr[k] += L;
                }

                // suma las diferencias cuadradas
                rij2 += dr[k] * dr[k];
            }

            rij = sqrt(rij2);
            // suma la energía de la interacción
            if(rij < rc){
                potencial += lookup(LJ_LUT, g, rij);
            }
        }
    }
    return potencial;
}

float potencial_exacto(float *pos, int N, float L, float rc) {
    float potencial=0;
    float rij, rij2, exp2, exp6, exp12;
    float dr[3];

    // Calcula la energia potencial de las n particulas
    for(int i=0; i<N; i++){
        // i<j para no repetir la misma interacción
        for (int j=i+1; j<N; j++)
        {
            rij2 = 0;

            for(int k=0; k<3; k++){
                // calcula los dk con k = (x, y, z)
                dr[k] = pos[i*3+k] - pos[j*3+k];

                // condiciones de contorno para dk
                if(dr[k] > L/2){
                    dr[k] -= L;
                }
                if(dr[k] < -L/2){
                    dr[k] += L;
                }

                // suma las diferencias cuadradas
                rij2 += dr[k] * dr[k];
            }

            // suma la energía de la interacción
            // (1 / r) ** 2
            exp2 = 1 / rij2;
            // (1 / r) ** 6
            exp6 = exp2 * exp2 * exp2;
            // (1 / r) ** 12
            exp12 = exp6 * exp6;

            rij = sqrt(rij2);
            // Lennard-Jones
            if(rij < rc){
                potencial += 4 * (exp12 - exp6);
            }
        }
    }

    return potencial;
}

float velocidad2(float *vel)
{
    // Calcula y devuelve el cuadrado de la velocidad
    return (vel[0] * vel[0]) + (vel[1] * vel[1]) + (vel[2] * vel[2]);
}

float distancia2(float *pos_i, float *pos_j)
{
    // Calcula y devuelve la distancia al cuadrado
    float x, y, z, r2;
    x = pos_i[0] - pos_j[0];
    y = pos_i[1] - pos_j[1];
    z = pos_i[2] - pos_j[2];
    r2 = x * x + y * y + z * z;
    return r2;
}


float lambda_verlet (float *pos, float N, float L) {
    int i;
    float a, lx, ly, lz, l, b;
    a = L/N; //separacion entre partículas
    b = (2*M_PI)/a; // parte del argumento de coseno
    lx = 0;
    ly = 0;
    lz = 0;
        //calculo lambda x : lx, lamba y :ly y lambda z : lz.
    for (i=0; i<=N-2;i++) {
        lx += cos (b*(pos[3*i]-a));
        ly += cos (b*(pos[3*i+1]-a));
        lz += cos (b*(pos[3*i+2]-a));
    }
    l = (lx+ly+lz)/(3*N); // lambda total
    return l;
}


float Hboltzmann (float *vel, float N, float T){
    int i;
    float h;
    h = 0;
    for (i=0;i<3*N;i++) {
        h += funcionH (vel[i],T);
    }
    return h;
}

float funcionH (float vel, float T) {
    float f;
    f = (4*M_PI) * pow((2*M_PI*T),(-3.0/2)) * vel * vel * exp(-(vel * vel) / (2*T));
    return f * log(f) * 0.05;
}


float distrib_radial(float *distrad, float *pos, float n, float L, float rho, float Q) {
    int bin;
    float rij, rij2, dR1;
    float dr[3];

    dR1 = L/(Q + 2); // longitud de un bin

    for(int i=0; i<n-1; i++) {

        for(int j=i+1; j<n; j++) {

            rij2 = 0;

            for(int k=0; k<3; k++) {
                // calcula los dk con k = (x, y, z)
                dr[k] = pos[i*3+k] - pos[j*3+k];

                // condiciones de contorno para dk
                if(dr[k] > 0.5*L){
                    dr[k] -= L;
                }
                else if(dr[k] < -(0.5*L)){
                    dr[k] += L;
                }

                // suma las diferencias cuadradas
                rij2 += dr[k] * dr[k];
            }

            // calcula el módulo de la distancia
            rij = sqrt(rij2);

            bin = floor(rij/dR1);
            distrad[bin] += 1.0 / (4 * M_PI * rij * rij * dR1 * rho);

        }
    }

    return 0;
}
