//
//  data.h
//  ingescapeWrapp
//
//  Created by vaugien on 14/02/2018.
//  Copyright © 2018 ingenuity. All rights reserved.
//
#include "data.h"
#include <stdio.h>
#include <ingescape/ingescape.h>


//igs_output_set_data
 PyObject * writeOutputAsData_wrapper(PyObject * self, PyObject * args)
{
    char * name;
    Py_buffer buf;
    int  result;
    // parse and cast the name, data and size argument given in python
    if (!PyArg_ParseTuple(args, "sy*", &name, &buf)) {
        return NULL;
    }
    result = igs_output_set_data(name, buf.buf, (size_t)buf.len);
    return PyLong_FromLong(result);
}


//igs_output_data
 PyObject * readOutputAsData_wrapper(PyObject * self, PyObject * args)
{
    char *name;
    void *myData;
    size_t valueSize;
    
    // parse and cast the name argument given in python
    if (!PyArg_ParseTuple(args, "s", &name)) {
        return NULL;
    }

    igs_output_data(name, &myData, &valueSize);
    
    // Cast the data read and the valueSize into a PyTuple and return it
    PyObject *ret = Py_BuildValue("y#", myData, valueSize);
    return ret;
}

//igs_input_data
 PyObject * readInputAsData_wrapper(PyObject * self, PyObject * args)
{
    char *name;
    void *myData;
    size_t valueSize;
    
    // parse and cast the name argument given in python
    if (!PyArg_ParseTuple(args, "s", &name)) {
        return NULL;
    }

    igs_input_data(name, &myData, &valueSize);
    
    // Cast the data read and the valueSize into a PyTuple and return it
    PyObject *ret = Py_BuildValue("y#", myData, valueSize);
    return ret;
}

//igs_input_set_data
 PyObject * writeInputAsData_wrapper(PyObject * self, PyObject * args)
{
    char * name;
    Py_buffer buf;
    int  result;
    
    // parse and cast the name, data and size argument given in python
    if (!PyArg_ParseTuple(args, "sy*", &name, &buf)) {
        return NULL;
    }
    result = igs_input_set_data(name, buf.buf, (size_t)buf.len);
    return PyLong_FromLong(result);
}


//igs_parameter_set_data
 PyObject * writeParameterAsData_wrapper(PyObject * self, PyObject * args)
{
    char * name;
    Py_buffer buf;
    int  result;
    
    // parse and cast the name, data and size argument given in python
    if (!PyArg_ParseTuple(args, "sy*", &name, &buf)) {
        return NULL;
    }
    result = igs_parameter_set_data(name, buf.buf, (size_t)buf.len);
    return PyLong_FromLong(result);
}



//igs_parameter_data
 PyObject * readParameterAsData_wrapper(PyObject * self, PyObject * args)
{
    char *name;
    void *myData;
    size_t valueSize;
    
    // parse and cast the name argument given in python
    if (!PyArg_ParseTuple(args, "s", &name)) {
        return NULL;
    }

    igs_parameter_data(name, &myData, &valueSize);
    
    // Cast the data read and the valueSize into a PyTuple and return it
    PyObject *ret = Py_BuildValue("y#", myData, &valueSize);
    return ret;
}




