
//
//  ingescapePython.c
//  ingescapeWrapp
//
//  Created by vaugien on 09/02/2018.
//  Copyright © 2018 ingenuity. All rights reserved.
//

#include <stdio.h>
#include <Python.h>
#include "uthash/utlist.h"

// Ingescape headers
#include "advanced.h"
#include "init.h"
#include "start.h"
#include "input.h"
#include "output.h"
#include "parameter.h"
#include "definition.h"
#include "mapping.h"
#include "admin.h"
#include "observecallback.h"
#include "freezecallback.h"
#include "data.h"
#include "stopcallback.h"
#include "service.h"
#include "agentEvent.h"

//Ingescape agent headers
#include "agent_definition.h"
#include "agent_init.h"
#include "agent_network.h"
#include "agent_mapping.h"
#include "agent_split.h"
#include "agent_service.h"
#include "agent.h"


/*
 *Defining all the methods of the Ingescape module
 */

static PyMethodDef ingescapeMethods[] =
{
    //start & stop the agent
    {"start_with_device",startWithDevice_wrapper, METH_VARARGS, startWithDeviceDoc },
    {"start_with_ip", startWithIP_wrapper, METH_VARARGS, startWithIPDoc},
    {"stop", stop_wrapper, METH_NOARGS, stopDoc},

    //agent name set and get
    {"agent_set_name", setAgentName_wrapper, METH_VARARGS, setAgentNameDoc},
    {"agent_name", getAgentName_wrapper, METH_NOARGS, getAgentNameDoc},
    {"agent_family", getAgentFamily_wrapper, METH_NOARGS, getAgentFamilyDoc},
    {"agent_set_family", setAgentFamily_wrapper, METH_VARARGS, setAgentFamilyDoc},

    //control agent state
    {"agent_set_state", setAgentState_wrapper, METH_VARARGS,  setAgentStateDoc},
    {"agent_state", getAgentState_wrapper, METH_NOARGS,  getAgentStateDoc},

    //mute the agent ouputs
    {"agent_mute", mute_wrapper, METH_NOARGS, muteDoc},
    {"agent_unmute", unmute_wrapper, METH_NOARGS, unmuteDoc},
    {"agent_is_muted", ismuted_wrapper, METH_NOARGS, ismutedDoc},

    //freeze and unfreeze the agent
    {"agent_freeze", freeze_wrapper, METH_NOARGS, freezeDoc},
    {"agent_unfreeze", unfreeze_wrapper, METH_NOARGS, unfreezeDoc},
    {"agent_is_frozen", isFrozen_wrapper, METH_NOARGS, isfrozenDoc},

    //read input per type
    {"input_bool", readInputAsBool_wrapper, METH_VARARGS, readInputAsBoolDoc},
    {"input_int", readInputAsInt_wrapper, METH_VARARGS, readInputAsIntDoc},
    {"input_double", readInputAsDouble_wrapper, METH_VARARGS, readInputAsDoubleDoc},
    {"input_string", readInputAsString_wrapper, METH_VARARGS, readInputAsStringDoc},
    {"input_data", readInputAsData_wrapper, METH_VARARGS,readInputAsDataDoc},

    //read output per type
    {"output_bool", readOutputAsBool_wrapper, METH_VARARGS, readOutputAsBoolDoc},
    {"output_int", readOutputAsInt_wrapper, METH_VARARGS, readOutputAsIntDoc},
    {"output_double", readOutputAsDouble_wrapper, METH_VARARGS, readOutputAsDoubleDoc},
    {"output_string", readOutputAsString_wrapper, METH_VARARGS, readOutputAsStringDoc},
    {"output_data", readOutputAsData_wrapper, METH_VARARGS, readOutputAsDataDoc},

    //read parameter per type
    {"parameter_bool", readParameterAsBool_wrapper, METH_VARARGS, readParameterAsBoolDoc},
    {"parameter_int", readParameterAsInt_wrapper, METH_VARARGS, readParameterAsIntDoc},
    {"parameter_double", readParameterAsDouble_wrapper, METH_VARARGS, readParameterAsDoubleDoc},
    {"parameter_string", readParameterAsString_wrapper, METH_VARARGS, readParameterAsStringDoc},
    {"parameter_data", readParameterAsData_wrapper, METH_VARARGS, readParameterAsDataDoc},

    //write input per type
    {"input_set_bool", writeInputAsBool_wrapper, METH_VARARGS, writeInputAsBoolDoc},
    {"input_set_int", writeInputAsInt_wrapper, METH_VARARGS, writeInputAsIntDoc},
    {"input_set_double", writeInputAsDouble_wrapper, METH_VARARGS, writeInputAsDoubleDoc},
    {"input_set_string", writeInputAsString_wrapper, METH_VARARGS, writeInputAsStringDoc},
    {"input_set_impulsion", writeInputAsImpulsion_wrapper, METH_VARARGS, writeInputAsImpulsionDoc},
    {"input_set_data", writeInputAsData_wrapper, METH_VARARGS, writeInputAsDataDoc},

    //write output per type
    {"output_set_bool", writeOutputAsBool_wrapper, METH_VARARGS, writeOutputAsBoolDoc},
    {"output_set_int", writeOutputAsInt_wrapper, METH_VARARGS, writeOutputAsIntDoc},
    {"output_set_double", writeOutputAsDouble_wrapper, METH_VARARGS, writeOutputAsDoubleDoc},
    {"output_set_string", writeOutputAsString_wrapper, METH_VARARGS, writeOutputAsStringDoc},
    {"output_set_impulsion", writeOutputAsImpulsion_wrapper, METH_VARARGS, writeOutputAsImpulsionDoc},
    {"output_set_data", writeOutputAsData_wrapper, METH_VARARGS, writeOutputAsDataDoc},

    //write Parameter per type
    {"parameter_set_bool", writeParameterAsBool_wrapper, METH_VARARGS, writeParameterAsBoolDoc},
    {"parameter_set_int", writeParameterAsInt_wrapper, METH_VARARGS, writeParameterAsIntDoc},
    {"parameter_set_double", writeParameterAsDouble_wrapper, METH_VARARGS, writeParameterAsDoubleDoc},
    {"parameter_set_string", writeParameterAsString_wrapper, METH_VARARGS, writeParameterAsStringDoc},
    {"parameter_set_data", writeParameterAsData_wrapper, METH_VARARGS, writeParameterAsDataDoc},

    //check IOP type
    {"input_type", getTypeForInput_wrapper, METH_VARARGS, getTypeForInputDoc},
    {"output_type", getTypeForOutput_wrapper, METH_VARARGS, getTypeForOutputDoc},
    {"parameter_type", getTypeForParameter_wrapper, METH_VARARGS, getTypeForParameterDoc},

    //get number of IOP
    {"input_count", getInputsNumber_wrapper, METH_NOARGS, getInputsNumberDoc},
    {"output_count", getOutputsNumber_wrapper, METH_NOARGS, getOutputsNumberDoc},
    {"parameter_count", getParametersNumber_wrapper, METH_NOARGS, getParametersNumberDoc},

    //check existence of IOP
    {"input_exists", checkInputExistence_wrapper, METH_VARARGS, checkInputExistenceDoc},
    {"output_exists", checkOutputExistence_wrapper, METH_VARARGS, checkOutputExistenceDoc},
    {"parameter_exists", checkParametersExistence_wrapper, METH_VARARGS, checkParameterExistenceDoc},

    // get Iop list
    {"input_list", igs_getInputsList_wrapper, METH_VARARGS, getInputsListDoc},
    {"output_list", igs_getOutputsList_wrapper, METH_VARARGS, getOutputsListDoc},
    {"parameter_list", igs_getParametersList_wrapper, METH_VARARGS, getParametersListDoc},

    //mute or unmute an IOP
    {"output_mute", muteOutput_wrapper, METH_VARARGS, muteOutputDoc},
    {"output_unmute", unmuteOutput_wrapper, METH_VARARGS, unmuteOutputDoc},
    {"output_is_muted", isOutputMuted_wrapper, METH_VARARGS,  isOutputMutedDoc},

    //load definition
    {"definition_load_str", loadDefinition_wrapper, METH_VARARGS, loadDefinitionDoc},
    {"definition_load_file", loadDefinitionFromPath_wrapper, METH_VARARGS, loadDefinitionFromPathDoc},
    {"clear_definition", clearDefinition_wrapper, METH_NOARGS, clearDefinitionDoc},

    //get information about definition
    {"definition_json", getDefinition_wrapper, METH_NOARGS, getDefinitionDoc},
    {"definition_description", getDefinitionDescription_wrapper, METH_NOARGS, getDefinitionDescriptionDoc},
    {"definition_version", getDefinitionVersion_wrapper, METH_NOARGS, getDefinitionVersionDoc},

    //set definition
    {"definition_set_description", setDefinitionDescription_wrapper, METH_VARARGS, setDefinitionDescriptionDoc},
    {"definition_set_version", setDefinitionVersion_wrapper, METH_VARARGS, setDefinitionVersionDoc},

    //remove IOP
    {"input_remove", removeInput_wrapper, METH_VARARGS, removeInputDoc},
    {"output_remove", removeOutput_wrapper, METH_VARARGS, removeOutputDoc},
    {"parameter_remove", removeParameter_wrapper, METH_VARARGS, removeParameterDoc},

    //createIOP
    {"input_create", createInput_wrapper, METH_VARARGS, createInputDoc},
    {"output_create", createOutput_wrapper, METH_VARARGS, createOutputDoc},
    {"parameter_create", createParameter_wrapper, METH_VARARGS, createParameterDoc},

    //load mapping
    {"mapping_load_str", loadMapping_wrapper, METH_VARARGS,loadMappingDoc},
    {"mapping_load_file", loadMappingFromPath_wrapper, METH_VARARGS, loadMappingFromPathDoc},
    {"clear_mappings", clearMapping_wrapper, METH_NOARGS, clearMappingDoc},

    //get information about mapping
    {"mapping_json", getMapping_wrapper, METH_NOARGS, getMappingDoc},
    {"mapping_count", getMappingEntriesNumber_wrapper, METH_NOARGS, getMappingEntriesNumberDoc},
    {"mapping_add", addMappingEntry_wrapper, METH_VARARGS, addMappingEntriesDoc},

    //remove mapping
    {"mapping_remove_with_id", removeMappingEntryWithId_wrapper, METH_VARARGS, removeMappingEntryWithIdDoc},
    {"mapping_remove_with_name", removeMappingEntryWithName_wrapper, METH_VARARGS, removeMappingEntryWithNameDoc},
    {"mapping_set_outputs_request", setRequestOutputsFromMappedAgents_wrapper, METH_VARARGS, ""},
    {"mapping_outputs_request", getRequestOutputsFromMappedAgents_wrapper, METH_NOARGS, ""},

    //split management
    {"split_count", (PyCFunction) split_count_wrapper, METH_NOARGS, ""},
    {"split_add", (PyCFunction) split_add_wrapper, METH_VARARGS, ""},
    {"split_remove_with_id", (PyCFunction) split_remove_with_id_wrapper, METH_VARARGS, ""},
    {"split_remove_with_name", (PyCFunction) split_remove_with_name_wrapper, METH_VARARGS, ""},

    //Command line for the agent can be passed here for inclusion in the agent's headers. If not set, header is initialized with exec path.
    {"set_command_line", setCommandLine_wrapper, METH_VARARGS, setCommandLineDoc},

    //logs and debug messages
    {"log_set_console", setVerbose_wrapper, METH_VARARGS, setVerboseDoc},
    {"log_console", getVerbose_wrapper, METH_NOARGS, isVerboseDoc},
    {"log_set_stream", setLogStream_wrapper, METH_VARARGS, setLogStreamDoc},
    {"log_stream", getLogStream_wrapper, METH_NOARGS, getLogStreamDoc},
    {"log_set_file", setLogInFile_wrapper, METH_VARARGS, setLogInFileDoc},
    {"log_file", getLogInFile_wrapper, METH_NOARGS, getLogInFileDoc},
    {"log_set_console_color", setUseColorVerbose_wrapper, METH_VARARGS, setUseColorVerboseDoc},
    {"log_console_color", getUseColorVerbose_wrapper, METH_NOARGS, getUseColorVerboseDoc},
    {"log_set_file_path", setLogPath_wrapper, METH_VARARGS, setLogPathDoc},
    {"log_file_path", getLogPath_wrapper, METH_NOARGS, getLogPathDoc},
    {"is_started", isStarted_wrapper, METH_NOARGS, interruptedDoc},

    //observe Iop, freeze and forced stop
    {"observe_input", (PyCFunction) observe_input_wrapper, METH_VARARGS, observeInputDoc},
    {"observe_output", (PyCFunction) observe_output_wrapper, METH_VARARGS, observeOutputDoc},
    {"observe_parameter", (PyCFunction) observe_parameter_wrapper, METH_VARARGS, observeParameterDoc},
    {"observe_freeze", igs_observeFreeze_wrapper, METH_VARARGS, observeFreezeDoc},
    {"observe_forced_stop", igs_observeExternalStop_wrapper, METH_VARARGS, observeForcedStopDoc},

    //resources file management
    {"definition_set_path", setDefinitionPath_wrapper, METH_VARARGS, setDefinitionPathDoc},
    {"mapping_set_path", setMappingPath_wrapper, METH_VARARGS, setMappingPathDoc},
    {"definition_save", writeDefinitionToPath_wrapper, METH_NOARGS, writeDefinitionToPathDoc},
    {"mapping_save", writeMappingToPath_wrapper, METH_NOARGS, writeMappingToPathDoc},
    {"version", version_wrapper, METH_NOARGS, versionDoc},
    {"protocol", protocol_wrapper, METH_NOARGS, protocolDoc},

    // advanced
    {"net_set_publishing_port", igs_setPublishingPort_wrapper, METH_VARARGS, setPublishingPortDoc},
    {"net_set_discovery_interval", igs_setDiscoveryInterval_wrapper, METH_VARARGS, setDiscoveryIntervalDoc},
    {"setAgentTimeOut", igs_setAgentTimeOut_wrapper, METH_VARARGS, setAgentTimeoutDoc},
    {"channel_join", igs_busJoinChannel_wrapper, METH_VARARGS, busJoinChannelDoc},
    {"channel_leave", igs_busLeaveChannel_wrapper, METH_VARARGS, busLeaveChannelDoc},
    {"channel_shout_str", igs_busSendStringToChannel_wrapper, METH_VARARGS, busSendStringToChannelDoc},
    {"channel_shout_data", igs_busSendDataToChannel_wrapper, METH_VARARGS, busSendDataToChannelDoc},
    {"channel_whisper_str", igs_busSendStringToAgent_wrapper, METH_VARARGS, busSendStringToAgentDoc},
    {"channel_whisper_data", igs_busSendDataToAgent_wrapper, METH_VARARGS, busSendDataToAgentDoc},
    {"peer_add_header", igs_busAddServiceDescription_wrapper, METH_VARARGS, busAddServiceDescriptionDoc},
    {"peer_remove_header", igs_busRemoveServiceDescription_wrapper, METH_VARARGS, busremoveServiceDescriptionDoc},

    // calls
    {"service_call", sendCall_wrapper, METH_VARARGS, sendCallDoc},
    {"service_remove", removeCall_wrapper, METH_VARARGS, removeCallDoc},
    {"service_arg_add", addArgumentToCall_wrapper, METH_VARARGS, addArgumentToCallDoc},
    {"service_arg_remove", removeArgumentFromCall_wrapper, METH_VARARGS, removeArgumentFromCallDoc},
    {"service_count", getNumberOfCalls_wrapper, METH_VARARGS, getNumberOfCallsDoc},
    {"service_exists", checkCallExistence_wrapper, METH_VARARGS, checkCallExistenceDoc},
    {"service_list", getCallsList_wrapper, METH_VARARGS, getCallsListDoc},
    {"service_args_count", getNumberOfArgumentForCall_wrapper, METH_VARARGS, getNumberOfArgumentForCallDoc},
    {"service_args_list", getArgumentListForCall_wrapper, METH_VARARGS, getArgumentListForCallDoc},
    {"service_arg_exists", checkCallArgumentExistence_wrapper, METH_VARARGS, checkCallArgumentExistenceDoc},
    {"service_init", initCall_wrapper, METH_VARARGS, initCallDoc},

    {"net_devices_list", igs_getNetdevicesList_wrapper, METH_NOARGS, ""},
    {"net_addresses_list", igs_getNetadressesList_wrapper, METH_NOARGS, ""},

    //logging
    {"log_set_console_level", setLogLevel_wrapper, METH_VARARGS, "set log level, \n Trace = 0, ..."},
    {"log_console_level", getLogLevel_wrapper, METH_VARARGS, "get log level, \n Trace = 0, ..."},
    {"trace", trace_wrapper, METH_VARARGS, ""},
    {"debug", debug_wrapper, METH_VARARGS, ""},
    {"info", info_wrapper, METH_VARARGS, ""},
    {"warn", warn_wrapper, METH_VARARGS, ""},
    {"error", error_wrapper, METH_VARARGS, ""},
    {"fatal", fatal_wrapper, METH_VARARGS, ""},

    //agentEvent
    {"observe_agent_events", igs_observeAgentEvents_wrapper, METH_VARARGS, ""},

    //Election
    {"election_join", igs_competeInElection_wrapper, METH_VARARGS, ""},
    {"election_leave", igs_leaveElection_wrapper, METH_VARARGS, ""},

    {NULL, NULL, 0, NULL}       /* Sentinel */
};

/*
 *Defining all the methods of the Agent Object
 * First new, destroy and __init__ the ingescape's methods
 */


static void Agent_dealloc(AgentObject *self)
{
    if(self->agent)
    {
        if (igsagent_is_activated(self->agent))
            igsagent_deactivate(self->agent);
        igsagent_destroy(&(self->agent));
    }

    {
        agentObserveEventsCB_t *it = NULL;
        do {
            DL_FOREACH(agentObserveEventsCBList, it) {
                if (it->agent == self) break;
            }
            if (it) {
                DL_DELETE(agentObserveEventsCBList, it);
                Py_CLEAR(it->callback);
                Py_CLEAR(it->my_data);
                free(it);
            }
        } while(it);
    }
    {
        agentobserve_iop_cb_t *it = NULL;
        do {
            DL_FOREACH(agentobserve_iop_cbList, it) {
                if (it->agent == self) break;
            }
            if (it) {
                DL_DELETE(agentobserve_iop_cbList, it);
                free(it->nameArg);
                Py_CLEAR(it->callback);
                Py_CLEAR(it->my_data);
                free(it);
            }
        } while(it);
    }
    {
        agentObserveCB_t *it = NULL;
        do {
            DL_FOREACH(agentObserveCBList, it) {
                if (it->agent == self) break;
            }
            if (it) {
                DL_DELETE(agentObserveCBList, it);
                Py_CLEAR(it->callback);
                Py_CLEAR(it->my_data);
                free(it);
            }
        } while(it);
    }
    {
        agentMuteCB_t *it = NULL;
        do {
            DL_FOREACH(agentMuteCBList, it) {
                if (it->agent == self) break;
            }
            if (it) {
                DL_DELETE(agentMuteCBList, it);
                Py_CLEAR(it->callback);
                Py_CLEAR(it->my_data);
                free(it);
            }
        } while(it);
    }
    {
        agentServiceCB_t *it = NULL;
        do {
            DL_FOREACH(agentServiceCBList, it) {
                if (it->agent == self) break;
            }
            if (it) {
                DL_DELETE(agentServiceCBList, it);
                free(it->serviceName);
                Py_CLEAR(it->callback);
                Py_CLEAR(it->my_data);
                free(it);
            }
        } while(it);
    }

    Py_TYPE(self)->tp_free((PyObject *) self);
}

static PyObject *Agent_new(PyTypeObject *type, PyObject *args, PyObject *kwds)
{
    AgentObject *self;
    self = (AgentObject *) type->tp_alloc(type, 0);
    if (self != NULL) {
        self->agent = NULL;
    }
    return (PyObject *) self;
}

static int *Agent_init(AgentObject *self, PyObject *args, PyObject *kwds)
{
    static char *kwlist[] = {"name", "activate_immediately", NULL};
    char *name = NULL;
    PyObject* activate_immediately = Py_False;

    if (!PyArg_ParseTupleAndKeywords(args, kwds, "s|O", kwlist,
                                     &name, &activate_immediately))
    {
        return -1;
    }
    if(activate_immediately == Py_True)
        self->agent = igsagent_new(name, true);
    else
        self->agent = igsagent_new(name, false);
    return 0;
}

static PyMethodDef Agent_methods[] = {
    ////////////////////////////////////////
    // Agent creation/destruction/activation

    {"activate", (PyCFunction) Agent_activate, METH_NOARGS, ""},
    {"deactivate", (PyCFunction) Agent_deactivate, METH_NOARGS, ""},
    {"is_activated", (PyCFunction) Agent_is_activated, METH_NOARGS, ""},
    {"observe", (PyCFunction) Agent_observe, METH_VARARGS, ""},

    ////////////////
    // Agent logging

    {"trace", (PyCFunction) Agent_trace, METH_VARARGS, ""},
    {"debug", (PyCFunction) Agent_debug, METH_VARARGS, ""},
    {"info", (PyCFunction) Agent_info, METH_VARARGS, ""},
    {"warn", (PyCFunction) Agent_warn, METH_VARARGS, ""},
    {"error", (PyCFunction) Agent_error, METH_VARARGS, ""},
    {"fatal", (PyCFunction) Agent_fatal, METH_VARARGS, ""},

    ///////////////////////////////////////////
    // Agent initialization, control and events

    {"name", (PyCFunction) Agent_name, METH_NOARGS, ""},
    {"set_name", (PyCFunction) Agent_set_name, METH_VARARGS, ""},
    {"family", (PyCFunction) Agent_family, METH_NOARGS, ""},
    {"set_family", (PyCFunction) Agent_set_family, METH_VARARGS, ""},
    {"uuid", (PyCFunction) Agent_uuid, METH_NOARGS, ""},
    {"state", (PyCFunction) Agent_state, METH_NOARGS, ""},
    {"set_state", (PyCFunction) Agent_set_state, METH_VARARGS, ""},
    {"mute", (PyCFunction) Agent_mute, METH_NOARGS, ""},
    {"unmute", (PyCFunction) Agent_unmute, METH_NOARGS, ""},
    {"is_muted", (PyCFunction) Agent_is_muted, METH_NOARGS, ""},
    {"observe_mute", (PyCFunction) Agent_observe_mute, METH_VARARGS, ""},

    {"observe_agent_event", (PyCFunction) Agent_observe_agent_event, METH_VARARGS, ""},

    //////////////////////////////////////////////////////////////////////////////////
    // Editing & inspecting definitions, adding and removing inputs/outputs/parameters

    {"definition_load_str", (PyCFunction) Agent_definition_load_str, METH_VARARGS, ""},
    {"definition_load_file", (PyCFunction) Agent_definition_load_file, METH_VARARGS, ""},
    {"clear_definition", (PyCFunction) Agent_clear_definition, METH_NOARGS, ""},
    {"definition_json", (PyCFunction) Agent_definition_json, METH_NOARGS, ""},
    {"definition_description", (PyCFunction) Agent_definition_description, METH_NOARGS, ""},
    {"definition_version", (PyCFunction) Agent_definition_version, METH_NOARGS, ""},
    {"definition_set_description", (PyCFunction) Agent_definition_set_description, METH_VARARGS, ""},
    {"definition_set_version", (PyCFunction) Agent_definition_set_version, METH_VARARGS, ""},

    {"input_create", (PyCFunction) Agent_input_create, METH_VARARGS, ""},
    {"output_create", (PyCFunction) Agent_output_create, METH_VARARGS, ""},
    {"parameter_create", (PyCFunction) Agent_parameter_create, METH_VARARGS, ""},

    {"input_remove", (PyCFunction) Agent_input_remove, METH_VARARGS, ""},
    {"output_remove", (PyCFunction) Agent_output_remove, METH_VARARGS, ""},
    {"parameter_remove", (PyCFunction) Agent_parameter_remove, METH_VARARGS, ""},

    {"input_type", (PyCFunction) Agent_input_type, METH_VARARGS, ""},
    {"output_type", (PyCFunction) Agent_output_type, METH_VARARGS, ""},
    {"parameter_type", (PyCFunction) Agent_parameter_type, METH_VARARGS, ""},

    {"input_count", (PyCFunction) Agent_input_count, METH_NOARGS, ""},
    {"output_count", (PyCFunction) Agent_output_count, METH_NOARGS, ""},
    {"parameter_count", (PyCFunction) Agent_parameter_count, METH_NOARGS, ""},

    {"input_list", (PyCFunction) Agent_input_list, METH_NOARGS, ""},
    {"output_list", (PyCFunction) Agent_output_list, METH_NOARGS, ""},
    {"parameter_list", (PyCFunction) Agent_parameter_list, METH_NOARGS, ""},

    {"input_exists", (PyCFunction) Agent_input_exists, METH_VARARGS, ""},
    {"output_exists", (PyCFunction) Agent_output_exists, METH_VARARGS, ""},
    {"parameter_exists", (PyCFunction) Agent_parameter_exists, METH_VARARGS, ""},

    ////////////////////////////////////////////////////////////
    // Reading and writing inputs/outputs/parameters, a.k.a IOPs

    {"input_bool", (PyCFunction) Agent_input_bool, METH_VARARGS, ""},
    {"input_int", (PyCFunction) Agent_input_int, METH_VARARGS, ""},
    {"input_double", (PyCFunction) Agent_input_double, METH_VARARGS, ""},
    {"input_string", (PyCFunction) Agent_input_string, METH_VARARGS, ""},
    {"input_data", (PyCFunction) Agent_input_data, METH_VARARGS, ""},

    {"output_bool", (PyCFunction) Agent_output_bool, METH_VARARGS, ""},
    {"output_int", (PyCFunction) Agent_output_int, METH_VARARGS, ""},
    {"output_double", (PyCFunction) Agent_output_double, METH_VARARGS, ""},
    {"output_string", (PyCFunction) Agent_output_string, METH_VARARGS, ""},
    {"output_data", (PyCFunction) Agent_output_data, METH_VARARGS, ""},

    {"parameter_bool", (PyCFunction) Agent_parameter_bool, METH_VARARGS, ""},
    {"parameter_int", (PyCFunction) Agent_parameter_int, METH_VARARGS, ""},
    {"parameter_double", (PyCFunction) Agent_parameter_double, METH_VARARGS, ""},
    {"parameter_string", (PyCFunction) Agent_parameter_string, METH_VARARGS, ""},
    {"parameter_data", (PyCFunction) Agent_parameter_data, METH_VARARGS, ""},

    {"input_set_bool", (PyCFunction) Agent_input_set_bool, METH_VARARGS, ""},
    {"input_set_int", (PyCFunction) Agent_input_set_int, METH_VARARGS, ""},
    {"input_set_double", (PyCFunction) Agent_input_set_double, METH_VARARGS, ""},
    {"input_set_string", (PyCFunction) Agent_input_set_string, METH_VARARGS, ""},
    {"input_set_impulsion", (PyCFunction) Agent_input_set_impulsion, METH_VARARGS, ""},
    {"input_set_data", (PyCFunction) Agent_input_set_data, METH_VARARGS, ""},

    {"output_set_bool", (PyCFunction) Agent_output_set_bool, METH_VARARGS, ""},
    {"output_set_int", (PyCFunction) Agent_output_set_int, METH_VARARGS, ""},
    {"output_set_double", (PyCFunction) Agent_output_set_double, METH_VARARGS, ""},
    {"output_set_string", (PyCFunction) Agent_output_set_string, METH_VARARGS, ""},
    {"output_set_impulsion", (PyCFunction) Agent_output_set_impulsion, METH_VARARGS, ""},
    {"output_set_data", (PyCFunction) Agent_output_set_data, METH_VARARGS, ""},

    {"parameter_set_bool", (PyCFunction) Agent_parameter_set_bool, METH_VARARGS, ""},
    {"parameter_set_int", (PyCFunction) Agent_parameter_set_int, METH_VARARGS, ""},
    {"parameter_set_double", (PyCFunction) Agent_parameter_set_double, METH_VARARGS, ""},
    {"parameter_set_string", (PyCFunction) Agent_parameter_set_string, METH_VARARGS, ""},
    {"parameter_set_data", (PyCFunction) Agent_parameter_set_data, METH_VARARGS, ""},

    {"clear_input", (PyCFunction) Agent_clear_input, METH_VARARGS, ""},
    {"clear_output", (PyCFunction) Agent_clear_output, METH_VARARGS, ""},
    {"clear_parameter", (PyCFunction) Agent_clear_parameter, METH_VARARGS, ""},

    {"observe_input", (PyCFunction) Agent_observe_input, METH_VARARGS, ""},
    {"observe_output", (PyCFunction) Agent_observe_output, METH_VARARGS, ""},
    {"observe_parameter", (PyCFunction) Agent_observe_parameter, METH_VARARGS, ""},

    {"output_mute", (PyCFunction) Agent_output_mute, METH_VARARGS, ""},
    {"output_unmute", (PyCFunction) Agent_output_unmute, METH_VARARGS, ""},
    {"output_is_muted", (PyCFunction) Agent_output_is_muted, METH_VARARGS, ""},

    ////////////////////////////////
    // Mapping edition & inspection

    {"mapping_load_str", (PyCFunction) Agent_mapping_load_str, METH_VARARGS, ""},
    {"mapping_load_file", (PyCFunction) Agent_mapping_load_file, METH_VARARGS, ""},
    {"mapping_json", (PyCFunction) Agent_mapping_json, METH_NOARGS, ""},
    {"mapping_count", (PyCFunction) Agent_mapping_count, METH_NOARGS, ""},

    {"clear_mappings", (PyCFunction) Agent_clear_mappings, METH_NOARGS, ""},
    {"clear_mappings_with_agent", (PyCFunction) Agent_clear_mappings_with_agent, METH_VARARGS, ""},

    {"mapping_add", (PyCFunction) Agent_mapping_add, METH_VARARGS, ""},
    {"mapping_remove_with_id", (PyCFunction) Agent_mapping_remove_with_id, METH_VARARGS, ""},
    {"mapping_remove_with_name", (PyCFunction) Agent_mapping_remove_with_name, METH_VARARGS, ""},

    {"split_count", (PyCFunction) Agent_split_count, METH_NOARGS, ""},
    {"split_add", (PyCFunction) Agent_split_add, METH_VARARGS, ""},
    {"split_remove_with_id", (PyCFunction) Agent_split_remove_with_id, METH_VARARGS, ""},
    {"split_remove_with_name", (PyCFunction) Agent_split_remove_with_name, METH_VARARGS, ""},

    {"mapping_outputs_request", (PyCFunction) Agent_mapping_outputs_request, METH_VARARGS, ""},
    {"mapping_set_outputs_request", (PyCFunction) Agent_mapping_set_outputs_request, METH_NOARGS, ""},

    ////////////////////////////////
    // Services edition & inspection

    {"service_call", (PyCFunction) Agent_service_call, METH_VARARGS, ""},

    {"service_init", (PyCFunction) Agent_service_init, METH_VARARGS, ""},
    {"service_remove", (PyCFunction) Agent_service_remove, METH_VARARGS, ""},
    {"service_arg_add", (PyCFunction) Agent_service_arg_add, METH_VARARGS, ""},
    {"service_arg_remove", (PyCFunction) Agent_service_arg_remove, METH_VARARGS, ""},
    {"service_count", (PyCFunction) Agent_service_count, METH_NOARGS, ""},
    {"service_exists", (PyCFunction) Agent_service_exists, METH_VARARGS, ""},
    {"service_list", (PyCFunction) Agent_service_list, METH_NOARGS, ""},
    {"service_args_count", (PyCFunction) Agent_service_args_count, METH_VARARGS, ""},
    {"service_args_list", (PyCFunction) Agent_service_args_list, METH_VARARGS, ""},
    {"service_arg_exists", (PyCFunction) Agent_service_args_exists, METH_VARARGS, ""},

    //////////////////////////////////////////
    // Elections and leadership between agents

    {"election_join", (PyCFunction) Agent_election_join, METH_VARARGS, ""},
    {"election_leave", (PyCFunction) Agent_election_leave, METH_VARARGS, ""},


    ///////////////////////////////////////////////////////
    // Administration, logging, configuration and utilities

    {"definition_set_path", (PyCFunction) Agent_definition_set_path, METH_VARARGS, ""},
    {"definition_save", (PyCFunction) Agent_definition_save, METH_NOARGS, ""},
    {"mapping_set_path", (PyCFunction) Agent_mapping_set_path, METH_VARARGS, ""},
    {"mapping_save", (PyCFunction) Agent_mapping_save, METH_NOARGS, ""},


    {NULL}  /* Sentinel */
};

//Definition of the Agent type
static PyTypeObject AgentType = {
    PyVarObject_HEAD_INIT(NULL, 0)
    .tp_name = "ingescape_agent.Agent",
    .tp_doc = "Agent objects",
    .tp_basicsize = sizeof(AgentObject),
    .tp_itemsize = 0,
    .tp_flags = Py_TPFLAGS_DEFAULT | Py_TPFLAGS_BASETYPE,
    .tp_new = Agent_new,
    .tp_init = (initproc) Agent_init,
    .tp_dealloc = (destructor) Agent_dealloc,
    .tp_methods = Agent_methods,
};



static struct PyModuleDef init_ingescape_wrapper =
{
    PyModuleDef_HEAD_INIT,
    "ingescape", //    Name of the python module
    "IngeScape", //    docstring of the module
    -1,
    ingescapeMethods
};

PyMODINIT_FUNC PyInit_ingescape(void)
{
    Py_Initialize();

    PyObject *module_ingescape = PyModule_Create(&init_ingescape_wrapper);
    if (module_ingescape == NULL)
        return NULL;


    PyModule_AddIntConstant(module_ingescape, "SUCCESS", 0);
    PyModule_AddIntConstant(module_ingescape, "FAILURE", -1);

    PyModule_AddIntConstant(module_ingescape, "PEER_ENTERED", 1);
    PyModule_AddIntConstant(module_ingescape, "PEER_EXITED", 2);
    PyModule_AddIntConstant(module_ingescape, "AGENT_ENTERED", 3);
    PyModule_AddIntConstant(module_ingescape, "AGENT_UPDATED_DEFINITION", 4);
    PyModule_AddIntConstant(module_ingescape, "AGENT_KNOWS_US", 5);
    PyModule_AddIntConstant(module_ingescape, "AGENT_EXITED", 6);
    PyModule_AddIntConstant(module_ingescape, "AGENT_UPDATED_MAPPING", 7);
    PyModule_AddIntConstant(module_ingescape, "AGENT_WON_ELECTION", 8);
    PyModule_AddIntConstant(module_ingescape, "AGENT_LOST_ELECTION", 9);

    PyModule_AddIntConstant(module_ingescape, "INPUT_T", 1);
    PyModule_AddIntConstant(module_ingescape, "OUTPUT_T", 2);
    PyModule_AddIntConstant(module_ingescape, "PARAMETER_T", 3);

    PyModule_AddIntConstant(module_ingescape, "INTEGER_T", 1);
    PyModule_AddIntConstant(module_ingescape, "DOUBLE_T", 2);
    PyModule_AddIntConstant(module_ingescape, "STRING_T", 3);
    PyModule_AddIntConstant(module_ingescape, "BOOL_T", 4);
    PyModule_AddIntConstant(module_ingescape, "IMPULSION_T", 5);
    PyModule_AddIntConstant(module_ingescape, "DATA_T", 6);
    PyModule_AddIntConstant(module_ingescape, "UNKNOWN_T", 7);

    PyModule_AddIntConstant(module_ingescape, "LOG_TRACE", 0);
    PyModule_AddIntConstant(module_ingescape, "LOG_DEBUG", 1);
    PyModule_AddIntConstant(module_ingescape, "LOG_INFO", 2);
    PyModule_AddIntConstant(module_ingescape, "LOG_WARN", 3);
    PyModule_AddIntConstant(module_ingescape, "LOG_ERROR", 4);
    PyModule_AddIntConstant(module_ingescape, "LOG_FATAL", 5);

    if (PyType_Ready(&AgentType) < 0)
            return NULL;

    Py_INCREF(&AgentType);
    if (PyModule_AddObject(module_ingescape, "Agent", (PyObject *) &AgentType) < 0) {
        Py_DECREF(&AgentType);
        Py_DECREF(module_ingescape);
        return NULL;
    }

    return module_ingescape;
}
