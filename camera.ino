/*
  Licensed under GPL v3.0.  See LICENSE.txt for details.
*/

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
}

// the loop function runs over and over again forever
void loop() {
  i += 1;
  val = 1023 - analogRead(lightSensor);
  // 10 seconds divided by SLEEPYTIME
  if (i % (10 * 1000 / SLEEPYTIME) == 0) {
    for (int j=0; j < 10; j++) {
      Serial.println("SLEEPYTIME");
      delay(1000);
    }
  } else {
    Serial.println(val);
    if (i % (1000 / SLEEPYTIME ) == 0) {
      Serial.println("*********************STEP");
    }
    delay(SLEEPYTIME);
  }
}
