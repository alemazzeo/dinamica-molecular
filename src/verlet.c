#include "stdio.h"

#include "verlet.h"
#include "energia.h"
#include "lennardjones.h"
#include "math.h"

int primer_paso(float *pos, float *vel, float *fza, int N, float h){

    // Actualiza medio paso para las velocidades
    // Actualiza las posiciones
    for(int i=0; i<3*N; i++){
        vel[i] += 0.5 * fza[i] * h;
        pos[i] += vel[i] * h;
    }

    return 0;
}

float nueva_fza(float *pos, float *fza, int n, float L,
    float rc, float *FZA_LUT, int g) {
    // Calcula la nueva fuerza

    float rij, rij2, fuerza, radial;
    float dr[3];
    float p_exceso = 0;

    //inicializa las fuerzas a cero
    for(int i=0; i<3*n; i++) {
        fza[i] = 0;
    }

    for(int i=0; i<n-1; i++) {

        for(int j=i+1; j<n; j++) {

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

            // calcula el módulo de la distancia
            rij = sqrt(rij2);

            if(rij < rc) {

                // calcula la parte radial de la fuerza mediante la LUT
                radial = lookup(FZA_LUT, g, rij);
		p_exceso += rij * radial;

                for(int k=0; k<3; k++) {

                    // calcula la componente k
                    fuerza = radial * dr[k] / rij;
                    // fuerza = 0; //ignorar
                    // le suma la fza a la particula i con componente k
                    fza[i * 3 + k] += fuerza;
                    // idem por simetria
                    fza[j * 3 + k] += -fuerza;
                }
            }
        }
    }
    return p_exceso;
}

int nueva_fza_exacto(float *pos, float *fza, int n, float L, float rc) {
    // Calcula la nueva fuerza

    float rij, rij2, fuerza, radial;
    float dr[3];

    //inicializa las fuerzas a cero
    for(int i=0; i<3*n; i++) {
        fza[i] = 0;
    }

    for(int i=0; i<n-1; i++) {

        for(int j=i+1; j<n; j++) {

            rij2 = 0;

            for(int k=0; k<3; k++){
                // calcula los dk con k = (x, y, z)
                dr[k] = pos[i*3+k] - pos[j*3+k];

                // condiciones de contorno para dk
                if(dr[k] > L/2){
                    dr[k] -= L;
                }
                else if(dr[k] < -L/2){
                    dr[k] += L;
                }

                // suma las diferencias cuadradas
                rij2 += dr[k] * dr[k];
            }

            // calcula el módulo de la distancia
            rij = sqrt(rij2);

            if(rij < rc) {

                // calcula la parte radial de la fuerza
                radial = -24 * (pow(rij, -7) - 2 * pow(rij, -13));

                for(int k=0; k<3; k++) {
                    // calcula la componente k
                    fuerza = radial * dr[k] / rij;
                    // le suma la fuerza a la particula i con componente k
                    fza[i * 3 + k] += fuerza;
                    // idem por simetria
                    fza[j * 3 + k] += -fuerza;
                }
            }
        }
    }
    return 0;
}

int ultimo_paso(float *vel, float *fza, int N, float h){
    // Hace el medio paso restante para las velocidades
    for(int i=0; i<3*N; i++){
        vel[i] += 0.5 * fza[i] * h;
    }

    return 0;
}

int c_cont(float *pos, int N, float L){
    // Aplica condiciones de contorno
    for(int i=0; i<3*N; i++) {
        pos[i] = pos[i] - L*floor(pos[i]/L);
    }
    return 0;
}
