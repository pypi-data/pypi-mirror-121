//
//  input.h
//  ingescapeWrapp
//
//  Created by vaugien on 12/02/2018.
//  Copyright © 2018 ingenuity. All rights reserved.
//

#include "input.h"
#include <stdio.h>
#include <ingescape/ingescape.h>

//igs_input_bool
 PyObject * readInputAsBool_wrapper(PyObject * self, PyObject * args)
{
    char * name;
    // parse arguments :  the name of the input
    if (!PyArg_ParseTuple(args, "s", &name)) {
        return NULL;
    }
    // build the resulting bool into a Python object and return it
    if (igs_input_bool(name)) {
        Py_RETURN_TRUE;
    } else{
        Py_RETURN_FALSE;
    }
}

//igs_input_int
 PyObject * readInputAsInt_wrapper(PyObject * self, PyObject * args)
{
    char * name;
    int result;
    // parse arguments
    if (!PyArg_ParseTuple(args, "s", &name)) {
        return NULL;
    }

    result = igs_input_int(name);
    return PyLong_FromLong(result);
}

//igs_input_double
 PyObject * readInputAsDouble_wrapper(PyObject * self, PyObject * args)
{
    char * name;
    double result;

    // parse arguments
    if (!PyArg_ParseTuple(args, "s", &name)) {
        return NULL;
    }
    result = igs_input_double(name);
    return PyFloat_FromDouble(result);
}

//igs_readInputAsStirng
 PyObject * readInputAsString_wrapper(PyObject * self, PyObject * args)
{
    char * name;
    char * result;
    PyObject * ret;

    // parse arguments
    if (!PyArg_ParseTuple(args, "s", &name)) {
        return NULL;
    }
    result = igs_input_string(name);
    // build the resulting string into a Python object.
    if(result != NULL){
        return Py_BuildValue("s",result);
    }else{
        return Py_BuildValue("s","");
    }

}

//igs_input_set_bool
 PyObject * writeInputAsBool_wrapper(PyObject * self, PyObject * args)
{
    char * name;
    PyObject *value;
    int result;
    // parse arguments : the name of the input and the bool we want to write
    if (!PyArg_ParseTuple(args, "sO", &name, &value)) {
        return NULL;
    }

    if (value == Py_True){
        result = igs_input_set_bool(name, true);
    }else{
        result = igs_input_set_bool(name, false);
    }
    return PyLong_FromLong(result);
}

//igs_input_set_int
 PyObject * writeInputAsInt_wrapper(PyObject * self, PyObject * args)
{
    char * name;
    int value;
    int result;
    // parse arguments : the name of the iop and the int
    if (!PyArg_ParseTuple(args, "si", &name, &value)) {
        return NULL;
    }
    result = igs_input_set_int(name, value);
    return PyLong_FromLong(result);
}

//igs_input_set_double
 PyObject * writeInputAsDouble_wrapper(PyObject * self, PyObject * args)
{
    char * name;
    double value;
    int result;

    // parse arguments : the iop aand the double
    if (!PyArg_ParseTuple(args, "sd", &name, &value)) {
        return NULL;
    }
    result = igs_input_set_double(name, value);
    return PyLong_FromLong(result);
}

//igs_input_set_string
 PyObject * writeInputAsString_wrapper(PyObject * self, PyObject * args)
{
    char * name;
    char * value;
    int result;
    // parse arguments : the iop and the string
    if (!PyArg_ParseTuple(args, "ss", &name, &value)) {
        return NULL;
    }
    result = igs_input_set_string(name, value);
    return PyLong_FromLong(result);
}

//igs_input_set_impulsion
 PyObject * writeInputAsImpulsion_wrapper(PyObject * self, PyObject * args)
{
    char * name;
    int result;
    // parse arguments : the name of the iop
    if (!PyArg_ParseTuple(args, "s", &name)) {
        return NULL;
    }
    result = igs_input_set_impulsion(name);
    return PyLong_FromLong(1);
}

//igs_input_type
 PyObject * getTypeForInput_wrapper(PyObject * self, PyObject * args)
{
    char* name;
    // parse the name of the input and cast into a char*
    if (!PyArg_ParseTuple(args, "s", &name)) {
        return NULL;
    }
    igs_result_t result = igs_input_type(name);
    return PyLong_FromLong(result);
}

//igs_input_count
 PyObject * getInputsNumber_wrapper(PyObject * self, PyObject * args)
{
     int result = igs_input_count();
    return PyLong_FromLong(result);
}


//igs_input_list
 PyObject * igs_getInputsList_wrapper(PyObject * self, PyObject * args)
{
    long nbOfElements;
    PyObject * ret;

    char **result = igs_input_list(&nbOfElements);

    // build the resulting list into a Python object.
    ret = PyList_New(nbOfElements);
    int i ;
    for (i = 0; i < nbOfElements; i++){
        //set items of the python list one by one
        PyList_SetItem(ret, i, Py_BuildValue("s",result[i]));
    }
    return ret;
}


//igs_input_exists
 PyObject * checkInputExistence_wrapper(PyObject * self, PyObject * args)
{
    char * name;
    // parse the name of the input
    if (!PyArg_ParseTuple(args, "s", &name)) {
        return NULL;
    }
    if (igs_input_exists(name)) {
          Py_RETURN_TRUE;
    } else{
        Py_RETURN_FALSE;
    }
}


//igs_input_create
 PyObject * createInput_wrapper(PyObject * self, PyObject * args)
{
    char * name;
    igs_iop_value_type_t type;
    int _type;
    PyObject *value;
    long size;
    int result;

    // parse and cast all the arguments for igs_input_create
    if (!PyArg_ParseTuple(args, "siO", &name, &_type, &value)) {
        return NULL;
    }
    type = (igs_iop_value_type_t)(_type);
    if (value == Py_None){
        result = igs_input_create(name, type, NULL, 0);

    }else if (type == IGS_STRING_T){
        char *value_c;
        if (!PyArg_ParseTuple(args, "sis", &name, &_type, &value_c)) {
            return NULL;
        }
        result = igs_input_create(name, type, value_c, strlen(value_c));
    }else if (type == IGS_INTEGER_T){
        int value_c;
        if (!PyArg_ParseTuple(args, "sii", &name, &_type, &value_c)) {
            return NULL;
        }
        result = igs_input_create(name, type, &value_c, sizeof(int));
    }else if (type == IGS_DOUBLE_T){
        double value_c;
        if (!PyArg_ParseTuple(args, "sid", &name, &_type, &value_c)) {
            return NULL;
        }
        result = igs_input_create(name, type, &value_c, sizeof(double));
    }else if (type == IGS_BOOL_T){
        if (value == Py_True)
        {
            bool value = true;
            result = igs_input_create(name, type, &value, sizeof(bool));
        }
        else
        {
            bool value = false;
            result = igs_input_create(name, type, &value, sizeof(bool));
        }
    }else{
        result = igs_input_create(name, type, value, (size_t)PyObject_Size(value));
    }
    return PyLong_FromLong(result);
}
