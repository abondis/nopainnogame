/*To control the rover, Copy and paste the code below into the Arduino software*/ 
// Test
int E1 = 6; //M1 Speed Control 
int E2 = 5; //M2 Speed Control 
int M1 = 8; //M1 Direction Control 
int M2 = 7; //M2 Direction Control 
int ENEyePin; // EN pin for the eyes
const int analogInPin1 = A0;  // Analog input pin that the potentiometer is attached to
const int analogInPin2 = A1;  // Analog input pin that the potentiometer is attached to
const int analogInPin3 = A2;  // Analog input pin that the potentiometer is attached to
const int analogInPin4 = A3;  // Analog input pin that the potentiometer is attached to
const int analogOutPin = 9; // Analog output pin that the LED is attached to

int sensorValue1 = 0;        // value read from the pot
int sensorValue2 = 0;        // value read from the pot
int sensorValue3 = 0;        // value read from the pot
int sensorValue4 = 0;        // value read from the pot


void setup(void) 
{ 
  int i; 
  for(i=5;i<=8;i++) 
  pinMode(i, OUTPUT); 
  Serial.begin(9600);
  pinMode(ENEyePin, OUTPUT);      // sets the digital pin as output
  digitalWrite(ENEyePin, HIGH);

} 
void loop(void) 
{ 
//  Serial.print("Ready to rock\n");  
  
  while (Serial.available() < 1) {} // Wait until a character is received 
  char val = Serial.read(); 
  int leftspeed = 255;  //255 is maximum speed  
  int rightspeed = 255; 
  switch(val) // Perform an action depending on the command 
  { 
  case 'f'://Move Forward 
    forward (leftspeed,rightspeed); 
    break; 
  case 'b'://Move Backwards 
    reverse (leftspeed,rightspeed); 
    break; 
  case 'l'://Turn Left 
    left (leftspeed,rightspeed); 
    break; 
  case 'r'://Turn Right 
    right (leftspeed,rightspeed); 
    break; 
  default: 
    stop(); 
    break; 
  }
  int i = 0;
  boolean collision = sense() & val == 'f'
  ;
  while (i <20 & !collision){
    delay(100);
    collision = sense( )& val == 'f';
    if(collision ) {
      break;
    }
    i++;
  }
  collision = sense();
  Serial.print(val);
  Serial.print(",");
  Serial.print(i*100);
  Serial.print(",");
  Serial.print(collision);
  Serial.print(";");
  stop();
}


void stop(void) //Stop 
{ 
  digitalWrite(E1,LOW); 
  digitalWrite(E2,LOW); 
//  Serial.print("Stop");
} 
void forward(char a,char b) 
{ 
  analogWrite (E1,a); 
  digitalWrite(M1,LOW); 
  analogWrite (E2,b); 
  digitalWrite(M2,LOW); 
//  Serial.print("J'avance");
} 
void reverse (char a,char b) 
{ 
  analogWrite (E1,a); 
  digitalWrite(M1,HIGH); 
  analogWrite (E2,b); 
  digitalWrite(M2,HIGH); 
//  Serial.print("Je recule");
} 
void left (char a,char b) 
{ 
  analogWrite (E1,a); 
  digitalWrite(M1,HIGH); 
  analogWrite (E2,b); 
  digitalWrite(M2,LOW); 
} 
void right (char a,char b) 
{ 
  analogWrite (E1,a); 
  digitalWrite(M1,LOW); 
  analogWrite (E2,b); 
  digitalWrite(M2,HIGH); 
}

int outputValue = 0;        // value output to the PWM (analog out)

boolean sense(void) // Sense objects
{ 
  
  // read the analog in value:
  sensorValue1 = analogRead(analogInPin1);            
  sensorValue2 = analogRead(analogInPin2);            
  sensorValue3 = analogRead(analogInPin3);            
  sensorValue4 = analogRead(analogInPin4);            
  // collision
  if( (sensorValue1 + sensorValue2 + sensorValue3 + sensorValue4) / 4 > 600) {
    return 1;
  } else {
    return 0;
  }
}

