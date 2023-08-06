//
//  agent_split.c
//  ingescape python wrapper
//
//  Created by vaugien on 06/09/2021.
//  Copyright © 2021 ingenuity. All rights reserved.
//

#include "agent_split.h"
#include <stdio.h>
#include <ingescape/ingescape.h>

PyObject *Agent_split_count(AgentObject *self, PyObject *args, PyObject *kwds)
{
    if(self->agent)
    {
       return PyLong_FromLong((long)igsagent_split_count(self->agent));
    }
    return NULL;
}

PyObject *Agent_split_add(AgentObject *self, PyObject *args, PyObject *kwds)
{
    static char *kwlist[] = {"from_our_input", "to_agent", "with_output",  NULL};
    char *from_our_input = NULL;
    char *to_agent = NULL;
    char *with_output = NULL;

    if (!PyArg_ParseTupleAndKeywords(args, NULL, "sss", kwlist, &from_our_input, &to_agent, &with_output))
        return NULL;
    if(self->agent)
        return PyLong_FromUnsignedLongLong((unsigned long long)igsagent_split_add(self->agent, from_our_input, to_agent, with_output));
    return NULL;
}

PyObject *Agent_split_remove_with_id(AgentObject *self, PyObject *args, PyObject *kwds)
{
    static char *kwlist[] = {"id",  NULL};
    unsigned long long id_mapp = 0;
    if (!PyArg_ParseTupleAndKeywords(args, NULL, "K", kwlist, &id_mapp))
        return NULL;
    if(self->agent)
        return PyLong_FromLong(igsagent_split_remove_with_id(self->agent, (uint64_t)id_mapp));
    return NULL;
}

PyObject *Agent_split_remove_with_name(AgentObject *self, PyObject *args, PyObject *kwds)
{
    if(!self->agent)
        return NULL;
    static char *kwlist[] = {"from_our_input", "to_agent", "with_output",  NULL};
    char *from_our_input = NULL;
    char *to_agent = NULL;
    char *with_output = NULL;

    if (!PyArg_ParseTupleAndKeywords(args, NULL, "sss", kwlist, &from_our_input, &to_agent, &with_output))
        return NULL;
    if(self->agent)
        return PyLong_FromLong(igsagent_split_remove_with_name(self->agent, from_our_input, to_agent, with_output));
    return NULL;
}

