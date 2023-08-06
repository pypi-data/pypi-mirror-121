//
//  init.h
//  ingescapeWrapp
//
//  Created by vaugien on 06/04/2018.
//  Copyright © 2018 ingenuity. All rights reserved.
//

#ifndef init_h
#define init_h
#include <Python.h>



// wrapper for igs_setAgentname
 PyObject * setAgentName_wrapper(PyObject * self, PyObject * args);

// wrapper for igs_getAgentname
 PyObject * getAgentName_wrapper(PyObject * self, PyObject * args);

// wrapper for igs_setAgentname
 PyObject * getAgentFamily_wrapper(PyObject * self, PyObject * args);

// wrapper for igs_getAgentname
 PyObject * setAgentFamily_wrapper(PyObject * self, PyObject * args);

// wrapper for igs_agent_set_state
 PyObject * setAgentState_wrapper(PyObject * self, PyObject * args);

// wrapper for igs_agent_state
 PyObject * getAgentState_wrapper(PyObject * self, PyObject * args);

// wrapper for igs_agent_mute
 PyObject * mute_wrapper(PyObject * self, PyObject * args);

// wrapper for igs_agent_unmute
 PyObject * unmute_wrapper(PyObject * self, PyObject * args);

// wrapper for igs_ismute
 PyObject * ismuted_wrapper(PyObject * self, PyObject * args);

// wrapper for igs_freeze
 PyObject * freeze_wrapper(PyObject * self, PyObject * args);

// wrapper for igs_unfreeze
 PyObject * unfreeze_wrapper(PyObject * self, PyObject * args);

// wrapper for igs_is_frozen
 PyObject * isFrozen_wrapper(PyObject * self, PyObject * args);

PyDoc_STRVAR(
             setAgentNameDoc,
             "igs_agent_set_name(agentName)\n"
             "--\n"
             "\n"
             "set the name of the agent");

PyDoc_STRVAR(
             getAgentNameDoc,
             "igs_agent_name()\n"
             "--\n"
             "\n"
             "get the name of the agent");

PyDoc_STRVAR(
             setAgentFamilyDoc,
             "igs_agent_set_family(family)\n"
             "--\n"
             "\n"
             "set the family of the agent");

PyDoc_STRVAR(
             getAgentFamilyDoc,
             "igs_agent_family()\n"
             "--\n"
             "\n"
             "get the family of the agent");

PyDoc_STRVAR(
             setAgentStateDoc,
             "igs_agent_set_state(agentState)\n"
             "--\n"
             "\n"
             "set the state of the agent");

PyDoc_STRVAR(
             getAgentStateDoc,
             "igs_agent_state()\n"
             "--\n"
             "\n"
             "get the state of the agent");

PyDoc_STRVAR(
             muteDoc,
             "igs_agent_mute()\n"
             "--\n"
             "\n"
             "mute the agent");

PyDoc_STRVAR(
             unmuteDoc,
             "igs_agent_unmute()\n"
             "--\n"
             "\n"
             "unmute the agent");

PyDoc_STRVAR(
             ismutedDoc,
             "igs_agent_is_muted()\n"
             "--\n"
             "\n"
             "return True if the agent is muted");

PyDoc_STRVAR(
             freezeDoc,
             "igs_freeze()\n"
             "--\n"
             "\n"
             "freeze the agent");

PyDoc_STRVAR(
             unfreezeDoc,
             "igs_unfreeze()\n"
             "--\n"
             "\n"
             "unfreeze the agent");

PyDoc_STRVAR(
             isfrozenDoc,
             "igs_is_frozen()\n"
             "--\n"
             "\n"
             "return True if the agent is frozen");

#endif /* init_h */
