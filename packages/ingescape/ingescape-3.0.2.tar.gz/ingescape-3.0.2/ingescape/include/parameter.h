//
//  parameter.h
//  ingescapeWrapp
//
//  Created by vaugien on 06/04/2018.
//  Copyright © 2018 ingenuity. All rights reserved.
//

#ifndef parameter_h
#define parameter_h

#include <Python.h>

PyDoc_STRVAR(
             readParameterAsBoolDoc,
             "igs_parameter_bool(nameOfParameter)\n"
             "--\n"
             "\n"
             "read the value of 'nameOfParameter as a Bool");

PyDoc_STRVAR(
             readParameterAsIntDoc,
             "igs_parameter_int(nameOfParameter)\n"
             "--\n"
             "\n"
             "read the value of 'nameOfParameter as an Int");

PyDoc_STRVAR(
             readParameterAsDoubleDoc,
             "igs_parameter_double(nameOfParameter)\n"
             "--\n"
             "\n"
             "read the value of 'nameOfParameter as a Double");

PyDoc_STRVAR(
             readParameterAsStringDoc,
             "igs_parameter_string(nameOfParameter)\n"
             "--\n"
             "\n"
             "read the value of 'nameOfParameter as a String");

PyDoc_STRVAR(
             writeParameterAsBoolDoc,
             "igs_parameter_set_bool(nameOfParameter, value)\n"
             "--\n"
             "\n"
             "write the value of 'nameOfParameter' as 'value'");

PyDoc_STRVAR(
             writeParameterAsIntDoc,
             "igs_parameter_set_int(nameOfParameter, value)\n"
             "--\n"
             "\n"
             "write the value of 'nameOfParameter' as 'value'");

PyDoc_STRVAR(
             writeParameterAsDoubleDoc,
             "igs_parameter_set_double(nameOfParameter, value)\n"
             "--\n"
             "\n"
             "write the value of 'nameOfParameter' as value");

PyDoc_STRVAR(
             writeParameterAsStringDoc,
             "igs_parameter_set_string(nameOfParameter, value)\n"
             "--\n"
             "\n"
             "write the value of 'nameOfParameter' as value");

PyDoc_STRVAR(
             getTypeForParameterDoc,
             "igs_parameter_type(nameOfParameter)\n"
             "--\n"
             "\n"
             "return the type of the Parameter 'nameOfParameter'\n0 the iop does not exist.\n-1 the definition live is NULL.\n If an error occurs a igs_debug will be set.");

PyDoc_STRVAR(
             getParametersNumberDoc,
             "igs_parameter_count()\n"
             "--\n"
             "\n"
             "return the number of Parameters for the agent");

PyDoc_STRVAR(
             getParametersListDoc,
             "igs_parameter_list(numberOfParameters)\n"
             "--\n"
             "\n"
             "return a list containing the name of Parameters");

PyDoc_STRVAR(
             checkParameterExistenceDoc,
             "igs_parameter_exists(nameOfParameter)\n"
             "--\n"
             "\n"
             "return True if the Parameter exist");

PyDoc_STRVAR(
             createParameterDoc,
             "igs_parameter_create(nameOfParameter, value_type, value, size)\n"
             "--\n"
             "\n"
             "Create and add an Parameter for the agent.\n"
             "return The error.\n 0 is ok\n");

//igs_readparameterAsBool
 PyObject * readParameterAsBool_wrapper(PyObject * self, PyObject * args);

//igs_parameter_int
 PyObject * readParameterAsInt_wrapper(PyObject * self, PyObject * args);

//igs_parameter_double
 PyObject * readParameterAsDouble_wrapper(PyObject * self, PyObject * args);

//igs_parameter_string
 PyObject * readParameterAsString_wrapper(PyObject * self, PyObject * args);

//igs_parameter_set_bool
 PyObject * writeParameterAsBool_wrapper(PyObject * self, PyObject * args);

//igs_parameter_set_int
 PyObject * writeParameterAsInt_wrapper(PyObject * self, PyObject * args);

//igs_parameter_set_double
 PyObject * writeParameterAsDouble_wrapper(PyObject * self, PyObject * args);

//igs_parameter_set_string
 PyObject * writeParameterAsString_wrapper(PyObject * self, PyObject * args);

//igs_parameter_type
 PyObject * getTypeForParameter_wrapper(PyObject * self, PyObject * args);

//igs_parameter_count
 PyObject * getParametersNumber_wrapper(PyObject * self, PyObject * args);

//igs_parameter_list
 PyObject * igs_getParametersList_wrapper(PyObject * self, PyObject * args);

//igs_checkParametersExistence
 PyObject * checkParametersExistence_wrapper(PyObject * self, PyObject * args);

//igs_parameter_create
 PyObject * createParameter_wrapper(PyObject * self, PyObject * args);


#endif /* parameter_h */
