#include <stdlib.h>
#include "dsp.h"

double goertzel(double* data, long data_len, int fs, double ft, 
                int filter_size)
{
    double k;		// Related to frequency bins
    double omega;
    double sine, cosine, coeff, sf, mag;
    double q0, q1, q2, real, imag;
    long int i;
    long int dlen;

    k = floor(0.5 + ((double)(filter_size*ft) / (double)fs));

    omega = 2.0*M_PI*k/(double)filter_size;
    sine = sin(omega);
    cosine = cos(omega);
    coeff = 2.0*cosine;
    sf = (double)data_len;		// scale factor: for normalization

    q0 = 0.0;
    q1 = 0.0;
    q2 = 0.0;

    dlen = data_len - data_len%3;
    for (i = 0; i < dlen; i+=3)
    {
        q0 = coeff*q1 - q2 + data[i];
        q2 = coeff*q0 - q1 + data[i+1];
        q1 = coeff*q2 - q0 + data[i+2];
    }
    for (; i < data_len; i++)
    {
        q0 = coeff*q1 - q2 + data[i];
        q2 = q1;
        q1 = q0;
    }

    real = (q1 - q2*cosine)/sf;
    imag = (q2*sine)/sf;
    mag = sqrt(real*real + imag*imag);

    return mag;
}

void goertzel_m(double* data, long int data_len, int fs, double* ft, 
                int ft_num, int filter_size, double* mag)
{
    double k;
    double omega;
    double sine, cosine, coeff, sf;
    double q0, q1, q2, real, imag;
    long int i, dlen;
    int cnt;

    for (cnt = 0; cnt < ft_num; cnt++)
    {
        k = floor(0.5 + ((double)(filter_size*ft[cnt]) / (double)fs));
        omega = 2.0*M_PI*k/(double)filter_size;
        sine = sin(omega);
        cosine = cos(omega);
        coeff = 2.0*cosine;
        sf = (double)data_len;

        q0 = 0.0;
        q1 = 0.0;
        q2 = 0.0;

        dlen = data_len - data_len%3;
        for (i = 0; i < dlen; i+=3)
        {
            q0 = coeff*q1 - q2 + data[i];
            q2 = coeff*q0 - q1 + data[i+1];
            q1 = coeff*q2 - q0 + data[i+2];
        }
        for (; i < data_len; i++)
        {
            q0 = coeff*q1 - q2 + data[i];
            q2 = q1;
            q1 = q0;
        }

        real = (q1 - q2*cosine)/sf;
        imag = (q2*sine)/sf;
        mag[cnt] = sqrt(real*real + imag*imag);
    }
}

double goertzel_rng(double* data, long data_len, int fs, double ft, 
                    int filter_size, double rng)
{
    double f_step, f_step_normalized, k_s, k_e;
    double omega, sine, cosine, coeff, mag;
    double real, imag;
    double sf;
    double q0, q1, q2;
    double k;
    double f;
    long int i;
    long int dlen;

    f_step = (double)fs/(double)filter_size;
    f_step_normalized = 1.0/(double)filter_size;
    k_s = floor(0.5+ft/f_step);
    k_e = floor(0.5+(ft+rng)/f_step);
    sf = (double)data_len;

    mag = 0.0;

    for (k=k_s; k<k_e; k+=1.0)
    {
        f = k*f_step_normalized;
        omega = 2.0*M_PI*f;
        sine = sin(omega);
        cosine = cos(omega);
        coeff = 2.0*cosine;

        q0 = 0.0;
        q1 = 0.0;
        q2 = 0.0;

        dlen = data_len - data_len%3;
        for (i = 0; i < dlen; i+=3)
        {
            q0 = coeff*q1 - q2 + data[i];
            q2 = coeff*q0 - q1 + data[i+1];
            q1 = coeff*q2 - q0 + data[i+2];
        }
        for (; i < data_len; i++)
        {
            q0 = coeff*q1 - q2 + data[i];
            q2 = q1;
            q1 = q0;
        }

        real = (q1 - q2*cosine)/sf;
        imag = (q2*sine)/sf;
        mag += sqrt(real*real + imag*imag);

    }
    return mag;
}