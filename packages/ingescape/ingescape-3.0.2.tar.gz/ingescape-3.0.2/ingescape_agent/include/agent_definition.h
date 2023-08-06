//
//  agent_definition.h
//  ingescape wrapper
//
//  Created by vaugien on 06/09/2021.
//  Copyright © 2021 ingenuity. All rights reserved.
//

#ifndef agent_definition_h
#define agent_definition_h

#define PY_SSIZE_T_CLEAN
#include <Python.h>
#include <frameobject.h>
#include "agent.h"

typedef struct agentobserve_iop_cb {
    AgentObject* agent;     // Agent ref
    char *nameArg;          // name of the iop
    igs_iop_type_t iopType; // IOP type
    PyObject *callback;     // observeCallback
    PyObject *my_data;      // argument of the callback
    struct agentobserve_iop_cb *next;
    struct agentobserve_iop_cb *prev;
} agentobserve_iop_cb_t;
extern agentobserve_iop_cb_t *agentobserve_iop_cbList;

PyObject *Agent_definition_load_str(AgentObject *self, PyObject *args, PyObject *kwds);
PyObject *Agent_definition_load_file(AgentObject *self, PyObject *args, PyObject *kwds);
PyObject *Agent_clear_definition(AgentObject *self, PyObject *args, PyObject *kwds);
PyObject *Agent_definition_json(AgentObject *self, PyObject *args, PyObject *kwds);
PyObject *Agent_definition_description(AgentObject *self, PyObject *args, PyObject *kwds);
PyObject *Agent_definition_version(AgentObject *self, PyObject *args, PyObject *kwds);
PyObject *Agent_definition_set_description(AgentObject *self, PyObject *args, PyObject *kwds);
PyObject *Agent_definition_set_version(AgentObject *self, PyObject *args, PyObject *kwds);

PyObject *Agent_input_create(AgentObject *self, PyObject *args, PyObject *kwds);
PyObject *Agent_output_create(AgentObject *self, PyObject *args, PyObject *kwds);
PyObject *Agent_parameter_create(AgentObject *self, PyObject *args, PyObject *kwds);

PyObject *Agent_input_remove(AgentObject *self, PyObject *args, PyObject *kwds);
PyObject *Agent_output_remove(AgentObject *self, PyObject *args, PyObject *kwds);
PyObject *Agent_parameter_remove(AgentObject *self, PyObject *args, PyObject *kwds);

PyObject *Agent_input_type(AgentObject *self, PyObject *args, PyObject *kwds);
PyObject *Agent_output_type(AgentObject *self, PyObject *args, PyObject *kwds);
PyObject *Agent_parameter_type(AgentObject *self, PyObject *args, PyObject *kwds);

PyObject *Agent_input_count(AgentObject *self, PyObject *args, PyObject *kwds);
PyObject *Agent_output_count(AgentObject *self, PyObject *args, PyObject *kwds);
PyObject *Agent_parameter_count(AgentObject *self, PyObject *args, PyObject *kwds);

PyObject *Agent_input_list(AgentObject *self, PyObject *args, PyObject *kwds);
PyObject *Agent_output_list(AgentObject *self, PyObject *args, PyObject *kwds);
PyObject *Agent_parameter_list(AgentObject *self, PyObject *args, PyObject *kwds);

PyObject *Agent_input_exists(AgentObject *self, PyObject *args, PyObject *kwds);
PyObject *Agent_output_exists(AgentObject *self, PyObject *args, PyObject *kwds);
PyObject *Agent_parameter_exists(AgentObject *self, PyObject *args, PyObject *kwds);

PyObject *Agent_input_bool(AgentObject *self, PyObject *args, PyObject *kwds);
PyObject *Agent_input_int(AgentObject *self, PyObject *args, PyObject *kwds);
PyObject *Agent_input_double(AgentObject *self, PyObject *args, PyObject *kwds);
PyObject *Agent_input_string(AgentObject *self, PyObject *args, PyObject *kwds);
PyObject *Agent_input_data(AgentObject *self, PyObject *args, PyObject *kwds);

PyObject *Agent_output_bool(AgentObject *self, PyObject *args, PyObject *kwds);
PyObject *Agent_output_int(AgentObject *self, PyObject *args, PyObject *kwds);
PyObject *Agent_output_double(AgentObject *self, PyObject *args, PyObject *kwds);
PyObject *Agent_output_string(AgentObject *self, PyObject *args, PyObject *kwds);
PyObject *Agent_output_data(AgentObject *self, PyObject *args, PyObject *kwds);

PyObject *Agent_parameter_bool(AgentObject *self, PyObject *args, PyObject *kwds);
PyObject *Agent_parameter_int(AgentObject *self, PyObject *args, PyObject *kwds);
PyObject *Agent_parameter_double(AgentObject *self, PyObject *args, PyObject *kwds);
PyObject *Agent_parameter_string(AgentObject *self, PyObject *args, PyObject *kwds);
PyObject *Agent_parameter_data(AgentObject *self, PyObject *args, PyObject *kwds);

PyObject *Agent_input_set_bool(AgentObject *self, PyObject *args, PyObject *kwds);
PyObject *Agent_input_set_int(AgentObject *self, PyObject *args, PyObject *kwds);
PyObject *Agent_input_set_double(AgentObject *self, PyObject *args, PyObject *kwds);
PyObject *Agent_input_set_string(AgentObject *self, PyObject *args, PyObject *kwds);
PyObject *Agent_input_set_impulsion(AgentObject *self, PyObject *args, PyObject *kwds);
PyObject *Agent_input_set_data(AgentObject *self, PyObject *args, PyObject *kwds);

PyObject *Agent_output_set_bool(AgentObject *self, PyObject *args, PyObject *kwds);
PyObject *Agent_output_set_int(AgentObject *self, PyObject *args, PyObject *kwds);
PyObject *Agent_output_set_double(AgentObject *self, PyObject *args, PyObject *kwds);
PyObject *Agent_output_set_string(AgentObject *self, PyObject *args, PyObject *kwds);
PyObject *Agent_output_set_impulsion(AgentObject *self, PyObject *args, PyObject *kwds);
PyObject *Agent_output_set_data(AgentObject *self, PyObject *args, PyObject *kwds);

PyObject *Agent_parameter_set_bool(AgentObject *self, PyObject *args, PyObject *kwds);
PyObject *Agent_parameter_set_int(AgentObject *self, PyObject *args, PyObject *kwds);
PyObject *Agent_parameter_set_double(AgentObject *self, PyObject *args, PyObject *kwds);
PyObject *Agent_parameter_set_string(AgentObject *self, PyObject *args, PyObject *kwds);
PyObject *Agent_parameter_set_data(AgentObject *self, PyObject *args, PyObject *kwds);

PyObject *Agent_clear_input(AgentObject *self, PyObject *args, PyObject *kwds);
PyObject *Agent_clear_output(AgentObject *self, PyObject *args, PyObject *kwds);
PyObject *Agent_clear_parameter(AgentObject *self, PyObject *args, PyObject *kwds);

PyObject *Agent_observe_input(AgentObject *self, PyObject *args, PyObject *kwds);
PyObject *Agent_observe_output(AgentObject *self, PyObject *args, PyObject *kwds);
PyObject *Agent_observe_parameter(AgentObject *self, PyObject *args, PyObject *kwds);

PyObject *Agent_output_mute(AgentObject *self, PyObject *args, PyObject *kwds);
PyObject *Agent_output_unmute(AgentObject *self, PyObject *args, PyObject *kwds);
PyObject *Agent_output_is_muted(AgentObject *self, PyObject *args, PyObject *kwds);

PyObject *Agent_definition_set_path(AgentObject *self, PyObject *args, PyObject *kwds);
PyObject *Agent_definition_save(AgentObject *self, PyObject *args, PyObject *kwds);

#endif /* agent_definition_h */
