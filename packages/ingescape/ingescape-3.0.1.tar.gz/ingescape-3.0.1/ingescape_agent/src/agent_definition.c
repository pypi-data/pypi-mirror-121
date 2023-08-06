//
//  agent_definition.c
//  ingescape python wrapper
//
//  Created by vaugien on 06/09/2021.
//  Copyright © 2021 ingenuity. All rights reserved.
//

#include "agent_definition.h"
#include <stdio.h>
#include <ingescape/ingescape.h>
#include <ingescape/igsagent.h>
#include "uthash/utlist.h"

agentobserve_iop_cb_t *agentobserve_iop_cbList = NULL;

static char *s_strndup (const char *str, size_t chars)
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

PyObject *Agent_definition_load_str(AgentObject *self, PyObject *args, PyObject *kwds)
{
    static char *kwlist[] = {"json_str",  NULL};
    char *json_str = NULL;

    if (!PyArg_ParseTupleAndKeywords(args, NULL, "s", kwlist, &json_str))
        Py_RETURN_NONE;
    if(self->agent)
        return PyLong_FromLong(igsagent_definition_load_str(self->agent, json_str));
    Py_RETURN_NONE;
}

PyObject *Agent_definition_load_file(AgentObject *self, PyObject *args, PyObject *kwds)
{
    static char *kwlist[] = {"file_path",  NULL};
    char *file_path = NULL;

    if (!PyArg_ParseTupleAndKeywords(args, NULL, "s", kwlist, &file_path))
        Py_RETURN_NONE;
    if(self->agent)
        return PyLong_FromLong(igsagent_definition_load_file(self->agent, file_path));
    Py_RETURN_NONE;
}

PyObject *Agent_clear_definition(AgentObject *self, PyObject *args, PyObject *kwds)
{
    if(self->agent)
    {
        igsagent_clear_definition(self->agent);
        agentobserve_iop_cb_t *it = NULL;
        do {
            DL_FOREACH(agentobserve_iop_cbList, it) {
                if (it->agent == self) break;
            }
            if (it) {
                DL_DELETE(agentobserve_iop_cbList, it);
                Py_CLEAR(it->callback);
                Py_CLEAR(it->my_data);
                free(it);
            }
        } while(it);
        return PyLong_FromLong(IGS_SUCCESS);
    }
    Py_RETURN_NONE;
}

PyObject *Agent_definition_json(AgentObject *self, PyObject *args, PyObject *kwds)
{
    if(self->agent)
    {
        char *def =  igsagent_definition_json(self->agent);
        if(def == NULL)
            Py_RETURN_NONE;
        
        return PyUnicode_FromFormat("%s", def);
    }
    Py_RETURN_NONE;
}

PyObject *Agent_definition_description(AgentObject *self, PyObject *args, PyObject *kwds)
{
    if(self->agent)
    {
        char *def =  igsagent_definition_description(self->agent);
        if(def == NULL)
            Py_RETURN_NONE;
        return PyUnicode_FromFormat("%s", def);
    }
    Py_RETURN_NONE;
}

PyObject *Agent_definition_version(AgentObject *self, PyObject *args, PyObject *kwds)
{
    if(self->agent)
    {
        char *def =  igsagent_definition_version(self->agent);
        if(def == NULL)
            Py_RETURN_NONE;
        return PyUnicode_FromFormat("%s", def);
    }
    Py_RETURN_NONE;
}

PyObject *Agent_definition_set_description(AgentObject *self, PyObject *args, PyObject *kwds)
{
    static char *kwlist[] = {"descritpion",  NULL};
    char *descritpion = NULL;

    if (!PyArg_ParseTupleAndKeywords(args, NULL, "s", kwlist, &descritpion))
        Py_RETURN_NONE;
    if(self->agent)
    {
        igsagent_definition_set_description(self->agent, descritpion);
        return PyLong_FromLong(IGS_SUCCESS);
    }
    Py_RETURN_NONE;
}

PyObject *Agent_definition_set_version(AgentObject *self, PyObject *args, PyObject *kwds)
{
    static char *kwlist[] = {"version",  NULL};
    char *version = NULL;

    if (!PyArg_ParseTupleAndKeywords(args, NULL, "s", kwlist, &version))
        Py_RETURN_NONE;
    if(self->agent)
    {
        igsagent_definition_set_version(self->agent, version);
        return PyLong_FromLong(IGS_SUCCESS);
    }
    Py_RETURN_NONE;
}


PyObject *Agent_input_create(AgentObject *self, PyObject *args, PyObject *kwds)
{
    char * name;
    igs_iop_value_type_t type;
    int _type;
    PyObject *value;
    long size;
    int result;

    if (!PyArg_ParseTuple(args, "siO", &name, &_type, &value)) {
        Py_RETURN_NONE;
    }
    type = (igs_iop_value_type_t)(_type);
    if (value == Py_None){
        result = igsagent_input_create(self->agent, name, type, NULL, 0);
    }
    else if (type == IGS_STRING_T)
    {
        char *value_c;
        if (!PyArg_ParseTuple(args, "sis", &name, &_type, &value_c)){
            return NULL;
        }
        result = igsagent_input_create(self->agent, name, type, value_c, strlen(value_c));
    }else if (type == IGS_INTEGER_T){
        int value_c;
        if (!PyArg_ParseTuple(args, "sii", &name, &_type, &value_c)) {
            return NULL;
        }
        result = igsagent_input_create(self->agent, name, type, &value_c, sizeof(int));
    }else if (type == IGS_DOUBLE_T){
        double value_c;
        if (!PyArg_ParseTuple(args, "sid", &name, &_type, &value_c)) {
            return NULL;
        }
        result = igsagent_input_create(self->agent, name, type, &value_c, sizeof(double));
    }else if (type == IGS_BOOL_T){
        if (value == Py_True)
        {
            bool value = true;
            result = igsagent_input_create(self->agent, name, type, &value, sizeof(bool));
        }
        else
        {
            bool value = false;
            result = igsagent_input_create(self->agent, name, type, false, sizeof(bool));
        }
    }else{
        result = igsagent_input_create(self->agent, name, type, value, (size_t)PyObject_Size(value));
    }
    return PyLong_FromLong(result);
}

PyObject *Agent_output_create(AgentObject *self, PyObject *args, PyObject *kwds)
{
    char * name;
    igs_iop_value_type_t type;
    int _type;
    PyObject *value;
    long size;
    int result;

    if (!PyArg_ParseTuple(args, "siO", &name, &_type, &value)) {
        Py_RETURN_NONE;
    }
    type = (igs_iop_value_type_t)(_type);
    if (value == Py_None){
        result = igsagent_output_create(self->agent, name, type, NULL, 0);
    }
    else if (type == IGS_STRING_T)
    {
        char *value_c;
        if (!PyArg_ParseTuple(args, "sis", &name, &_type, &value_c)){
            return NULL;
        }
        result = igsagent_output_create(self->agent, name, type, value_c, strlen(value_c));
    }else if (type == IGS_INTEGER_T){
        int value_c;
        if (!PyArg_ParseTuple(args, "sii", &name, &_type, &value_c)) {
            return NULL;
        }
        result = igsagent_output_create(self->agent, name, type, &value_c, sizeof(int));
    }else if (type == IGS_DOUBLE_T){
        double value_c;
        if (!PyArg_ParseTuple(args, "sid", &name, &_type, &value_c)) {
            return NULL;
        }
        result = igsagent_output_create(self->agent, name, type, &value_c, sizeof(double));
    }else if (type == IGS_BOOL_T){
        if (value == Py_True)
        {
            bool value = true;
            result = igsagent_output_create(self->agent, name, type, &value, sizeof(bool));
        }
        else
        {
            bool value = false;
            result = igsagent_output_create(self->agent, name, type, &value, sizeof(bool));
        }
    }else{
        result = igsagent_output_create(self->agent, name, type, value, (size_t)PyObject_Size(value));
    }
    return PyLong_FromLong(result);
}

PyObject *Agent_parameter_create(AgentObject *self, PyObject *args, PyObject *kwds)
{
    char * name;
    igs_iop_value_type_t type;
    int _type;
    PyObject *value;
    long size;
    int result;

    if (!PyArg_ParseTuple(args, "siO", &name, &_type, &value)) {
        Py_RETURN_NONE;
    }
    type = (igs_iop_value_type_t)(_type);
    if (value == Py_None){
        result = igsagent_parameter_create(self->agent, name, type, NULL, 0);
    }
    else if (type == IGS_STRING_T)
    {
        char *value_c;
        if (!PyArg_ParseTuple(args, "sis", &name, &_type, &value_c)){
            return NULL;
        }
        result = igsagent_parameter_create(self->agent, name, type, value_c, strlen(value_c));
    }else if (type == IGS_INTEGER_T){
        int value_c;
        if (!PyArg_ParseTuple(args, "sii", &name, &_type, &value_c)) {
            return NULL;
        }
        result = igsagent_parameter_create(self->agent, name, type, &value_c, sizeof(int));
    }else if (type == IGS_DOUBLE_T){
        double value_c;
        if (!PyArg_ParseTuple(args, "sid", &name, &_type, &value_c)) {
            return NULL;
        }
        result = igsagent_parameter_create(self->agent, name, type, &value_c, sizeof(double));
    }else if (type == IGS_BOOL_T){
        if (value == Py_True)
        {
            bool value = true;
            result = igsagent_parameter_create(self->agent, name, type, &value, sizeof(bool));
        }
        else
        {
            bool value = false;
            result = igsagent_parameter_create(self->agent, name, type, &value, sizeof(bool));
        }
    }else{
        result = igsagent_parameter_create(self->agent, name, type, value, (size_t)PyObject_Size(value));
    }
    return PyLong_FromLong(result);
}


PyObject *Agent_input_remove(AgentObject *self, PyObject *args, PyObject *kwds)
{
    static char *kwlist[] = {"name",  NULL};
    char *name = NULL;
    if (!PyArg_ParseTupleAndKeywords(args, NULL, "s", kwlist, &name))
        return PyLong_FromLong(IGS_FAILURE);
    agentobserve_iop_cb_t *it = NULL;
    do {
        DL_FOREACH(agentobserve_iop_cbList, it) {
            if (it->agent == self
                && it->nameArg == name
                && it->iopType == IGS_INPUT_T) break;
        }
        if (it) {
            DL_DELETE(agentobserve_iop_cbList, it);
            Py_CLEAR(it->callback);
            Py_CLEAR(it->my_data);
            free(it->nameArg);
            free(it);
        }
    } while(it);
    return PyLong_FromLong(igsagent_input_remove(self->agent, name));
}

PyObject *Agent_output_remove(AgentObject *self, PyObject *args, PyObject *kwds)
{
    static char *kwlist[] = {"name",  NULL};
    char *name = NULL;
    if (!PyArg_ParseTupleAndKeywords(args, NULL, "s", kwlist, &name))
        return PyLong_FromLong(IGS_FAILURE);
    agentobserve_iop_cb_t *it = NULL;
    do {
        DL_FOREACH(agentobserve_iop_cbList, it) {
            if (it->agent == self
                && it->nameArg == name
                && it->iopType == IGS_OUTPUT_T) break;
        }
        if (it) {
            DL_DELETE(agentobserve_iop_cbList, it);
            Py_CLEAR(it->callback);
            Py_CLEAR(it->my_data);
            free(it->nameArg);
            free(it);
        }
    } while(it);
    return PyLong_FromLong(igsagent_output_remove(self->agent, name));
}

PyObject *Agent_parameter_remove(AgentObject *self, PyObject *args, PyObject *kwds)
{
    static char *kwlist[] = {"name",  NULL};
    char *name = NULL;
    if (!PyArg_ParseTupleAndKeywords(args, NULL, "s", kwlist, &name))
        Py_RETURN_NONE;
    if(self->agent)
    {
        agentobserve_iop_cb_t *it = NULL;
        do {
            DL_FOREACH(agentobserve_iop_cbList, it) {
                if (it->agent == self
                    && it->nameArg == name
                    && it->iopType == IGS_PARAMETER_T) break;
            }
            if (it) {
                DL_DELETE(agentobserve_iop_cbList, it);
                Py_CLEAR(it->callback);
                Py_CLEAR(it->my_data);
                free(it->nameArg);
                free(it);
            }
        } while(it);
        return PyLong_FromLong(igsagent_parameter_remove(self->agent, name));
    }
    Py_RETURN_NONE;
}


PyObject *Agent_input_type(AgentObject *self, PyObject *args, PyObject *kwds)
{
    static char *kwlist[] = {"name",  NULL};
    char *name = NULL;
    if (!PyArg_ParseTupleAndKeywords(args, NULL, "s", kwlist, &name))
        Py_RETURN_NONE;
    if(self->agent)
    {
        return PyLong_FromLong(igsagent_input_type(self->agent, name));
    }
    Py_RETURN_NONE;
}

PyObject *Agent_output_type(AgentObject *self, PyObject *args, PyObject *kwds)
{
   static char *kwlist[] = {"name",  NULL};
    char *name = NULL;
    if (!PyArg_ParseTupleAndKeywords(args, NULL, "s", kwlist, &name))
        Py_RETURN_NONE;
    if(self->agent)
    {
        return PyLong_FromLong(igsagent_output_type(self->agent, name));
    }
    Py_RETURN_NONE;
}

PyObject *Agent_parameter_type(AgentObject *self, PyObject *args, PyObject *kwds)
{
    static char *kwlist[] = {"name",  NULL};
    char *name = NULL;
    if (!PyArg_ParseTupleAndKeywords(args, NULL, "s", kwlist, &name))
        Py_RETURN_NONE;
    if(self->agent)
    {
        return PyLong_FromLong(igsagent_parameter_type(self->agent, name));
    }
    Py_RETURN_NONE;
}


PyObject *Agent_input_count(AgentObject *self, PyObject *args, PyObject *kwds)
{
    if(self->agent)
    {
        return PyLong_FromLong(igsagent_input_count(self->agent));
    }
    Py_RETURN_NONE;
}

PyObject *Agent_output_count(AgentObject *self, PyObject *args, PyObject *kwds)
{
    if(self->agent)
    {
        return PyLong_FromLong(igsagent_output_count(self->agent));
    }
    Py_RETURN_NONE;
}

PyObject *Agent_parameter_count(AgentObject *self, PyObject *args, PyObject *kwds)
{
    if(self->agent)
    {
        return PyLong_FromLong(igsagent_parameter_count(self->agent));
    }
    Py_RETURN_NONE;
}


PyObject *Agent_input_list(AgentObject *self, PyObject *args, PyObject *kwds)
{
    if(!self->agent)
        return PyLong_FromLong(IGS_FAILURE);
    size_t nbOfElements;
    PyObject * ret;

    char **result = igsagent_input_list(self->agent, &nbOfElements);
    ret = PyList_New(nbOfElements);
    for (int i = 0; i < nbOfElements; i++){
        PyList_SetItem(ret, i, Py_BuildValue("s",result[i]));
    }
    return ret;
}

PyObject *Agent_output_list(AgentObject *self, PyObject *args, PyObject *kwds)
{
    if(!self->agent)
        Py_RETURN_NONE;
    size_t nbOfElements;
    PyObject * ret;
    char **result = igsagent_output_list(self->agent, &nbOfElements);

    ret = PyList_New(nbOfElements);
    for (int i = 0; i < nbOfElements; i++){
        PyList_SetItem(ret, i, Py_BuildValue("s",result[i]));
    }
    return ret;
}

PyObject *Agent_parameter_list(AgentObject *self, PyObject *args, PyObject *kwds)
{
    if(!self->agent)
        Py_RETURN_NONE;
    size_t nbOfElements;
    char **result = igsagent_parameter_list(self->agent, &nbOfElements);
    PyObject * ret = PyList_New(nbOfElements);
    for (int i = 0; i < nbOfElements; i++){
        PyList_SetItem(ret, i, Py_BuildValue("s",result[i]));
    }
    return ret;
}


PyObject *Agent_input_exists(AgentObject *self, PyObject *args, PyObject *kwds)
{
    static char *kwlist[] = {"name",  NULL};
    char *name = NULL;

    if (!PyArg_ParseTupleAndKeywords(args, NULL, "s", kwlist, &name))
        Py_RETURN_NONE;
    if(igsagent_input_exists(self->agent,name)) {
        Py_RETURN_TRUE;
    }else{
        Py_RETURN_FALSE;
    }
}

PyObject *Agent_output_exists(AgentObject *self, PyObject *args, PyObject *kwds)
{
    static char *kwlist[] = {"name",  NULL};
    char *name = NULL;

    if (!PyArg_ParseTupleAndKeywords(args, NULL, "s", kwlist, &name))
        Py_RETURN_NONE;
    if (igsagent_output_exists(self->agent,name)) {
        Py_RETURN_TRUE;
    }else{
        Py_RETURN_FALSE;
    }
}

PyObject *Agent_parameter_exists(AgentObject *self, PyObject *args, PyObject *kwds)
{
    static char *kwlist[] = {"name",  NULL};
    char *name = NULL;

    if (!PyArg_ParseTupleAndKeywords(args, NULL, "s", kwlist, &name))
        Py_RETURN_NONE;
    if (igsagent_parameter_exists(self->agent,name)) {
        Py_RETURN_TRUE;
    }else{
        Py_RETURN_FALSE;
    }
}


PyObject *Agent_input_bool(AgentObject *self, PyObject *args, PyObject *kwds)
{
    static char *kwlist[] = {"name",  NULL};
    char *name = NULL;

    if (!PyArg_ParseTupleAndKeywords(args, NULL, "s", kwlist, &name))
        Py_RETURN_NONE;
    if (igsagent_input_bool(self->agent, name)) {
        Py_RETURN_TRUE;
    } else{
        Py_RETURN_FALSE;
    }
}

PyObject *Agent_input_int(AgentObject *self, PyObject *args, PyObject *kwds)
{
    if(!self->agent)
        Py_RETURN_NONE;
    static char *kwlist[] = {"name",  NULL};
    char *name = NULL;

    if (!PyArg_ParseTupleAndKeywords(args, NULL, "s", kwlist, &name))
        Py_RETURN_NONE;
    return PyLong_FromLong(igsagent_input_int(self->agent, name));
}

PyObject *Agent_input_double(AgentObject *self, PyObject *args, PyObject *kwds)
{
    if(!self->agent)
        Py_RETURN_NONE;
    static char *kwlist[] = {"name",  NULL};
    char *name = NULL;

    if (!PyArg_ParseTupleAndKeywords(args, NULL, "s", kwlist, &name))
        Py_RETURN_NONE;
    return PyFloat_FromDouble(igsagent_input_double(self->agent, name));
}

PyObject *Agent_input_string(AgentObject *self, PyObject *args, PyObject *kwds)
{
    if(!self->agent)
        Py_RETURN_NONE;
    static char *kwlist[] = {"name",  NULL};
    char *name = NULL;

    if (!PyArg_ParseTupleAndKeywords(args, NULL, "s", kwlist, &name))
        Py_RETURN_NONE;
    char *value = igsagent_input_string(self->agent, name);
    if(value == NULL)
        Py_RETURN_NONE;
    return PyUnicode_FromFormat("%s", value);
}

PyObject *Agent_input_data(AgentObject *self, PyObject *args, PyObject *kwds)
{
    if(!self->agent)
        Py_RETURN_NONE;
    static char *kwlist[] = {"name",  NULL};
    char *name = NULL;

    if (!PyArg_ParseTupleAndKeywords(args, NULL, "s", kwlist, &name))
        Py_RETURN_NONE;

    void *my_data = NULL;
    size_t valueSize = 0;
    igsagent_input_data(self->agent, name, &my_data, &valueSize);
    PyObject *ret = Py_BuildValue("y#", my_data, valueSize);
    return ret;
}


PyObject *Agent_output_bool(AgentObject *self, PyObject *args, PyObject *kwds)
{
    static char *kwlist[] = {"name",  NULL};
    char *name = NULL;

    if (!PyArg_ParseTupleAndKeywords(args, NULL, "s", kwlist, &name))
        return PyLong_FromLong(IGS_FAILURE);
    if (igsagent_output_bool(self->agent, name)) {
        Py_RETURN_TRUE;
    } else{
        Py_RETURN_FALSE;
    }
}

PyObject *Agent_output_int(AgentObject *self, PyObject *args, PyObject *kwds)
{
    if(!self->agent)
        Py_RETURN_NONE;
    static char *kwlist[] = {"name",  NULL};
    char *name = NULL;

    if (!PyArg_ParseTupleAndKeywords(args, NULL, "s", kwlist, &name))
        Py_RETURN_NONE;
    return PyLong_FromLong(igsagent_output_int(self->agent,name));
}

PyObject *Agent_output_double(AgentObject *self, PyObject *args, PyObject *kwds)
{
    if(!self->agent)
        Py_RETURN_NONE;
    static char *kwlist[] = {"name",  NULL};
    char *name = NULL;

    if (!PyArg_ParseTupleAndKeywords(args, NULL, "s", kwlist, &name))
        Py_RETURN_NONE;
    return PyFloat_FromDouble(igsagent_output_double(self->agent, name));
}

PyObject *Agent_output_string(AgentObject *self, PyObject *args, PyObject *kwds)
{
    if(!self->agent)
        Py_RETURN_NONE;
    static char *kwlist[] = {"name",  NULL};
    char *name = NULL;

    if (!PyArg_ParseTupleAndKeywords(args, NULL, "s", kwlist, &name))
        Py_RETURN_NONE;
    char *value = igsagent_output_string(self->agent, name);
    if(value == NULL)
        Py_RETURN_NONE;
    return PyUnicode_FromFormat("%s", value);
}

PyObject *Agent_output_data(AgentObject *self, PyObject *args, PyObject *kwds)
{
    if(!self->agent)
        Py_RETURN_NONE;
    static char *kwlist[] = {"name",  NULL};
    char *name = NULL;

    if (!PyArg_ParseTupleAndKeywords(args, NULL, "s", kwlist, &name))
        Py_RETURN_NONE;

    void *my_data = NULL;
    size_t valueSize = 0;
    igsagent_output_data(self->agent, name, &my_data, &valueSize);

    PyObject *ret = Py_BuildValue("y#", my_data, valueSize);
    return ret;
}


PyObject *Agent_parameter_bool(AgentObject *self, PyObject *args, PyObject *kwds)
{
    static char *kwlist[] = {"name",  NULL};
    char *name = NULL;

    if (!PyArg_ParseTupleAndKeywords(args, NULL, "s", kwlist, &name))
        return PyLong_FromLong(IGS_FAILURE);
    if (igsagent_parameter_bool(self->agent, name)) {
        Py_RETURN_TRUE;
    } else{
        Py_RETURN_FALSE;
    }
}

PyObject *Agent_parameter_int(AgentObject *self, PyObject *args, PyObject *kwds)
{
    if(!self->agent)
        Py_RETURN_NONE;
    static char *kwlist[] = {"name",  NULL};
    char *name = NULL;

    if (!PyArg_ParseTupleAndKeywords(args, NULL, "s", kwlist, &name))
        Py_RETURN_NONE;
    return PyLong_FromLong(igsagent_parameter_int(self->agent,name));
}

PyObject *Agent_parameter_double(AgentObject *self, PyObject *args, PyObject *kwds)
{
    if(!self->agent)
        Py_RETURN_NONE;
    static char *kwlist[] = {"name",  NULL};
    char *name = NULL;

    if (!PyArg_ParseTupleAndKeywords(args, NULL, "s", kwlist, &name))
        Py_RETURN_NONE;
    return PyFloat_FromDouble(igsagent_parameter_double(self->agent, name));
}

PyObject *Agent_parameter_string(AgentObject *self, PyObject *args, PyObject *kwds)
{
    if(!self->agent)
        Py_RETURN_NONE;
    static char *kwlist[] = {"name",  NULL};
    char *name = NULL;

    if (!PyArg_ParseTupleAndKeywords(args, NULL, "s", kwlist, &name))
        Py_RETURN_NONE;
    char *value = igsagent_parameter_string(self->agent, name);
    if(value == NULL)
        Py_RETURN_NONE;
    return PyUnicode_FromFormat("%s", value);
}

PyObject *Agent_parameter_data(AgentObject *self, PyObject *args, PyObject *kwds)
{
    if(!self->agent)
        Py_RETURN_NONE;
    static char *kwlist[] = {"name",  NULL};
    char *name = NULL;

    if (!PyArg_ParseTupleAndKeywords(args, NULL, "s", kwlist, &name))
        Py_RETURN_NONE;

    void *my_data = NULL;
    size_t valueSize = 0;
    igsagent_parameter_data(self->agent, name, &my_data, &valueSize);

    PyObject *ret = Py_BuildValue("y#", my_data, valueSize);
    return ret;
}


PyObject *Agent_input_set_bool(AgentObject *self, PyObject *args, PyObject *kwds)
{
    if(!self->agent)
        Py_RETURN_NONE;
    static char *kwlist[] = {"name", "value", NULL};
    char *name = NULL;
    int value;
    int result;

    if (!PyArg_ParseTupleAndKeywords(args, NULL, "sp", kwlist, &name, &value))
        Py_RETURN_NONE;

    if (value == 1){
        result = igsagent_input_set_bool(self->agent, name, true);
    }else{
        result = igsagent_input_set_bool(self->agent, name, false);
    }
    return PyLong_FromLong(result);
}

PyObject *Agent_input_set_int(AgentObject *self, PyObject *args, PyObject *kwds)
{
    if(!self->agent)
        Py_RETURN_NONE;
    static char *kwlist[] = {"name", "value", NULL};
    char *name = NULL;
    int value;

    if (!PyArg_ParseTupleAndKeywords(args, NULL, "si", kwlist, &name, &value))
        Py_RETURN_NONE;

    return PyLong_FromLong(igsagent_input_set_int(self->agent, name, value));
}

PyObject *Agent_input_set_double(AgentObject *self, PyObject *args, PyObject *kwds)
{
    if(!self->agent)
        Py_RETURN_NONE;
    static char *kwlist[] = {"name", "value", NULL};
    char *name = NULL;
    double value;

    if (!PyArg_ParseTupleAndKeywords(args, NULL, "sd", kwlist, &name, &value))
        Py_RETURN_NONE;

    return PyLong_FromLong(igsagent_input_set_double(self->agent, name, value));
}

PyObject *Agent_input_set_string(AgentObject *self, PyObject *args, PyObject *kwds)
{
   if(!self->agent)
        Py_RETURN_NONE;
    static char *kwlist[] = {"name", "value", NULL};
    char *name = NULL;
    char *value = NULL;

    // if (!PyArg_ParseTupleAndKeywords(args, kwds, "ss", kwlist, &name, &value)) //FIXME Cannot seem to make this work... May be related to my machine only due to a hazardous installation of python (brew vs. built-in and such)
    if (!PyArg_ParseTuple(args, "ss", &name, &value))
        Py_RETURN_NONE;

    return PyLong_FromLong(igsagent_input_set_string(self->agent, name, value));
}

PyObject *Agent_input_set_impulsion(AgentObject *self, PyObject *args, PyObject *kwds)
{
    if(!self->agent)
        Py_RETURN_NONE;
    static char *kwlist[] = {"name",NULL};
    char *name = NULL;

    if (!PyArg_ParseTupleAndKeywords(args, NULL, "s", kwlist, &name))
        Py_RETURN_NONE;

    return PyLong_FromLong(igsagent_input_set_impulsion(self->agent, name));
}

PyObject *Agent_input_set_data(AgentObject *self, PyObject *args, PyObject *kwds)
{
    if(!self->agent)
        Py_RETURN_NONE;
    static char *kwlist[] = {"name", "value", NULL};
    char * name;
    Py_buffer buf;
    if (!PyArg_ParseTupleAndKeywords(args, NULL, "sy*", kwlist, &name, &buf))
        Py_RETURN_NONE;

    return PyLong_FromLong(igsagent_input_set_data(self->agent, name, buf.buf, (size_t)buf.len));
}


PyObject *Agent_output_set_bool(AgentObject *self, PyObject *args, PyObject *kwds)
{
    if(!self->agent)
        Py_RETURN_NONE;
    static char *kwlist[] = {"name", "value", NULL};
    char *name = NULL;
    int value;
    int result = 0;
    if (!PyArg_ParseTupleAndKeywords(args, NULL, "sp", kwlist, &name, &value))
        Py_RETURN_NONE;

    if (value == 1){
        result = igsagent_output_set_bool(self->agent, name, true);
    }else{
        result = igsagent_output_set_bool(self->agent, name, false);
    }
    return PyLong_FromLong(result);
}

PyObject *Agent_output_set_int(AgentObject *self, PyObject *args, PyObject *kwds)
{
    if(!self->agent)
        Py_RETURN_NONE;
    static char *kwlist[] = {"name", "value", NULL};
    char *name = NULL;
    int value;

    if (!PyArg_ParseTupleAndKeywords(args, NULL, "si", kwlist, &name, &value))
        Py_RETURN_NONE;

    return PyLong_FromLong(igsagent_output_set_int(self->agent, name, value));
}

PyObject *Agent_output_set_double(AgentObject *self, PyObject *args, PyObject *kwds)
{
    if(!self->agent)
        Py_RETURN_NONE;
    static char *kwlist[] = {"name", "value", NULL};
    char *name = NULL;
    double value;

    if (!PyArg_ParseTupleAndKeywords(args, NULL, "sd", kwlist, &name, &value))
        Py_RETURN_NONE;

    return PyLong_FromLong(igsagent_output_set_double(self->agent, name, value));
}

PyObject *Agent_output_set_string(AgentObject *self, PyObject *args, PyObject *kwds)
{
   if(!self->agent)
        Py_RETURN_NONE;
    static char *kwlist[] = {"name", "value", NULL};
    char *name = NULL;
    char *value = NULL;

    // if (!PyArg_ParseTupleAndKeywords(args, NULL, "ss", kwlist, &name, &value)) //FIXME Cannot seem to make this work... May be related to my machine only due to a hazardous installation of python (brew vs. built-in and such)
    if (!PyArg_ParseTuple(args, "ss", &name, &value))
        Py_RETURN_NONE;

    return PyLong_FromLong(igsagent_output_set_string(self->agent, name, value));
}

PyObject *Agent_output_set_impulsion(AgentObject *self, PyObject *args, PyObject *kwds)
{
    if(!self->agent)
        Py_RETURN_NONE;
    static char *kwlist[] = {"name",NULL};
    char *name = NULL;

    if (!PyArg_ParseTupleAndKeywords(args, NULL, "s", kwlist, &name))
        Py_RETURN_NONE;

    return PyLong_FromLong(igsagent_output_set_impulsion(self->agent, name));
}

PyObject *Agent_output_set_data(AgentObject *self, PyObject *args, PyObject *kwds)
{
    if(!self->agent)
        Py_RETURN_NONE;
    static char *kwlist[] = {"name", "value", NULL};
    char * name;
    Py_buffer buf;
    if (!PyArg_ParseTupleAndKeywords(args, NULL, "sy*", kwlist, &name, &buf))
        Py_RETURN_NONE;

    return PyLong_FromLong(igsagent_output_set_data(self->agent, name, buf.buf, (size_t)buf.len));
}


PyObject *Agent_parameter_set_bool(AgentObject *self, PyObject *args, PyObject *kwds)
{
    if(!self->agent)
        Py_RETURN_NONE;
    static char *kwlist[] = {"name", "value", NULL};
    char *name = NULL;
    int value;
    int result;

    if (!PyArg_ParseTupleAndKeywords(args, NULL, "sp", kwlist, &name, &value))
        Py_RETURN_NONE;

    if (value == 1){
        result = igsagent_parameter_set_bool(self->agent, name, true);
    }else{
        result = igsagent_parameter_set_bool(self->agent, name, false);
    }
    return PyLong_FromLong(result);
}

PyObject *Agent_parameter_set_int(AgentObject *self, PyObject *args, PyObject *kwds)
{
    if(!self->agent)
        Py_RETURN_NONE;
    static char *kwlist[] = {"name", "value", NULL};
    char *name = NULL;
    int value;

    if (!PyArg_ParseTupleAndKeywords(args, NULL, "si", kwlist, &name, &value))
        Py_RETURN_NONE;

    return PyLong_FromLong(igsagent_parameter_set_int(self->agent, name, value));
}

PyObject *Agent_parameter_set_double(AgentObject *self, PyObject *args, PyObject *kwds)
{
    if(!self->agent)
        Py_RETURN_NONE;
    static char *kwlist[] = {"name", "value", NULL};
    char *name = NULL;
    double value;

    if (!PyArg_ParseTupleAndKeywords(args, NULL, "sd", kwlist, &name, &value))
        Py_RETURN_NONE;

    return PyLong_FromLong(igsagent_parameter_set_double(self->agent, name, value));
}

PyObject *Agent_parameter_set_string(AgentObject *self, PyObject *args, PyObject *kwds)
{
   if(!self->agent)
        Py_RETURN_NONE;
    static char *kwlist[] = {"name", "value", NULL};
    char *name = NULL;
    char *value = NULL;

    // if (!PyArg_ParseTupleAndKeywords(args, NULL, "ss", kwlist, &name, &value)) //FIXME Cannot seem to make this work... May be related to my machine only due to a hazardous installation of python (brew vs. built-in and such)
    if (!PyArg_ParseTuple(args, "ss", &name, &value))
        Py_RETURN_NONE;

    return PyLong_FromLong(igsagent_parameter_set_string(self->agent, name, value));
}

PyObject *Agent_parameter_set_data(AgentObject *self, PyObject *args, PyObject *kwds)
{
    if(!self->agent)
        Py_RETURN_NONE;
    static char *kwlist[] = {"name", "value", NULL};
    char * name;
    Py_buffer buf;
    if (!PyArg_ParseTupleAndKeywords(args, NULL, "sy*", kwlist, &name, &buf))
        Py_RETURN_NONE;

    return PyLong_FromLong(igsagent_parameter_set_data(self->agent, name, buf.buf, (size_t)buf.len));
}

PyObject *Agent_clear_input(AgentObject *self, PyObject *args, PyObject *kwds)
{
    if(!self->agent)
        Py_RETURN_NONE;
    static char *kwlist[] = {"name",  NULL};
    char *name = NULL;

    if (!PyArg_ParseTupleAndKeywords(args, NULL, "s", kwlist, &name))
        Py_RETURN_NONE;
    igsagent_clear_input(self->agent, name);
    return PyLong_FromLong(IGS_SUCCESS);
}

PyObject *Agent_clear_output(AgentObject *self, PyObject *args, PyObject *kwds)
{
    if(!self->agent)
        Py_RETURN_NONE;
    static char *kwlist[] = {"name",  NULL};
    char *name = NULL;

    if (!PyArg_ParseTupleAndKeywords(args, NULL, "s", kwlist, &name))
        Py_RETURN_NONE;
    igsagent_clear_output(self->agent, name);
    return PyLong_FromLong(IGS_SUCCESS);
}

PyObject *Agent_clear_parameter(AgentObject *self, PyObject *args, PyObject *kwds)
{
    if(!self->agent)
        Py_RETURN_NONE;
    static char *kwlist[] = {"name",  NULL};
    char *name = NULL;

    if (!PyArg_ParseTupleAndKeywords(args, NULL, "s", kwlist, &name))
        Py_RETURN_NONE;
    igsagent_clear_parameter(self->agent, name);
    return PyLong_FromLong(IGS_SUCCESS);
}

//observeCallback that execute the callback for the iop that has been changed
void agent_observe(igsagent_t* agent, igs_iop_type_t iopType, const char* name, igs_iop_value_type_t valueType, void* value, unsigned long valueSize, void* myData){
    IGS_UNUSED(myData);
    PyGILState_STATE d_gstate;
    d_gstate = PyGILState_Ensure();
    //run through all callbacks to execute them
    PyObject *tupleArgs = PyTuple_New(6);
    PyTuple_SetItem(tupleArgs, 1, Py_BuildValue("i", iopType));
    PyTuple_SetItem(tupleArgs, 2, Py_BuildValue("s", name));
    PyTuple_SetItem(tupleArgs, 3, Py_BuildValue("i", valueType));
    switch(valueType){
        case IGS_BOOL_T:
            if (*(bool*)value){
                PyTuple_SetItem(tupleArgs, 4, Py_True);
            }else{
                PyTuple_SetItem(tupleArgs, 4, Py_False);
            }
            break;
        case IGS_INTEGER_T:
            PyTuple_SetItem(tupleArgs, 4, Py_BuildValue("i", *(int*)value));
            break;
        case IGS_DOUBLE_T:
            PyTuple_SetItem(tupleArgs, 4, Py_BuildValue("d", *(double*)value));
            break;
        case IGS_STRING_T:
            PyTuple_SetItem(tupleArgs, 4, Py_BuildValue("s", (char*)value));
            break;
        case IGS_IMPULSION_T:
            PyTuple_SetItem(tupleArgs, 4, Py_None);
            break;
        case IGS_DATA_T:
            PyTuple_SetItem(tupleArgs, 4, Py_BuildValue("y#", value, valueSize));
            break;
        case IGS_UNKNOWN_T:
            break;
    }

    agentobserve_iop_cb_t *actuel = NULL;
    DL_FOREACH(agentobserve_iop_cbList, actuel) {
        if (streq(actuel->nameArg, name)
            && (actuel->agent->agent == agent)
            && (actuel->iopType == iopType)) {
            PyTuple_SetItem(tupleArgs, 0, Py_BuildValue("O", actuel->agent));
            Py_INCREF(actuel->my_data);
            PyTuple_SetItem(tupleArgs, 5, actuel->my_data);
            PyObject_Call(actuel->callback, tupleArgs, NULL);
            Py_DECREF(tupleArgs);
        }
    }
    PyGILState_Release(d_gstate);
}

PyObject *_Agent_observe_generic(AgentObject *self, PyObject *args, PyObject *kwds, igs_iop_type_t iopType)
{
    if(!self->agent)
        return PyLong_FromLong(IGS_FAILURE);

    PyObject *callback = NULL;
    PyObject *my_data = NULL;
    char *iopName = NULL;
    // static char *kwlist[] = {"iop_name", "callback", "args", NULL};
    // if (PyArg_ParseTupleAndKeywords(args, NULL, "sOO", kwlist, &iopName, &callback, &my_data)) { //FIXME Cannot seem to make this work... May be related to my machine only due to a hazardous installation of python (brew vs. built-in and such)
    if (PyArg_ParseTuple(args, "sOO", &iopName, &callback, &my_data)) {
        if (!PyCallable_Check(callback)) { // check if the callback is a function
            PyErr_SetString(PyExc_TypeError, "'callback' parameter must be callable");
            return PyLong_FromLong(IGS_FAILURE);;
        }
    }
    else {
        return PyLong_FromLong(IGS_FAILURE);
    }

    // add the callback to the list of Callbacks
    agentobserve_iop_cb_t *newElt = calloc(1, sizeof(agentobserve_iop_cb_t));
    newElt->agent = self;
    newElt->iopType = iopType;
    newElt->nameArg = strdup(iopName);
    newElt->my_data = Py_BuildValue("O", my_data);
    newElt->callback = callback;
    DL_APPEND(agentobserve_iop_cbList, newElt);
    switch(iopType)
    {
        case IGS_INPUT_T:
            igsagent_observe_input(self->agent, iopName, agent_observe, NULL);
            break;
        case IGS_OUTPUT_T:
            igsagent_observe_output(self->agent, iopName, agent_observe, NULL);
            break;
        case IGS_PARAMETER_T:
            igsagent_observe_parameter(self->agent, iopName, agent_observe, NULL);
            break;
    }

    return PyLong_FromLong(IGS_SUCCESS);
}

PyObject *Agent_observe_input(AgentObject *self, PyObject *args, PyObject *kwds)
{
    return _Agent_observe_generic(self, args, NULL, IGS_INPUT_T);
}

PyObject *Agent_observe_output(AgentObject *self, PyObject *args, PyObject *kwds)
{
    return _Agent_observe_generic(self, args, NULL, IGS_OUTPUT_T);
}

PyObject *Agent_observe_parameter(AgentObject *self, PyObject *args, PyObject *kwds)
{
    return _Agent_observe_generic(self, args, NULL, IGS_PARAMETER_T);
}


PyObject *Agent_output_mute(AgentObject *self, PyObject *args, PyObject *kwds)
{
    if(!self->agent)
        Py_RETURN_NONE;
    static char *kwlist[] = {"name",  NULL};
    char *name = NULL;

    if (!PyArg_ParseTupleAndKeywords(args, NULL, "s", kwlist, &name))
        Py_RETURN_NONE;
    igsagent_output_mute(self->agent, name);
    return PyLong_FromLong(IGS_SUCCESS);
}

PyObject *Agent_output_unmute(AgentObject *self, PyObject *args, PyObject *kwds)
{
    if(!self->agent)
        Py_RETURN_NONE;
    static char *kwlist[] = {"name",  NULL};
    char *name = NULL;

    if (!PyArg_ParseTupleAndKeywords(args, NULL, "s", kwlist, &name))
        Py_RETURN_NONE;
    igsagent_output_unmute(self->agent, name);
    return PyLong_FromLong(IGS_SUCCESS);
}

PyObject *Agent_output_is_muted(AgentObject *self, PyObject *args, PyObject *kwds)
{
    if(!self->agent)
        Py_RETURN_NONE;
    static char *kwlist[] = {"name",  NULL};
    char *name = NULL;

    if (!PyArg_ParseTupleAndKeywords(args, NULL, "s", kwlist, &name))
        Py_RETURN_NONE;
    if (igsagent_output_is_muted(self->agent, name)) {
        Py_RETURN_TRUE;
    }else{
        Py_RETURN_FALSE;
    }
}

PyObject *Agent_definition_set_path(AgentObject *self, PyObject *args, PyObject *kwds)
{
    if(!self->agent)
        Py_RETURN_NONE;
    static char *kwlist[] = {"path",  NULL};
    char *path = NULL;

    if (!PyArg_ParseTupleAndKeywords(args, NULL, "s", kwlist, &path))
        Py_RETURN_NONE;
    igsagent_definition_set_path(self->agent, path);
    return PyLong_FromLong(0);
}

PyObject *Agent_definition_save(AgentObject *self, PyObject *args, PyObject *kwds)
{
    if(!self->agent)
        Py_RETURN_NONE;
    igsagent_definition_save(self->agent);
    return PyLong_FromLong(0);
}
