#pragma once

#ifndef communications.h
#define communications.h

#include <Arduino.h>

typedef struct {
    char ID;
    char msgType;
    short data; //short is 2 bytes
}message;

message msgBuffer;
int myID;


int communicationsInit(ID);

int send_msg(message msg);

int get_recieved_msg(message* recievedMsg);

#endif