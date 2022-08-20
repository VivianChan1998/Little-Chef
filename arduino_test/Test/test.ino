#include <FastLED.h>
#define LED_PIN     6
#define NUM_LEDS    50
CRGB leds[NUM_LEDS];


#define X_DELAY 5
#define Y_DELAY 5

#define X_DIR 8
#define X_STEP 9
#define Y_DIR 10
#define Y_STEP 11

#define X_STEP_ONE_BLOCK 200
#define Y_STEP_ONE_BLOCK 200
#define X_FORWARD_DIR 1 // 1 or 0
#define Y_FROWARD_DIR 1 // 1 or 0

int x_count = 0;
int y_count = 0;

void setup() {
  // Sets the two pins as Outputs
    Serial.begin(9600);
  
    pinMode(X_STEP, OUTPUT); 
    pinMode(X_DIR, OUTPUT);
    digitalWrite(X_STEP, LOW);
    digitalWrite(X_DIR, HIGH);

    pinMode(Y_STEP, OUTPUT); 
    pinMode(Y_DIR, OUTPUT);
    digitalWrite(Y_STEP, LOW);
    digitalWrite(Y_DIR, HIGH);

    FastLED.addLeds<WS2812, LED_PIN, GRB>(leds, NUM_LEDS);

    /*TEMP*/
    Serial.println("X1");
    move_blocks('X', 1);
    delay(2000);
    Serial.println("X2");
    move_blocks('X', 2);
    delay(2000);
    Serial.println("Y1");
    move_blocks('Y', 1);
    delay(2000);
    Serial.println("Y-1");
    move_blocks('Y', -1);
    delay(2000);
    Serial.println("=========test done=========");
    

    Serial.println("start");
}
void loop() {

  if (Serial.available() > 0)
  {
    String data = Serial.readStringUntil('\n');
    Serial.print("[RECIEVED]: ");
    Serial.println(data); //ex: MOVE_X+1 MOVE_Y-1 LEDS_11_ffffff

    if(data[0] == 'M')
    {
        int m = (data.substring(6)).toInt();
        move_blocks(data[5], m);
        Serial.println('DONE');
    }
    else if(data[0] == 'L')
    {
        /*
        leds[0] = CRGB(0, 255, 100);
        leds[1] = CRGB(0, 255, 100);
        */
        FastLED.show();
    }
  }

}

void move_blocks(char dimension, int move) // could be negative val, [-5 ~ +5], no 0
{
    Serial.print('move ' + dimension, + ' ' + move); //TEMP

    int steps = move *  (dimension == 'X'? abs(X_STEP_ONE_BLOCK) : abs(Y_STEP_ONE_BLOCK));
    int pin_dir = dimension == 'X'? X_DIR : Y_DIR;
    int pin_step = dimension == 'X'? X_STEP : Y_STEP;
    int d = dimension == 'X'? X_DELAY : Y_DELAY;
    bool dir = dimension == 'X'? X_FORWARD_DIR : Y_FROWARD_DIR;
    dir = move > 0? dir : !dir;

    digitalWrite(pin_dir, dir);
    for(; steps > 0; steps--)
    {
        digitalWrite(pin_step, HIGH); 
        delay(d);
        digitalWrite(pin_step, LOW); 
        delay(d);
    }
}
