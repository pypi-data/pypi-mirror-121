//
//  definition.h
//  ingescapeWrapp
//
//  Created by vaugien on 06/04/2018.
//  Copyright © 2018 ingenuity. All rights reserved.
//

#ifndef definition_h
#define definition_h

#define PY_SSIZE_T_CLEAN
#include <Python.h>


PyDoc_STRVAR(
             loadDefinitionDoc,
             "igs_definition_load_str(jsonDefinition)\n"
             "--\n"
             "\n"
             "load definition in variable 'igs_definition_loaded' & copy in 'igs_internal_definition' from a json string\n"
             "return The error.\n 0 is ok\n");

PyDoc_STRVAR(
             loadDefinitionFromPathDoc,
             "igs_definition_load_file(path)\n"
             "--\n"
             "\n"
             "load definition in variable 'igs_definition_loaded' & copy in 'igs_internal_definition' from a file path\n"
             "return The error.\n 0 is ok\n");

PyDoc_STRVAR(
             clearDefinitionDoc,
             "igs_clear_definition()\n"
             "--\n"
             "\n"
             "Clear the internal definition of the agent.\n"
             "Free all members of the structure igs_definition_loaded & igs_internal_definition.\n"
             "But the pointer of these structure is not free and stay allocated.\n return 0 if ok\n");

PyDoc_STRVAR(
             getDefinitionDoc,
             "igs_definition_json()\n"
             "--\n"
             "\n"
             "the agent definition getter."
             "\n return The loaded definition string in json format (allocated).\n"
             "if igs_definition_loaded was not initialized raise SystemError.\n");

PyDoc_STRVAR(
             getDefinitionDescriptionDoc,
             "igs_definition_description()\n"
             "--\n"
             "\n"
             "the agent definition description getter."
             "\n return The loaded definition description string .\n"
             "If igs_definition_loaded was not initialized raise SystemError.\n");

PyDoc_STRVAR(
             getDefinitionVersionDoc,
             "igs_definition_version()\n"
             "--\n"
             "\n"
             "the agent definition version getter."
             "\n return The loaded definition version string .\n"
             "If igs_definition_loaded was not initialized raise SystemError.\n");

PyDoc_STRVAR(
             setDefinitionDescriptionDoc,
             "igs_definition_set_description(definitionDescription)\n"
             "--\n"
             "\n"
             "the agent definition description setter."
             "\n return The error.\n 0 is ok\n");

PyDoc_STRVAR(
             setDefinitionVersionDoc,
             "igs_definition_set_version(definitionVersion)\n"
             "--\n"
             "\n"
             "the agent definition version setter."
             "\n return The error.\n 0 is ok\n");

PyDoc_STRVAR(
             removeInputDoc,
             "igs_input_remove(inputName)\n"
             "--\n"
             "\n"
             "Remove and free an input for the agent.\n"
             "return The error.\n "
             "0 is ok\n");

PyDoc_STRVAR(
             removeOutputDoc,
             "igs_output_remove(OutputName)\n"
             "--\n"
             "\n"
             "Remove and free an Output for the agent.\n"
             "return The error.\n "
             "0 is ok\n");
             
PyDoc_STRVAR(
             removeParameterDoc,
             "igs_parameter_remove(ParameterName)\n"
             "--\n"
             "\n"
             "Remove and free an Parameter for the agent.\n"
             "return The error.\n "
             "0 is ok\n");


//igs_definition_load_str
 PyObject * loadDefinition_wrapper(PyObject * self, PyObject * args);

//igs_definition_load_file
 PyObject * loadDefinitionFromPath_wrapper(PyObject * self, PyObject * args);

//igs_clear_definition
 PyObject * clearDefinition_wrapper(PyObject * self, PyObject * args);

//igs_definition_json
 PyObject * getDefinition_wrapper(PyObject * self, PyObject * args);

//igs_definition_description
 PyObject * getDefinitionDescription_wrapper(PyObject * self, PyObject * args);

//igs_definition_version
 PyObject * getDefinitionVersion_wrapper(PyObject * self, PyObject * args);

//setDefinitionDescription
 PyObject * setDefinitionDescription_wrapper(PyObject * self, PyObject * args);

//setDefinitionVersion
 PyObject * setDefinitionVersion_wrapper(PyObject * self, PyObject * args);

//igs_input_remove
 PyObject * removeInput_wrapper(PyObject * self, PyObject * args);

//igs_output_remove
 PyObject * removeOutput_wrapper(PyObject * self, PyObject * args);

//igs_parameter_remove
 PyObject * removeParameter_wrapper(PyObject * self, PyObject * args);

#endif /* definition_h */
