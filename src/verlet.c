#include "verlet.h"

int verlet(float *pos, float *vel, float **fza, float **fza_aux,
	   int n, float L, float h)
{
    float *swap; // Puntero auxiliar para intercambiar las fuerzas

    // Calcula la nueva posición sobrescribiendo el vector pos
    nueva_pos(pos, vel, *fza, n, h);

    // Calcula la nueva fuerza y la escribe en el vector fza_aux
    fuerzas(pos, *fza_aux, n);

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

int nueva_pos(float *pos, float *vel, float *fza, int n, float h)
{
    // Calcula las 3n coordenadas espaciales
    for(int i=0; i<3*n; i++)
    {
	pos[i] = pos[i] + vel[i] * h + 0.5 * fza[i] * h * h / M;
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

float energia(float *pos, float *vel, int n)
{
    float energia=0;

    // Calcula la energia de las n particulas
    for(int i=0; i<n; i++)
    {
	// suma la energía cinética
	energia += velocidad2(&pos[i*3]) / (2 * M);

	// i<j para no repetir la misma interacción
	for (int j=i+1; j<n; j++)
	{
	    // suma la energía de la interacción
	    energia += potencial(&pos[i*3], &pos[j*3]);
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
