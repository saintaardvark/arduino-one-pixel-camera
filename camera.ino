/*
  Licensed under GPL v3.0.  See LICENSE.txt for details.
*/

#include <Servo.h>

Servo myservo;  // create servo object to control a servo
int pos = 0;    // variable to store the servo position


int lightSensor = 0;
int val = 0;
int i = 0;
int SLEEPYTIME = 10;

// the setup function runs once when you press reset or power the board
void setup() {
  // initialize digital pin LED_BUILTIN as an output.
  pinMode(LED_BUILTIN, OUTPUT);
  Serial.begin(9600);
  Serial.println("Hello, world!");
  pinMode(lightSensor, INPUT);
  myservo.attach(9);  // attaches the servo on pin 9 to the servo object
}

// the loop function runs over and over again forever
void loop() {
  i += 1;
  for (pos = 0; pos <= 180; pos += 1) { // goes from 0 degrees to 180 degrees
    // in steps of 1 degree
    myservo.write(pos);              // tell servo to go to position in variable 'pos'
    delay(15);                       // waits 15ms for the servo to reach the position
		val = 1023 - analogRead(lightSensor);
  }
  for (pos = 180; pos >= 0; pos -= 1) { // goes from 180 degrees to 0 degrees
    myservo.write(pos);              // tell servo to go to position in variable 'pos'
    delay(15);                       // waits 15ms for the servo to reach the position
  }
}

