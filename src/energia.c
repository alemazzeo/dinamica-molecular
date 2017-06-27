#include <math.h>
#include "energia.h"
#include "lennardjones.h"

float energia(float *pos, float *vel, int n, float *LJ_LUT, int g, float rc)
{
    float energia=0;
    float rij2, rij;

    // Calcula la energia de las n particulas
    for(int i=0; i<n; i++){
    	// suma la energía cinética
    	energia += velocidad2(&vel[i*3]) / (2 * M);

    	// i<j para no repetir la misma interacción
    	for (int j=i+1; j<n; j++)
    	{
            rij2 = distancia2(&pos[i*3], &pos[j*3]);
            rij = sqrt(rij2);
    	    // suma la energía de la interacción
            if(rij < rc){
                energia += lookup(LJ_LUT, g, rij);
            }
    	}
    }
    return energia;
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

float potencial(float *pos_i, float *pos_j)
{
    // Calcula el potencial de Lennard-Jones
    float r2, pot, exp2, exp6, exp12;

    // Distancia al cuadrado
    r2 = distancia2(pos_i, pos_j);

    // (Gamma / r) ** 2
    exp2 = GAMMA * GAMMA / r2;
    // (Gamma / r) ** 6
    exp6 = exp2 * exp2 * exp2;
    // (Gamma / r) ** 12
    exp12 = exp6 * exp6;

    // Lennard-Jones
    pot = 4 * EPS * (exp12 - exp6);
    return pot;
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
        lx += cos (b*(pos[3*i]-(a/2)));
        ly += cos (b*(pos[3*i+1]-(a/2)));
        lz += cos (b*(pos[3*i+2]-(a/2)));
    }
    lx =  (lx/N);
    ly =  (ly/N);
    lz =  (lz/N);
    l = (lx+ly+lz)/3; // lambda total
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
    f = (4*M_PI) * pow((2*M_PI*T),(-3.0/2)) * vel * vel * exp(-(vel * vel)/ 2*T);
    return f * log(f) * 0.05;
}
