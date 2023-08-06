//
//  observecallback.h
//  ingescapeWrapp
//
//  Created by vaugien on 06/04/2018.
//  Copyright © 2018 ingenuity. All rights reserved.
//

#ifndef observecallback_h
#define observecallback_h
#define PY_SSIZE_T_CLEAN
#include <Python.h>
#include <ingescape/ingescape.h>

PyDoc_STRVAR(
             observeInputDoc,
             "igs_observe_input(input, callback, args)\n"
             "--\n"
             "\n"
             "Observe a parameter and associate a callback to it.\n"
             "When the input value will change the associated callback will be called.\n \n"
             "param input The string which contains the name of the input we want to observe. Can't be NULL.\n"
             "param callback is the function we want to be executed when the input is changed. Can't be NULL.\n"
             "param args A tuple containing the args of the callback in python. Can't be NULL.\n "
             "return The error.\n 0 is ok\n");

PyDoc_STRVAR(
             observeOutputDoc,
             "igs_observe_output(output, callback, args)\n"
             "--\n"
             "\n"
             "Observe a parameter and associate a callback to it.\n"
             "When the output value will change the associated callback will be called.\n \n"
             "param output The string which contains the name of the input we want to observe. Can't be NULL.\n"
             "param callback is the function we want to be executed when the output is changed. Can't be NULL.\n"
             "param args A tuple containing the args of the callback in python. Can't be NULL.\n "
             "return The error.\n 0 is ok\n");

PyDoc_STRVAR(
             observeParameterDoc,
             "igs_observe_parameter(parameter, callback, args)\n"
             "--\n"
             "\n"
             "Observe a parameter and associate a callback to it.\n"
             "When the parameter value will change the associated callback will be called.\n \n"
             "param parameter The string which contains the name of the parameter we want to observe. Can't be NULL.\n"
             "param callback is the function we want to be executed when the parameter is changed. Can't be NULL.\n"
             "param args A tuple containing the args of the callback in python. Can't be NULL.\n "
             "return The error.\n 0 is ok\n");

typedef struct observe_iop_cb {
    char *nameArg;          // name of the iop
    igs_iop_type_t iopType; // IOP type
    PyObject *callback;     // observeCallback
    PyObject *my_data;      // argument of the callback
    struct observe_iop_cb *next;
    struct observe_iop_cb *prev;
} observe_iop_cb_t;
extern observe_iop_cb_t *observe_iop_cbList;

PyObject *observe_input_wrapper(PyObject *self, PyObject *args, PyObject *kwds);

PyObject *observe_output_wrapper(PyObject *self, PyObject *args, PyObject *kwds);

PyObject *observe_parameter_wrapper(PyObject *self, PyObject *args, PyObject *kwds);

#endif /* observecallback_h */
