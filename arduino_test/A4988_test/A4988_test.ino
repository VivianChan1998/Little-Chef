// defines pins numbers
#define DELAY 300000
#define DELAY2 5
#define STEP 200
const int dirPin[6] = {8, 30, 36, 42, 48, 52}; 
const int stepPin[6] = {9, 28, 34, 40, 46, 50};

void setup() {
  // Sets the two pins as Outputs
  Serial.begin(9600);
  for(int i = 0; i < 1; i++){
    pinMode(stepPin[i], OUTPUT); 
    pinMode(dirPin[i], OUTPUT);
    digitalWrite(dirPin[i], HIGH);
    digitalWrite(stepPin[i], LOW);
  }
  Serial.println("start");
}
void loop() {
  Serial.println("one cycle");
  // Makes 200 pulses for making one full cycle rotation
  //digitalWrite(dirPin,HIGH);
  for(int i = 0; i < 1; i++){
    Serial.print("Layer");
    Serial.println(i);
    for(int x = 0; x < STEP; x++) {
      //Serial.println(i);
      digitalWrite(stepPin[i],HIGH); 
      //delayMicroseconds(DELAY);
      delay(DELAY2);
      digitalWrite(stepPin[i],LOW); 
      //delayMicroseconds(DELAY);
      delay(DELAY2);
    }
    Serial.println("================");
    delay(1000);
  }
  /*
  digitalWrite(dirPin,LOW);
  for(int x = 0; x < 2; x++) {
    digitalWrite(stepPin,HIGH); 
    delayMicroseconds(DELAY);
    digitalWrite(stepPin,LOW); 
    delayMicroseconds(DELAY);
  }
  delay(5000);

  digitalWrite(dirPin,LOW);
  for(int x = 0; x < STEP; x++) {
    digitalWrite(stepPin,HIGH); 
    delayMicroseconds(DELAY);
    digitalWrite(stepPin,LOW); 
    delayMicroseconds(DELAY);
  }
  digitalWrite(dirPin,HIGH);
  for(int x = 0; x < 2; x++) {
    digitalWrite(stepPin,HIGH); 
    delayMicroseconds(DELAY);
    digitalWrite(stepPin,LOW); 
    delayMicroseconds(DELAY);
  }
  */
  delay(5000);

}
