//
//  agent_split.h
//  ingescape wrapper
//
//  Created by vaugien on 06/09/2021.
//  Copyright © 2021 ingenuity. All rights reserved.
//

#ifndef agent_split_h
#define agent_split_h

#include <Python.h>
#include <frameobject.h>
#include "agent.h"

PyObject *Agent_split_count(AgentObject *self, PyObject *args, PyObject *kwds);
PyObject *Agent_split_add(AgentObject *self, PyObject *args, PyObject *kwds);
PyObject *Agent_split_remove_with_id(AgentObject *self, PyObject *args, PyObject *kwds);
PyObject *Agent_split_remove_with_name(AgentObject *self, PyObject *args, PyObject *kwds);

#endif /* agent_split_h */