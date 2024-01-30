#include  "tools.h"
#include <Servo.h> 
 

Servo Pusher;
Motor Band(3,4,5);



void setup() { 
  Band.uSteps(1);
  Band.speed(500);
  Band.uSteps(16);
  Band.aus();
	Serial.begin(9600);
	Serial.println("Start...");
  Pusher.attach(8);
}

static bool initialised =false; 
     
void loop() 
{   

  delay(1000);
  if ( initialised && Serial.available())
  {
    delay(200);
    Serial.println("RX...\n");
        int cmd = Serial.readStringUntil(':').toInt(); 
        
        if (cmd == 1)// Motor band
        {
          int steps = Serial.readStringUntil(';').toInt(); 
          Band.ein();
          Band.rechts(steps);
          Band.aus();
        }
        else if (cmd == 2)
        {
          int angle = Serial.readStringUntil(';').toInt(); 
          Pusher.write(angle);
        }
    }
    if (!initialised){
      Serial.readStringUntil('?');
    }
    initialised = true;
}
