/*
  Licensed under GPL v3.0.  See LICENSE.txt for details.
*/

/* #include <Servo.h> */
#include <Adafruit_PWMServoDriver.h>

Adafruit_PWMServoDriver board1 = Adafruit_PWMServoDriver(0x40);  // called this way, it uses the default address 0x40

#define SERVOMIN 125  // this is the 'minimum' pulse length count (out of 4096)
#define SERVOMAX 625  // this is the 'maximum' pulse length count (out of 4096)

#define XSERVO 0
#define YSERVO 1

/* microseconds to sleep at each degree.  Since code currently assumes
   10 sec to sweep, that's 10 s / 180 degrees = 56 microseconds
*/
#define SERVO_DELAY 1000

//gets angle in degree and returns the pulse width
int angleToPulse(int ang) {
  int pulse = map(ang, 0, 180, SERVOMIN, SERVOMAX);  // map angle of 0 to 180 to Servo min and Servo max
  /* Serial.print("Angle: "); */
  /* Serial.print(ang); */
  /* Serial.print(" pulse: "); */
  /* Serial.println(pulse); */
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

String xmsg, ymsg;



/*
  The initial setting of the position to 0 is quite fast; here we slow
  that down.
 */
/* void resetServosSlowly() { */
/* 	Serial.println("About to set x slowly to 0"); */
/*   for (int i = servo_x.read(); i > 0 ; i--) { */
/*     servo_x.write(i); */
/*     delay(100); */
/*   } */
/* 	Serial.println("About to set y slowly to 0"); */
/*   for (int i = servo_y.read(); i > 0 ; i--) { */
/* 		servo_y.write(i); */
/*     delay(100); */
/*   } */
/* } */

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
  /* resetServosSlowly(); */
  delay(1000);
}

/*
 Previously, this function used servo.write(degrees) -- and that's an
 int, so we only get 180 values.

 We can *also* use servo.writeMicroseconds(usec),which can go from 544
 to 2400 (limits set in Servo.h).  This gets us 1856 values, a much
 finer-grained movement.  Call that 1800 for simplicity.

 TODO: Code written, compiles, not yet tested.
 TODO: Logger will need to be adjusted as well
 TODO: Break out 1800 to a constant (or just calculate it, which'd be better)
 TODO: SERVO_DELAY will need to be adjusted? maybe?
*/

// the loop function runs over and over again forever
void loop() {
  /* for (ypos = 0; ypos <= 900; ypos += (2 * ygap)) { */
  for (ypos = 0; ypos <= 180; ypos += 2) {
		ymsg = "YYYYY ";
		ymsg += String(ypos);
		board1.setPWM(YSERVO, 0, angleToPulse(ypos));
    for (xpos = 0; xpos <= 180; xpos += 1) {
			xmsg = " XXXXX ";
			xmsg += String(xpos);
			Serial.println(String(ymsg + xmsg));
			board1.setPWM(XSERVO, 0, angleToPulse(xpos));
      val = 1023 - analogRead(lightSensor);
			delay(SERVO_DELAY);
      /* Serial.println(val); */
    }
		Serial.println("ypos ++ ");
		board1.setPWM(YSERVO, 0, angleToPulse(ypos + 1));
		ymsg = "YYYYY ";
		ymsg += String(ypos + 1);
    for (xpos = 180; xpos >= 0; xpos -= xgap) {
			xmsg = " XXXXX ";
			xmsg += String(xpos);
			Serial.println(String(ymsg + xmsg));
			board1.setPWM(XSERVO, 0, angleToPulse(xpos));
      delay(SERVO_DELAY);
      val = 1023 - analogRead(lightSensor);
      /* Serial.println(val); */
    }
  }
	/* resetServosSlowly(); */
	for (;;) {
		delay(50000);
	}
}
