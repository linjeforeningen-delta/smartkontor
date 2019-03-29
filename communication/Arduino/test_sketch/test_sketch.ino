typedef struct
{
    char ID;
    char msgType;
    short data; //short is 2 bytes
} message, *ptrmessage;

int ID=1;
message test;


int communicationsInit(int ID){
    Serial.begin(9600);
    test.ID = 1;
    test.msgType = 2;
    test.data = 'a';
}

int send_msg(message msg){
    int len = sizeof(msg);
    byte buf[len];
    memcpy(buf, &msg, len); //danger-function. don't fuck with it
    int bytesSent = Serial.write(buf, len);
    if (len== bytesSent){
        return 1;
    }
    return 0;
}


void setup() {
  // put your setup code here, to run once:
  communicationsInit(ID);


}

void loop() {
  // put your main code here, to run repeatedly:
    send_msg(test);
    delay(2000);
}

