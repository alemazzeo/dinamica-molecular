#include "verlet.h"
#include "energia.h"
#include "lennardjones.h"
#include "math.h"

int primer_paso(float *pos, float *vel, float *fza, int N, float h){

    // Actualiza medio paso para las velocidades
    // Actualizo las posiciones
    for(int i=0; i<3*N; i++){
        vel[i] += 0.5 * fza[i] * h;
        pos[i] += vel[i] * h;
    }

    return 0;
}

int ultimo_paso(float *vel, float *fza, int N, float h){
    // Hace el segundo medio paso para las velocidades
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
