int nueva_pos(float *pos, float *vel, float *fza, int N, float h){
    // Actualiza las posiciones
    for(int i=0, i<3*N, i++){
        pos[i] = pos[i] + vel[i]*h + (fza[i]/2)*h*h;
    }
    // Aplica condiciones de contorno
    c_cont(pos, N, L);

    return 0;
}

int c_cont(float *pos, int N, float L){
    for(int i=0, i<3*N, i++){
        pos[i] = pos[i] - L*floor(pos[i]/L);
    }
    return 0;
}

int velocidades(float *vel, int N, float T){
    float sigma = sqrt(T);
    float vels;
    int k = 20;
    int i,j;

    // Genero distribucion de velocidades
    for(i=0, i<3*N, i++){
        vels = 0;
        for(j=0, j<k, j++){
            vels += (rand()/RAND_MAX - 0.5)*2*sigma*sqrt(3*n);
        }
        vels /= k;
        vel[i] = vels;
    }

    // Resto velocidad promedio
    for(i=0, i<3, i++){
        float promedio = avg_vel(vel, N, i);
        for(j=0, j<3*N, j=j+3){
            vel[j+i] -= promedio;
        }
    }

    return 0;
}

float avg_vel(float *vel, int N, int coordenada){
    float promedio = 0;
    for(int i=0, i<3*N, i=i+3){
        promedio += vel[i+coordenada];
    }
    return promedio/N;
}
