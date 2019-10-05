#include "include.h"
#include <math.h>

static PyObject* dsp_goertzel(PyObject* self, PyObject* args)
{
    PyArrayObject *ap;
    int filter_size, fs;
    double ft;
    long int data_len;
    double *data;
    double mag;

    if(!PyArg_ParseTuple(args, "O!idi",
        &PyArray_Type, &ap, &fs, &ft, &filter_size)) {
        return NULL;
    }
    if (ap == NULL) return NULL;

    // Ensure the input array is contiguous.
    // PyArray_GETCONTIGUOUS will increase the reference count.
    ap = PyArray_GETCONTIGUOUS(ap);

    data = (double *)PyArray_DATA((PyArrayObject *)ap);
    data_len = (long int)PyArray_DIM(ap, 0);

    mag = goertzel(data, data_len, fs, ft, filter_size);

    // Decrease the reference count of ap.
    Py_DECREF(ap);
    return Py_BuildValue("d", mag);
}

static PyObject* dsp_goertzel_m(PyObject* self, PyObject* args)
{
    PyArrayObject *ap1, *ap2;
    PyObject *output;
    int filter_size, fs, ft_num;
    long int data_len;
    double *data, *ft, *mag;

    if(!PyArg_ParseTuple(args, "O!iO!i",
        &PyArray_Type, &ap1, &fs, &PyArray_Type, &ap2, &filter_size)) {
        return NULL;
    }
    if (ap1 == NULL) return NULL;
    if (ap2 == NULL) return NULL;

    ap1 = PyArray_GETCONTIGUOUS(ap1);

    data = (double *)PyArray_DATA(ap1);
    data_len = (long int)PyArray_DIM(ap1, 0);
    ft = (double *)PyArray_DATA(ap2);
    ft_num = (int)PyArray_DIM(ap2, 0);

    output = PyArray_SimpleNew(1, PyArray_DIMS(ap2), NPY_DOUBLE);
    mag = (double *)PyArray_DATA((PyArrayObject *)output);

    goertzel_m(data, data_len, fs, ft, ft_num, filter_size, mag);

    Py_DECREF(ap1);
    return output;
}

static PyObject* dsp_goertzel_rng(PyObject* self, PyObject* args)
{
    PyArrayObject *ap;
    int filter_size, fs;
    double ft;
    double rng;
    long data_len;
    double *data;
	
    double magnitude;
	
    if(!PyArg_ParseTuple(args, "O!idid",
        &PyArray_Type, &ap, &fs, &ft, &filter_size, &rng)) {
        return NULL;
    }
    if (ap == NULL) return NULL;

    ap = PyArray_GETCONTIGUOUS(ap);

    data = (double *)PyArray_DATA(ap);
    data_len = (long)PyArray_DIM(ap, 0);

    magnitude = goertzel_rng(data, data_len, fs, ft, filter_size, rng);

    Py_DECREF(ap);
    return Py_BuildValue("d", magnitude);
}

/* Set up the methods table */
static PyMethodDef methods[] = {
    {"goertzel", dsp_goertzel,  // Python name, C name
    METH_VARARGS,               // Input parameters
    "Goertzel algorithm."},     // Doc string
    {"goertzel_m", dsp_goertzel_m,
    METH_VARARGS,
    "Goertzel algorithm for multiple target frequency."},
    {"goertzel_rng", dsp_goertzel_rng,
    METH_VARARGS,
    "Goertzel algorithm for specific frequency range."},
    {NULL, NULL, 0, NULL}       // Sentinel
};

/* Initialize module */
#if PY_VERSION_HEX >= 0x03000000
static struct PyModuleDef moduledef = {
    PyModuleDef_HEAD_INIT,
    "dsp_ext",
    NULL,
    -1,
    methods,
    NULL,
    NULL,
    NULL,
    NULL
};
PyMODINIT_FUNC PyInit_dsp_ext(void)
{
    import_array();             // Must be called for NumPy.
    PyObject *m;
    m = PyModule_Create(&moduledef);
    if (!m) {
        return NULL;
    }
    return m;
}
#else
PyMODINIT_FUNC initdsp_ext(void)
{
    (void)Py_InitModule("dsp_ext", methods);
    import_array();             // Must be called for NumPy.
}
#endif
