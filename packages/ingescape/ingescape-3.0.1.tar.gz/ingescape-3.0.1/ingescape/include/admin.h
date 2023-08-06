//
//  admin.h
//  ingescapeWrapp
//
//  Created by vaugien on 06/04/2018.
//  Copyright © 2018 ingenuity. All rights reserved.
//

#ifndef admin_h
#define admin_h

#include <Python.h>
#include <frameobject.h>

//wrapper for igs_set_command_line
PyObject * setCommandLine_wrapper(PyObject * self, PyObject * args);

//wrapper for igs_log_set_console
PyObject * setVerbose_wrapper(PyObject * self, PyObject * args);

//wrapper for igs_getVerbose
PyObject * getVerbose_wrapper(PyObject * self, PyObject * args);

//wrapper for igs_log_set_stream
PyObject * setLogStream_wrapper(PyObject * self, PyObject * args);

//wrapper for igs_log_stream
PyObject * getLogStream_wrapper(PyObject * self, PyObject * args);

//wrapper for igs_log_set_file
PyObject * setLogInFile_wrapper(PyObject * self, PyObject * args);

//wrapper for igs_log_file
PyObject * getLogInFile_wrapper(PyObject * self, PyObject * args);

//wrapper for igs_log_set_console_color
PyObject * setUseColorVerbose_wrapper(PyObject * self, PyObject * args);

//wrapper for igs_log_console_color
PyObject * getUseColorVerbose_wrapper(PyObject * self, PyObject * args);

//wrapper for igs_log_set_file_path
PyObject * setLogPath_wrapper(PyObject * self, PyObject * args);

//wrapper for igs_log_file_path
PyObject * getLogPath_wrapper(PyObject * self, PyObject * args);

//wrapper for igs_interrupted
PyObject * isStarted_wrapper(PyObject * self, PyObject * args);

//wrapper for igs_definition_set_path
PyObject * setDefinitionPath_wrapper(PyObject * self, PyObject * args);

//wrapper for igs_mapping_set_path
PyObject * setMappingPath_wrapper(PyObject * self, PyObject * args);

//wrapper for igs_definition_save
PyObject * writeDefinitionToPath_wrapper(PyObject * self, PyObject * args);

//wrapper for igs_mapping_save
PyObject * writeMappingToPath_wrapper(PyObject * self, PyObject * args);

//wrapper for igs_version
PyObject * version_wrapper(PyObject * self, PyObject * args);

//wrapper for igs_protocol
PyObject * protocol_wrapper(PyObject * self, PyObject * args);

PyObject * trace_wrapper(PyObject * self, PyObject * args);

PyObject * debug_wrapper(PyObject * self, PyObject * args);

PyObject * info_wrapper(PyObject * self, PyObject * args);

PyObject * warn_wrapper(PyObject * self, PyObject * args);

PyObject * error_wrapper(PyObject * self, PyObject * args);

PyObject * fatal_wrapper(PyObject * self, PyObject * args);

PyObject * setLogLevel_wrapper(PyObject * self, PyObject * args);

PyObject * getLogLevel_wrapper(PyObject * self, PyObject * args);


PyObject * igs_getNetdevicesList_wrapper(PyObject * self, PyObject * args);

PyObject * igs_getNetadressesList_wrapper(PyObject * self, PyObject * args);

PyObject * igs_competeInElection_wrapper(PyObject * self, PyObject * args);

PyObject * igs_leaveElection_wrapper(PyObject * self, PyObject * args);

PyDoc_STRVAR(
            setDefinitionPathDoc,
             "igs_definition_set_path()\n"
             "--\n"
             "\n"
             "Set the path to write the current definition with igs_definition_save .");

PyDoc_STRVAR(
             setMappingPathDoc,
             "igs_mapping_set_path()\n"
             "--\n"
             "\n"
             "Set the path to write the current mapping with igs_mapping_save.");

PyDoc_STRVAR(
             writeDefinitionToPathDoc,
             "igs_definition_save()\n"
             "--\n"
             "\n"
             "Write the current definition to th file setted in igs_definition_set_path.");

PyDoc_STRVAR(
             writeMappingToPathDoc,
             "igs_mapping_save()\n"
             "--\n"
             "\n"
             "Write the current mapping to th file setted in igs_mapping_set_path.");

PyDoc_STRVAR(
             versionDoc,
             "igs_version()\n"
             "--\n"
             "\n"
             "Return the version of IngeScape.");

PyDoc_STRVAR(
             protocolDoc,
             "igs_protocol()\n"
             "--\n"
             "\n"
             "Return the protocol version of IngeScape.");

PyDoc_STRVAR(
             interruptedDoc,
             "igs_interrupted()\n"
             "--\n"
             "\n"
             "Return True if agent is stopped.");

PyDoc_STRVAR(
             setCommandLineDoc,
             "igs_set_command_line(commandLine)\n"
             "--\n"
             "\n"
             "Command line for the agent can be passed here for inclusion in the agent's headers.\n"
             "If not set, header is initialized with exec path.\n");

PyDoc_STRVAR(
             setVerboseDoc,
             "igs_log_set_console(verbose)\n"
             "--\n"
             "\n"
             "enable log in console (enabled by default).\n Param verbose is a boolean");

PyDoc_STRVAR(
             isVerboseDoc,
             "igs_log_console()\n"
             "--\n"
             "\n"
             "Return True if log in console is enabled (enabled by default).");

PyDoc_STRVAR(
             setLogStreamDoc,
             "igs_log_set_stream(log)\n"
             "--\n"
             "\n"
             "enable log in socket.\n Param verbose is a boolean");

PyDoc_STRVAR(
             getLogStreamDoc,
             "igs_log_stream()\n"
             "--\n"
             "\n"
             "Return True if log in socket is enabled.");

PyDoc_STRVAR(
             setLogInFileDoc,
             "igs_log_set_file(log)\n"
             "--\n"
             "\n"
             "enable log in file.\n Param verbose is a boolean");

PyDoc_STRVAR(
             getLogInFileDoc,
             "igs_log_file()\n"
             "--\n"
             "\n"
             "Return True if log in file is enabled.");

PyDoc_STRVAR(
             setLogPathDoc,
             "igs_log_set_file_path(path)\n"
             "--\n"
             "\n"
             "Set the path of the file were log will be saved.\n Param is a string containing the path to the file");

PyDoc_STRVAR(
             getLogPathDoc,
             "igs_log_file_path()\n"
             "--\n"
             "\n"
             "Get the path of the file were log will be saved.\n Return a string containing the path to the file");

PyDoc_STRVAR(
             setUseColorVerboseDoc,
             "igs_log_set_console_color(verbose)\n"
             "--\n"
             "\n"
             "Enable use colors in console.\n Param is boolean.");

PyDoc_STRVAR(
             getUseColorVerboseDoc,
             "igs_log_console_color()\n"
             "--\n"
             "\n"
             "Return true if colors are used in console.");

#endif /* admin_h */
