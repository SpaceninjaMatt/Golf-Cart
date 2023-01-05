// Pins 
#define dir_pin       8
#define step_pin      9
#define steps_from_left 4500
#define limit_pin     10
#define max_rate      4000 //hz
#define min_rate      500 //hz

// global variables
long step_val;    // current step count
long step_ref;    // desired step count
int  dir;
int done;
int frequency;
int last_val;
double steps;
double up_down_steps;


// setup code
void setup() {
  
  pinMode(dir_pin, OUTPUT);
  pinMode(step_pin, OUTPUT);
  pinMode(limit_pin, INPUT);
  digitalWrite(dir_pin, LOW);
  digitalWrite(step_pin, LOW);

  // Setup Serial Monitor
  Serial.begin(9600);
  Serial.setTimeout(50);

  // Timer2
  frequency = min_rate; //initial frequency
  setupTimer2(); //hz

  // init. variables
  step_val = 0;    // current step count
  step_ref = 0;    // desired step count
  dir = 0;
  done = 0;
}

// DO NOT EDIT 
void setupTimer2() {
  noInterrupts();
  // Clear registers
  //Serial.println(frequency);
  TCCR2A = 0;
  TCCR2B = 0;
  TCNT2 = 0;

  // Calculate compare value based on gloabl frequency
  long compareValue = (16000000L/(frequency*128L))-1; //logic to find OCR2A based on a desired f; forces everything to long
  OCR2A = int(compareValue);

  // CTC
  TCCR2A |= (1 << WGM21);
  // Prescaler 128
  TCCR2B |= (1 << CS22) | (1 << CS20);
  // Output Compare Match A Interrupt Enable
  TIMSK2 |= (1 << OCIE2A);
  interrupts();
}

// ISR for TIMER2
ISR(TIMER2_COMPA_vect) {
  
  noInterrupts();
  // update dir
  dir = 0;
  done = 1;//not moving
  if (step_ref > step_val) {
    dir = 1;
    digitalWrite(dir_pin, HIGH);
  }
  if (step_ref < step_val) {
    dir = -1;
    digitalWrite(dir_pin, LOW);
  }
  
  // apply pulse  
  if (dir != 0) { 
    done = 0;//moving
    digitalWrite(step_pin, HIGH);
    delayMicroseconds(int(1000000/(frequency*2))); //50% duty cycle
    digitalWrite(step_pin, LOW);
    step_val = step_val + dir;
    steps++; // increases the step count for the ramp
  }
  interrupts();
}

void step_cal(){
  digitalWrite(dir_pin, LOW);
  step_ref = 0;
  step_val = 0;
  while(digitalRead(limit_pin)==LOW){
    noInterrupts();
    step_ref--;
    interrupts();
  }
  step_val = -steps_from_left;
  step_ref = 0;
}
// ======================================================================================= //
// Main loop
void loop() {
  char cmdStr[] = {0,0,0,0,0,0,0,0,0,0};        // Max. 10 character messages
  int numBytes;
  //Ramp code
  noInterrupts();
    //Serial.println(up_down_steps);
    if(steps <= up_down_steps && done == 0){ //done is 0 when the motor is moving. This is from 0 steps to half the travel
      double tF = (((max_rate-min_rate)/2000)*steps)+min_rate;
      Serial.println(tF);
      frequency = int(tF); //4000hz/half the travel (ex 4000hz/2000steps) 2hz increase per step
      setupTimer2(); // updates the frequency
    }
    else if(steps > up_down_steps && done == 0) {// the ramp down half 
      double tF = (((max_rate-min_rate)/2000)*(up_down_steps*2-steps))+min_rate;
      Serial.println(tF);
      frequency = int(tF);
      setupTimer2();
    }
    if(done == 1 && frequency!= min_rate){
      frequency = min_rate;//resets the frwuqncy when the motor is no longer moving
      setupTimer2();
    }
  interrupts();
  // Is new command available ?
  numBytes = Serial.readBytesUntil('\n', cmdStr, 10);
    // CRITICAL SECTION
  if (numBytes != 0) {
    // CRITICAL SECTION
    noInterrupts();     
    // parse cmdstr
    if (cmdStr[1] == 'R'){  
      step_ref = atof(&cmdStr[2]);
      if(step_ref > 4000){
        step_ref = 4000;
      }
    }
    if (cmdStr[1] == 'L'){  
      step_ref = -atof(&cmdStr[2]);
      if(step_ref < -4000){
        step_ref = -4000;
      }
    }
    if (cmdStr[1] == 'C'){   
      step_cal();   
    } 
    int round = (step_ref/10); 
    step_ref = round*10;
    if(abs(step_val) > abs(step_ref)){
      frequency = min_rate;//resets the frwuqncy when the motor is no longer moving
      setupTimer2();      
    }
    last_val = step_ref;
    steps = 0; //resets step counter for current task
    int diff = abs(step_ref-step_val); //find the amount of steps for total  travel
    up_down_steps = diff/2;//find the amount of steps for half the travel
    interrupts();
  }
}
