#include <FastLED.h>
#define LED_PIN     9
#define TOUCH 10
#define NUM_LEDS    2
CRGB leds[NUM_LEDS];
void setup() {
  FastLED.addLeds<WS2812, LED_PIN, GRB>(leds, NUM_LEDS);
  Serial.begin(9600);
}
void loop() {

  bool a = digitalRead(TOUCH);
  Serial.println(a);
  if(a){
     leds[0] = CRGB(0, 255, 100);
     leds[1] = CRGB(0, 255, 100);
     FastLED.show();
  }
  else{
    leds[0] = CRGB(255, 0, 100);
    leds[1] = CRGB(255, 0, 100);
      FastLED.show();
  }

}
