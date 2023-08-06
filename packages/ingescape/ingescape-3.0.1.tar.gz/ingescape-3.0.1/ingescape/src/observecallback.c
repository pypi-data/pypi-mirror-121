//
//  observecallback.h
//  ingescapeWrapp
//
//  Created by vaugien on 12/02/2018.
//  Copyright © 2018 ingenuity. All rights reserved.
//
#include "observecallback.h"
#include <stdio.h>
#include "uthash/utlist.h"

static char *s_strndup (const char *str, size_t chars)
{
    size_t n = 0;
    char *buffer = (char *) malloc (chars + 1);
    if (buffer) {
        for (n = 0; ((n < chars) && (str[n] != 0)); n++)
            buffer[n] = str[n];
        buffer[n] = 0;
    }
    return buffer;
}

observe_iop_cb_t *observe_iop_cbList = NULL;
//observeCallback that execute the callback for the iop that has been changed
void observe(igs_iop_type_t iopType, const char* name, igs_iop_value_type_t valueType, void* value, unsigned long valueSize, void* myData){
    IGS_UNUSED(myData);
    // Lock the GIL to execute the callback safely
    PyGILState_STATE d_gstate;
    d_gstate = PyGILState_Ensure();
    //run through all callbacks to execute them
    PyObject *tupleArgs = PyTuple_New(5);
    PyTuple_SetItem(tupleArgs, 0, Py_BuildValue("i", iopType));
    PyTuple_SetItem(tupleArgs, 1, Py_BuildValue("s", name));
    PyTuple_SetItem(tupleArgs, 2, Py_BuildValue("i", valueType));
    switch(valueType){
        case IGS_BOOL_T:
            if (*(bool*)value){
                PyTuple_SetItem(tupleArgs, 3, Py_True);
            }else{
                PyTuple_SetItem(tupleArgs, 3, Py_False);
            }
            break;
        case IGS_INTEGER_T:
            PyTuple_SetItem(tupleArgs, 3, Py_BuildValue("i", *(int*)value));
            break;
        case IGS_DOUBLE_T:
            PyTuple_SetItem(tupleArgs, 3, Py_BuildValue("d", *(double*)value));
            break;
        case IGS_STRING_T:
            PyTuple_SetItem(tupleArgs, 3, Py_BuildValue("s", (char*)value));
            break;
        case IGS_IMPULSION_T:
            PyTuple_SetItem(tupleArgs, 3, Py_None);
            break;
        case IGS_DATA_T:
            PyTuple_SetItem(tupleArgs, 3, Py_BuildValue("y#", value, valueSize));
            break;
        case IGS_UNKNOWN_T:
            break;
    }

    observe_iop_cb_t *actuel = NULL;
    DL_FOREACH(observe_iop_cbList, actuel) {
        if (streq(actuel->nameArg, name)
            && (actuel->iopType == iopType)) {
            Py_INCREF(actuel->my_data);
            PyTuple_SetItem(tupleArgs, 4, actuel->my_data);
            PyObject_Call(actuel->callback, tupleArgs, NULL);
            Py_DECREF(tupleArgs);
        }
    }

    //release the GIL
    PyGILState_Release(d_gstate);
}

PyObject *_observe_generic(PyObject *self, PyObject *args, PyObject *kwds, igs_iop_type_t iopType)
{
    // parse the callback and arguments sent from python
    PyObject *callback = NULL;
    PyObject *my_data = NULL;
    char *iopName = NULL;
    // static char *kwlist[] = {"iop_name", "callback", "args", NULL};
    // if (PyArg_ParseTupleAndKeywords(args, kwds, "sOO", kwlist, &iopName, &callback, &my_data)) { //FIXME Cannot seem to make this work... May be related to my machine only due to a hazardous installation of python (brew vs. built-in and such)
    if (PyArg_ParseTuple(args, "sOO", &iopName, &callback, &my_data)) {
        if (!PyCallable_Check(callback)) { // check if the callback is a function
            PyErr_SetString(PyExc_TypeError, "'callback' parameter must be callable");
            return PyLong_FromLong(IGS_FAILURE);;
        }
    }
    else {
        return PyLong_FromLong(IGS_FAILURE);
    }

    // add the callback to the list of Callbacks
    observe_iop_cb_t *newElt = calloc(1, sizeof(observe_iop_cb_t));
    newElt->iopType = iopType;
    newElt->nameArg = strdup(iopName);
    newElt->my_data = Py_BuildValue("O", my_data);
    newElt->callback = callback;
    DL_APPEND(observe_iop_cbList, newElt);
    switch(iopType)
    {
        case IGS_INPUT_T:
            igs_observe_input(iopName, observe, NULL);
            break;
        case IGS_OUTPUT_T:
            igs_observe_output(iopName, observe, NULL);
            break;
        case IGS_PARAMETER_T:
            igs_observe_parameter(iopName, observe, NULL);
            break;
    }
    return PyLong_FromLong(IGS_SUCCESS);
}

PyObject *observe_input_wrapper(PyObject *self, PyObject *args, PyObject *kwds)
{
    return _observe_generic(self, args, kwds, IGS_INPUT_T);
}

PyObject *observe_output_wrapper(PyObject *self, PyObject *args, PyObject *kwds)
{
    return _observe_generic(self, args, kwds, IGS_OUTPUT_T);
}

PyObject *observe_parameter_wrapper(PyObject *self, PyObject *args, PyObject *kwds)
{
    return _observe_generic(self, args, kwds, IGS_PARAMETER_T);
}