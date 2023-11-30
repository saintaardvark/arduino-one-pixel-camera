/*
  Licensed under GPL v3.0.  See LICENSE.txt for details.
*/

#include <Servo.h>

/* TODO: Rename these to x/y servo */
Servo myservo1; // x
Servo myservo2;	// y
int xpos = 0;
int ypos = 0;

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
  for (int i = myservo1.read(); i > 0 ; i--) {
    myservo1.write(i);
    delay(100);
  }
  for (int i = myservo2.read(); i > 0 ; i--) {
    myservo1.write(i);
    delay(100);
  }
}

// the setup function runs once when you press reset or power the board
void setup() {
  // initialize digital pin LED_BUILTIN as an output.
  pinMode(LED_BUILTIN, OUTPUT);
  Serial.begin(9600);
  Serial.println("Hello, world!");
  pinMode(lightSensor, INPUT);
  myservo1.attach(9);  // attaches the servo on pin 9 to the servo object
  myservo2.attach(8);  // attaches the servo on pin 9 to the servo object
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
  for (ypos = 0; ypos <= 1800; ypos += 1) { // goes from 0 degrees to 180 degrees
    myservo2.writeMicroseconds(MIN_PULSE_WIDTH + ypos); // tell servo to go to position in variable 'pos'
    for (xpos = 0; xpos <= 1800; xpos += 1) { // goes from 0 degrees to 180 degrees
      // in steps of 1 degree
      myservo1.write(MIN_PULSE_WIDTH + xpos); // tell servo to go to position in variable 'pos'
      delay(SERVO_DELAY); // waits  for the servo to reach the position
      val = 1023 - analogRead(lightSensor);
      Serial.println(val);
    }
    for (xpos = 1800; xpos >= 0; xpos -= 1) { // goes from 180 degrees to 0 degrees
      myservo1.writeMicroseconds(MIN_PULSE_WIDTH + xpos);              // tell servo to go to position in variable 'pos'
      delay(SERVO_DELAY);                       // waits 15ms for the servo to reach the position
      val = 1023 - analogRead(lightSensor);
      Serial.println(val);
    }
    Serial.println("YYYYY");
  }
}

