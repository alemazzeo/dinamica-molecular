#include "verlet.h"
#include "math.h"

int verlet(float *pos, float *vel, float **fza, float **fza_aux,
	   int n, float L, float h, float rc)
{
    float *swap; // Puntero auxiliar para intercambiar las fuerzas

    // Calcula la nueva posición sobrescribiendo el vector pos
    nueva_pos(pos, vel, *fza, n, h, L);

    // Calcula la nueva fuerza y la escribe en el vector fza_aux
    nueva_fza(pos, *fza_aux, n, rc);

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
    for(int i=0; i<3*n; i++){
      pos[i] = pos[i] + vel[i] * h + 0.5 * fza[i] * h * h / M;
    }

    // Aplica condiciones de contorno
    c_cont(pos, n, L);

    return 0;
}

int c_cont(float *pos, int N, float L){
    for(int i=0; i<3*N; i++){
        pos[i] = pos[i] - L*floor(pos[i]/L);
    }
    return 0;
}

int nueva_vel(float *vel, float *fza, float *fza0, int n, float h)
{
    // Calcula las 3n coordenadas de velocidad
    for(int i=0; i<3*n; i++)
    {
	vel[i] = vel[i] + (fza[i] + fza0[i]) * h / (2 * M);
    }

    return 0;
}

int nueva_fza(float *pos, float *fza, int n, float rc) {
  int i, j, k;
  float dist, rij, fuerza, radial;
  for(i = 0; i < n - 1; i++) {
    for(j = i + 1; j < n; j++) {
      // distancia entre particulas
      rij = pow(( *(pos + i * n) - *(pos + j * n) ), 2) + pow(( *(pos + i * n + 1) - *(pos + j * n + 1) ), 2) + pow(( *(pos + i * n + 2) - *(pos + j * n + 2) ), 2);
      if (rij < rc) {
        radial = (24 / rij) * (2 * pow(rij, -6) - pow(rij, -3));  // parte radial de la fuerza
        //en x
        for(k = 0; k < 3; k++) {
          dist =  *(pos + i * n + k) - *(pos + j * n + k);
          fuerza = radial * dist;
          *(fza + i * 3 + k) += fuerza; //le sumo la fza a la particula i
          *(fza + j * 3 + k) += -fuerza; //por simetria
        }
      }
    }
  }
  return 0;
}
