// Get it from https://github.com/dreamcat4/CmdMessenger
#include <CmdMessenger.h>

// Get it from https://github.com/br3ttb/Arduino-PID-Library
#include <PID_v1.h>

const byte pumpPin = 2;
const byte heaterPin = 4;

unsigned long currentMillis;
unsigned long previousMillis;
byte slowCount;


// Lookup table for thermistor. Substract adcSubstract from ADC and then
// use the result as an index. Temp is in 23.1 format. Range from -5
// to 40 degrees only. Calculated for bridge formed by therm, 15k and 4.7V
// the therm is 10k at 25C and has a B of 3988
double temperature;
double setpoint;
double dutyCycle;
double pValue = 10;
double iValue = 0.11;
PID temperaturePID(&temperature, &dutyCycle, &setpoint, pValue, iValue, 0, DIRECT);
  
const int adcSubstract = 51;
const int adcMax = 784;
const int temperatureTable[] PROGMEM = {1093,1086,1078,1071,1064,1057,1051,1044,1037,1031,1025,1019,1013,1007,1001,995,990,984,979,974,968,963,958,953,948,943,939,934,929,925,920,916,911,907,903,898,894,890,886,882,878,874,870,867,863,859,855,852,848,844,841,837,834,831,827,824,820,817,814,811,808,804,801,798,795,792,789,786,783,780,777,774,772,769,766,763,760,758,755,752,750,747,744,742,739,736,734,731,729,726,724,721,719,717,714,712,709,707,705,702,700,698,696,693,691,689,687,684,682,680,678,676,674,672,669,667,665,663,661,659,657,655,653,651,649,647,645,643,641,639,637,636,634,632,630,628,626,624,623,621,619,617,615,614,612,610,608,606,605,603,601,600,598,596,594,593,591,589,588,586,584,583,581,579,578,576,575,573,571,570,568,567,565,564,562,560,559,557,556,554,553,551,550,548,547,545,544,542,541,539,538,537,535,534,532,531,529,528,527,525,524,522,521,520,518,517,515,514,513,511,510,509,507,506,505,503,502,501,499,498,497,495,494,493,491,490,489,488,486,485,484,482,481,480,479,477,476,475,474,472,471,470,469,468,466,465,464,463,461,460,459,458,457,455,454,453,452,451,450,448,447,446,445,444,443,441,440,439,438,437,436,434,433,432,431,430,429,428,427,425,424,423,422,421,420,419,418,417,415,414,413,412,411,410,409,408,407,406,405,404,403,401,400,399,398,397,396,395,394,393,392,391,390,389,388,387,386,385,384,383,382,381,380,379,377,376,375,374,373,372,371,370,369,368,367,366,365,364,363,362,361,360,359,358,357,356,355,354,354,353,352,351,350,349,348,347,346,345,344,343,342,341,340,339,338,337,336,335,334,333,332,331,330,329,329,328,327,326,325,324,323,322,321,320,319,318,317,316,315,314,314,313,312,311,310,309,308,307,306,305,304,303,303,302,301,300,299,298,297,296,295,294,293,293,292,291,290,289,288,287,286,285,284,284,283,282,281,280,279,278,277,276,275,275,274,273,272,271,270,269,268,268,267,266,265,264,263,262,261,260,260,259,258,257,256,255,254,253,253,252,251,250,249,248,247,247,246,245,244,243,242,241,240,240,239,238,237,236,235,234,234,233,232,231,230,229,228,228,227,226,225,224,223,222,222,221,220,219,218,217,216,216,215,214,213,212,211,210,210,209,208,207,206,205,204,204,203,202,201,200,199,198,198,197,196,195,194,193,192,192,191,190,189,188,187,186,186,185,184,183,182,181,181,180,179,178,177,176,175,175,174,173,172,171,170,169,169,168,167,166,165,164,163,163,162,161,160,159,158,157,157,156,155,154,153,152,151,151,150,149,148,147,146,145,145,144,143,142,141,140,139,139,138,137,136,135,134,133,133,132,131,130,129,128,127,126,126,125,124,123,122,121,120,120,119,118,117,116,115,114,113,113,112,111,110,109,108,107,106,105,105,104,103,102,101,100,99,98,97,97,96,95,94,93,92,91,90,89,89,88,87,86,85,84,83,82,81,80,80,79,78,77,76,75,74,73,72,71,70,69,69,68,67,66,65,64,63,62,61,60,59,58,57,56,56,55,54,53,52,51,50,49,48,47,46,45,44,43,42,41,40,39,38,37,36,35,34,34,33,32,31,30,29,28,27,26,25,24,23,22,21,20,19,18,17,16,15,14,13,12,11,10,9,8};

unsigned long windowStartTime;
boolean inDutyCycleMode;
boolean heaterIsOn = LOW;
boolean pumpIsOn = LOW;


// Attach CmdMessenger
CmdMessenger cmdMessenger = CmdMessenger(Serial);

// Commands we send from the Arduino to be received on the PC
enum
{
  kAcknowledge,
  kError,
  kFullStatus,
  kTemperature, 
  kPumpStatus,
  kHeaterStatus,
  kDutyCycleStatus,
  kPIDStatus,
  kPID,
  kHeater,
  kDutyCycle,
  kPump,
  kSetpoint,
  kPValue,
  kIValue,
};

void onTemperature() {
  cmdMessenger.sendCmd(kTemperature, temperature);
}

void onPumpStatus() {
  cmdMessenger.sendCmd(kPumpStatus, pumpIsOn);
}

void onHeaterStatus() {
  cmdMessenger.sendCmd(kHeaterStatus, heaterIsOn);
}

void onDutyCycleStatus() {
  cmdMessenger.sendCmd(kDutyCycleStatus, dutyCycle);
}

void onDutyCycle() {
  float requestedDC = cmdMessenger.readFloatArg();
  setDutyCycle(requestedDC);
}

void onPump() {
  bool requestedStatus = cmdMessenger.readBoolArg();

  if (requestedStatus) {
    pumpOn();
  }
  else {
    pumpOff();
  }
}
  

void attachCommandCallbacks() {
  cmdMessenger.attach(kTemperature, onTemperature);
  cmdMessenger.attach(kPumpStatus, onPumpStatus);
  cmdMessenger.attach(kHeaterStatus, onHeaterStatus);
  cmdMessenger.attach(kDutyCycleStatus, onDutyCycleStatus);
  cmdMessenger.attach(kDutyCycle, onDutyCycle);
  cmdMessenger.attach(kPump, onPump);
}

void measureTemperature() {
  int index = analogRead(A0) - adcSubstract;
  if (index < 0)
  {
    index = 0;
  }
  if (index>adcMax)
  {
    index = adcMax;
  }
  int lookup = pgm_read_word(&temperatureTable[index]);
  temperature = double(lookup)/10.0;
}

int temperatureToInt(double temperature) {
  return int(round(10*temperature));
}

void setSetPoint(int value) {
  setpoint = double(value) / 10;
}
    
void setDutyCycle(double value) {
  // Check bounds
  if (value > 100) {
    value = 100;
  }
  if (value < 0) {
    value = 0;
  }
  dutyCycle = value;
}

void setPValue(double value) {
  pValue = value;
  temperaturePID.SetTunings(pValue, iValue, 0);
}

void setIValue(double value) {
  iValue = value;
  temperaturePID.SetTunings(pValue, iValue, 0);
}
    
void heaterOn() {
  if (!heaterIsOn) {
    digitalWrite(heaterPin, HIGH);
  }
  heaterIsOn = HIGH;
}

void heaterOff() {
  if (heaterIsOn) {
    digitalWrite(heaterPin, LOW);
  }
  heaterIsOn = LOW;
}

void pumpOn() {
  if (!pumpIsOn) {
    digitalWrite(pumpPin, HIGH);
  }
  pumpIsOn = HIGH;
}

void pumpOff() {
  if (pumpIsOn) {
    digitalWrite(pumpPin, LOW);
  }
  pumpIsOn = LOW;
}


// 30 sec
const unsigned long windowSize = 10000;

void controlHeater() {
  // Convert double duty cycle to long for calculation
  unsigned long intDutyCycle = int(dutyCycle);
  
  // If we are not in PID controlled mode
  // we can skip the calculation of the window size
  // and be constantly on or off if the duty cycle is
  // larger then 100 or smaller then 0
  // If we wouldn't check for being in PID mode
  // then the PID would set the duty cycle to 
  // zero, we would exit the dutycycle mode and
  // when the PID sets it greater then zero again enter
  // it again, but the window would be reset... this leads
  // to a lot of relay action around setpoint...
  boolean inPIDmode = temperaturePID.GetMode();
  
  if (!inPIDmode && intDutyCycle < 0) {
    heaterOff();
    inDutyCycleMode = LOW;
  }
  else if (!inPIDmode && intDutyCycle > 99) {
    heaterOn();
    inDutyCycleMode = LOW;
  }
  else {
    // If you just entered duty cycle mode
    // start first window
    if (!inDutyCycleMode) {
      windowStartTime = currentMillis;
    }
    
    // The onTime is windowSize * dutyCycle and since
    // dutyCycle is in percent we divide by 100
    unsigned long onTime = intDutyCycle * (windowSize / 100);
    
    // Shift window time if  needed
    if (currentMillis - windowStartTime > windowSize)
      windowStartTime += windowSize;

    if (currentMillis - windowStartTime < onTime) {
      heaterOn();
    }
    else {
      heaterOff();
    }
    inDutyCycleMode = HIGH;
  }
}

void setup() {
  pinMode(pumpPin, OUTPUT);
  pinMode(heaterPin, OUTPUT);
  dutyCycle = 0;
  
  measureTemperature();
  setpoint = temperature + 1;
  
  temperaturePID.SetMode(MANUAL);
  temperaturePID.SetOutputLimits(0, 100);
  temperaturePID.SetSampleTime(windowSize);
  
  Serial.begin(115200);

  cmdMessenger.printLfCr();
  
  attachCommandCallbacks();
  
  cmdMessenger.sendCmd(kAcknowledge, "Arduino ready");
}

void loop () {
  currentMillis = millis();
  cmdMessenger.feedinSerialData();
  
  if (currentMillis - previousMillis > 100) {
    measureTemperature();
    temperaturePID.Compute();
    controlHeater();
    previousMillis = currentMillis;
    slowCount++;
    if (slowCount > 50) {
      slowCount = 0;
    }
  }
}
