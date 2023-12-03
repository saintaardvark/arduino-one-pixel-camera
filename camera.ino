/*
  Licensed under GPL v3.0.  See LICENSE.txt for details.
*/

#include <Servo.h>

/* TODO: Rename these to x/y servo */
Servo servo_x; // x
int X_PIN = 9;
Servo servo_y;	// y
int Y_PIN = 8;
int xpos = 0;
int ypos = 0;

int ygap = 30;
int xgap = 20;

int lightSensor = 0;
int val = 0;
int i = 0;
int SLEEPYTIME = 10;

/* microseconds to sleep at each degree.  Since code currently assumes
   10 sec to sweep, that's 10 s / 180 degrees = 56 microseconds
*/
int SERVO_DELAY = 56;

/*
  The initial setting of the position to 0 is quite fast; here we slow
  that down.
 */
void resetServosSlowly() {
	Serial.println("About to set x slowly to 0");
  for (int i = servo_x.read(); i > 0 ; i--) {
    servo_x.write(i);
    delay(100);
  }
	Serial.println("About to set y slowly to 0");
  for (int i = servo_y.read(); i > 0 ; i--) {
		servo_y.write(i);
    delay(100);
  }
}

// the setup function runs once when you press reset or power the board
void setup() {
  // initialize digital pin LED_BUILTIN as an output.
  pinMode(LED_BUILTIN, OUTPUT);
  Serial.begin(9600);
  Serial.println("Hello, world!");
	Serial.println("setting light sensor...");
  pinMode(lightSensor, INPUT);
	Serial.println("attaching X servo...");
  servo_x.attach(X_PIN);  // attaches the servo on pin 9 to the servo object
	Serial.println("Attaching Y servo...");
  servo_y.attach(Y_PIN);  // attaches the servo on pin 9 to the servo object
  resetServosSlowly();
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
	String msg;
  for (ypos = 0; ypos <= 900; ypos += (2 * ygap)) {
		msg = "YYYYY ";
		msg += String(ypos);
		Serial.println(msg);
    servo_y.writeMicroseconds(MIN_PULSE_WIDTH + ypos);
    for (xpos = 0; xpos <= 1800; xpos += xgap) {
      servo_x.write(MIN_PULSE_WIDTH + xpos);
      delay(SERVO_DELAY);
      val = 1023 - analogRead(lightSensor);
      Serial.println(val);
    }
		Serial.println("ypos ++ ");
		servo_y.writeMicroseconds(MIN_PULSE_WIDTH + ypos + ygap);
    for (xpos = 1800; xpos >= 0; xpos -= xgap) {
      servo_x.writeMicroseconds(MIN_PULSE_WIDTH + xpos);
      delay(SERVO_DELAY);
      val = 1023 - analogRead(lightSensor);
      Serial.println(val);
    }
  }
	for (;;) {
		delay(50000);
	}
}
