//
//  data.h
//  ingescapeWrapp
//
//  Created by vaugien on 06/04/2018.
//  Copyright © 2018 ingenuity. All rights reserved.
//

#ifndef data_h
#define data_h

#define PY_SSIZE_T_CLEAN
#include <Python.h>

PyDoc_STRVAR(
             readInputAsDataDoc,
             "igs_input_data(nameOfInput)\n"
             "--\n"
             "\n"
             "read the value of 'nameOfInput as Data \n"
             "return a Tuple contaning the data serialized and the size of the data byte");

PyDoc_STRVAR(
             readOutputAsDataDoc,
             "igs_output_data(nameOfOutput)\n"
             "--\n"
             "\n"
             "read the value of 'nameOfOutput as Data \n"
             "return a Tuple contaning the data serialized and the size of the data byte");

PyDoc_STRVAR(
             readParameterAsDataDoc,
             "igs_parameter_data(nameOfParameter)\n"
             "--\n"
             "\n"
             "read the value of 'nameOfParameter as Data \n"
             "return a Tuple contaning the data serialized and the size of the data byte");


PyDoc_STRVAR(
             writeInputAsDataDoc,
             "igs_input_set_data(nameOfInput, dataSerialized, sizeOfDataSerialized)\n"
             "--\n"
             "\n"
             "write a value as data into an agent's input.\n" 
             "Return 0 if ok\n");

PyDoc_STRVAR(
             writeOutputAsDataDoc,
             "igs_output_set_data(nameOfOuput, dataSerialized, sizeOfDataSerialized)\n"
             "--\n"
             "\n"
             "write a value as data into an agent's Ouput.\n"
             "Return 0 if ok\n"); 

PyDoc_STRVAR(
             writeParameterAsDataDoc,
             "igs_parameter_set_data(nameOfParameter, dataSerialized, sizeOfDataSerialized)\n"
             "--\n"
             "\n"
             "write a value as data into an agent's Parameter.\n"
             "Return 0 if ok\n");

//igs_output_set_data
 PyObject * writeOutputAsData_wrapper(PyObject * self, PyObject * args);

//igs_output_data
 PyObject * readOutputAsData_wrapper(PyObject * self, PyObject * args);

//igs_input_data
 PyObject * readInputAsData_wrapper(PyObject * self, PyObject * args);

//igs_input_set_data
 PyObject * writeInputAsData_wrapper(PyObject * self, PyObject * args);

//igs_parameter_set_data
 PyObject * writeParameterAsData_wrapper(PyObject * self, PyObject * args);

//igs_parameter_data
 PyObject * readParameterAsData_wrapper(PyObject * self, PyObject * args);

#endif /* data_h */
