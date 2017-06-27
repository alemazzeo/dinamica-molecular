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

int nueva_fza(float *pos, float *fza, int n, float L, float rc,
            float *FZA_LUT, int g) {
    int i, j, k;
    float dist, rij, rij2, fuerza, radial;
    float pos_interaccion[3];

    //inicializo las fuerzas a cero
    for(i = 0; i < 3 * n; i++) {
        fza[i] = 0;
    }

    for(i = 0; i < n - 1; i++) {
        for(j = i + 1; j < n; j++) {

    	    // Verifica si las partículas interaccionan teniendo
    	    // en cuenta las condiciones de contorno
    	    // En caso afirmativo guarda en pos_interaccion la posición
    	    // de la particula que cumple rij < rc

            if (par_interaccion(&pos[i*3], &pos[j*3], pos_interaccion, L, rc)) {

        		// Calcula rij
        		rij2 = distancia2(&pos[i*3], pos_interaccion);
                rij = sqrt(rij2);

        		// parte radial de la fuerza
                //radial = (24 / pow(rij2, 0.5)) * (2*pow(rij2, -6)-pow(rij2, -3));
                radial = lookup(FZA_LUT, g, rij);

                for(k = 0; k < 3; k++) {
                    dist =  pos[i * 3 + k] - pos_interaccion[k];
                    fuerza = radial * dist / rij;
                    fza[i * 3 + k] += fuerza; //le sumo la fza a la particula i
                    fza[j * 3 + k] += -fuerza; //por simetria
                }
            }
        }
    }
    return 0;
}

int par_interaccion(float *pos_fija, float *pos_movil,
		    float *pos_interaccion, float L, float rc){

    // NOTA: Esta función supone que cada particula solo puede
    // interactuar con una copia de las 26 (¿debería no?)

    float rc2 = rc * rc;
    float r[3]; // Vector para la partícula desplazada

    // Revisa los 27 cuadrantes vecinos en busca
    // de una distancia menor a rc
    // Para cada variable toma X-L, X, X+L

    for(int i=0; i<3; i++){
	r[0] = pos_movil[0] + (i - 1) * L;

    	for(int j=0; j<3; j++){
    	    r[1] = pos_movil[1] + (j - 1) * L;

    	    for(int k=0; k<3; k++){
        		r[2] = pos_movil[2] + (k - 1) * L;

        		// Calcula la distancia cuadrada entre la partícula
        		// desplazada (o no) y la partícula fija
        		// y la compara con rc.

        		if(distancia2(r, pos_fija) < rc2){
        		    pos_interaccion[0] = r[0];
        		    pos_interaccion[1] = r[1];
        		    pos_interaccion[2] = r[2];

        		    // Devuelve 1 para avisar que hay interacción
        		    return 1;
        		}
    	    }
    	}
    }

    // Caso contrario devuelve 0
    return 0;

}
