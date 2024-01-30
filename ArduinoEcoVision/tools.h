#define Solange while


void warte(long ms)
{
  delay(ms);
}

#define sage(text) Serial.println(text);

#define WiederholeFortlaufend while(true)

class LichtSchranke
{
  public:
  int _pin;
  LichtSchranke(int pin):_pin(pin)
  {
    pinMode(_pin, INPUT_PULLUP);    
  }  

  bool auf()
  {
    return digitalRead(_pin) == 0;
  }

  bool zu()
  {
    return digitalRead(_pin) == 1;
  } 
};


class Motor
{
  enum MotorType {MTINV,MT28,MT4988};
  public:
  int _p1;
  int _p2;
  int _p3;
  int _p4;
  int _dir;
  int _step;
  int _en;
  int _speed;
  int _uSteps;
  MotorType _motorType;
  Motor(int p1=-1, int p2=-1, int p3=-1, int p4=-1):_p1(p1),_p2(p2),_p3(p3),_p4(p4),_en(p1),_dir(p2),_step(p3)
  {
    if (p1>0 && p2>0 && p3>0 && p4>0)
    { 
      _motorType = MT28;
      _speed = 1300;        
      pinMode(_p1, OUTPUT);
      pinMode(_p2, OUTPUT);
      pinMode(_p3, OUTPUT);
      pinMode(_p4, OUTPUT);
    }
    else if (p1>0 && p2>0 && p3>0 )
    { 
      _motorType = MT4988;
      _speed=50;
      _uSteps=16;
      pinMode(_en, OUTPUT);
      pinMode(_dir, OUTPUT);
      pinMode(_step, OUTPUT);
    }
    else
    {
      _motorType = MTINV;      
    }
  }

  void ein()
  {
    if (_motorType == MT28 )
    {
   
    }
    else if (_motorType == MT4988 )
    {
      digitalWrite(_en,LOW);
    }
  } 

  void aus()
  {
    if (_motorType == MT28 )
    {
      digitalWrite(_p1, LOW); 
      digitalWrite(_p2, LOW); 
      digitalWrite(_p3, LOW); 
      digitalWrite(_p4, LOW);      
    }
    else if (_motorType == MT4988 )
    {
      digitalWrite(_en,HIGH);
    }
  }

  void speed(int s)
  {
    _speed = s;
  }

  void uSteps(int us)
  {
    _uSteps = us;
  }

  void auf(int steps){ links (steps);}
  void L(int steps){ links (steps);}
  void links(int steps)
  {
    move(steps*-1);
  }

  void ab(int steps){ rechts (steps);}
  void R(int steps){ rechts (steps);}
  void rechts(int steps)
  {
    move(steps);
  }

  void move(int steps)
  { 
    int T = _speed;
    int asteps = abs(steps);

    if (_motorType==MT4988)
    {
      if (steps > 0)
      {
        digitalWrite(_dir, HIGH);        
      }
      else
      {
        digitalWrite(_dir, LOW);
      }
      for (int i=0; i < asteps; i++)
      {
        for (int m=0; m < _uSteps; m++)
        {
          digitalWrite(_step, HIGH);
          digitalWrite(_step, LOW);
          delayMicroseconds(T*16/_uSteps);
        }
      }
    }
    else if (_motorType == MT28)
    {
      for (int i=0; i < asteps; i++)
      {
        if (steps > 0)
        {
          digitalWrite(_p1, LOW); 
          digitalWrite(_p2, LOW); 
          digitalWrite(_p3, LOW); 
          digitalWrite(_p4, LOW);
          delayMicroseconds(T);
          digitalWrite(_p1, LOW); 
          digitalWrite(_p2, LOW); 
          digitalWrite(_p3, LOW); 
          digitalWrite(_p4, HIGH);
          delayMicroseconds(T);
          digitalWrite(_p1, LOW); 
          digitalWrite(_p2, LOW); 
          digitalWrite(_p3, HIGH); 
          digitalWrite(_p4, HIGH);
          delayMicroseconds(T);
          digitalWrite(_p1, LOW); 
          digitalWrite(_p2, LOW); 
          digitalWrite(_p3, HIGH); 
          digitalWrite(_p4, LOW);
          delayMicroseconds(T);
          digitalWrite(_p1, LOW); 
          digitalWrite(_p2, HIGH); 
          digitalWrite(_p3, HIGH); 
          digitalWrite(_p4, LOW);
          delayMicroseconds(T);
          digitalWrite(_p1, LOW); 
          digitalWrite(_p2, HIGH); 
          digitalWrite(_p3, LOW); 
          digitalWrite(_p4, LOW);
          delayMicroseconds(T);
          digitalWrite(_p1, HIGH); 
          digitalWrite(_p2, HIGH); 
          digitalWrite(_p3, LOW); 
          digitalWrite(_p4, LOW);
          delayMicroseconds(T);
          digitalWrite(_p1, HIGH); 
          digitalWrite(_p2, LOW); 
          digitalWrite(_p3, LOW); 
          digitalWrite(_p4, LOW);
          delayMicroseconds(T);
          digitalWrite(_p1, LOW); 
          digitalWrite(_p2, LOW); 
          digitalWrite(_p3, LOW); 
          digitalWrite(_p4, LOW);
        }
        else if (steps < 0)
        {
          digitalWrite(_p1, LOW); 
          digitalWrite(_p2, LOW); 
          digitalWrite(_p3, LOW); 
          digitalWrite(_p4, LOW);
          delayMicroseconds(T);
          digitalWrite(_p1, HIGH); 
          digitalWrite(_p2, LOW); 
          digitalWrite(_p3, LOW); 
          digitalWrite(_p4, LOW);
          delayMicroseconds(T);
          digitalWrite(_p1, HIGH); 
          digitalWrite(_p2, HIGH); 
          digitalWrite(_p3, LOW); 
          digitalWrite(_p4, LOW);
          delayMicroseconds(T);
          digitalWrite(_p1, LOW); 
          digitalWrite(_p2, HIGH); 
          digitalWrite(_p3, LOW); 
          digitalWrite(_p4, LOW);
          delayMicroseconds(T);
          digitalWrite(_p1, LOW); 
          digitalWrite(_p2, HIGH); 
          digitalWrite(_p3, HIGH); 
          digitalWrite(_p4, LOW);
          delayMicroseconds(T);
          digitalWrite(_p1, LOW); 
          digitalWrite(_p2, LOW); 
          digitalWrite(_p3, HIGH); 
          digitalWrite(_p4, LOW);
          delayMicroseconds(T);
          digitalWrite(_p1, LOW); 
          digitalWrite(_p2, LOW); 
          digitalWrite(_p3, HIGH); 
          digitalWrite(_p4, HIGH);
          delayMicroseconds(T);
          digitalWrite(_p1, LOW); 
          digitalWrite(_p2, LOW); 
          digitalWrite(_p3, LOW); 
          digitalWrite(_p4, HIGH);
          delayMicroseconds(T);
        }
      }
      digitalWrite(_p1, LOW); 
      digitalWrite(_p2, LOW); 
      digitalWrite(_p3, LOW); 
      digitalWrite(_p4, LOW);
    }
  }

};



/*
/////////////////////////////////////////////
const int M1_1 = 5;
const int M1_2 = 4;
const int M1_3 = 3;
const int M1_4 = 2;

const int M2_1 = 9;
const int M2_2 = 8;
const int M2_3 = 7;
const int M2_4 = 6;



int i1 = 5;
int i2 = 4;
int i3 = 3;
int i4 = 2;


void move(int m, int steps)
{
  if (m==1)
  {
    i1=M1_1; 
    i2=M1_2;
    i3=M1_3; 
    i4=M1_4;
  } 
  else if (m==2)
  {
    i1=M2_1; 
    i2=M2_2;
    i3=M2_3; 
    i4=M2_4;
  }
  else
     return;
  
  int T = 1200;
  int asteps = abs(steps);
  for (int i=0; i <= asteps; i++)
  {
    if (steps > 0)
    {
     
      digitalWrite(i1, LOW); 
      digitalWrite(i2, LOW); 
      digitalWrite(i3, LOW); 
      digitalWrite(i4, LOW);
      delayMicroseconds(T);
      digitalWrite(i1, LOW); 
      digitalWrite(i2, LOW); 
      digitalWrite(i3, LOW); 
      digitalWrite(i4, HIGH);
      delayMicroseconds(T);
      digitalWrite(i1, LOW); 
      digitalWrite(i2, LOW); 
      digitalWrite(i3, HIGH); 
      digitalWrite(i4, HIGH);
      delayMicroseconds(T);
      digitalWrite(i1, LOW); 
      digitalWrite(i2, LOW); 
      digitalWrite(i3, HIGH); 
      digitalWrite(i4, LOW);
      delayMicroseconds(T);
      digitalWrite(i1, LOW); 
      digitalWrite(i2, HIGH); 
      digitalWrite(i3, HIGH); 
      digitalWrite(i4, LOW);
      delayMicroseconds(T);
      digitalWrite(i1, LOW); 
      digitalWrite(i2, HIGH); 
      digitalWrite(i3, LOW); 
      digitalWrite(i4, LOW);
      delayMicroseconds(T);
      digitalWrite(i1, HIGH); 
      digitalWrite(i2, HIGH); 
      digitalWrite(i3, LOW); 
      digitalWrite(i4, LOW);
      delayMicroseconds(T);
      digitalWrite(i1, HIGH); 
      digitalWrite(i2, LOW); 
      digitalWrite(i3, LOW); 
      digitalWrite(i4, LOW);
      delayMicroseconds(T);
      digitalWrite(i1, LOW); 
      digitalWrite(i2, LOW); 
      digitalWrite(i3, LOW); 
      digitalWrite(i4, LOW);
    }
    else if (steps < 0)
    {
      digitalWrite(i1, LOW); 
      digitalWrite(i2, LOW); 
      digitalWrite(i3, LOW); 
      digitalWrite(i4, LOW);
      delayMicroseconds(T);
      digitalWrite(i1, HIGH); 
      digitalWrite(i2, LOW); 
      digitalWrite(i3, LOW); 
      digitalWrite(i4, LOW);
      delayMicroseconds(T);
      digitalWrite(i1, HIGH); 
      digitalWrite(i2, HIGH); 
      digitalWrite(i3, LOW); 
      digitalWrite(i4, LOW);
      delayMicroseconds(T);
      digitalWrite(i1, LOW); 
      digitalWrite(i2, HIGH); 
      digitalWrite(i3, LOW); 
      digitalWrite(i4, LOW);
      delayMicroseconds(T);
      digitalWrite(i1, LOW); 
      digitalWrite(i2, HIGH); 
      digitalWrite(i3, HIGH); 
      digitalWrite(i4, LOW);
      delayMicroseconds(T);
      digitalWrite(i1, LOW); 
      digitalWrite(i2, LOW); 
      digitalWrite(i3, HIGH); 
      digitalWrite(i4, LOW);
      delayMicroseconds(T);
      digitalWrite(i1, LOW); 
      digitalWrite(i2, LOW); 
      digitalWrite(i3, HIGH); 
      digitalWrite(i4, HIGH);
      delayMicroseconds(T);
      digitalWrite(i1, LOW); 
      digitalWrite(i2, LOW); 
      digitalWrite(i3, LOW); 
      digitalWrite(i4, HIGH);
      delayMicroseconds(T);
    }
  }
  digitalWrite(i1, LOW); 
  digitalWrite(i2, LOW); 
  digitalWrite(i3, LOW); 
  digitalWrite(i4, LOW);
}
*/
