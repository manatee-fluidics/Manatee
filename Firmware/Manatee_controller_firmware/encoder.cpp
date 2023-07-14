#include "encoder.h"

// Encoder settings
Encoder myEnc(31, 33);                             // Encoder rotary pins
long encoder_pososition;                           // Current encoder position
long new_encoder_pososition;                       // New encoder position, used to see if encoder is changing
int encoder_button_pin = 35;                       // Encoder button pin
long new_encoder_position;                         // New encoder position, used to see if encoder is changing
long encoder_position;                             // Current encoder position
boolean encoder_button = 1;                        // Encoder button state

// Functions

void handle_encoder(){
  new_encoder_pososition = myEnc.read();
  if (encoder_pososition != new_encoder_pososition){
    encoder_pososition = new_encoder_pososition;
    screen_refresh = 1;
    }
  if (encoder_button != digitalRead(encoder_button_pin)){
    handleBtn();
    screen_refresh = 1;
  }
}

void handleBtn(){
  int go_flag = 0;

  for (int gi=0;gi<5;gi++){
    if (digitalRead(encoder_button_pin)==0){
      go_flag ++;
      delay(1); 
      //Serial.println(go_flag);
       
    }
  }
}
