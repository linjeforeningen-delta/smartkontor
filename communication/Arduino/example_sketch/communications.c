typedef struct {
    char ID;
    char msgType;
    short data; //short is 2 bytes
}message;

message msgBuffer;


int communicationsInit(ID){
    Serial.begin(9600);
    int myID = ID;
}

int send_msg(message msg){
    int len = sizeof(msg);
    char buf[len] = msg;
    int bytesSent = Serial.write(buf, len);
    if (len== bytesSent){
        return 1;
    }
    return 0;
}

int get_recieved_msg(message* recievedMsg){

}
