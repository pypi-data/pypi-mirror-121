//
//  service.c
//  ingescapeWrapp
//
//  Created by vaugien on 24/03/2020.
//  Copyright © 2021 ingenuity. All rights reserved.
//

#include "service.h"
#include <Python.h>
#include <ingescape/ingescape.h>
#include "uthash/utlist.h"

char *s_strndup (const char *str, size_t chars)
{
    size_t n = 0;
    char *buffer = (char *) malloc (chars + 1);
    if (buffer) {
        for (n = 0; ((n < chars) && (str[n] != 0)); n++)
            buffer[n] = str[n];
        buffer[n] = 0;
    }
    return buffer;
}


PyObject * sendCall_wrapper(PyObject * self, PyObject * args)
{
    igs_service_arg_t *argumentList = NULL;
    char* agentNameOrUUID;
    char *callName;
    char *token;
    PyObject *argTuple = NULL;

    if (PyTuple_Size(args) != 4){
        printf("Expect 4 arguments, %zu were given \n", PyTuple_Size(args));
        return PyLong_FromLong(-1);
    }
    int format = 0;
    if (PyArg_ParseTuple(args, "ssOz",&agentNameOrUUID, &callName, &argTuple, &token)) 
    {
        if(argTuple == NULL || argTuple == Py_None)
        {
            format = 0;
        }
        else if(PyTuple_Check(argTuple) && PyTuple_Size(argTuple) > 0)
        {
            format = 2;
        }
        else if(!PyTuple_Check(argTuple)){
            format = 1;
        }
    }
    int result;
    // Argument parsing
    if(format == 2)
    {
        size_t tupleArgumentSize = PyTuple_Size(argTuple);
        for (size_t index = 0; index < tupleArgumentSize; index++)
        {
            PyObject *newArgument = PyTuple_GetItem(argTuple, index);
            if(newArgument != Py_None)
            {
                if(PyLong_CheckExact(newArgument))
                {
                    igs_service_args_add_int(&argumentList, (int)PyLong_AsLong(newArgument));
                }
                else if(PyFloat_CheckExact(newArgument))
                {
                    igs_service_args_add_double(&argumentList, PyFloat_AsDouble(newArgument));
                }
                else if(PyBool_Check(newArgument))
                {
                    if(newArgument == Py_True)
                        igs_service_args_add_bool(&argumentList, true);
                    else
                        igs_service_args_add_bool(&argumentList, false);
                }
                else if(PyUnicode_Check(newArgument))
                {
                    Py_ssize_t size;
                    igs_service_args_add_string(&argumentList, PyUnicode_AsUTF8AndSize(newArgument, &size));
                }
                else
                {
                    igs_service_args_add_data(&argumentList, PyBytes_FromObject(newArgument), PyBytes_Size(newArgument));
                }
            }
        }
        result = igs_service_call(agentNameOrUUID, callName, &argumentList, token);
        igs_service_args_destroy(&argumentList);
    }else if (format == 1){
        if(argTuple != Py_None)
        {
            if(PyLong_CheckExact(argTuple))
            {
                igs_service_args_add_int(&argumentList, (int)PyLong_AsLong(argTuple));
            }
            else if(PyFloat_CheckExact(argTuple))
            {
                igs_service_args_add_double(&argumentList, PyFloat_AsDouble(argTuple));
            }
            else if(PyBool_Check(argTuple))
            {
                if(argTuple == Py_True)
                    igs_service_args_add_bool(&argumentList, true);
                else
                    igs_service_args_add_bool(&argumentList, false);
            }
            else if(PyUnicode_Check(argTuple))
            {
                Py_ssize_t size;
                igs_service_args_add_string(&argumentList, PyUnicode_AsUTF8AndSize(argTuple, &size));
            }
            else
            {
                igs_service_args_add_data(&argumentList, PyBytes_FromObject(argTuple), PyBytes_Size(argTuple));
            }
        }
        else
        {
            result = igs_service_call(agentNameOrUUID, callName, NULL, token);
            igs_service_args_destroy(&argumentList);
            return PyLong_FromLong(result);
        }
       
        result = igs_service_call(agentNameOrUUID, callName, &argumentList, token);
        igs_service_args_destroy(&argumentList);
    }else{
        result = igs_service_call(agentNameOrUUID, callName, NULL, token);
    }
    return PyLong_FromLong(result);
}

/* igs_service_remove
 *Function in c that wrapp the removeCall Function
 */
PyObject * removeCall_wrapper(PyObject * self, PyObject * args){
    char *name;
    int result;
    // parse arguments
    if (!PyArg_ParseTuple(args, "s", &name)) {
        return NULL;
    }
    result = igs_service_remove(name);
    return PyLong_FromLong(result);
}

/* igs_service_arg_add
 *Function in c that wrapp the addArgumentToCall function
 */
PyObject * addArgumentToCall_wrapper(PyObject * self, PyObject * args){
    char *callName;
    char *argName;
    int type;
    int result;
    // parse arguments
    if (!PyArg_ParseTuple(args, "ssi", &callName, &argName, &type)) {
        return PyLong_FromLong(-1);
    }
    result = igs_service_arg_add(callName, argName, type);
    return PyLong_FromLong(result);
}


/* igs_service_arg_remove
 *Function in c that wrapp the removeArgumentFromCall function
 */
PyObject * removeArgumentFromCall_wrapper(PyObject * self, PyObject * args){
    char *callName;
    char *argName;
    int result;
    // parse arguments
    if (!PyArg_ParseTuple(args, "ss", &callName, &argName)) {
        return PyLong_FromLong(-1);
    }
    result = igs_service_arg_remove(callName, argName);
    return PyLong_FromLong(result);
}

//igs_service_count
PyObject * getNumberOfCalls_wrapper(PyObject * self, PyObject * args)
{
    size_t result;
    result = igs_service_count();
    return PyLong_FromLong(result);
}

//igs_service_exists
PyObject * checkCallExistence_wrapper(PyObject * self, PyObject * args)
{
    char * name;
    if (!PyArg_ParseTuple(args, "s", &name)) {
        return NULL;
    }
    if (igs_service_exists(name)) {
        Py_RETURN_TRUE;
    }else{
        Py_RETURN_FALSE;
    }
}

//igs_service_list
PyObject * getCallsList_wrapper(PyObject * self, PyObject * args)
{
    PyObject * ret;

    size_t nbOfElements = igs_service_count();
    char **result = igs_service_list(&nbOfElements);

    // build the resulting list into a Python object.
    ret = PyTuple_New(nbOfElements);
    size_t i ;
    for (i = 0; i < nbOfElements; i++){
        //set items of the python list one by one
        PyTuple_SetItem(ret, i, Py_BuildValue("s",result[i]));
    }
    igs_free_services_list(result, nbOfElements);
    return ret;
}

//igs_getNumberOfArgumentForCall
PyObject * getNumberOfArgumentForCall_wrapper(PyObject * self, PyObject * args)
{
    char* callName;
    // parse the number of element
    if (!PyArg_ParseTuple(args, "s", &callName)) {
        return NULL;
    }
    size_t result = igs_service_args_count(callName);
    return PyLong_FromLong(result);
}

//igs_getArgumentListForCall
PyObject * getArgumentListForCall_wrapper(PyObject * self, PyObject * args)
{
    char* callName;

    // parse the number of element
    if (!PyArg_ParseTuple(args, "s", &callName)) {
        printf("Error parsing in getArgumentListForCall");
        return NULL;
    }

    igs_service_arg_t *firstElement = igs_service_args_first(callName);
    size_t nbOfElements = igs_service_args_count(callName);

    // build the resulting list into a Python object.
    PyObject *ret = PyTuple_New(nbOfElements);
    size_t index = 0;
    igs_service_arg_t *newArg = NULL;
    LL_FOREACH(firstElement, newArg){
        PyTuple_SetItem(ret, index, Py_BuildValue("(si)",newArg->name, newArg->type));
        index ++;
    }
    return ret;
}

//igs_service_arg_exists
PyObject * checkCallArgumentExistence_wrapper(PyObject * self, PyObject * args)
{
    char * callName;
    char * argName;
    if (!PyArg_ParseTuple(args, "ss", &callName, &argName)) {
        return NULL;
    }
    if (igs_service_arg_exists(callName, argName)) {
        Py_RETURN_TRUE;
    }else{
        Py_RETURN_FALSE;
    }
}

typedef struct callCallback {
    char *callName;      // name of the iop
    PyObject *call;     //observeCallback
    PyObject *arglist;  //argument of the callback
    struct callCallback *next;
    struct callCallback *prev;
}callCallback;
callCallback *callList = NULL;

void observeCall(const char *senderAgentName, const char *senderAgentUUID,
             const char *callName, igs_service_arg_t *firstArgument, size_t nbArgs,
             const char *token, void* myData){
    PyGILState_STATE d_gstate;
    d_gstate = PyGILState_Ensure();
    //run through all callbacks to execute them
    callCallback *actuel = NULL;
    DL_FOREACH(callList, actuel){
        if (strcmp(actuel->callName, callName) == 0){
            PyObject *tupleArgs = PyTuple_New(nbArgs);
            igs_service_arg_t *currentArg = NULL;
            size_t index = 0;
            LL_FOREACH(firstArgument, currentArg){
                switch(currentArg->type){
                    case IGS_BOOL_T:
                        if (currentArg->b){
                            PyTuple_SetItem(tupleArgs, index, Py_True);
                        }else{
                            PyTuple_SetItem(tupleArgs, index, Py_False);
                        }
                        break;
                    case IGS_INTEGER_T:
                        PyTuple_SetItem(tupleArgs, index, Py_BuildValue("i", currentArg->i));
                        break;
                    case IGS_DOUBLE_T:
                        PyTuple_SetItem(tupleArgs, index, Py_BuildValue("d", currentArg->d));
                        break;
                    case IGS_STRING_T:
                        PyTuple_SetItem(tupleArgs, index, Py_BuildValue("s", currentArg->c));
                        break;
                    case IGS_IMPULSION_T:
                        PyTuple_SetItem(tupleArgs, index, Py_None);
                        break;
                    case IGS_DATA_T:
                        PyTuple_SetItem(tupleArgs, index, Py_BuildValue("y#", currentArg->data, currentArg->size));
                        break;
                    case IGS_UNKNOWN_T:
                        break;
                }
                index ++;
            }
            // call python code
            PyObject *pyAgentName = Py_BuildValue("(sssOsO)", senderAgentName, senderAgentUUID, callName, tupleArgs, token, actuel->arglist);
            PyObject *KWARGS = NULL;
            PyObject_Call(actuel->call, pyAgentName, KWARGS);
            Py_XDECREF(pyAgentName);
            Py_XDECREF(KWARGS);
            break;
        }
    }
    PyGILState_Release(d_gstate);
}

PyObject * initCall_wrapper(PyObject *self, PyObject *args)
{
    PyObject *temp;
    PyObject *temparglist;
    PyObject *arg;
    char *callName;

    if (PyArg_ParseTuple(args, "sOO", &callName, &temp, &arg)) {
        if (!PyCallable_Check(temp)) {
            PyErr_SetString(PyExc_TypeError, "parameter must be callable");
            return NULL;
        }
    }
    Py_XINCREF(temp);
    temparglist = Py_BuildValue("O", arg);
    Py_INCREF(temparglist);

    callCallback *newElt = calloc(1, sizeof(callCallback));
    newElt->callName = s_strndup(callName, strlen(callName));
    newElt->arglist = temparglist;
    newElt->call = temp;
    DL_APPEND(callList, newElt);
    igs_result_t ret = igs_service_init(callName, observeCall, NULL);
    if (ret == IGS_SUCCESS){
        DL_APPEND(callList, newElt);
    }
    return PyLong_FromLong(ret);

}
