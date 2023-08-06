//
//  output.h
//  ingescapeWrapp
//
//  Created by vaugien on 06/04/2018.
//  Copyright © 2018 ingenuity. All rights reserved.
//

#ifndef output_h
#define output_h

#include <Python.h>

PyDoc_STRVAR(
             readOutputAsBoolDoc,
             "igs_output_bool(nameOfOutput)\n"
             "--\n"
             "\n"
             "read the value of 'nameOfOutput as a Bool");

PyDoc_STRVAR(
             readOutputAsIntDoc,
             "igs_output_int(nameOfOutput)\n"
             "--\n"
             "\n"
             "read the value of 'nameOfOutput as an Int");

PyDoc_STRVAR(
             readOutputAsDoubleDoc,
             "igs_output_double(nameOfOutput)\n"
             "--\n"
             "\n"
             "read the value of 'nameOfOutput as a Double");

PyDoc_STRVAR(
             readOutputAsStringDoc,
             "igs_output_string(nameOfOutput)\n"
             "--\n"
             "\n"
             "read the value of 'nameOfOutput as a String");

PyDoc_STRVAR(
             writeOutputAsBoolDoc,
             "igs_output_set_bool(nameOfOutput, value)\n"
             "--\n"
             "\n"
             "write the value of 'nameOfOutput' as 'value'");

PyDoc_STRVAR(
             writeOutputAsIntDoc,
             "igs_output_set_int(nameOfOutput, value)\n"
             "--\n"
             "\n"
             "write the value of 'nameOfOutput' as 'value'");

PyDoc_STRVAR(
             writeOutputAsDoubleDoc,
             "igs_output_set_double(nameOfOutput, value)\n"
             "--\n"
             "\n"
             "write the value of 'nameOfOutput' as value");

PyDoc_STRVAR(
             writeOutputAsStringDoc,
             "igs_output_set_string(nameOfOutput, value)\n"
             "--\n"
             "\n"
             "write the value of 'nameOfOutput' as value");

PyDoc_STRVAR(
             writeOutputAsImpulsionDoc,
             "igs_output_set_impulsion(nameOfOutput)\n"
             "--\n"
             "\n"
             "write the value of 'nameOfOutput' as an impulsion");

PyDoc_STRVAR(
             getTypeForOutputDoc,
             "igs_output_type(nameOfOutput)\n"
             "--\n"
             "\n"
             "return the type of the Output 'nameOfOutput'\n-1 the definition live is NULL.\n If an error occurs a igs_debug will be set.");

PyDoc_STRVAR(
             getOutputsNumberDoc,
             "igs_output_count()\n"
             "--\n"
             "\n"
             "return the number of Outputs for the agent");

PyDoc_STRVAR(
             getOutputsListDoc,
             "igs_output_list(numberOfOutputs)\n"
             "--\n"
             "\n"
             "return a list containing the name of Outputs");

PyDoc_STRVAR(
             checkOutputExistenceDoc,
             "igs_output_exists(nameOfOutput)\n"
             "--\n"
             "\n"
             "return True if the Output exist");

PyDoc_STRVAR(
             createOutputDoc,
             "igs_output_create(nameOfOutput, value_type, value, size)\n"
             "--\n"
             "\n"
             "Create and add an Output for the agent.\n"
             "return The error.\n 0 is ok\n");

PyDoc_STRVAR(
             muteOutputDoc,
             "igs_output_mute(nameOfOutput)\n"
             "--\n"
             "\n"
             "Mute an Output of the agent.\n"
             "return The error.\n  0 is ok\n");

PyDoc_STRVAR(
             unmuteOutputDoc,
             "igs_output_unmute(nameOfOutput)\n"
             "--\n"
             "\n"
             "Unmute an Output of the agent.\n"
             "return The error.\n  0 is ok\n");

PyDoc_STRVAR(
             isOutputMutedDoc,
             "igs_output_is_muted(nameOfOutput)\n"
             "--\n"
             "\n"
             "Give the state of an agent output (mute/unmute).\n"
             "return true if muted else false");

//igs_output_bool
 PyObject * readOutputAsBool_wrapper(PyObject * self, PyObject * args);

//igs_output_int
 PyObject * readOutputAsInt_wrapper(PyObject * self, PyObject * args);

//igs_output_double
 PyObject * readOutputAsDouble_wrapper(PyObject * self, PyObject * args);

//igs_readOutputAsStirng
 PyObject * readOutputAsString_wrapper(PyObject * self, PyObject * args);

//igs_output_set_bool
 PyObject * writeOutputAsBool_wrapper(PyObject * self, PyObject * args);

//igs_output_set_int
 PyObject * writeOutputAsInt_wrapper(PyObject * self, PyObject * args);

//igs_output_set_double
 PyObject * writeOutputAsDouble_wrapper(PyObject * self, PyObject * args);

//igs_output_set_string
 PyObject * writeOutputAsString_wrapper(PyObject * self, PyObject * args);

//igs_output_set_impulsion
 PyObject * writeOutputAsImpulsion_wrapper(PyObject * self, PyObject * args);

//igs_output_type
 PyObject * getTypeForOutput_wrapper(PyObject * self, PyObject * args);

//igs_output_count
 PyObject * getOutputsNumber_wrapper(PyObject * self, PyObject * args);

//igs_output_list

 PyObject * igs_getOutputsList_wrapper(PyObject * self, PyObject * args);

//igs_output_exists
 PyObject * checkOutputExistence_wrapper(PyObject * self, PyObject * args);

//igs_output_mute
 PyObject * muteOutput_wrapper(PyObject * self, PyObject * args);

//igs_output_unmute
 PyObject * unmuteOutput_wrapper(PyObject * self, PyObject * args);

//igs_output_is_muted
 PyObject * isOutputMuted_wrapper(PyObject * self, PyObject * args);

//igs_output_create
 PyObject * createOutput_wrapper(PyObject * self, PyObject * args);

#endif /* output_h */
