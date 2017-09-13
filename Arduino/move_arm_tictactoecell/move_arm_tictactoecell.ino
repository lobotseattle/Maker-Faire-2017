char userInput;
char userInputInt;
int greenPin = 13;
#include <Wire.h>
#include <Adafruit_MotorShield.h>
#include "utility/Adafruit_MS_PWMServoDriver.h"
#include "motordriver.h"

//get the motor shield object
Adafruit_MotorShield AFMS = Adafruit_MotorShield(); 



//base motor + its pot
int m1Num = 1;
int m1PotPin = 1;

//shoulder motor + its pot
int m2Num = 2;
int m2PotPin = 2;

//shoulder motor + its pot
int m3Num = 3;
int m3PotPin = 3;

//the claw
int m4Num = 4;
int m4PotPin = 0;

//the default speed for all the motors
int motorSpeed = 125;
   
int val = 0; 
int robotState =0;

// the motor objects
ArmMotor* m1 = NULL;        //abstractiob
ArmMotor* m2 = NULL;
ArmMotor* m3 = NULL;
//ArmMotor* m4 = NULL;
  
void setup()
{
  Serial.begin(9600);          
  Serial.print("Adafruit Motorshield v2 - DC Motor test!");Serial.println();
  initializeMotors();
}

// initialize all the motors
// initialize all the motors
void initializeMotors()
{ 
  m1 = new ArmMotor (AFMS.getMotor(m1Num),m1PotPin);
  m1->setSpeed(motorSpeed);
  m1->calibratePotentiometer(594,90,491,68) ;
  m1->setMinAngle(60);
  m1->setMaxAngle(120);
  m1->printObject();

  m2 = new ArmMotor (AFMS.getMotor(m2Num), m2PotPin);
  m2->setSpeed(motorSpeed);
  m2->calibratePotentiometer(449,0,291,90) ;
  m2->setMinAngle(-30);
  m2->setMaxAngle(120);
  m2->printObject();
  m3 = new ArmMotor (AFMS.getMotor(m3Num), m3PotPin);
  m3->setSpeed(motorSpeed);
  m3->calibratePotentiometer(29,0,426,90) ;
  m3->setMinAngle(-15);
  m3->setMaxAngle(150);
  m3->printObject();

  m4 = new ArmMotor (AFMS.getMotor(m4Num), m4PotPin);
  m4->setSpeed(50);
  m4->calibratePotentiometer(355,15,679,90) ;
  m4->setMinAngle(10);
  m4->setMaxAngle(80);
  m4->printObject();

  AFMS.begin();
}

void loop(){
  {
  if (Serial.available() > 0 )
  {
     //String cell = Serial.readString();
     int cell = Serial.parseInt();
     if (cell == 1))
     {
        m1->gotoTargetAngle(degree);
        m2->gotoTargetAngle(degree);
        m3->gotoTargetAngle(degree);
        m4->gotoTargetAngle(degree);  
     }
     if (cell == 2))
     {
        m1->gotoTargetAngle(degree);
        m2->gotoTargetAngle(degree);
        m3->gotoTargetAngle(degree);
        m4->gotoTargetAngle(degree);  
     }
     if (cell == 3))
     {
        m1->gotoTargetAngle(degree);
        m2->gotoTargetAngle(degree);
        m3->gotoTargetAngle(degree);
        m4->gotoTargetAngle(degree);  
     }
     if (cell == 4))
     {
        m1->gotoTargetAngle(degree);
        m2->gotoTargetAngle(degree);
        m3->gotoTargetAngle(degree);
        m4->gotoTargetAngle(degree);  
     }
     if (cell == 5))
     {
        m1->gotoTargetAngle(degree);
        m2->gotoTargetAngle(degree);
        m3->gotoTargetAngle(degree);
        m4->gotoTargetAngle(degree);  
     }     
     if (cell == 6))
     {
        m1->gotoTargetAngle(degree);
        m2->gotoTargetAngle(degree);
        m3->gotoTargetAngle(degree);
        m4->gotoTargetAngle(degree);  
     } 
     if (cell == 7))
     {
        m1->gotoTargetAngle(degree);
        m2->gotoTargetAngle(degree);
        m3->gotoTargetAngle(degree);
        m4->gotoTargetAngle(degree);  
     }
     if (cell == 8))
     {
        m1->gotoTargetAngle(degree);
        m2->gotoTargetAngle(degree);
        m3->gotoTargetAngle(degree);
        m4->gotoTargetAngle(degree);  
     }
     if (cell == 9))
     {
        m1->gotoTargetAngle(degree);
        m2->gotoTargetAngle(degree);
        m3->gotoTargetAngle(degree);
        m4->gotoTargetAngle(degree);  
     }
     if (cell == 0)) //GoHome
     { 
        m1->gotoTargetAngle(degree);
        m2->gotoTargetAngle(degree);
        m3->gotoTargetAngle(degree);
        m4->gotoTargetAngle(degree);  
     }     
    }
  } 
