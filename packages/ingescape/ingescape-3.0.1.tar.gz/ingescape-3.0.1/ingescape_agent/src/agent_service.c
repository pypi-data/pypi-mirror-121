//
//  agent_service.c
//  ingescape python wrapper
//
//  Created by vaugien on 06/09/2021.
//  Copyright © 2021 ingenuity. All rights reserved.
//

#include "agent_service.h"
#include <stdio.h>
#include <ingescape/ingescape.h>
#include "uthash/utlist.h"

PyObject *Agent_service_call(AgentObject *self, PyObject *args, PyObject *kwds)
{
    igs_service_arg_t *argumentList = NULL;
    char* agentNameOrUUID;
    char *serviceName;
    char *token;
    PyObject *argTuple = NULL;
    if (PyTuple_Size(args) != 4){
        printf("Expect 4 arguments, %zu were given \n", PyTuple_Size(args));
        return PyLong_FromLong(-1);
    }
    int format = 0;
    static char *kwlist[] = {"agent_name","service_name","argument_list", "token", NULL};
    if (PyArg_ParseTupleAndKeywords(args, NULL, "ssOz", kwlist, &agentNameOrUUID, &serviceName, &argTuple, &token ) == true) 
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
    else
    {
        return PyLong_FromLong(-1);
    }
    int result = 0;
    // Argument parsing
    if(format == 2){
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
        result = igsagent_service_call(self->agent, agentNameOrUUID, serviceName, &argumentList, token);
        igs_service_args_destroy(&argumentList);
    }else if (format == 1){
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
        result = igsagent_service_call(self->agent, agentNameOrUUID, serviceName, &argumentList, token);
        igs_service_args_destroy(&argumentList);
    }else{
        result = igsagent_service_call(self->agent, agentNameOrUUID, serviceName, NULL, token);
    }

    return PyLong_FromLong(result);
}

agentServiceCB_t* agentServiceCBList = NULL;
void agentServiceCB(igsagent_t *agent,
                    const char *sender_agent_name,
                    const char *sender_agent_uuid,
                    const char *service_name,
                    igs_service_arg_t *first_argument,
                    size_t args_nbr,
                    const char *token,
                    void *data)
{
    IGS_UNUSED(data);
    // Lock the GIL to execute the callback safely
    PyGILState_STATE d_gstate;
    d_gstate = PyGILState_Ensure();

    //run through all callbacks to execute them
    PyObject *tupleArgs = PyTuple_New(7);
    PyTuple_SetItem(tupleArgs, 1, Py_BuildValue("s", sender_agent_name));
    PyTuple_SetItem(tupleArgs, 2, Py_BuildValue("s", sender_agent_uuid));
    PyTuple_SetItem(tupleArgs, 3, Py_BuildValue("s", service_name));

    // Making args into a tuple's tuple
    PyObject *serviceArgsTuple = PyTuple_New(args_nbr);
    igs_service_arg_t* argIt = first_argument;
    for (size_t argIdx = 0 ; argIdx < args_nbr ; ++argIdx) {
        switch(argIt->type){
            case IGS_BOOL_T:
                if (argIt->b){
                    PyTuple_SetItem(serviceArgsTuple, argIdx, Py_True);
                }else{
                    PyTuple_SetItem(serviceArgsTuple, argIdx, Py_False);
                }
                break;
            case IGS_INTEGER_T:
                PyTuple_SetItem(serviceArgsTuple, argIdx, Py_BuildValue("i", argIt->i));
                break;
            case IGS_DOUBLE_T:
                PyTuple_SetItem(serviceArgsTuple, argIdx, Py_BuildValue("d", argIt->d));
                break;
            case IGS_STRING_T:
                PyTuple_SetItem(serviceArgsTuple, argIdx, Py_BuildValue("s", argIt->c));
                break;
            case IGS_IMPULSION_T:
                PyTuple_SetItem(serviceArgsTuple, argIdx, Py_None);
                break;
            case IGS_DATA_T:
                PyTuple_SetItem(serviceArgsTuple, argIdx, Py_BuildValue("y#", argIt->data, argIt->size));
                break;
            case IGS_UNKNOWN_T:
                break;
        }
        argIt = argIt->next;
    }

    PyTuple_SetItem(tupleArgs, 4, Py_BuildValue("O", serviceArgsTuple));
    PyTuple_SetItem(tupleArgs, 5, Py_BuildValue("s", token));

    agentServiceCB_t* service_it = NULL;
    DL_FOREACH(agentServiceCBList, service_it) {
        if ((service_it->agent->agent == agent) && streq(service_it->serviceName, service_name)) {
            PyTuple_SetItem(tupleArgs, 0, Py_BuildValue("O", service_it->agent));
            PyTuple_SetItem(tupleArgs, 6, service_it->my_data);
            PyObject_Call(service_it->callback, tupleArgs, NULL);
            Py_DECREF(tupleArgs);
        }
    }

    //release the GIL
    PyGILState_Release(d_gstate);
}

PyObject *Agent_service_init(AgentObject *self, PyObject *args, PyObject *kwds)
{
    char* serviceName = NULL;
    igs_service_arg_t *argumentList = NULL;
    PyObject *callback = NULL;
    PyObject *myData = NULL;

    if (PyTuple_Size(args) != 3){
        printf("Expect 3 arguments, %zu were given \n", PyTuple_Size(args));
        return PyLong_FromLong(IGS_FAILURE);
    }
    int format = 0;
    if (PyArg_ParseTuple(args, "sOO", &serviceName, &callback, &myData)) {
        if (!PyCallable_Check(callback)) {
            PyErr_SetString(PyExc_TypeError, "parameter 3 must be callable");
            return PyLong_FromLong(IGS_FAILURE);;
        }
    }

    igs_result_t result = igsagent_service_init(self->agent, serviceName, agentServiceCB, NULL);
    if (result == IGS_SUCCESS) {
        // add the callback to the list of Callbacks
        agentServiceCB_t *newElt = calloc(1, sizeof(agentServiceCB_t));
        newElt->agent = self;
        newElt->serviceName = strdup(serviceName);
        newElt->my_data = Py_BuildValue("O", myData);
        newElt->callback = callback;
        DL_APPEND(agentServiceCBList, newElt);
    }

    return PyLong_FromLong(result);
}

PyObject *Agent_service_remove(AgentObject *self, PyObject *args, PyObject *kwds)
{
    static char *kwlist[] = {"service_name",  NULL};
    char *service_name = 0;
    if (!PyArg_ParseTupleAndKeywords(args, NULL, "s", kwlist, &service_name))
        return NULL;
    if(self->agent)
        return PyLong_FromLong(igsagent_service_remove(self->agent, service_name));
    return NULL;
}

PyObject *Agent_service_arg_add(AgentObject *self, PyObject *args, PyObject *kwds)
{
    char *service_name;
    char *arg_name;
    int value_type;

    // static char *kwlist[] = {"service_name", "arg_name", "value_type", NULL};
    // if (!PyArg_ParseTupleAndKeywords(args, NULL, "ssi", kwlist, &service_name, &arg_name, &value_type))
    if (!PyArg_ParseTuple(args, "ssi", &service_name, &arg_name, &value_type))
        return NULL;

    return PyLong_FromLong(igsagent_service_arg_add(self->agent, service_name, arg_name, value_type));
}

PyObject *Agent_service_arg_remove(AgentObject *self, PyObject *args, PyObject *kwds)
{
    static char *kwlist[] = {"service_name", "arg_name", NULL};
    char *service_name;
    char *arg_name;
    if (!PyArg_ParseTupleAndKeywords(args, NULL, "ss", kwlist, &service_name, &arg_name))
        return NULL;

    return PyLong_FromLong(igsagent_service_arg_remove(self->agent, service_name, arg_name));
}

PyObject *Agent_service_count(AgentObject *self, PyObject *args, PyObject *kwds)
{
    if(self->agent)
    {
       return PyLong_FromLong((long)igsagent_service_count(self->agent));
    }
    return NULL;
}

PyObject *Agent_service_exists(AgentObject *self, PyObject *args, PyObject *kwds)
{
    if(!self->agent)
        return NULL;
    static char *kwlist[] = {"service_name", NULL};
    char *service_name;
    if (!PyArg_ParseTupleAndKeywords(args, NULL, "s", kwlist, &service_name))
        return NULL;
    if(igsagent_service_exists(self->agent, service_name))
        Py_RETURN_TRUE;
    else
        Py_RETURN_FALSE;
    return PyLong_FromLong(IGS_SUCCESS);
}

PyObject *Agent_service_list(AgentObject *self, PyObject *args, PyObject *kwds)
{
    PyObject * ret;

    size_t nbOfElements = igsagent_service_count(self->agent);
    char **result = igsagent_service_list(self->agent, &nbOfElements);

    ret = PyTuple_New(nbOfElements);
    size_t i ;
    for (i = 0; i < nbOfElements; i++){
        PyTuple_SetItem(ret, i, Py_BuildValue("s",result[i]));
    }
    igs_free_services_list(result, nbOfElements);
    return ret;
}

PyObject *Agent_service_args_count(AgentObject *self, PyObject *args, PyObject *kwds)
{
    static char *kwlist[] = {"service_name", NULL};
    char *service_name;
    if (!PyArg_ParseTupleAndKeywords(args, NULL, "s", kwlist, &service_name))
        return NULL;
    if(self->agent)
    {
       return PyLong_FromLong((long)igsagent_service_args_count(self->agent, service_name));
    }
    return NULL;
}

PyObject *Agent_service_args_list(AgentObject *self, PyObject *args, PyObject *kwds)
{
    static char *kwlist[] = {"service_name", NULL};
    char *service_name;
    if (!PyArg_ParseTupleAndKeywords(args, NULL, "s", kwlist, &service_name))
        return NULL;

    igs_service_arg_t *firstElement = igsagent_service_args_first(self->agent, service_name);
    size_t nbOfElements = igsagent_service_args_count(self->agent, service_name);

    PyObject *ret = PyTuple_New(nbOfElements);
    size_t index = 0;
    igs_service_arg_t *newArg = NULL;
    LL_FOREACH(firstElement, newArg){
        PyTuple_SetItem(ret, index, Py_BuildValue("(si)",newArg->name, newArg->type));
        index ++;
    }
    return ret;
}

PyObject *Agent_service_args_exists(AgentObject *self, PyObject *args, PyObject *kwds)
{
    if(!self->agent)
        return NULL;
    static char *kwlist[] = {"service_name", "arg_name", NULL};
    char *service_name;
    char *arg_name;
    if (!PyArg_ParseTupleAndKeywords(args, NULL, "ss", kwlist, &service_name, &arg_name))
        return NULL;
    if(igsagent_service_arg_exists(self->agent, service_name, arg_name))
        Py_RETURN_TRUE;
    else
        Py_RETURN_FALSE;
    return PyLong_FromLong(IGS_SUCCESS);
}
