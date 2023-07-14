#include "display.h"

U8GLIB_ST7920_128X64_1X u8g(23, 17, 16); // SPI Com: SCK = en = 23, MOSI = rw = 17, CS = di = 16

// Functions
void draw() {
  if (controller_state != last_controller_state || screen_refresh == 1){
    int pi = 0;
    String my_string;    
    my_string = "Cycle " + String(cycle_count) + " Step " + String(command_active-start_cycle+1);
    char char_buf_c[my_string.length()+1];
    my_string.toCharArray(char_buf_c, my_string.length()+1);
    
    my_string ="W " + String((wait_ms-millis())/1000/86400) + "d" + String(((wait_ms-millis())/1000%86400)/3600)  + "h" + String(((wait_ms-millis())/1000%3600)/60) + "m" +String(((wait_ms-millis())/1000%60)) +"s";
    for (int pi=0;pi<n_pumps;pi++){
      if (states[pi]==1){
         my_string = "Homing pump " + String(pi+1);
      }
      if (states[pi]==5){
        my_string = "Wp" + String(pi+1) + " " + String((abs(wait_steps[pi] - motor_positions[pi])/motor_calibrations[pi] * volume_factors[pi])) + "ul";
      }
    }
    
    char char_buf_w[my_string.length()+1];
    my_string.toCharArray(char_buf_w, my_string.length()+1);
    my_string = "Elapsed: " + String((millis()-millis_end)/1000) + "s";
    char char_buf_e[my_string.length()+1];
    my_string.toCharArray(char_buf_e, my_string.length()+1);

    switch(alarm_type){
      case 0:
        my_string = "High pressure!";
        break;
      case 1:
        my_string = "Low pressure!";
        break;
      case 2:
        my_string = "Timeout!";
        break;
      case 3:
        my_string = "High speed!";
        break;
      case 4:
        my_string = "Low speed!";
        break;
    }
    
    char char_buf_a[my_string.length()+1];
    my_string.toCharArray(char_buf_a, my_string.length()+1);

          
    u8g.firstPage();
    do {   
  
  
    
      switch(controller_state){
        case 0:                                         // Home screen
          u8g.setFont(u8g_font_unifont);
          //u8g.setFont(u8g_font_osb21);
          u8g.drawStr( 8, 10, "Start program?");
          u8g.drawStr( 45, 62, ">Yes");
          break;
    
          case 2:                                     // Running
            u8g.setFont(u8g_font_unifont);
            //u8g.setFont(u8g_font_osb21);
            u8g.drawStr( 5, 10, "Program running!");
            u8g.drawStr( 5, 28, char_buf_c);
            u8g.drawStr( 5, 43, char_buf_w);
            
            if (((encoder_pososition/4) % 2) == 0){
              u8g.drawStr( 10, 62, ">Pause   Stop");
            }
            else{
              u8g.drawStr( 10, 62, " Pause  >Stop");
            }
          break;
    
          case 3:                                    // Pause
            u8g.setFont(u8g_font_unifont);
            //u8g.setFont(u8g_font_osb21);
            u8g.drawStr( 0, 10, "Paused...");
            if (((encoder_pososition/4) % 2) == 0){
              u8g.drawStr( 10, 62, ">Resume   Stop");
            }
            else{
              u8g.drawStr( 10, 62, " Resume  >Stop");
            }
          break;
          
        case 1:                                         // Done
          u8g.setFont(u8g_font_unifont);
          //u8g.setFont(u8g_font_osb21);
          u8g.drawStr( 0, 10, "Program complete!");
          u8g.drawStr( 5, 28, char_buf_e);
          u8g.drawStr( 30, 62, ">Restart?");
          break;

        case 4:                                         // Alarm

          u8g.setFont(u8g_font_unifont);
          u8g.drawStr( 0, 10, "Alarm triggered!");
          u8g.drawStr( 5, 28, char_buf_a);
          u8g.drawStr( 30, 62, ">Restart?");
          break;
      }
    }
    while( u8g.nextPage() );
    last_controller_state = controller_state;
    screen_refresh = 0;
  }   
}
