//
//  definition.h
//  ingescapeWrapp
//
//  Created by vaugien on 12/02/2018.
//  Copyright © 2018 ingenuity. All rights reserved.
//
#include "definition.h"
#include <stdio.h>
#include <ingescape/ingescape.h>
#include "uthash/utlist.h"
#include "observecallback.h"


//igs_definition_load_str
 PyObject * loadDefinition_wrapper(PyObject * self, PyObject * args)
{
    char * json_str;
    int result;
    // parse arguments : get the char* sent in python in json_str
    if (!PyArg_ParseTuple(args, "s", &json_str)) {
        return NULL;
    }
    result = igs_definition_load_str(json_str);
    // build the resulting int into a Python object.
    return PyLong_FromLong(result);
}

//igs_definition_load_file
 PyObject * loadDefinitionFromPath_wrapper(PyObject * self, PyObject * args)
{
    char* file_path;
    int result;
    // parse the file path file_path argument
    if (!PyArg_ParseTuple(args, "s", &file_path)) {
        return NULL;
    }
    result = igs_definition_load_file(file_path);
    // build the resulting int into a Python object.
    return PyLong_FromLong(result);
}

//igs_clear_definition
 PyObject * clearDefinition_wrapper(PyObject * self, PyObject * args)
{
    igs_clear_definition();
    observe_iop_cb_t *actuel = NULL;
    DL_FOREACH(observe_iop_cbList, actuel)
    {
        DL_DELETE(observe_iop_cbList, actuel);
        Py_CLEAR(actuel->callback);
        Py_CLEAR(actuel->my_data);
        free(actuel->nameArg);
        free(actuel);
    }
    return PyLong_FromLong(0);
}

//igs_definition_json
 PyObject * getDefinition_wrapper(PyObject * self, PyObject * args)
{
    char * result;
    PyObject * ret;
    result = igs_definition_json();
    // build the resulting string into a Python object.
    if(result!=NULL){
        return Py_BuildValue("s",result);
    }else{
        return Py_BuildValue("s","");
    }
}

//igs_definition_description
 PyObject * getDefinitionDescription_wrapper(PyObject * self, PyObject * args)
{
    char * result;
    PyObject * ret;
    result = igs_definition_description();
    // build the resulting string into a Python object.
   if(result!=NULL){
        return Py_BuildValue("s",result);
    }else{
        return Py_BuildValue("s","");
    }
}

//igs_definition_version
 PyObject * getDefinitionVersion_wrapper(PyObject * self, PyObject * args)
{
    char * result;
    PyObject * ret;
    result = igs_definition_version();
    // build the resulting string into a Python object.
    if(result!=NULL){
        return Py_BuildValue("s",result);
    }else{
        return Py_BuildValue("s","");
    }
}


//setDefinitionDescription
 PyObject * setDefinitionDescription_wrapper(PyObject * self, PyObject * args)
{
    char* description ;
    // parse arguments
    if (!PyArg_ParseTuple(args, "s", &description)) {
        return NULL;
    }
    igs_definition_set_description(description);
    return PyLong_FromLong(0);
}

//setDefinitionVersion
 PyObject * setDefinitionVersion_wrapper(PyObject * self, PyObject * args)
{
    char* version ;
    // parse arguments
    if (!PyArg_ParseTuple(args, "s", &version)) {
        return NULL;
    }
    igs_definition_set_version(version);
    return PyLong_FromLong(0);
}

//igs_input_remove
 PyObject * removeInput_wrapper(PyObject * self, PyObject * args)
{
    char* name ;
    int result;
    // parse arguments
    if (!PyArg_ParseTuple(args, "s", &name)) {
        return NULL;
    }
    result = igs_input_remove(name);
    if(result == IGS_SUCCESS)
    {
        observe_iop_cb_t *actuel = NULL;
        DL_FOREACH(observe_iop_cbList, actuel)
        {
            if (streq(actuel->nameArg, name)
                && (actuel->iopType == IGS_INPUT_T))
            {
                DL_DELETE(observe_iop_cbList, actuel);
                Py_CLEAR(actuel->callback);
                Py_CLEAR(actuel->my_data);
                free(actuel->nameArg);
                free(actuel);
            }
        }
    }
    // build the resulting int into a Python object.
    return PyLong_FromLong(result);
}


//igs_output_remove
 PyObject * removeOutput_wrapper(PyObject * self, PyObject * args)
{
    char* name ;
    int result;
    // parse arguments
    if (!PyArg_ParseTuple(args, "s", &name)) {
        return NULL;
    }
    result = igs_output_remove(name);
    if(result == IGS_SUCCESS)
    {
        observe_iop_cb_t *actuel = NULL;
        DL_FOREACH(observe_iop_cbList, actuel)
        {
            if (streq(actuel->nameArg, name)
                && (actuel->iopType == IGS_OUTPUT_T))
            {
                DL_DELETE(observe_iop_cbList, actuel);
                Py_CLEAR(actuel->callback);
                Py_CLEAR(actuel->my_data);
                free(actuel->nameArg);
                free(actuel);
            }
        }
    }
    // build the resulting int into a Python object.
    return PyLong_FromLong(result);
}

//igs_parameter_remove
 PyObject * removeParameter_wrapper(PyObject * self, PyObject * args)
{
    char* name ;
    int result;
    // parse arguments
    if (!PyArg_ParseTuple(args, "s", &name)) {
        return NULL;
    }
    result = igs_parameter_remove(name);
    if(result == IGS_SUCCESS)
    {
        observe_iop_cb_t *actuel = NULL;
        DL_FOREACH(observe_iop_cbList, actuel)
        {
            if (streq(actuel->nameArg, name)
                && (actuel->iopType == IGS_PARAMETER_T))
            {
                DL_DELETE(observe_iop_cbList, actuel);
                Py_CLEAR(actuel->callback);
                Py_CLEAR(actuel->my_data);
                free(actuel->nameArg);
                free(actuel);
            }
        }
    }
    // build the resulting int into a Python object.
    return PyLong_FromLong(result);
}
