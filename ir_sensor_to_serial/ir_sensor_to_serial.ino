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
int outputValue = 0;        // value output to the PWM (analog out)


void setup()
{
  pinMode(ENEyePin, OUTPUT);      // sets the digital pin as output
  Serial.begin(9600); 
  digitalWrite(ENEyePin, HIGH);
  
}

void loop()
{

    // read the analog in value:
  sensorValue1 = analogRead(analogInPin1);            
  sensorValue2 = analogRead(analogInPin2);            
  sensorValue3 = analogRead(analogInPin3);            
  sensorValue4 = analogRead(analogInPin4);            
  // map it to the range of the analog out:
          

  // print the results to the serial monitor:
  Serial.print("sensor1 = " );                       
  Serial.println(sensorValue1);      
  Serial.print("sensor2 = " );                       
  Serial.println(sensorValue2);      
  Serial.print("sensor3 = " );                       
  Serial.println(sensorValue3);      
  Serial.print("sensor4 = " );                       
  Serial.println(sensorValue4);      
  

  // wait 10 milliseconds before the next loop
  // for the analog-to-digital converter to settle
  // after the last reading:
  delay(1000); 
}
