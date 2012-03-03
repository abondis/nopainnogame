void setup() 
{
  Serial.begin(9600);             //Set serial baud rate to 9600
} 

void loop()
{
  Serial.print("Hello!");           //print out hello string 
  delay(1000);                  //1 second delay

  while (!Serial.available());

}
