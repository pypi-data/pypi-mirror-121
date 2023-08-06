//
//  agent_init.h
//  ingescape wrapper
//
//  Created by vaugien on 06/09/2021.
//  Copyright © 2021 ingenuity. All rights reserved.
//

#ifndef agent_init_h
#define agent_init_h

#include <Python.h>
#include <frameobject.h>
#include "agent.h"

typedef struct agentObserveCB {
    AgentObject* agent;
    PyObject* callback;
    PyObject* my_data;
    struct agentObserveCB *prev;
    struct agentObserveCB *next;
} agentObserveCB_t;
extern agentObserveCB_t* agentObserveCBList;

typedef struct agentObserveEventsCB {
    AgentObject* agent;
    PyObject* callback;
    PyObject* my_data;
    struct agentObserveEventsCB *prev;
    struct agentObserveEventsCB *next;
} agentObserveEventsCB_t;
extern agentObserveEventsCB_t *agentObserveEventsCBList;

PyObject *Agent_activate(AgentObject *self, PyObject *args, PyObject *kwds);
PyObject *Agent_deactivate(AgentObject *self, PyObject *args, PyObject *kwds);
PyObject *Agent_is_activated(AgentObject *self, PyObject *args, PyObject *kwds);
PyObject *Agent_observe(AgentObject *self, PyObject *args, PyObject *kwds);
PyObject *Agent_observe_agent_event(AgentObject *self, PyObject *args, PyObject *kwds);

PyObject *Agent_trace(AgentObject *self, PyObject *args, PyObject *kwds);
PyObject *Agent_debug(AgentObject *self, PyObject *args, PyObject *kwds);
PyObject *Agent_info(AgentObject *self, PyObject *args, PyObject *kwds);
PyObject *Agent_warn(AgentObject *self, PyObject *args, PyObject *kwds);
PyObject *Agent_error(AgentObject *self, PyObject *args, PyObject *kwds);
PyObject *Agent_fatal(AgentObject *self, PyObject *args, PyObject *kwds);

#endif /* agent_init_h */
