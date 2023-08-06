//
//  admin.h
//  ingescapeWrapp
//
//  Created by vaugien on 12/02/2018.
//  Copyright © 2018 ingenuity. All rights reserved.
//

#include "admin.h"
#include <stdio.h>
#include <ingescape/ingescape.h>


//wrapper for igs_set_command_line
PyObject * setCommandLine_wrapper(PyObject * self, PyObject * args)
{
    char * line;
    // parse and cast the line argument given in python
    if (!PyArg_ParseTuple(args, "s", &line)) {
        return NULL;
    }
    igs_set_command_line(line);
    return PyLong_FromLong(0);
}


//wrapper for igs_log_set_console
PyObject * setVerbose_wrapper(PyObject * self, PyObject * args)
{
    bool verbose;
    // parse and cast the verbose argument given in python
    if (!PyArg_ParseTuple(args, "b", &verbose)) {
        return NULL;
    }
    igs_log_set_console(verbose);
    return PyLong_FromLong(0);
}

//wrapper for igs_getVerbose
PyObject * getVerbose_wrapper(PyObject * self, PyObject * args)
{
    bool verbose;
    verbose = igs_log_console();
    // build the resulting bool into a Python boolean and return it
     if(verbose){
        Py_RETURN_TRUE;
    }else{
        Py_RETURN_FALSE;
    }
}

//wrapper for igs_log_set_stream
PyObject * setLogStream_wrapper(PyObject * self, PyObject * args)
{
    bool stream;
    // parse and cast into a bool the stream argument given in python
    if (!PyArg_ParseTuple(args, "b", &stream)) {
        return NULL;
    }
    igs_log_set_stream(stream);
    return PyLong_FromLong(0);
}

//wrapper for igs_log_stream
PyObject * getLogStream_wrapper(PyObject * self, PyObject * args)
{
    bool stream;
    stream = igs_log_stream();
    // build the resulting bool into a Python boolean and return it
    if(stream){
        Py_RETURN_TRUE;
    }else{
        Py_RETURN_FALSE;
    }
}

//wrapper for igs_log_set_file
PyObject * setLogInFile_wrapper(PyObject * self, PyObject * args)
{
    bool useLogFile;
    PyObject *pathObject;
     // parse and cast into a bool the useLogFile argument given in python
    if (!PyArg_ParseTuple(args, "bO", &useLogFile, &pathObject)) {
        return NULL;
    }
    if(pathObject != Py_None)
    {
        char *path_c;
        if (!PyArg_ParseTuple(args, "bO", &useLogFile, &path_c)) {
            return NULL;
        }
        igs_log_set_file(useLogFile, path_c);
    }
    else
    {
        igs_log_set_file(useLogFile, NULL);
    }
    return PyLong_FromLong(0);
}

//wrapper for igs_log_file
PyObject * getLogInFile_wrapper(PyObject * self, PyObject * args)
{
    bool useLogFile;
    useLogFile = igs_log_file();
    // build the resulting bool into a Python boolean and return it
    if(useLogFile){
        Py_RETURN_TRUE;
    }else{
        Py_RETURN_FALSE;
    }
}

//wrapper for igs_log_set_console_color
PyObject * setUseColorVerbose_wrapper(PyObject * self, PyObject * args)
{
    bool useColorVerbose;
    // parse and cast into a bool the useColorVerbose argument given in python
    if (!PyArg_ParseTuple(args, "b", &useColorVerbose)) {
        return NULL;
    }
    igs_log_set_console_color(useColorVerbose);
    return PyLong_FromLong(0);
}

//wrapper for igs_log_console_color
PyObject * getUseColorVerbose_wrapper(PyObject * self, PyObject * args)
{
    bool useColorVerbose;
    useColorVerbose = igs_log_console_color();
    // build the resulting bool into a Python boolean and return it
    if(useColorVerbose){
        Py_RETURN_TRUE;
    }else{
        Py_RETURN_FALSE;
    }
}

//wrapper for igs_log_set_file_path
PyObject * setLogPath_wrapper(PyObject * self, PyObject * args)
{
    char * path;
    // parse and cast into a bool the useColorVerbose argument given in python
    if (!PyArg_ParseTuple(args, "s", &path)) {
        return NULL;
    }
    igs_log_set_file_path(path);
    return PyLong_FromLong(0);
}

//wrapper for igs_log_file_path
PyObject * getLogPath_wrapper(PyObject * self, PyObject * args)
{
    char * path;
    PyObject *ret;
    path = igs_log_file_path();
    // build the resulting char* into a Python bytes and return it
    if(path != NULL){
        return Py_BuildValue("s", path);
    }else{
        return Py_BuildValue("s","");;
    }
}


//wrapper for igs_is_started
PyObject * isStarted_wrapper(PyObject * self, PyObject * args)
{
    if (igs_is_started()){
        Py_RETURN_TRUE;
    }else{
        Py_RETURN_FALSE;
    }
}


//wrapper for igs_definition_set_path
PyObject * setDefinitionPath_wrapper(PyObject * self, PyObject * args)
{
    char * path;
    // parse and cast into a char* the string path given in python
    if (!PyArg_ParseTuple(args, "s", &path)) {
        return NULL;
    }
    igs_definition_set_path(path);
    return PyLong_FromLong(0);
}

//wrapper for igs_mapping_set_path
PyObject * setMappingPath_wrapper(PyObject * self, PyObject * args)
{
    char * path;
    // parse and cast into a char* the string path given in python
    if (!PyArg_ParseTuple(args, "s", &path)) {
        return NULL;
    }
    igs_mapping_set_path(path);
    return PyLong_FromLong(0);
}

//wrapper for igs_definition_save
PyObject * writeDefinitionToPath_wrapper(PyObject * self, PyObject * args)
{
    igs_definition_save();
    return PyLong_FromLong(0);
}


//wrapper for igs_mapping_save
PyObject * writeMappingToPath_wrapper(PyObject * self, PyObject * args)
{
    igs_mapping_save();
    return PyLong_FromLong(0);
}

//wrapper for igs_version
PyObject * version_wrapper(PyObject * self, PyObject * args)
{
    int version;
    version = igs_version();
    return PyLong_FromLong(version);
}

//wrapper for igs_protocol
PyObject * protocol_wrapper(PyObject * self, PyObject * args)
{
    int protocol;
    protocol = igs_protocol();
    return PyLong_FromLong(protocol);
}

//wrapper for igs_trace
PyObject * trace_wrapper(PyObject * self, PyObject * args)
{
    char * log;
    // parse and cast into a bool the useColorVerbose argument given in python
    if (!PyArg_ParseTuple(args, "s", &log)) {
        return NULL;
    }

    PyFrameObject* frame = PyEval_GetFrame();
    Py_INCREF(frame);
    PyObject *function = frame->f_code->co_name;
    Py_INCREF(function);
    Py_DECREF(frame);

    PyObject* funcTuple = Py_BuildValue("(O)", function);
    Py_DECREF(function);
    if (!funcTuple) return 0;
    const char* functionStr = 0;
    if (!PyArg_ParseTuple(funcTuple, "s", &functionStr)) {
        Py_DECREF(args);
        return 0;
    }

    /* s now points to a const char* - use it, delete args when done */

    Py_DECREF(funcTuple);

    if(strcmp(functionStr, "<module>") == 0){
        igs_log(IGS_LOG_TRACE, "main", "%s", log);
    }else{
        igs_log(IGS_LOG_DEBUG, functionStr, "%s", log);
    }
    return PyLong_FromLong(0);
}

PyObject * debug_wrapper(PyObject * self, PyObject * args)
{
    char * log;

    // parse and cast into a bool the useColorVerbose argument given in python
    if (!PyArg_ParseTuple(args, "s", &log)) {
        return NULL;
    }

    PyFrameObject* frame = PyEval_GetFrame();
    Py_INCREF(frame);
    PyObject *function = frame->f_code->co_name;
    Py_INCREF(function);
    Py_DECREF(frame);

    PyObject* funcTuple = Py_BuildValue("(O)", function);
    Py_DECREF(function);
    if (!funcTuple) return 0;
    const char* functionStr = 0;
    if (!PyArg_ParseTuple(funcTuple, "s", &functionStr)) {
        Py_DECREF(args);
        return 0;
    }

    /* s now points to a const char* - use it, delete args when done */

    Py_DECREF(funcTuple);

    if(strcmp(functionStr, "<module>") == 0){
        igs_log(IGS_LOG_DEBUG, "main", "%s", log);
    }else{
        igs_log(IGS_LOG_DEBUG, functionStr, "%s", log);
    }
    return PyLong_FromLong(0);
}


PyObject * info_wrapper(PyObject * self, PyObject * args)
{
    char * log;

    // parse and cast into a bool the useColorVerbose argument given in python
    if (!PyArg_ParseTuple(args, "s", &log)) {
        return NULL;
    }

    PyFrameObject* frame = PyEval_GetFrame();
    Py_INCREF(frame);
    PyObject *function = frame->f_code->co_name;
    Py_INCREF(function);
    Py_DECREF(frame);

    PyObject* funcTuple = Py_BuildValue("(O)", function);
    Py_DECREF(function);
    if (!funcTuple) return 0;
    const char* functionStr = 0;
    if (!PyArg_ParseTuple(funcTuple, "s", &functionStr)) {
        Py_DECREF(args);
        return 0;
    }

    /* s now points to a const char* - use it, delete args when done */

    Py_DECREF(funcTuple);

    if(strcmp(functionStr, "<module>") == 0){
        igs_log(IGS_LOG_INFO, "main", "%s", log);
    }else{
        igs_log(IGS_LOG_INFO, functionStr, "%s", log);
    }
    return PyLong_FromLong(0);
}


PyObject * warn_wrapper(PyObject * self, PyObject * args)
{
    char * log;

    // parse and cast into a bool the useColorVerbose argument given in python
    if (!PyArg_ParseTuple(args, "s", &log)) {
        return NULL;
    }

    PyFrameObject* frame = PyEval_GetFrame();
    Py_INCREF(frame);
    PyObject *function = frame->f_code->co_name;
    Py_INCREF(function);
    Py_DECREF(frame);

    PyObject* funcTuple = Py_BuildValue("(O)", function);
    Py_DECREF(function);
    if (!funcTuple) return 0;
    const char* functionStr = 0;
    if (!PyArg_ParseTuple(funcTuple, "s", &functionStr)) {
        Py_DECREF(args);
        return 0;
    }

    /* s now points to a const char* - use it, delete args when done */

    Py_DECREF(funcTuple);

    if(strcmp(functionStr, "<module>") == 0){
        igs_log(IGS_LOG_WARN, "main", "%s", log);
    }else{
        igs_log(IGS_LOG_WARN, functionStr, "%s", log);
    }
    return PyLong_FromLong(0);
}

PyObject * error_wrapper(PyObject * self, PyObject * args)
{
    char * log;

    // parse and cast into a bool the useColorVerbose argument given in python
    if (!PyArg_ParseTuple(args, "s", &log)) {
        return NULL;
    }

    PyFrameObject* frame = PyEval_GetFrame();
    Py_INCREF(frame);
    PyObject *function = frame->f_code->co_name;
    Py_INCREF(function);
    Py_DECREF(frame);

    PyObject* funcTuple = Py_BuildValue("(O)", function);
    Py_DECREF(function);
    if (!funcTuple) return 0;
    const char* functionStr = 0;
    if (!PyArg_ParseTuple(funcTuple, "s", &functionStr)) {
        Py_DECREF(args);
        return 0;
    }

    /* s now points to a const char* - use it, delete args when done */

    Py_DECREF(funcTuple);

    if(strcmp(functionStr, "<module>") == 0){
        igs_log(IGS_LOG_ERROR, "main", "%s", log);
    }else{
        igs_log(IGS_LOG_ERROR, functionStr, "%s", log);
    }
    return PyLong_FromLong(0);
}

PyObject * fatal_wrapper(PyObject * self, PyObject * args)
{
    char * log;

    // parse and cast into a bool the useColorVerbose argument given in python
    if (!PyArg_ParseTuple(args, "s", &log)) {
        return NULL;
    }

    PyFrameObject* frame = PyEval_GetFrame();
    Py_INCREF(frame);
    PyObject *function = frame->f_code->co_name;
    Py_INCREF(function);
    Py_DECREF(frame);

    PyObject* funcTuple = Py_BuildValue("(O)", function);
    Py_DECREF(function);
    if (!funcTuple) return 0;
    const char* functionStr = 0;
    if (!PyArg_ParseTuple(funcTuple, "s", &functionStr)) {
        Py_DECREF(args);
        return PyLong_FromLong(1);
    }

    /* s now points to a const char* - use it, delete args when done */

    Py_DECREF(funcTuple);
    if(strcmp(functionStr, "<module>") == 0){
        igs_log(IGS_LOG_FATAL, "main", "%s", log);
    }else{
        igs_log(IGS_LOG_FATAL, functionStr, "%s", log);
    }
    return PyLong_FromLong(0);
}

PyObject * setLogLevel_wrapper(PyObject * self, PyObject * args)
{
    int logLevel;
    // parse and cast into a bool the useColorVerbose argument given in python
    if (!PyArg_ParseTuple(args, "i", &logLevel)) {
        return NULL;
    }
    igs_log_set_console_level(logLevel);
    return PyLong_FromLong(0);
}

PyObject * getLogLevel_wrapper(PyObject * self, PyObject * args)
{
    int log = igs_log_console_level();
    return PyLong_FromLong(log);
}

PyObject * igs_getNetdevicesList_wrapper(PyObject * self, PyObject * args)
{
    int nbList;
    char **resultList = igs_net_devices_list(&nbList);

    // build the resulting list into a Python object.
    PyObject *ret = PyList_New(nbList);
    int i ;
    for (i = 0; i < nbList; i++){
        //set items of the python list one by one
        PyList_SetItem(ret, i, Py_BuildValue("s",resultList[i]));
    }
    igs_free_net_devices_list(resultList, nbList);
    return ret;
}

PyObject * igs_getNetadressesList_wrapper(PyObject * self, PyObject * args)
{
    int nbList;
    char **resultList = igs_net_addresses_list(&nbList);

    // build the resulting list into a Python object.
    PyObject *ret = PyList_New(nbList);
    int i ;
    for (i = 0; i < nbList; i++){
        //set items of the python list one by one
        PyList_SetItem(ret, i, Py_BuildValue("s",resultList[i]));
    }
    igs_free_net_addresses_list(resultList, nbList);
    return ret;
}

PyObject * igs_competeInElection_wrapper(PyObject * self, PyObject * args)
{
    char * electionName;
    if (!PyArg_ParseTuple(args, "s", &electionName)) {
        return NULL;
    }
    int result = igs_election_join(electionName);

    return PyLong_FromLong(result);
}

PyObject * igs_leaveElection_wrapper(PyObject * self, PyObject * args)
{
    char * electionName;
    if (!PyArg_ParseTuple(args, "s", &electionName)) {
        return NULL;
    }
    int result = igs_election_leave(electionName);

    return PyLong_FromLong(result);
}
