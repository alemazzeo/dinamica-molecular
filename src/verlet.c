#include "verlet.h"
#include "energia.h"
#include "lennardjones.h"
#include "math.h"

int verlet(float *pos, float *vel, float **fza, float **fza_aux,
	   int n, float L, float h, float rc, float *FZA_LUT, int g)
{
    float *swap; // Puntero auxiliar para intercambiar las fuerzas

    // Calcula la nueva posición sobrescribiendo el vector pos
    nueva_pos(pos, vel, *fza, n, h, L);

    // Calcula la nueva fuerza y la escribe en el vector fza_aux
    nueva_fza(pos, *fza_aux, n, L, rc, FZA_LUT, g);

    // Calcula la nueva velocidad con la fuerza nueva y la original
    nueva_vel(vel, *fza_aux, *fza, n, h);

    // Recuerda la posición de memoria del vector fza
    swap = *fza;

    // Apunta fza al vector fza_auxiliar de modo que
    // el vector fza corresponda a la ultima fuerza calculada
    *fza = *fza_aux;

    // Apunta fza_aux al vector con la fuerza vieja para que
    // en la siguiente iteración sirva como vector auxiliar
    *fza_aux = swap;

    return 0;
}

int nueva_pos(float *pos, float *vel, float *fza, int n, float h, float L)
{
    // Calcula las 3n coordenadas espaciales
    for(int i=0; i<3*n; i++) {
        pos[i] = pos[i] + vel[i] * h + 0.5 * fza[i] * h * h / M;
    }

    // Aplica condiciones de contorno
    c_cont(pos, n, L);

    return 0;
}

int c_cont(float *pos, int N, float L){
    for(int i=0; i<3*N; i++) {
        pos[i] = pos[i] - L*floor(pos[i]/L);
    }
    return 0;
}

int nueva_vel(float *vel, float *fza, float *fza0, int n, float h)
{
    // Calcula las 3n coordenadas de velocidad
    for(int i=0; i<3*n; i++) {
	       vel[i] = vel[i] + (fza[i] + fza0[i]) * h / (2 * M);
    }

    return 0;
}

int nueva_fza(float *pos, float *fza, int n, float L,
	      float rc, float *FZA_LUT, int g) {
    
    float rij, rij2, fuerza, radial;
    float dr[3];

    //inicializo las fuerzas a cero
    for(i = 0; i < 3 * n; i++) {
        fza[i] = 0;
    }

    for(int i=0; i<n-1; i++) {
	
        for(int j=i+1; j<n; j++) {

	    rij2 = 0;
	    for(int k=0; k<3; k++){
		dr[k] = pos[i*3+k] - pos[j*3+k];
		if(dr[k] > L/2){
		    dr[k] -= L;
		}
		if(dr[k] < -L/2){
		    dr[k] += L;
		}
		rij2 += dr[k] * dr[k];
	    }
	    
	    rij = sqrt(rij2); 

            if(rij < rc) {

		// parte radial de la fuerza
                radial = lookup(FZA_LUT, g, rij);

                for(int k=0; k<3; k++) {
                    fuerza = radial * dr[k] / rij;
                    fza[i * 3 + k] += fuerza; //le sumo la fza a la particula i
                    fza[j * 3 + k] += -fuerza; //por simetria
                }
            }
        }
    }
    return 0;
}

