//
//  agent_init.c
//  ingescape python wrapper
//
//  Created by vaugien on 06/09/2021.
//  Copyright © 2021 ingenuity. All rights reserved.
//

#include "agent_init.h"
#include <stdio.h>
#include <ingescape/ingescape.h>
#include "uthash/utlist.h"

PyObject *Agent_activate(AgentObject *self, PyObject *args, PyObject *kwds)
{
    if(!self->agent)
        return NULL;
    return PyLong_FromLong(igsagent_activate(self->agent));
}

PyObject *Agent_deactivate(AgentObject *self, PyObject *args, PyObject *kwds)
{
    if(!self->agent)
        return NULL;
    return PyLong_FromLong(igsagent_deactivate(self->agent));
}

PyObject *Agent_is_activated(AgentObject *self, PyObject *args, PyObject *kwds)
{
    if(!self->agent)
        return NULL;
    if(igsagent_is_activated(self->agent))
        Py_RETURN_TRUE;
    else
        Py_RETURN_FALSE;
    return PyLong_FromLong(IGS_SUCCESS);
}

agentObserveCB_t* agentObserveCBList = NULL;
void agentObserveCB(igsagent_t *agent, bool is_activated, void *my_data)
{
    // Lock the GIL to execute the callback safely
    PyGILState_STATE d_gstate;
    d_gstate = PyGILState_Ensure();

    //run through all callbacks to execute them
    PyObject *tupleArgs = PyTuple_New(3);
    PyTuple_SetItem(tupleArgs, 1, Py_BuildValue("O", is_activated ? Py_True : Py_False));

    agentObserveCB_t* agentCBIt = NULL;
    DL_FOREACH(agentObserveCBList, agentCBIt) {
        if ((agentCBIt->agent->agent == agent)) {
            PyTuple_SetItem(tupleArgs, 0, Py_BuildValue("O", agentCBIt->agent));
            Py_INCREF(agentCBIt->my_data);
            PyTuple_SetItem(tupleArgs, 2, agentCBIt->my_data);
            PyObject_Call(agentCBIt->callback, tupleArgs, NULL);
            Py_DECREF(tupleArgs);
        }
    }

    //release the GIL
    PyGILState_Release(d_gstate);
}

PyObject *Agent_observe(AgentObject *self, PyObject *args, PyObject *kwds)
{
    if(!self->agent)
        return PyLong_FromLong(IGS_FAILURE);

    // parse the callback and arguments sent from python
    PyObject *callback = NULL;
    PyObject *my_data = NULL;
    // static char *kwlist[] = {"callback", "args", NULL};
    // if (PyArg_ParseTupleAndKeywords(args, kwds, "OO", kwlist, &callback, &arg)) { //FIXME Cannot seem to make this work... May be related to my machine only due to a hazardous installation of python (brew vs. built-in and such)
    if (PyArg_ParseTuple(args, "OO", &callback, &my_data)) {
        if (!PyCallable_Check(callback)) { // check if the callback is callable
            PyErr_SetString(PyExc_TypeError, "'callback' parameter must be callable");
            return PyLong_FromLong(IGS_FAILURE);;
        }
    }
    else {
        return PyLong_FromLong(IGS_FAILURE);
    }

    agentObserveCB_t* newElt = calloc(1, sizeof(agentObserveCB_t));
    newElt->agent = self;
    newElt->my_data = Py_BuildValue("O", my_data);
    newElt->callback = callback;
    DL_APPEND(agentObserveCBList, newElt);
    igsagent_observe(self->agent, agentObserveCB, NULL);
    return PyLong_FromLong(IGS_SUCCESS);
}

agentObserveEventsCB_t *agentObserveEventsCBList = NULL;
void agentObserveEventsCB(igsagent_t *agent,
                          igs_agent_event_t event,
                          const char *uuid,
                          const char *name,
                          void *event_data,
                          void *data)
{
    // Lock the GIL to execute the callback safely
    PyGILState_STATE d_gstate;
    d_gstate = PyGILState_Ensure();

    //run through all callbacks to execute them
    PyObject *tupleArgs = PyTuple_New(6);
    PyTuple_SetItem(tupleArgs, 1, Py_BuildValue("i", event));
    PyTuple_SetItem(tupleArgs, 2, Py_BuildValue("s", uuid));
    PyTuple_SetItem(tupleArgs, 3, Py_BuildValue("s", name));
    if (event == IGS_AGENT_WON_ELECTION || event == IGS_AGENT_LOST_ELECTION)
        PyTuple_SetItem(tupleArgs, 4, Py_BuildValue("s", (char*)event_data));
    else if (event == IGS_PEER_ENTERED)
        PyTuple_SetItem(tupleArgs, 4,Py_None); // FIXME: cast zhash into python item
    else
        PyTuple_SetItem(tupleArgs, 4, Py_None);

    agentObserveEventsCB_t* agentEventCBIt = NULL;
    DL_FOREACH(agentObserveEventsCBList, agentEventCBIt) {
        if ((agentEventCBIt->agent->agent == agent)) {
            PyTuple_SetItem(tupleArgs, 0, Py_BuildValue("O", agentEventCBIt->agent));
            Py_INCREF(agentEventCBIt->my_data);
            PyTuple_SetItem(tupleArgs, 5, agentEventCBIt->my_data);
            PyObject_Call(agentEventCBIt->callback, tupleArgs, NULL);
            Py_DECREF(tupleArgs);
        }
    }

    //release the GIL
    PyGILState_Release(d_gstate);
}

PyObject *Agent_observe_agent_event(AgentObject *self, PyObject *args, PyObject *kwds)
{
    if(!self->agent)
        return PyLong_FromLong(IGS_FAILURE);

    // parse the callback and arguments sent from python
    PyObject *callback;
    PyObject *my_data;
    // static char *kwlist[] = {"callback", "args", NULL};
    // if (PyArg_ParseTupleAndKeywords(args, kwds, "OO", kwlist, &callback, &arg)) { //FIXME Cannot seem to make this work... May be related to my machine only due to a hazardous installation of python (brew vs. built-in and such)
    if (PyArg_ParseTuple(args, "OO", &callback, &my_data)) {
        if (!PyCallable_Check(callback)) { // check if the callback is callable
            PyErr_SetString(PyExc_TypeError, "'callback' parameter must be callable");
            return PyLong_FromLong(IGS_FAILURE);;
        }
    }
    else {
        return PyLong_FromLong(IGS_FAILURE);
    }

    agentObserveEventsCB_t* newElt = calloc(1, sizeof(agentObserveEventsCB_t));
    newElt->agent = self;
    newElt->my_data = Py_BuildValue("O", my_data);
    newElt->callback = callback;
    DL_APPEND(agentObserveEventsCBList, newElt);
    igsagent_observe_agent_events(self->agent, agentObserveEventsCB, NULL);
    return PyLong_FromLong(IGS_SUCCESS);
}


PyObject *Agent_trace(AgentObject *self, PyObject *args, PyObject *kwds)
{
    if(!self->agent)
        return NULL;
    char * log;
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
        return NULL;
    }

    Py_DECREF(funcTuple);

    if(strcmp(functionStr, "<module>") == 0){
        igsagent_log(IGS_LOG_TRACE, "main", self->agent, "%s", log);
    }else{
        igsagent_log(IGS_LOG_DEBUG, functionStr, self->agent, "%s", log);
    }
    return PyLong_FromLong(0);
}

PyObject *Agent_debug(AgentObject *self, PyObject *args, PyObject *kwds)
{
    if(!self->agent)
        return NULL;
    char * log;
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
        return NULL;
    }

    Py_DECREF(funcTuple);

    if(strcmp(functionStr, "<module>") == 0){
        igsagent_log(IGS_LOG_DEBUG, "main", self->agent, "%s", log);
    }else{
        igsagent_log(IGS_LOG_DEBUG, functionStr, self->agent, "%s", log);
    }
    return PyLong_FromLong(0);
}

PyObject *Agent_info(AgentObject *self, PyObject *args, PyObject *kwds)
{
    if(!self->agent)
        return NULL;
    char * log;
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
        return NULL;
    }

    Py_DECREF(funcTuple);

    if(strcmp(functionStr, "<module>") == 0){
        igsagent_log(IGS_LOG_INFO, "main", self->agent, "%s", log);
    }else{
        igsagent_log(IGS_LOG_INFO, functionStr, self->agent, "%s", log);
    }
    return PyLong_FromLong(0);
}

PyObject *Agent_warn(AgentObject *self, PyObject *args, PyObject *kwds)
{
    if(!self->agent)
        return NULL;
    char * log;
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
        return NULL;
    }

    Py_DECREF(funcTuple);

    if(strcmp(functionStr, "<module>") == 0){
        igsagent_log(IGS_LOG_WARN, "main", self->agent, "%s", log);
    }else{
        igsagent_log(IGS_LOG_WARN, functionStr, self->agent, "%s", log);
    }
    return PyLong_FromLong(0);
}

PyObject *Agent_error(AgentObject *self, PyObject *args, PyObject *kwds)
{
    if(!self->agent)
        return NULL;
    char * log;
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
        return NULL;
    }

    Py_DECREF(funcTuple);

    if(strcmp(functionStr, "<module>") == 0){
        igsagent_log(IGS_LOG_ERROR, "main", self->agent, "%s", log);
    }else{
        igsagent_log(IGS_LOG_ERROR, functionStr, self->agent, "%s", log);
    }
    return PyLong_FromLong(0);
}

PyObject *Agent_fatal(AgentObject *self, PyObject *args, PyObject *kwds)
{
    if(!self->agent)
        return NULL;
    char * log;
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
        return NULL;
    }

    Py_DECREF(funcTuple);

    if(strcmp(functionStr, "<module>") == 0){
        igsagent_log(IGS_LOG_FATAL, "main", self->agent, "%s", log);
    }else{
        igsagent_log(IGS_LOG_FATAL, functionStr, self->agent, "%s", log);
    }
    return PyLong_FromLong(0);
}
