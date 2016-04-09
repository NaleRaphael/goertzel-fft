#define _USE_MATH_DEFINES	// for C
#include <math.h>

// Goertzel algorithm (for single tone detection)
double goertzel(double* data, long data_len, int fs, int ft, int filter_size);
void goertzel_m(double* data, long int data_len, int fs, double* ft, int ft_num, int filter_size, double* mag);
double goertzel_rng(double* data, long data_len, int fs, int ft, double rng, int filter_size);