//
//  agent_service.h
//  ingescape wrapper
//
//  Created by vaugien on 06/09/2021.
//  Copyright © 2021 ingenuity. All rights reserved.
//

#ifndef agent_service_h
#define agent_service_h

#include <Python.h>
#include <frameobject.h>
#include "agent.h"

typedef struct agentServicesCB {
    AgentObject* agent;      // Agent ref
    const char* serviceName; // Service name
    PyObject *callback;      // python method to call back
    PyObject *my_data;       // myData argument of the callback
    struct agentServicesCB *next;
    struct agentServicesCB *prev;
} agentServiceCB_t;
extern agentServiceCB_t* agentServiceCBList;

PyObject *Agent_service_call(AgentObject *self, PyObject *args, PyObject *kwds);
PyObject *Agent_service_init(AgentObject *self, PyObject *args, PyObject *kwds);
PyObject *Agent_service_remove(AgentObject *self, PyObject *args, PyObject *kwds);
PyObject *Agent_service_arg_add(AgentObject *self, PyObject *args, PyObject *kwds);
PyObject *Agent_service_arg_remove(AgentObject *self, PyObject *args, PyObject *kwds);
PyObject *Agent_service_count(AgentObject *self, PyObject *args, PyObject *kwds);
PyObject *Agent_service_exists(AgentObject *self, PyObject *args, PyObject *kwds);
PyObject *Agent_service_list(AgentObject *self, PyObject *args, PyObject *kwds);
PyObject *Agent_service_args_count(AgentObject *self, PyObject *args, PyObject *kwds);
PyObject *Agent_service_args_list(AgentObject *self, PyObject *args, PyObject *kwds);
PyObject *Agent_service_args_exists(AgentObject *self, PyObject *args, PyObject *kwds);

#endif /* agent_service_h */
