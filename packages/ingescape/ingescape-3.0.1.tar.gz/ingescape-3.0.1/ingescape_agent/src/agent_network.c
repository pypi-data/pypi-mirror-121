//
//  agent_network.c
//  ingescape python wrapper
//
//  Created by vaugien on 06/09/2021.
//  Copyright © 2021 ingenuity. All rights reserved.
//

#include "agent_network.h"
#include <stdio.h>
#include <ingescape/ingescape.h>
#include "uthash/utlist.h"

PyObject *Agent_name(AgentObject *self, PyObject *args, PyObject *kwds)
{

    PyObject * name = PyUnicode_FromFormat("%s", igsagent_name(self->agent));
    Py_INCREF(name);
    return name;

}

PyObject *Agent_set_name(AgentObject *self, PyObject *args, PyObject *kwds)
{
    static char *kwlist[] = {"name",  NULL};
    char *name = NULL;
    if (!PyArg_ParseTupleAndKeywords(args, NULL, "s", kwlist, &name))
        return NULL;
    if(self->agent)
    {
        igsagent_set_name(self->agent, name);
        return PyLong_FromLong(IGS_SUCCESS);
    }
    return PyLong_FromLong(IGS_FAILURE);
}

PyObject *Agent_family(AgentObject *self, PyObject *args, PyObject *kwds)
{
    if(self->agent)
    {
        char *family = igsagent_family(self->agent);
        if (family == NULL)
            Py_RETURN_NONE;
        return PyUnicode_FromFormat("%s", family);
    }
    return NULL;
}

PyObject *Agent_set_family(AgentObject *self, PyObject *args, PyObject *kwds)
{
    static char *kwlist[] = {"family",  NULL};
    char *family = NULL;

    if (!PyArg_ParseTupleAndKeywords(args, NULL, "s", kwlist, &family))
        return NULL;
    if(self->agent)
    {
        igsagent_set_family(self->agent, family);
        return PyLong_FromLong(IGS_SUCCESS);
    }
    return NULL;
}

PyObject *Agent_uuid(AgentObject *self, PyObject *args, PyObject *kwds)
{
    if(self->agent)
    {
       return PyUnicode_FromFormat("%s", igsagent_uuid(self->agent));
    }
    return NULL;
}

PyObject *Agent_state(AgentObject *self, PyObject *args, PyObject *kwds)
{
    if(self->agent)
    {
        char *state = igsagent_state(self->agent);
        if(state == NULL)
            Py_RETURN_NONE;
        return PyUnicode_FromFormat("%s", state);
    }
    return NULL;
}

PyObject *Agent_set_state(AgentObject *self, PyObject *args, PyObject *kwds)
{
    static char *kwlist[] = {"state",  NULL};
    char *state = NULL;

    if (!PyArg_ParseTupleAndKeywords(args, NULL, "s", kwlist, &state))
        return NULL;
    if(self->agent)
    {
        igsagent_set_state(self->agent, state);
        return PyLong_FromLong(IGS_SUCCESS);
    }
    return NULL;
}

PyObject *Agent_mute(AgentObject *self, PyObject *args, PyObject *kwds)
{
    if(self->agent)
    {
        igsagent_mute(self->agent);
        return PyLong_FromLong(IGS_SUCCESS);
    }
    return NULL;
}

PyObject *Agent_unmute(AgentObject *self, PyObject *args, PyObject *kwds)
{
    if(self->agent)
    {
        igsagent_unmute(self->agent);
        return PyLong_FromLong(IGS_SUCCESS);
    }
    return NULL;
}

PyObject *Agent_is_muted(AgentObject *self, PyObject *args, PyObject *kwds)
{
    if(!self->agent)
        return NULL;
    if(igsagent_is_muted(self->agent))
        Py_RETURN_TRUE;
    else
        Py_RETURN_FALSE;
}

agentMuteCB_t *agentMuteCBList = NULL;
void agentObserveMute(igsagent_t* agent, bool mute, void* my_data)
{
    // Lock the GIL to execute the callback safely
    PyGILState_STATE d_gstate;
    d_gstate = PyGILState_Ensure();

    //run through all callbacks to execute them
    PyObject *tupleArgs = PyTuple_New(3);
    PyTuple_SetItem(tupleArgs, 1, Py_BuildValue("O", mute ? Py_True : Py_False));

    agentMuteCB_t* agentMuteCBIt = NULL;
    DL_FOREACH(agentMuteCBList, agentMuteCBIt) {
        if ((agentMuteCBIt->agent->agent == agent)) {
            PyTuple_SetItem(tupleArgs, 0, Py_BuildValue("O", agentMuteCBIt->agent));
            Py_INCREF(agentMuteCBIt->my_data);
            PyTuple_SetItem(tupleArgs, 2, agentMuteCBIt->my_data);
            PyObject_Call(agentMuteCBIt->callback, tupleArgs, NULL);
            Py_DECREF(tupleArgs);
        }
    }

    //release the GIL
    PyGILState_Release(d_gstate);
}

PyObject *Agent_observe_mute(AgentObject *self, PyObject *args, PyObject *kwds)
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

    agentMuteCB_t* newElt = calloc(1, sizeof(agentMuteCB_t));
    newElt->agent = self;
    newElt->my_data = Py_BuildValue("O", my_data);
    newElt->callback = callback;
    DL_APPEND(agentMuteCBList, newElt);
    igsagent_observe_mute(self->agent, agentObserveMute, NULL);
    return PyLong_FromLong(IGS_SUCCESS);
}


PyObject *Agent_election_join(AgentObject *self, PyObject *args, PyObject *kwds)
{
    static char *kwlist[] = {"election_name",  NULL};
    char *election_name = NULL;

    if (!PyArg_ParseTupleAndKeywords(args, NULL, "s", kwlist, &election_name))
        return NULL;
    if(self->agent)
        return PyLong_FromLong(igsagent_election_join(self->agent, election_name));
    return NULL;
}

PyObject *Agent_election_leave(AgentObject *self, PyObject *args, PyObject *kwds)
{
    static char *kwlist[] = {"election_name",  NULL};
    char *election_name = NULL;

    if (!PyArg_ParseTupleAndKeywords(args, NULL, "s", kwlist, &election_name))
        return NULL;
    if(self->agent)
        return PyLong_FromLong(igsagent_election_leave(self->agent, election_name));
    return NULL;
}
