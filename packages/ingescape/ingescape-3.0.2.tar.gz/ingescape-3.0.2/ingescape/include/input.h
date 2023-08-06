//
//  input.h
//  ingescapeWrapp
//
//  Created by vaugien on 06/04/2018.
//  Copyright © 2018 ingenuity. All rights reserved.
//

#ifndef input_h
#define input_h
#define PY_SSIZE_T_CLEAN
#include <Python.h>

PyDoc_STRVAR(
             readInputAsBoolDoc,
             "igs_input_bool(nameOfInput)\n"
             "--\n"
             "\n"
             "read the value of 'nameOfInput' as a Bool");

PyDoc_STRVAR(
             readInputAsIntDoc,
             "igs_input_int(nameOfInput)\n"
             "--\n"
             "\n"
             "read the value of 'nameOfInput' as an Int");

PyDoc_STRVAR(
             readInputAsDoubleDoc,
             "igs_input_double(nameOfInput)\n"
             "--\n"
             "\n"
             "read the value of 'nameOfInput' as a Double");

PyDoc_STRVAR(
             readInputAsStringDoc,
             "igs_input_string(nameOfInput)\n"
             "--\n"
             "\n"
             "read the value of 'nameOfInput' as a String");



PyDoc_STRVAR(
             writeInputAsBoolDoc,
             "igs_input_set_bool(nameOfInput, value)\n"
             "--\n"
             "\n"
             "write the value of 'nameOfInput' as 'value'");

PyDoc_STRVAR(
             writeInputAsIntDoc,
             "igs_input_set_int(nameOfInput, value)\n"
             "--\n"
             "\n"
             "write the value of 'nameOfInput' as 'value'");

PyDoc_STRVAR(
             writeInputAsDoubleDoc,
             "igs_input_set_double(nameOfInput, value)\n"
             "--\n"
             "\n"
             "write the value of 'nameOfInput' as value");

PyDoc_STRVAR(
             writeInputAsStringDoc,
             "igs_input_set_string(nameOfInput, value)\n"
             "--\n"
             "\n"
             "write the value of 'nameOfInput' as value");

PyDoc_STRVAR(
             writeInputAsImpulsionDoc,
             "igs_input_set_impulsion(nameOfInput)\n"
             "--\n"
             "\n"
             "write the value of 'nameOfInput' as an impulsion");

PyDoc_STRVAR(
             getTypeForInputDoc,
             "igs_input_type(nameOfInput)\n"
             "--\n"
             "\n"
             "return the type of the input 'nameOfInput' \n-1 the definition live is NULL.\n If an error occurs a igs_debug will be set.");

PyDoc_STRVAR(
             getInputsNumberDoc,
             "igs_input_count()\n"
             "--\n"
             "\n"
             "return the number of inputs for the agent");

PyDoc_STRVAR(
             getInputsListDoc,
             "igs_input_list(numberOfInputs)\n"
             "--\n"
             "\n"
             "return a list containing the name of inputs");

PyDoc_STRVAR(
             checkInputExistenceDoc,
             "igs_input_exists(nameOfInput)\n"
             "--\n"
             "\n"
             "return True if the input exist");

PyDoc_STRVAR(
             createInputDoc,
             "igs_input_create(nameOfInput, value_type, value, size)\n"
             "--\n"
             "\n"
             "Create and add an input for the agent.\n"
             "return The error.\n 0 is ok\n");

//igs_input_bool
 PyObject * readInputAsBool_wrapper(PyObject * self, PyObject * args);

//igs_input_int
 PyObject * readInputAsInt_wrapper(PyObject * self, PyObject * args);

//igs_input_double
 PyObject * readInputAsDouble_wrapper(PyObject * self, PyObject * args);

//igs_readInputAsStirng
 PyObject * readInputAsString_wrapper(PyObject * self, PyObject * args);

//igs_input_set_bool
 PyObject * writeInputAsBool_wrapper(PyObject * self, PyObject * args);

//igs_input_set_int
 PyObject * writeInputAsInt_wrapper(PyObject * self, PyObject * args);

//igs_input_set_double
 PyObject * writeInputAsDouble_wrapper(PyObject * self, PyObject * args);

//igs_input_set_string
 PyObject * writeInputAsString_wrapper(PyObject * self, PyObject * args);

//igs_input_set_impulsion
 PyObject * writeInputAsImpulsion_wrapper(PyObject * self, PyObject * args);

//igs_input_type
 PyObject * getTypeForInput_wrapper(PyObject * self, PyObject * args);

//igs_input_count
 PyObject * getInputsNumber_wrapper(PyObject * self, PyObject * args);

//igs_input_list
 PyObject * igs_getInputsList_wrapper(PyObject * self, PyObject * args);

//igs_input_exists
 PyObject * checkInputExistence_wrapper(PyObject * self, PyObject * args);

//igs_input_create
 PyObject * createInput_wrapper(PyObject * self, PyObject * args);


#endif /* input_h */
