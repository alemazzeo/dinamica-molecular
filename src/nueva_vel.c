#include <stdio.h>
#include <stdlib.h>
#include <math.h>

#include "nueva_vel.h"

int nueva_vel(float *vel, float *fza, float *fza0, float m, int n, float h) {
  int i, j;
  for(i = 0; i < n; i++) {
    for (j = 0; j < 3; j++) {
      *(vel + i* n + j) = calcVi(*(vel + 3 * i + j), *(fza + 3 * i + j), *(fza0 + 3 * i + j), h);
    }
  }
  return 0;
}

float calcVi(float vi, float fi, float fi0, float h) {
  return vi + (fi - fi0) * h * 0.5; // faltaria dividir por m
}
