#include <stdlib.h>
#include <stdio.h>
#include <time.h>
#include <math.h>

int llenar (float *pos, float N, float L){
  int n,i,j,k,l,s;
  float p,a;
  p = pow(N, (double)1/3);
  n = floor(p);
  printf("%d\n", n );
  a = L/N;
  printf("%f\n", a);
  float r = p - n;
  if (r < 0.5) {
    n = n;
    s = N - n*n*n;
  printf("%d\n", s);
  for (k=0;k<n;k++){
    for (j=0;j<n;j++){
      for (i=0;i<n;i++) {
      *(pos + 3*i + (3*n)*j + (3*n*n)*k) = (a/2) + i*a;
      *(pos + 1 + 3*i + (3*n)*j + (3*n*n)*k) = (a/2) + j*a;
      *(pos + 2 + 3*i + (3*n)*j + (3*n*n)*k) = (a/2) + k*a;
      }
    }
  }

  if (s<=n){
    for (i=0;i<s;i++) {
    *(pos + 3*(n*n*n) + 3*i) = a + i*a;
    *(pos + 1 + 3*(n*n*n) + 3*i) = a;
    *(pos + 2 + 3*(n*n*n) + 3*i) = a ;
  }
}
 int v = floor (s/n);
   if (s>n && s<n*n){
    for (j=0;j<v;j++) {
      for (i=0;i<n;i++) {
     *(pos + 3*(n*n*n) + 3*i + 3*n*j) = a + i*a;
     *(pos + 1 + 3*(n*n*n) + 3*i + 3*n*j) = a + j*a;
     *(pos + 2 + 3*(n*n*n) + 3*i + 3*n*j) = a ;
   }
 }
 }
 int vv = floor (s/n*n);

if (s>n*n && s<n*n*n) {
  for (k=0;k<vv;k++){
  for (j=0;j<v;j++) {
    for (i=0;i<n;i++) {
   *(pos + 3*(n*n*n) + 3*i + 3*n*j + 3*(n*n)*k) = a + i*a;
   *(pos + 1 + 3*(n*n*n) + 3*i + 3*n*j + 3*(n*n)*k) = a + j*a;
   *(pos + 2 + 3*(n*n*n) + 3*i + 3*n*j + 3*(n*n)*k) = a + k*a ;
    }
  }
}
}
}
  else {
    n = n+1;

  printf("%d\n", n );
  for (k=0;k<n;k++){
    for (j=0;j<n;j++){
      for (i=0;i<n;i++) {
      *(pos + 3*i + (3*n)*j + (3*n*n)*k) = (a/2) + i*a;
      *(pos + 1 + 3*i + (3*n)*j + (3*n*n)*k) = (a/2) + j*a;
      *(pos + 2 + 3*i + (3*n)*j + (3*n*n)*k) = (a/2) + k*a;
      }
    }
  }
}

  for (l=0;l<3*N;l++) {
    printf ("%f\n",*(pos + l));
  }

return 0;

}


int velocidades (float *vel, int N, float T){
  int i;
  srand(time(NULL));
  for (i=0;i<3*N;i++) {
    *(vel + i) = T + i*((double)rand())/RAND_MAX;
  }

  return 0;
}
