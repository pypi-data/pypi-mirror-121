//
//  parameter.h
//  ingescapeWrapp
//
//  Created by vaugien on 12/02/2018.
//  Copyright © 2018 ingenuity. All rights reserved.
//

#include "parameter.h"
#include <stdio.h>
#include <ingescape/ingescape.h>


//igs_readparameterAsBool
 PyObject * readParameterAsBool_wrapper(PyObject * self, PyObject * args)
{
    char * name;
    // parse argument and cast it : the name of the output
    if (!PyArg_ParseTuple(args, "s", &name)) {
        return NULL;
    }
    // build the resulting bool into a Python object.
    if (igs_parameter_bool(name)) {
        Py_RETURN_TRUE;
    } else{
        Py_RETURN_FALSE;
    }
}

//igs_parameter_int
 PyObject * readParameterAsInt_wrapper(PyObject * self, PyObject * args)
{
    char * name;
    int result;
    // parse argument and cast it : the name of the Parameter
    if (!PyArg_ParseTuple(args, "s", &name)) {
        return NULL;
    }
    result = igs_parameter_int(name);
    return PyLong_FromLong(result);
}

//igs_parameter_double
 PyObject * readParameterAsDouble_wrapper(PyObject * self, PyObject * args)
{
    char * name;
    double result;
    // parse argument and cast it : the name of the Parameter
    if (!PyArg_ParseTuple(args, "s", &name)) {
        return NULL;
    }
    result = igs_parameter_double(name);
    return PyFloat_FromDouble(result);
}


//igs_parameter_string
 PyObject * readParameterAsString_wrapper(PyObject * self, PyObject * args)
{
    char * name;
    char * result;
    PyObject * ret;
    // parse argument and cast it : the name of the Parameter
    if (!PyArg_ParseTuple(args, "s", &name)) {
        return NULL;
    }
    result = igs_parameter_string(name);
    if(result != NULL){
        return Py_BuildValue("s",result);
    }else{
        return Py_BuildValue("s","");
    }
}

//igs_parameter_set_bool
 PyObject * writeParameterAsBool_wrapper(PyObject * self, PyObject * args)
{
    char * name;
    PyObject *value;
    int result;
    // parse arguments and cast them : name of the param and the boolean
    if (!PyArg_ParseTuple(args, "sO", &name, &value)) {
        return NULL;
    }

    if (value == Py_True){
        result = igs_parameter_set_bool(name, true);
    }else{
        result = igs_parameter_set_bool(name, false);
    }
    return PyLong_FromLong(result);
}

//igs_parameter_set_int
 PyObject * writeParameterAsInt_wrapper(PyObject * self, PyObject * args)
{
    char * name;
    int value;
    int result;
    // parse arguments and cast them : the name and the integer
    if (!PyArg_ParseTuple(args, "si", &name, &value)) {
        return NULL;
    }
    result = igs_parameter_set_int(name, value);
    return PyLong_FromLong(result);
}

//igs_parameter_set_double
 PyObject * writeParameterAsDouble_wrapper(PyObject * self, PyObject * args)
{
    char * name;
    double value;
    int result;
    if (!PyArg_ParseTuple(args, "sd", &name, &value)) {
        return NULL;
    }
    result = igs_parameter_set_double(name, value);
    return PyLong_FromLong(result);
}

//igs_parameter_set_string
 PyObject * writeParameterAsString_wrapper(PyObject * self, PyObject * args)
{
    char * name;
    char * value;
    int result;
    if (!PyArg_ParseTuple(args, "ss", &name, &value)) {
        return NULL;
    }
    result = igs_parameter_set_string(name, value);
    return PyLong_FromLong(result);
}


//igs_parameter_type
 PyObject * getTypeForParameter_wrapper(PyObject * self, PyObject * args)
{
    char* name;
    int result;
    if (!PyArg_ParseTuple(args, "s", &name)) {
        return NULL;
    }
    result = igs_parameter_type(name);
    return PyLong_FromLong(result);
}


//igs_parameter_count
 PyObject * getParametersNumber_wrapper(PyObject * self, PyObject * args)
{
    int result = igs_parameter_count();
    return PyLong_FromLong(result);
}


//igs_parameter_list
 PyObject * igs_getParametersList_wrapper(PyObject * self, PyObject * args)
{
    long nbOfElements;
    PyObject * ret;

    char **result = igs_parameter_list(&nbOfElements);
    // create a Python List and add element one by one
    ret = PyList_New(nbOfElements);
    int i ;
    for (i = 0; i < nbOfElements; i++){
        PyList_SetItem(ret, i, Py_BuildValue("s",result[i]));
    }
    return ret;
}


//igs_checkParametersExistence
 PyObject * checkParametersExistence_wrapper(PyObject * self, PyObject * args)
{
    char * name;
    if (!PyArg_ParseTuple(args, "s", &name)) {
        return NULL;
    }
    // build the resulting double into a Python object.
    if (igs_parameter_exists(name)) {
        Py_RETURN_TRUE;
    }else{
        Py_RETURN_FALSE;
    }
}

//igs_parameter_create
 PyObject * createParameter_wrapper(PyObject * self, PyObject * args)
{
    char * name;
    igs_iop_value_type_t type;
    int _type;
    void *value;
    long size;
    int result;
    // parse arguments and cast them : name of the parameter, type, value
    if (!PyArg_ParseTuple(args, "siO", &name, &_type, &value)) {
        return NULL;
    }
    // get the type of the iop
    type = (igs_iop_value_type_t)(_type);
    if (value == Py_None){
        result = igs_parameter_create(name, type, NULL, 0);

    }else if (type == IGS_STRING_T){
        char *value_c;
        if (!PyArg_ParseTuple(args, "sis", &name, &_type, &value_c)) {
            return NULL;
        }
        result = igs_parameter_create(name, type, (void*)value_c, strlen(value_c));
    }else if (type == IGS_INTEGER_T){
        int value_c;
        if (!PyArg_ParseTuple(args, "sii", &name, &_type, &value_c)) {
            return NULL;
        }
        result = igs_parameter_create(name, type, &value_c, sizeof(int));
    }else if (type == IGS_DOUBLE_T){
        double value_c;
        if (!PyArg_ParseTuple(args, "sid", &name, &_type, &value_c)) {
            return NULL;
        }
        result = igs_parameter_create(name, type, &value_c, sizeof(double));
    }else if (type == IGS_BOOL_T){
        if (value == Py_True)
        {
            bool value = true;
            result = igs_parameter_create(name, type, &value, sizeof(bool));
        }
        else
        {
            bool value = false;
            result = igs_parameter_create(name, type, false, sizeof(bool));
        }
    }else{
        result = igs_parameter_create(name, type, value, (size_t)PyObject_Size(value));
    }
    return PyLong_FromLong(result);
}
