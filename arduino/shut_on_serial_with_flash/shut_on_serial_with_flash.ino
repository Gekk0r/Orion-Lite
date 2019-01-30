
String inputString = "";         // a string to hold incoming data
boolean stringComplete = false;  // whether the string is complete
int focuspin1 = 8;
int takepin1 = 9;
int focuspin2 = 11;
int takepin2 = 10;
int flashPin1 = 13;
int flashPin2 = 9;
void setup() {
  // initialize serial:
  Serial.begin(9600);
  pinMode(focuspin1, OUTPUT);
  pinMode(takepin1, OUTPUT);
  pinMode(focuspin2, OUTPUT);
  pinMode(takepin2, OUTPUT);
  pinMode(flashPin1, OUTPUT);
  pinMode(flashPin2, OUTPUT);
  // reserve 200 bytes for the inputString:
  //inputString.reserve(200);
}

void take_with_external_flash() {
  long int d;

  for (int d = 117; d < 118; d += 1) {
    digitalWrite(focuspin1, HIGH);
    digitalWrite(focuspin2, HIGH);
    digitalWrite(flashPin1, HIGH);
    delay(1);
    digitalWrite(flashPin1, LOW);
    delay(1000);
    digitalWrite(takepin1, HIGH);
    //delayMicroseconds(6000);
    delay(3);
    digitalWrite(takepin2, HIGH);
    //delayMicroseconds(d);
    //delayMicroseconds(d);
    delay(d);
    digitalWrite(flashPin1, HIGH);
    delay(5);
    digitalWrite(flashPin1, LOW);
    delay(1000);
    digitalWrite(takepin1, LOW);
    digitalWrite(takepin2, LOW);
    delay(500);
    digitalWrite(focuspin1, LOW);    // turn the LED off by making the voltage LOW
    digitalWrite(focuspin2, LOW);    // turn the LED off by making the voltage LOW
    //delay(10000);              // wait for a second
    //Serial.println(d);
    //d=d+1000;
    Serial.println("gata");
    delay(300);
  }

}
void take_only_cameras() {

  digitalWrite(focuspin1, HIGH);
  digitalWrite(focuspin2, HIGH);
  delay(1000);
  digitalWrite(takepin1, HIGH);
  //delayMicroseconds(6000);
  delay(3);
  digitalWrite(takepin2, HIGH);
  delay(1000);
  digitalWrite(takepin1, LOW);
  digitalWrite(takepin2, LOW);
  delay(500);
  digitalWrite(focuspin1, LOW);    // turn the LED off by making the voltage LOW
  digitalWrite(focuspin2, LOW);    // turn the LED off by making the voltage LOW
  Serial.println("gata");
  delay(300);
  }

void loop() {
  // print the string when a newline arrives:
  if (stringComplete) {
    if (inputString.substring(0,3) =="xxx"){
      Serial.println("Arrivato in xxx");
      if (inputString.substring(4,5) =="1"){
        Serial.println("Arrivato in 1");
        take_only_cameras();
      }
      else if (inputString.substring(4,5) =="2"){
        Serial.println("Arrivato in 2");
        take_with_external_flash();
      }
    }
    else if(inputString.substring(0,2) =="$$"){

      Serial.println("1234xak56789");
    }
    //Serial.println(inputString);
    // clear the string:
    inputString = "";
    stringComplete = false;
  }

}

/*
  SerialEvent occurs whenever a new data comes in the
 hardware serial RX.  This routine is run between each
 time loop() runs, so using delay inside loop can delay
 response.  Multiple bytes of data may be available.
 */
void serialEvent() {
  while (Serial.available()) {
    // get the new byte:
    char inChar = (char)Serial.read();
    // add it to the inputString:
    inputString += inChar;
    // if the incoming character is a newline, set a flag
    // so the main loop can do something about it:
    if (inChar == '\n') {
      stringComplete = true;
    }
  }
}


