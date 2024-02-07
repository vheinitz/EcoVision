#include  "tools.h"
#include <Servo.h> 
 

Servo Pusher1;
Servo Pusher2;
Motor Band(3,4,5);



void setup() { 
  Band.uSteps(1);
  Band.speed(500);
  Band.uSteps(16);
  Band.aus();
	Serial.begin(9600);
	Serial.println("Start...");
  Pusher1.attach(9);
  Pusher2.attach(10);
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
          Pusher1.write(angle);
          Serial.println("PSH1\n");
        }
        else if (cmd == 3)
        {
          int angle = Serial.readStringUntil(';').toInt(); 
          Pusher2.write(angle);
          Serial.println("PSH2\n");
        }
    }
    if (!initialised){
      Serial.readStringUntil('?');
    }
    initialised = true;
}
