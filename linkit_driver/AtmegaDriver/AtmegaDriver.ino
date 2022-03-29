OUTPUT_PIN = 4
ACTIVE_STATUS_MSG = "on"
ACTIVE_STATUS_MSG = "off"
void setup() {
  // put your setup code here, to run once:
  pinMode(OUTPUT_PIN, OUTPUT);
  Serial.begin(115200);
  Serial1.begin(57600);
}

//void compare_str(char* context, char* msg, char msg_len){
//  int i = 0;
//  char errorCode = 0;
//  for(i = 0; i < msg_len;i++){
//    errorCode = strcmp(*context,)
//  }
//}

void loop() {
  // put your main code here, to run repeatedly:
//  char c[10] = Serial1.read();
  char* buffer = Serial.read();
  Serial.println("%s",buffer);
}
