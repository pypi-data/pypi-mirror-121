//
//  init.c
//  ingescapeWrapp
//
//  Created by vaugien on 06/02/2018.
//  Copyright © 2018 ingenuity. All rights reserved.
//

#include "init.h"
#include <stdio.h>
#include <ingescape/ingescape.h>



 // wrapper for igs_setAgentname
 PyObject * setAgentName_wrapper(PyObject * self, PyObject * args)
{
    char * name;
    // parse arguments
    if (!PyArg_ParseTuple(args, "s", &name)) {
        return NULL;
    }
    igs_agent_set_name(name);
    return PyLong_FromLong(0);
}

 // wrapper for igs_getAgentname
 PyObject * getAgentName_wrapper(PyObject * self, PyObject * args)
{
    char * result;
    PyObject * ret;
    result = igs_agent_name();
    // build the resulting string into a Python object.
    if(result != NULL){
        return Py_BuildValue("s",result);
    }else{
        return Py_BuildValue("s","");
    }
}

// wrapper for igs_setAgentname
PyObject * getAgentFamily_wrapper(PyObject * self, PyObject * args)
{
    char * family;
    PyObject * ret;
    family = igs_agent_family();
    // build the resulting string into a Python object.
    if(family != NULL){
        return Py_BuildValue("s", family);
    }else{
        Py_RETURN_NONE;
    }
}

// wrapper for igs_getAgentname
PyObject * setAgentFamily_wrapper(PyObject * self, PyObject * args)
{
    char * family;
    // parse arguments
    if (!PyArg_ParseTuple(args, "s", &family)) {
        return NULL;
    }
    igs_agent_set_family(family);
    return PyLong_FromLong(IGS_SUCCESS);
}

 // wrapper for igs_agent_set_state
 PyObject * setAgentState_wrapper(PyObject * self, PyObject * args)
{
    char * state;
    // parse arguments
    if (!PyArg_ParseTuple(args, "s", &state)) {
        return NULL;
    }
    igs_agent_set_state(state);
    return PyLong_FromLong(0);
}

 // wrapper for igs_agent_state
 PyObject * getAgentState_wrapper(PyObject * self, PyObject * args)
{
    char * result;
    PyObject * ret;
    result = igs_agent_state();
    // build the resulting string into a Python object.
    if(result != NULL){
        return Py_BuildValue("s",result);
    }else{
        return Py_BuildValue("s","");
    }
}

 // wrapper for igs_agent_mute
 PyObject * mute_wrapper(PyObject * self, PyObject * args)
{
    igs_agent_mute();
    return PyLong_FromLong(0);
}



// wrapper for igs_agent_unmute
 PyObject * unmute_wrapper(PyObject * self, PyObject * args)
{
    igs_agent_unmute();
    return PyLong_FromLong(0);
}


// wrapper for igs_ismute
 PyObject * ismuted_wrapper(PyObject * self, PyObject * args)
{
    if (igs_agent_is_muted()){
        Py_RETURN_TRUE;
    }else{
        Py_RETURN_FALSE;
    }
}


// wrapper for igs_freeze
 PyObject * freeze_wrapper(PyObject * self, PyObject * args)
{
    igs_freeze();
    return PyLong_FromLong(0);
}



// wrapper for igs_unfreeze
 PyObject * unfreeze_wrapper(PyObject * self, PyObject * args)
{
    igs_unfreeze();
    return PyLong_FromLong(0);
}

// wrapper for igs_is_frozen
 PyObject * isFrozen_wrapper(PyObject * self, PyObject * args)
{
    if (igs_is_frozen()){
        Py_RETURN_TRUE;
    }else{
        Py_RETURN_FALSE;
    }
}
