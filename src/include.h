// Hack for debug mode
#ifdef _DEBUG
#define _DEBUG_WAS_DEFINED 1
#undef _DEBUG
#endif

#include <Python.h>

// Hack for debug mode
#ifdef _DEBUG_WAS_DEFINED
#define _DEBUG 1
#endif

#define NPY_NO_DEPRECATED_API NPY_1_7_API_VERSION
#include <numpy/arrayobject.h>
#include "dsp.h"