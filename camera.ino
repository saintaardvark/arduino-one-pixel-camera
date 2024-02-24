/*
  Licensed under GPL v3.0.  See LICENSE.txt for details.
*/

/* #include <Servo.h> */
#include <Adafruit_PWMServoDriver.h>

Adafruit_PWMServoDriver board1 = Adafruit_PWMServoDriver(0x40);  // called this way, it uses the default address 0x40

/* Both of these were determined experimentally */
#define SERVOMIN 105  // this is the 'minimum' pulse length count (out of 4096)
#define SERVOMAX 625  // this is the 'maximum' pulse length count (out of 4096)

#define START_X_ANGLE 45
#define END_X_ANGLE 90

#define START_Y_ANGLE 90
#define END_Y_ANGLE 135

#define XSERVO 0
#define YSERVO 1

/* microseconds to sleep at each degree.  Since code currently assumes
   10 sec to sweep, that's 10 s / 180 degrees = 56 microseconds.  Doubling
   this (sorta) arbitrarily to 100 microseconds.
*/
#define SERVO_DELAY 100

//gets angle in degree and returns the pulse width
int angleToPulse(int ang) {
  int pulse = map(ang, 0, 180, SERVOMIN, SERVOMAX);  // map angle of 0 to 180 to Servo min and Servo max
  return pulse;
}


int xpos = 0;
int ypos = 0;

int ygap = 1;
int xgap = 1;

int lightSensor = 0;
int val = 0;
int i = 0;
int SLEEPYTIME = 1000;

String xmsg, ymsg, valmsg;

// the setup function runs once when you press reset or power the board
void setup() {
  // initialize digital pin LED_BUILTIN as an output.
  board1.begin();
  board1.setPWMFreq(60);  // Analog servos run at ~60 Hz updates
  pinMode(LED_BUILTIN, OUTPUT);
  Serial.begin(9600);
  Serial.println("Hello, world!");
  Serial.println("setting light sensor...");
  pinMode(lightSensor, INPUT);
  /* TODO: Would be nice to have this again.  But we can't read the
     servo angle from the board. */
  /* resetServosSlowly(); */
  Serial.println("Initial set!");
  board1.setPWM(XSERVO, 0, angleToPulse(0));
  board1.setPWM(YSERVO, 0, angleToPulse(0));
  delay(1000);
}

void loop() {
  for (xpos = START_X_ANGLE ; xpos <= END_X_ANGLE; xpos += 1) {
    xmsg = "XXXXX ";
    xmsg += String(xpos);
    board1.setPWM(XSERVO, 0, angleToPulse(xpos));
    delay(SERVO_DELAY);
    for (ypos = START_Y_ANGLE; ypos <= END_Y_ANGLE; ypos += 1) {
      ymsg = " YYYYY ";
      ymsg += String(ypos);
      board1.setPWM(YSERVO, 0, angleToPulse(ypos));
      delay(SERVO_DELAY);
      val = 1023 - analogRead(lightSensor);
      valmsg = " VAL ";
      valmsg += String(val);
      Serial.println(String(xmsg + ymsg + valmsg));
    }
    board1.setPWM(XSERVO, 0, angleToPulse(xpos + 1));
    xmsg = "XXXXX ";
    xmsg += String(xpos + 1);
    for (ypos = END_Y_ANGLE; ypos >= START_Y_ANGLE; ypos -= 1) {
     ymsg = " YYYYY ";
      ymsg += String(ypos);
      board1.setPWM(YSERVO, 0, angleToPulse(ypos));
      delay(SERVO_DELAY);
      val = 1023 - analogRead(lightSensor);
      valmsg = " VAL ";
      valmsg += String(val);
      Serial.println(String(xmsg + ymsg + valmsg));
     }
  }
	/* And now we rest. */
	Serial.println("END END END");
  /* resetServosSlowly(); */
  for (;;) {
    delay(50000);
  }
}
