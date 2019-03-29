extern "C"{
  #include "communications.h"
};


void setup() {
  // put your setup code here, to run once:
  communicationsInit(ID=1);
  message test;
  test.ID = 1;
  test.msgType = 2;
  test.data = 'a';

}

void loop() {
  // put your main code here, to run repeatedly:
    send_msg(test);
    delay(2000);
}
