//
//  agent_mapping.c
//  ingescape python wrapper
//
//  Created by vaugien on 06/09/2021.
//  Copyright © 2021 ingenuity. All rights reserved.
//

#include "agent_mapping.h"
#include <stdio.h>
#include <ingescape/ingescape.h>

PyObject *Agent_mapping_load_str(AgentObject *self, PyObject *args, PyObject *kwds)
{
    static char *kwlist[] = {"json_str",  NULL};
    char *json_str = NULL;

    if (!PyArg_ParseTupleAndKeywords(args, NULL, "s", kwlist, &json_str))
        return NULL;
    if(self->agent)    
        return PyLong_FromLong(igsagent_mapping_load_str(self->agent, json_str));
    return NULL;
}

PyObject *Agent_mapping_load_file(AgentObject *self, PyObject *args, PyObject *kwds)
{
    static char *kwlist[] = {"file_path",  NULL};
    char *file_path = NULL;

    if (!PyArg_ParseTupleAndKeywords(args, NULL, "s", kwlist, &file_path))
        return NULL;
    if(self->agent)    
        return PyLong_FromLong(igsagent_mapping_load_file(self->agent, file_path));
    return NULL;
}

PyObject *Agent_mapping_json(AgentObject *self, PyObject *args, PyObject *kwds)
{
    if(self->agent)
    {
        char *json_mapp = igsagent_mapping_json(self->agent);
        if(json_mapp == NULL)
        {
            Py_RETURN_NONE;
        }
        return PyUnicode_FromFormat("%s", json_mapp);
    }
    return NULL;
}

PyObject *Agent_mapping_count(AgentObject *self, PyObject *args, PyObject *kwds)
{
    if(self->agent)
    {
       return PyLong_FromLong((long)igsagent_mapping_count(self->agent));
    }
    return NULL;
}

PyObject *Agent_clear_mappings(AgentObject *self, PyObject *args, PyObject *kwds)
{
    if(self->agent)
    {
        igsagent_clear_mappings(self->agent);
        return PyLong_FromLong(IGS_SUCCESS);
    }
    return NULL;
}

PyObject *Agent_clear_mappings_with_agent(AgentObject *self, PyObject *args, PyObject *kwds)
{
    static char *kwlist[] = {"agent_name",  NULL};
    char *agent_name = NULL;

    if (!PyArg_ParseTupleAndKeywords(args, NULL, "s", kwlist, &agent_name))
        return NULL;
    if(self->agent)
        igsagent_clear_mappings_with_agent(self->agent, agent_name);
        return PyLong_FromLong(IGS_SUCCESS);
    return NULL;
}

PyObject *Agent_mapping_add(AgentObject *self, PyObject *args, PyObject *kwds)
{
    static char *kwlist[] = {"from_our_input", "to_agent", "with_output",  NULL};
    char *from_our_input = NULL;
    char *to_agent = NULL;
    char *with_output = NULL;

    if (!PyArg_ParseTupleAndKeywords(args, NULL, "sss", kwlist, &from_our_input, &to_agent, &with_output))
        return NULL;
    if(self->agent)
        return PyLong_FromUnsignedLongLong((unsigned long long)igsagent_mapping_add(self->agent, from_our_input, to_agent, with_output));
    return NULL;
}

PyObject *Agent_mapping_remove_with_id(AgentObject *self, PyObject *args, PyObject *kwds)
{
    static char *kwlist[] = {"id",  NULL};
    unsigned long long id_mapp = 0;
    if (!PyArg_ParseTupleAndKeywords(args, NULL, "K", kwlist, &id_mapp))
        return NULL;
    if(self->agent)
        return PyLong_FromLong(igsagent_mapping_remove_with_id(self->agent, (uint64_t)id_mapp));
    return NULL;
}

PyObject *Agent_mapping_remove_with_name(AgentObject *self, PyObject *args, PyObject *kwds)
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
        return PyLong_FromLong(igsagent_mapping_remove_with_name(self->agent, from_our_input, to_agent, with_output));
    return NULL;
}


PyObject *Agent_mapping_outputs_request(AgentObject *self, PyObject *args, PyObject *kwds)
{
    if(!self->agent)
        return NULL;
    if(igsagent_mapping_outputs_request(self->agent))
        Py_RETURN_TRUE;
    else
        Py_RETURN_FALSE;
    return PyLong_FromLong(IGS_SUCCESS);
}

PyObject *Agent_mapping_set_outputs_request(AgentObject *self, PyObject *args, PyObject *kwds)
{
    if(!self->agent)
        return NULL;
    static char *kwlist[] = {"notify",  NULL};
    bool notify = false;
    if (!PyArg_ParseTupleAndKeywords(args, NULL, "p", kwlist, &notify))
        return NULL;

    if (notify){
        igsagent_mapping_set_outputs_request(self->agent, true);
        return PyLong_FromLong(IGS_SUCCESS);
    }else{
        igsagent_mapping_set_outputs_request(self->agent, false);
        return PyLong_FromLong(IGS_SUCCESS);
    }
}


PyObject *Agent_mapping_set_path(AgentObject *self, PyObject *args, PyObject *kwds)
{
    static char *kwlist[] = {"path",  NULL};
    char *path = NULL;

    if (!PyArg_ParseTupleAndKeywords(args, NULL, "s", kwlist, &path))
        return NULL;
    if(self->agent)
        igsagent_mapping_set_path(self->agent, path);
        return PyLong_FromLong(IGS_SUCCESS);
    return NULL;
}

PyObject *Agent_mapping_save(AgentObject *self, PyObject *args, PyObject *kwds)
{
    if(self->agent)
    {
        igsagent_mapping_save(self->agent);
        return PyLong_FromLong(IGS_SUCCESS);
    }
    return NULL;
}

