// Get it from https://github.com/dreamcat4/CmdMessenger
#include <CmdMessenger.h>

// Get it at http://arduiniana.org/libraries/streaming/
#include <Streaming.h>

// Mustnt conflict / collide with our message payload data.
char field_separator = ',';
char command_separator = ';';

// Attach a new CmdMessenger object to the default Serial port
CmdMessenger cmdMessenger = CmdMessenger(Serial, field_separator, \
					 command_separator);

// Commands we send from the Arduino to be received on the PC
enum
{
  kCOMM_ERROR = 000, 
  kACK = 001,
  kARDUINO_READY = 002, 
  kERR = 003,

  kSEND_CMDS_END, // Mustnt delete this line
};

// Commands we send from the PC and want to recieve on the Arduino.
// They start at the address kSEND_CMDS_END
messengerCallbackFunction messengerCallbacks[] =
{
  pump_msg, // 004 in this example
  NULL
};

void pump_msg() {
  cmdMessenger.sendCmd(kACK, "Pump msg received");
  while (cmdMessenger.available()) {
    char buf[350] = {'\0'};
    cmdMessenger.copyString(buf, 350);
    if (buf[0]) {
      cmdMessenger.sendCmd(kACK, buf);
    }
  }
}

void arduino_ready() {
  // In response to ping. We just send a throw-away ack to say "im alive"
  cmdMessenger.sendCmd(kACK,"Arduino ready");
}

void unknownCmd()
{
  // Default response for unknown commands and corrupt messages
  cmdMessenger.sendCmd(kERR,"Unknown command");
}

void setup() {
  Serial.begin(57600);
  cmdMessenger.print_LF_CR();
  
  cmdMessenger.attach(kARDUINO_READY, arduino_ready);
  cmdMessenger.attach(unknownCmd);
  cmdMessenger.attach(4, pump_msg);
  arduino_ready();
}

unsigned long previousMillis;
void loop () {
  unsigned long currentMillis = millis();
  cmdMessenger.feedinSerialData();
  //  if (currentMillis - previousMillis > 100) {
  //    previousMillis = currentMillis;
  //}
}
  
