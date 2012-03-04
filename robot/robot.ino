
/*To control the rover, Copy and paste the code below into the Arduino software*/ 
// Test
int E1 = 6; //M1 Speed Control 
int E2 = 5; //M2 Speed Control 
int M1 = 8; //M1 Direction Control 
int M2 = 7; //M2 Direction Control 

//Pins and vars for the eye
int eyePin; // EN pin for the eyes
const int analogInPin1 = A0;  // Analog input pin 
const int analogInPin2 = A1;  // Analog input pin 
const int analogInPin3 = A2;  // Analog input pin 
const int analogInPin4 = A3;  // Analog input pin 

int sensorValue1 = 0;        
int sensorValue2 = 0;       
int sensorValue3 = 0;      
int sensorValue4 = 0;     

int turnMultiplier = 1300; //ms par 90degré de rotation
float speedModificator = 13; //77.5mm par sec
int leftspeed = 255;  //255 is maximum speed  
int rightspeed = 255; 

void setup(void) 
{ 
  int i; 
  for(i=5;i<=8;i++) { 
    pinMode(i, OUTPUT);
  }
  
  
  pinMode(eyePin, OUTPUT); 
  Serial.begin(9600);
  Serial.println("Start;");
}

void loop(void) 
{  
  while (Serial.available() < 4 ); // Wait until a character is received 
  char command = Serial.read();
  int magnitude = readInt();
  Serial.println(magnitude);
  
  boolean finish = 0;
  int collision = 0;
  int timeCount = 0;
  int timeLimit = 0;
  Serial.println("test");
  
  switch(command) // Perform an action depending on the command 
  {
  case 'f'://Move Forward 
    forward();
    timeLimit = magnitude * speedModificator;
    break; 
  case 'b'://Move Backwards 
    reverse();
    timeLimit = magnitude * speedModificator;
    break; 
  case 'l'://Turn Left 
    left();
    timeLimit = magnitude * turnMultiplier;
    break; 
  case 'r'://Turn Right 
    right(); 
    timeLimit = magnitude * turnMultiplier;
    break; 
  default: 
    stop(); 
    break; 
  }
  //finish = sense() & command == 'f' ;
  
  while (finish == 0) { // loop each 50ms
    
    timeCount = timeCount + 50;
    delay(50);
    
    if(timeLimit !=0 && timeLimit < timeCount){
      finish = 1;
    }
    
    if(sense() && command == 'f') {
      collision = 1;
      finish = 1;
    }
  }
  collision = sense();
  stop();
  
  //Envoyer un réponse
  Serial.print(command);
  Serial.print(",");
  if(command == 'f' || command == 'b'){
    Serial.print(int( timeCount / speedModificator ));
  } else {
    Serial.print(magnitude);
  }
  Serial.print(",");
  Serial.print(collision);
  Serial.println(";");
  
}

int readInt(){
  Serial.read(); // protocol f,100; (forward,magnit
  int tmp = Serial.read() - '0';
  int i = 0;
  while(tmp != ';' - '0') {
    i = i*10 + tmp;
    while(Serial.available() < 1);
    tmp = Serial.read() - '0';
  }
 // Serial.println(i, DEC);
  return i;
}

void stop(void) //Stop 
{ 
  digitalWrite(E1,LOW); 
  digitalWrite(E2,LOW); 
} 
void forward() 
{ 
  analogWrite (E1,leftspeed); 
  digitalWrite(M1,LOW); 
  analogWrite (E2,rightspeed); 
  digitalWrite(M2,LOW); 
} 
void reverse () 
{ 
  analogWrite (E1,leftspeed); 
  digitalWrite(M1,HIGH); 
  analogWrite (E2,rightspeed); 
  digitalWrite(M2,HIGH); 
} 
void left () 
{ 
  analogWrite (E1,leftspeed); 
  digitalWrite(M1,HIGH); 
  analogWrite (E2,rightspeed); 
  digitalWrite(M2,LOW); 
} 
void right () 
{ 
  analogWrite (E1,leftspeed); 
  digitalWrite(M1,LOW); 
  analogWrite (E2,rightspeed); 
  digitalWrite(M2,HIGH); 
}


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

