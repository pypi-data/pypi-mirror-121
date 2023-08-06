//
//  agent_network.h
//  ingescape wrapper
//
//  Created by vaugien on 06/09/2021.
//  Copyright © 2021 ingenuity. All rights reserved.
//

#ifndef agent_network_h
#define agent_network_h

#include <Python.h>
#include <frameobject.h>
#include "agent.h"

typedef struct agentMuteCB {
    AgentObject* agent;
    PyObject* callback;
    PyObject* my_data;
    struct agentMuteCB *prev;
    struct agentMuteCB *next;
} agentMuteCB_t;
extern agentMuteCB_t *agentMuteCBList;

PyObject *Agent_name(AgentObject *self, PyObject *args, PyObject *kwds);
PyObject *Agent_set_name(AgentObject *self, PyObject *args, PyObject *kwds);
PyObject *Agent_family(AgentObject *self, PyObject *args, PyObject *kwds);
PyObject *Agent_set_family(AgentObject *self, PyObject *args, PyObject *kwds);
PyObject *Agent_uuid(AgentObject *self, PyObject *args, PyObject *kwds);
PyObject *Agent_state(AgentObject *self, PyObject *args, PyObject *kwds);
PyObject *Agent_set_state(AgentObject *self, PyObject *args, PyObject *kwds);
PyObject *Agent_mute(AgentObject *self, PyObject *args, PyObject *kwds);
PyObject *Agent_unmute(AgentObject *self, PyObject *args, PyObject *kwds);
PyObject *Agent_is_muted(AgentObject *self, PyObject *args, PyObject *kwds);
PyObject *Agent_observe_mute(AgentObject *self, PyObject *args, PyObject *kwds);

PyObject *Agent_election_join(AgentObject *self, PyObject *args, PyObject *kwds);
PyObject *Agent_election_leave(AgentObject *self, PyObject *args, PyObject *kwds);

#endif /* agent_network_h */
