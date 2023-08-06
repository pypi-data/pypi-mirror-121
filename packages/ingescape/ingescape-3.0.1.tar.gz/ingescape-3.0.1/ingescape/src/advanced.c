//
//  advanced.c
//  ingescapeWrapp
//
//  Created by vaugien on 10/04/2018.
//  Copyright © 2018 ingenuity. All rights reserved.
//

#include "advanced.h"
#include <ingescape/ingescape.h>

PyObject * igs_setPublishingPort_wrapper(PyObject *self, PyObject *args)
{
    unsigned int port;
    // parse arguments received from python function into c object
    if (!PyArg_ParseTuple(args, "i", &port)) {
        return NULL;
    }
    igs_net_set_publishing_port(port);
    return PyLong_FromLong(0);
}

PyObject * igs_setDiscoveryInterval_wrapper(PyObject *self, PyObject *args)
{
    unsigned int interval;
    // parse arguments received from python function into c object
    if (!PyArg_ParseTuple(args, "i", &interval)) {
        return NULL;
    }
    igs_net_set_discovery_interval(interval);
    return PyLong_FromLong(0);
}

PyObject * igs_setAgentTimeOut_wrapper(PyObject *self, PyObject *args)
{
    unsigned int duration;
    // parse arguments received from python function into c object
    if (!PyArg_ParseTuple(args, "i", &duration)) {
        return NULL;
    }
    igs_net_set_discovery_interval(duration);
    return PyLong_FromLong(0);
}

PyObject * igs_busJoinChannel_wrapper(PyObject *self, PyObject *args)
{
    char *channel;
    // parse arguments received from python function into c object
    if (!PyArg_ParseTuple(args, "s", &channel)) {
        return NULL;
    }
    return PyLong_FromLong(igs_channel_join(channel));
}

PyObject * igs_busLeaveChannel_wrapper(PyObject *self, PyObject *args)
{
    char *channel;
    // parse arguments received from python function into c object
    if (!PyArg_ParseTuple(args, "s", &channel)) {
        return NULL;
    }
    igs_channel_leave(channel);
    return PyLong_FromLong(0);
}

PyObject * igs_busSendStringToChannel_wrapper(PyObject *self, PyObject *args)
{
    char *channel;
    char *msg;
    int result;
    // parse arguments received from python function into c object
    if (!PyArg_ParseTuple(args, "ss", &channel, &msg)) {
        return NULL;
    }
    result = igs_channel_shout_str(channel, msg);
    return PyLong_FromLong(result);
}

PyObject * igs_busSendDataToChannel_wrapper(PyObject *self, PyObject *args)
{
    char * channel;
    size_t size;
    Py_buffer buf;
    int  result;
    
    // parse and cast the channel, data and size argument given in python
    if (!PyArg_ParseTuple(args, "sy*k", &channel, &buf, &size)) {
        return NULL;
    }
    result = igs_channel_shout_data(channel, buf.buf, size);
    return PyLong_FromLong(result);
}


PyObject * igs_busSendStringToAgent_wrapper(PyObject *self, PyObject *args)
{
    char *agentNameOrPeerID;
    char *msg;
    int result;
    
    // parse arguments received from python function into c object
    if (!PyArg_ParseTuple(args, "ss", &agentNameOrPeerID, &msg)) {
        return NULL;
    }
    result = igs_channel_whisper_str(agentNameOrPeerID, msg);
    return PyLong_FromLong(result);
}
PyObject * igs_busSendDataToAgent_wrapper(PyObject *self, PyObject *args)
{
    char * agentNameOrPeerID;
    size_t size;
    Py_buffer buf;
    int  result;
    // parse and cast the channel, data and size argument given in python
    if (!PyArg_ParseTuple(args, "sy*k", &agentNameOrPeerID, &buf, &size)) {
        return NULL;
    }
    result = igs_channel_whisper_data(agentNameOrPeerID, buf.buf, size);
    return PyLong_FromLong(result);
}

PyObject * igs_busAddServiceDescription_wrapper(PyObject *self, PyObject *args)
{
    char *key;
    char *value;
    // parse arguments received from python function into c object
    if (!PyArg_ParseTuple(args, "ss", &key, &value)) {
        return NULL;
    }
    return PyLong_FromLong(igs_peer_add_header(key, value));
}

PyObject * igs_busRemoveServiceDescription_wrapper(PyObject *self, PyObject *args)
{
    char *key;
    // parse arguments received from python function into c object
    if (!PyArg_ParseTuple(args, "s", &key)) {
        return NULL;
    }
    return PyLong_FromLong(igs_peer_remove_header(key));
}



