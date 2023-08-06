//
//  agent_mapping.h
//  ingescape wrapper
//
//  Created by vaugien on 06/09/2021.
//  Copyright © 2021 ingenuity. All rights reserved.
//

#ifndef agent_mapping_h
#define agent_mapping_h

#include <Python.h>
#include <frameobject.h>
#include "agent.h"

PyObject *Agent_mapping_load_str(AgentObject *self, PyObject *args, PyObject *kwds);
PyObject *Agent_mapping_load_file(AgentObject *self, PyObject *args, PyObject *kwds);
PyObject *Agent_mapping_json(AgentObject *self, PyObject *args, PyObject *kwds);
PyObject *Agent_mapping_count(AgentObject *self, PyObject *args, PyObject *kwds);
PyObject *Agent_clear_mappings(AgentObject *self, PyObject *args, PyObject *kwds);
PyObject *Agent_clear_mappings_with_agent(AgentObject *self, PyObject *args, PyObject *kwds);
PyObject *Agent_mapping_add(AgentObject *self, PyObject *args, PyObject *kwds);
PyObject *Agent_mapping_remove_with_id(AgentObject *self, PyObject *args, PyObject *kwds);
PyObject *Agent_mapping_remove_with_name(AgentObject *self, PyObject *args, PyObject *kwds);

PyObject *Agent_mapping_outputs_request(AgentObject *self, PyObject *args, PyObject *kwds);
PyObject *Agent_mapping_set_outputs_request(AgentObject *self, PyObject *args, PyObject *kwds);

PyObject *Agent_mapping_set_path(AgentObject *self, PyObject *args, PyObject *kwds);
PyObject *Agent_mapping_save(AgentObject *self, PyObject *args, PyObject *kwds);

#endif /* agent_mapping_h */