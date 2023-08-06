//
//  mapping.h
//  ingescapeWrapp
//
//  Created by vaugien on 12/02/2018.
//  Copyright © 2018 ingenuity. All rights reserved.
//

#include "mapping.h"
#include <stdio.h>
#include <ingescape/ingescape.h>

//igs_mapping_load_str
 PyObject * loadMapping_wrapper(PyObject * self, PyObject * args)
{
    char * json_str;
    int result;
    // parse arguments
    if (!PyArg_ParseTuple(args, "s", &json_str)) {
        return NULL;
    }
    result = igs_mapping_load_str(json_str);
    return PyLong_FromLong(result);
}

//igs_mapping_load_file
 PyObject * loadMappingFromPath_wrapper(PyObject * self, PyObject * args)
{
    char* file_path;
    // parse arguments
    if (!PyArg_ParseTuple(args, "s", &file_path)) {
        return NULL;
    }
    int result = igs_mapping_load_file(file_path);
    return PyLong_FromLong(result);
}

//igs_clear_mappings
 PyObject * clearMapping_wrapper(PyObject * self, PyObject * args)
{
    igs_clear_mappings();
    return PyLong_FromLong(0);
}

//igs_mapping_json
 PyObject * getMapping_wrapper(PyObject * self, PyObject * args)
{
    char * result;
    PyObject * ret;
    result = igs_mapping_json();
    if(result != NULL){
        return Py_BuildValue("s",result);
    }else{
        return Py_BuildValue("s","");
    }
}

//getMappingEntriesNumber
 PyObject * getMappingEntriesNumber_wrapper(PyObject * self, PyObject * args)
{
    int result = igs_mapping_count();
    return PyLong_FromLong(result);
}


//addMappingEntry
PyObject * addMappingEntry_wrapper(PyObject * self, PyObject * args)
{
    char * fromOutput;
    char * toAgent;
    char * withOutput;
    uint64_t result;
    // parse arguments : the input, the agent and the output of the entry
    if (!PyArg_ParseTuple(args, "sss", &fromOutput, &toAgent, &withOutput)) {
        return NULL;
    }
    result = igs_mapping_add(fromOutput, toAgent, withOutput);
    return PyLong_FromUnsignedLongLong((unsigned long long)result);
}

//igs_mapping_remove_with_id
 PyObject * removeMappingEntryWithId_wrapper(PyObject * self, PyObject * args)
{
    unsigned long long theId;
    unsigned long result;
    // parse and cast the id of the entry
    if (!PyArg_ParseTuple(args, "K", &theId)) {
        return NULL;
    }
    result = igs_mapping_remove_with_id((u_int64_t)theId);
    return PyLong_FromLong(result);
}

//igs_mapping_remove_with_name
 PyObject * removeMappingEntryWithName_wrapper(PyObject * self, PyObject * args)
{
    char * fromOurInput;
    char * toAgent;
    char * withOutput;
    int result;
    // parse arguments : the input, the agent and the output of the entry
    if (!PyArg_ParseTuple(args, "sss", &fromOurInput, &toAgent, &withOutput)) {
        return NULL;
    }
    result = igs_mapping_remove_with_name(fromOurInput, toAgent, withOutput);
    return PyLong_FromLong(result);
}

 PyObject * setRequestOutputsFromMappedAgents_wrapper(PyObject * self, PyObject * args)
{
    int notify;
    // parse arguments
    if (!PyArg_ParseTuple(args, "i", &notify)) {
        return NULL;
    }
    igs_mapping_set_outputs_request(notify);
    return PyLong_FromLong(0);
}

 PyObject * getRequestOutputsFromMappedAgents_wrapper(PyObject * self, PyObject * args)
{
    bool notify = igs_mapping_outputs_request();
    // build the resulting bool into a Python object and return it
    if(notify){
        Py_RETURN_TRUE;
    }else{
        Py_RETURN_FALSE;
    }

}


PyObject *split_count_wrapper(PyObject *self, PyObject *args, PyObject *kwds)
{
    return PyLong_FromLong((long)igs_split_count());
}

PyObject *split_add_wrapper(PyObject *self, PyObject *args, PyObject *kwds)
{
    static char *kwlist[] = {"from_our_input", "to_agent", "with_output",  NULL};
    char *from_our_input = NULL;
    char *to_agent = NULL;
    char *with_output = NULL;

    if (!PyArg_ParseTupleAndKeywords(args, NULL, "sss", kwlist, &from_our_input, &to_agent, &with_output))
        return NULL;
    return PyLong_FromUnsignedLongLong((unsigned long long)igs_split_add(from_our_input, to_agent, with_output));
    
}

PyObject *split_remove_with_id_wrapper(PyObject *self, PyObject *args, PyObject *kwds)
{
    static char *kwlist[] = {"id",  NULL};
    unsigned long long id_mapp = 0;
    if (!PyArg_ParseTupleAndKeywords(args, NULL, "K", kwlist, &id_mapp))
        return NULL;
    return PyLong_FromLong(igs_split_remove_with_id((uint64_t)id_mapp));
}

PyObject *split_remove_with_name_wrapper(PyObject *self, PyObject *args, PyObject *kwds)
{
    static char *kwlist[] = {"from_our_input", "to_agent", "with_output",  NULL};
    char *from_our_input = NULL;
    char *to_agent = NULL;
    char *with_output = NULL;

    if (!PyArg_ParseTupleAndKeywords(args, NULL, "sss", kwlist, &from_our_input, &to_agent, &with_output))
        return NULL;
    return PyLong_FromLong(igs_split_remove_with_name(from_our_input, to_agent, with_output));
}
