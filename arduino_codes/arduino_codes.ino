int PTC_Val,POT_Val,LDR_Val,but_stop,but_forw,but_back,counter;
char But_Val;

void setup() {

    Serial.begin(9600);

    pinMode(3,OUTPUT);
    pinMode(8,INPUT_PULLUP);
    pinMode(9,INPUT_PULLUP);
    pinMode(10,INPUT_PULLUP);

}

void loop() {

     PTC_Val += analogRead(A0);
     POT_Val += analogRead(A1);
     LDR_Val += analogRead(A2);

     but_back = digitalRead(8);
     but_stop = digitalRead(9);
     but_forw = digitalRead(10);
     
    if(but_stop == 0){
        But_Val =  's';}
    else if(but_forw == 0)
        {But_Val =  'f';}
    else if(but_back == 0)
        {But_Val =  'b';}
    else
        {But_Val =  'k';}

    if(PTC_Val > 2400){
       digitalWrite(3,LOW);}
    else if(PTC_Val < 1800)
      {digitalWrite(3,HIGH);}
      
      
    if(counter == 12){
      Serial.println("x" + String(map(LDR_Val/13,10,150,0,100)) + "." + String(PTC_Val/13) + "." + String(POT_Val/13) + "." + (But_Val)+ "c");
      counter=0;
      PTC_Val = 0;
      POT_Val = 0;
      LDR_Val = 0;
      }
    else{counter+=1;}

     delay(1);

}
