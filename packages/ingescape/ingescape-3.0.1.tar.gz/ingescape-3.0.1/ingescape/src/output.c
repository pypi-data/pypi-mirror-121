//
//  output.h
//  ingescapeWrapp
//
//  Created by vaugien on 12/02/2018.
//  Copyright © 2018 ingenuity. All rights reserved.
//
#include "output.h"
#include <stdio.h>
#include <ingescape/ingescape.h>

//igs_output_bool
 PyObject * readOutputAsBool_wrapper(PyObject * self, PyObject * args)
{
    char * name;
    // parse arguments and cast them : the name of the output and the boolean
    if (!PyArg_ParseTuple(args, "s", &name)) {
        return NULL;
    }
    // build the resulting bool into a Python object.
    if (igs_output_bool(name)) {
        Py_RETURN_TRUE;
    } else{
        Py_RETURN_FALSE;
    }
}

//igs_output_int
 PyObject * readOutputAsInt_wrapper(PyObject * self, PyObject * args)
{
    char * name;
    int result;
    // parse argument and cast it : the name of the output
    if (!PyArg_ParseTuple(args, "s", &name)) {
        return NULL;
    }
    result = igs_output_int(name);
    return PyLong_FromLong(result);
}

//igs_output_double
 PyObject * readOutputAsDouble_wrapper(PyObject * self, PyObject * args)
{
    char * name;
    double result;
    // parse argument and cast it : the name of the output
    if (!PyArg_ParseTuple(args, "s", &name)) {
        return NULL;
    }
    result = igs_output_double(name);
    return PyFloat_FromDouble(result);
}


//igs_readOutputAsStirng
 PyObject * readOutputAsString_wrapper(PyObject * self, PyObject * args)
{
    char * name;
    char * result;
    PyObject * ret;
    // parse argument and cast it : the name of the output
    if (!PyArg_ParseTuple(args, "s", &name)) {
        return NULL;
    }
    result = igs_output_string(name);
    if(result != NULL){
        return Py_BuildValue("s",result);
    }else{
       return Py_BuildValue("s","");
    }
}

//igs_output_set_bool
 PyObject * writeOutputAsBool_wrapper(PyObject * self, PyObject * args)
{
    char * name;
    PyObject *value;
    int result;
    // parse arguments and cast them : the name of the output and the boolean
    if (!PyArg_ParseTuple(args, "sO", &name, &value)) {
        return NULL;
    }
    if (value == Py_True){
        result = igs_output_set_bool(name, true);
    }else{
        result = igs_output_set_bool(name, false);
    }
    return PyLong_FromLong(result);
}

//igs_output_set_int
 PyObject * writeOutputAsInt_wrapper(PyObject * self, PyObject * args)
{
    char * name;
    int value;
    int result;
    // parse arguments and cast them : the name of the output and the integer
    if (!PyArg_ParseTuple(args, "si", &name, &value)) {
        return NULL;
    }
    result = igs_output_set_int(name, value);
    return PyLong_FromLong(result);
}

//igs_output_set_double
 PyObject * writeOutputAsDouble_wrapper(PyObject * self, PyObject * args)
{
    char * name;
    double value;
    int result;
    // parse arguments and cast them : the name of the output and the double
    if (!PyArg_ParseTuple(args, "sd", &name, &value)) {
        return NULL;
    }
    result = igs_output_set_double(name, value);
    return PyLong_FromLong(result);
}

//igs_output_set_string
 PyObject * writeOutputAsString_wrapper(PyObject * self, PyObject * args)
{
    char * name;
    char * value;
    int result;
    // parse arguments and cast them : the name of the output and the string/char*
    if (!PyArg_ParseTuple(args, "ss", &name, &value)) {
        return NULL;
    }
    result = igs_output_set_string(name, value);
    return PyLong_FromLong(result);
}

//igs_output_set_impulsion
 PyObject * writeOutputAsImpulsion_wrapper(PyObject * self, PyObject * args)
{
    char * name;
    int result;
    // parse argument and cast it : the name of the output
    if (!PyArg_ParseTuple(args, "s", &name)) {
        return NULL;
    }
    result = igs_output_set_impulsion(name);
    return PyLong_FromLong(result);
}

//igs_output_type
 PyObject * getTypeForOutput_wrapper(PyObject * self, PyObject * args)
{
    char* name;
    int result;
    // parse argument and cast it : the name of the output
    if (!PyArg_ParseTuple(args, "s", &name)) {
        return NULL;
    }
    result = igs_output_type(name);
    return PyLong_FromLong(result);
}


//igs_output_count
 PyObject * getOutputsNumber_wrapper(PyObject * self, PyObject * args)
{
    int result;
    result = igs_output_count();
    return PyLong_FromLong(result);
}


//igs_output_list

 PyObject * igs_getOutputsList_wrapper(PyObject * self, PyObject * args)
{
    long nbOfElements;
    PyObject * ret;

    char **result = igs_output_list(&nbOfElements);
    ret = PyList_New(nbOfElements);
    int i ;
    for (i = 0; i < nbOfElements; i++){
        PyList_SetItem(ret, i, Py_BuildValue("s",result[i]));
    }
    return ret;
}

//igs_output_exists
 PyObject * checkOutputExistence_wrapper(PyObject * self, PyObject * args)
{
    char * name;
    // parse argument : the name of the output
    if (!PyArg_ParseTuple(args, "s", &name)) {
        return NULL;
    }
    // build the resulting bool into a Python object and return it
    if (igs_output_exists(name)) {
        Py_RETURN_TRUE;
    }else{
        Py_RETURN_FALSE;
    }
}

//igs_output_mute
 PyObject * muteOutput_wrapper(PyObject * self, PyObject * args)
{
    char * name;
    // parse argument : the name of the output
    if (!PyArg_ParseTuple(args, "s", &name)) {
        return NULL;
    }
    igs_output_mute(name);
    return PyLong_FromLong(0);
}

//igs_output_unmute
 PyObject * unmuteOutput_wrapper(PyObject * self, PyObject * args)
{
    char * name;
    // parse argument : the name of the output
    if (!PyArg_ParseTuple(args, "s", &name)) {
        return NULL;
    }
    igs_output_unmute(name);
    return PyLong_FromLong(0);
}

//igs_output_is_muted
 PyObject * isOutputMuted_wrapper(PyObject * self, PyObject * args)
{
    char * name;
    if (!PyArg_ParseTuple(args, "s", &name)) {
        return NULL;
    }
    // build the resulting bool into a Python object and return it
    if (igs_output_is_muted(name)) {
        Py_RETURN_TRUE;
    }else{
        Py_RETURN_FALSE;
    }
}

//igs_output_create
 PyObject * createOutput_wrapper(PyObject * self, PyObject * args)
{
    char * name;
    igs_iop_value_type_t type;
    int _type;
    void *value;
    long size;
    int result;
    // parse arguments and cast them : name of the output, type, value and size of the value
    if (!PyArg_ParseTuple(args, "siO", &name, &_type, &value)) {
        return NULL;
    }
    // get the type of the iop
    type = (igs_iop_value_type_t)(_type);
    if (value == Py_None){
        result = igs_output_create(name, type, NULL, 0);

    }else if (type == IGS_STRING_T){
        char *value_c;
        if (!PyArg_ParseTuple(args, "sis", &name, &_type, &value_c)) {
            return NULL;
        }
        result = igs_output_create(name, type, (void*)value_c, strlen(value_c));
    }else if (type == IGS_INTEGER_T){
        int value_c;
        if (!PyArg_ParseTuple(args, "sii", &name, &_type, &value_c)) {
            return NULL;
        }
        result = igs_output_create(name, type, &value_c, sizeof(int));
    }else if (type == IGS_DOUBLE_T){
        double value_c;
        if (!PyArg_ParseTuple(args, "sid", &name, &_type, &value_c)) {
            return NULL;
        }
        result = igs_output_create(name, type, &value_c, sizeof(double));
    }else if (type == IGS_BOOL_T){
        if (value == Py_True)
        {
            bool value = true;
            result = igs_output_create(name, type, &value, sizeof(bool));
        }
        else
        {
            bool value = false;
            result = igs_output_create(name, type, false, sizeof(bool));
        }
    }else{
        result = igs_output_create(name, type, value,(size_t)PyObject_Size(value));
    }
    return PyLong_FromLong(result);
}
