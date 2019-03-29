#include <communications.h>

message msgBuffer;


int communicationsInit(ID){
    Serial.begin(9600);
    myID = ID;
}

int send_msg(message msg){
    len = sizeof(msg);
    char buf[len] = msg;
    bytesSent = Serial.write(buf, len);
    if (len== bytesSent){
        return 1;
    }
    return 0;
}

int get_recieved_msg(message* recievedMsg){

}