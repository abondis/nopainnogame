
/*To control the rover, Copy and paste the code below into the Arduino software*/ 
// Test
int E1 = 6; //M1 Speed Control 
int E2 = 5; //M2 Speed Control 
int M1 = 8; //M1 Direction Control 
int M2 = 7; //M2 Direction Control 

int turnMultiplier = 1300; //ms par 90degré de rotation
float accelerationModificator = 1.3; //7.75cm par sec. 1000ms/775 = 1.3
int leftspeed = 255;  //255 is maximum speed  
int rightspeed = 255; 

void setup(void) 
{ 
  //int i; 
  //for(i=5;i<=8;i++) 
  //pinMode(i, OUTPUT); 
  Serial.begin(9600);
  Serial.println("Start;");
}

void loop(void) 
{  
  while (Serial.available() < 1) {} // Wait until a character is received 
  char command = Serial.read();
  int magnitude = readInt();
  int finish = 0;
  int collision = 0;
  int timeCount = 0;
  int timeLimit = 0;
  
  switch(command) // Perform an action depending on the command 
  {
  case 'f'://Move Forward 
    forward();
    timeLimit = magnitude * accelerationModificator;
    break; 
  case 'b'://Move Backwards 
    reverse();
    timeLimit = magnitude * accelerationModificator;
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
  
  while (finish == 0) { // loop each 50ms
    
    timeCount = timeCount + 50;
    delay(50);
    
    if(timeLimit !=0 && timeLimit < timeCount){
      finish = 1;
    }
    
    //TODO détection de colision.
    /*
    if(collision){
      collision = 1;
      finish = 1;
    }
    */
  }
  
  stop();
  
  //Envoyer un réponse
  Serial.print(command);
  Serial.print(",");
  if(command == 'f' || command == 'b'){
    Serial.print(int( timeCount / accelerationModificator ));
  } else {
    Serial.print(magnitude);
  }
  Serial.print(",");
  Serial.print(collision);
  Serial.println(";");
  
}

int readInt(){
  char buffer = int(Serial.read());
  int value = 0;
  
  while (buffer != ';') {
    value = value * 10;
    value = value + buffer;
    buffer = int(Serial.read());
  }
  return value;
}

void stop(void) //Stop 
{ 
  digitalWrite(E1,LOW); 
  digitalWrite(E2,LOW); 
  Serial.print("Stop");
} 
void forward() 
{ 
  analogWrite (E1,leftspeed); 
  digitalWrite(M1,LOW); 
  analogWrite (E2,rightspeed); 
  digitalWrite(M2,LOW); 
  Serial.print("J'avance");
} 
void reverse () 
{ 
  analogWrite (E1,leftspeed); 
  digitalWrite(M1,HIGH); 
  analogWrite (E2,rightspeed); 
  digitalWrite(M2,HIGH); 
  Serial.print("Je recule");
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