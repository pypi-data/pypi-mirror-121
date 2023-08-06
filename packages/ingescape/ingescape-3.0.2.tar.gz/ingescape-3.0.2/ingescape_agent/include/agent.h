//
//  agent.h
//  ingescapeWrapp
//
//  Created by vaugien on 31/08/2021.
//  Copyright © 2021 ingenuity. All rights reserved.
//

#ifndef agent_h
#define agent_h

#include <Python.h>
#include <frameobject.h>
#include <ingescape/igsagent.h>

typedef struct {
    PyObject_HEAD
    igsagent_t *agent;
} AgentObject;

#endif /* agent_h */
