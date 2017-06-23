#include <stdio.h>
#include <stdlib.h>
#include <math.h>

#include "fuerza.h"

int fuerzas (float *pos, float *fza, int n, float rc) {
  int i;
  for (i = 0; i < 3 * n ; i++) { *(fza + i) = 0; }
  calcFza(pos, fza, n, rc);
  return 0;
}

int calcFza(float *pos, float *fza, int n, float rc) {
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
