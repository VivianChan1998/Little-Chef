#include <FastLED.h>
#define B_PIN     6
#define T_PIN     5
#define B_NUM_LEDS    100
#define T_NUM_LEDS    100
#define button_pin 3
CRGB b_leds[B_NUM_LEDS];
CRGB t_leds[T_NUM_LEDS];

#define X_DELAY 2
#define Y_DELAY 3

#define X_DIR 8
#define X_STEP 9
#define Y_DIR 10
#define Y_STEP 11

#define X_STEP_ONE_BLOCK 360
#define Y_STEP_ONE_BLOCK 300
#define X_FORWARD_DIR 1 // 1 or 0
#define Y_FORWARD_DIR 1 // 1 or 0

int x_count = 0;
int y_count = 0;

int tile_x[3] = {18, 16, 14};
int tile_y[8] = {22, 23, 24, 25, 26, 27, 28, 29};

bool btn = false;

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

    pinMode(button_pin, INPUT);

    FastLED.addLeds<WS2812, T_PIN, GRB>(t_leds, T_NUM_LEDS);
    FastLED.addLeds<WS2812, B_PIN, GRB>(b_leds, B_NUM_LEDS);
    
    long c = strtol("ffffff", NULL, 16);
    for(int i=29; i<99; i++)
    {
      t_leds[i] = c;
    }
    FastLED.show();

    Serial.println("start");
    //Serial.println("BUTTON");
}

void loop() {

  if(digitalRead(button_pin) && !btn){
    Serial.println("BUTTON");
    btn = true;
  }

  if (Serial.available() > 0)
  {
    String data = Serial.readStringUntil('\n');
    Serial.print("[RECIEVED]: ");
    Serial.println(data); //ex: MOVE_X+1 MOVE_Y-1 LEDS_11_ffffff

    if(data[0] == 'M')
    {
        int m = (data.substring(6)).toInt();
        move_blocks(data[5], m);
        Serial.println("DONE");
    }
    else if(data[0] == 'E')
    {
      btn = false;
      Serial.println("DONE");
    }
    else if(data[0] == 'L')
    {
      if(data[3] == 'B')
      {
        long c = strtol(data.substring(5).c_str(), NULL, 16);
        Serial.println(c);
        for(int i=14; i<21;i++) b_leds[i] = c;
        
        FastLED.show();
        Serial.println("DONE");
      }
      else
      {
        //long c = strtol(data.substring(5).c_str(), NULL, 16);
        for(int i=0; i<3; ++i){
          t_leds[tile_x[i]] = 0;
        }
        for(int i=0; i<8; ++i){
          t_leds[tile_y[i]] = 0;
        }
        int posx = tile_x[data[5] - '0'];
        int posy = tile_y[data[6] - '0'];
        Serial.println(posx);
        Serial.println(posy);
        t_leds[posx] = "ffffff";
        t_leds[posy] = "ffffff";
        
        FastLED.show();
        Serial.println("DONE");
      }
        
    }
  }

}

void move_blocks(char dimension, int move) // could be negative val, [-5 ~ +5], no 0
{
    Serial.print("move ");
    Serial.print(dimension);
    Serial.print(' ');
    Serial.print(move);
    Serial.println();

    int steps = dimension == 'X'? abs(X_STEP_ONE_BLOCK) : abs(Y_STEP_ONE_BLOCK);
    int pin_dir = dimension == 'X'? X_DIR : Y_DIR;
    int pin_step = dimension == 'X'? X_STEP : Y_STEP;
    int d = dimension == 'X'? X_DELAY : Y_DELAY;
    bool dir = dimension == 'X'? X_FORWARD_DIR : Y_FORWARD_DIR;
    dir = move > 0? dir : !dir;
    Serial.println(steps);

    digitalWrite(pin_dir, dir);
    for(; steps != 0; steps--)
    {
        digitalWrite(pin_step, HIGH); 
        delay(d);
        digitalWrite(pin_step, LOW); 
        delay(d);
    }
}
