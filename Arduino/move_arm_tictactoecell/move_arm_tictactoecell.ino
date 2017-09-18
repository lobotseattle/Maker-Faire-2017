/*
 * Credit: Adafruit Motor shield, Srikanth Ranganathan
 * Calibrate_4_motors
 * 
 */
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
ArmMotor* m4 = NULL;

void pickupObject()
{
  clawOpen();
  delay(2000);
  clawClose();  
}

void StartFromHome()
{
  pickupObject();
}

void clawOpen()
{
  //m4->gotoTargetAngle(80);
}

void clawClose()
{
  //m4->gotoTargetAngle(17.5);
}

void dropObject()
{
      clawOpen();
      delay(500);
      clawClose();
}

void setup()
{
  Serial.begin(9600);          
  Serial.print("Adafruit Motorshield v2 - DC Motor test!");
  Serial.println();
  initializeMotors();
}

// initialize all the motors
// initialize all the motors
void initializeMotors()
{ 
  m1 = new ArmMotor (AFMS.getMotor(m1Num),m1PotPin);
  m1->setSpeed(motorSpeed);
  m1->calibratePotentiometer(545,90,642,115) ;
  m1->setMinAngle(60);
  m1->setMaxAngle(120);
  m1->printObject();

  m2 = new ArmMotor (AFMS.getMotor(m2Num), m2PotPin);
  m2->setSpeed(motorSpeed);
  m2->calibratePotentiometer(136,0,491,90) ;
  m2->setMinAngle(-100);
  m2->setMaxAngle(120);
  m2->printObject();

  m3 = new ArmMotor (AFMS.getMotor(m3Num), m3PotPin);
  m3->setSpeed(motorSpeed);
  m3->calibratePotentiometer(171,0,505,90) ;
  m3->setMinAngle(-115);
  m3->setMaxAngle(150);
  m3->printObject();

  m4 = new ArmMotor (AFMS.getMotor(m4Num), m4PotPin);
  m4->setSpeed(50);
  m4->calibratePotentiometer(10,16,135,80) ;
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

     
     StartFromHome();
     
     if (cell == 1)
     {
        m1->gotoTargetAngle(117);
        m3->gotoTargetAngle(-15);
        m2->gotoTargetAngle(80); 
        m3->gotoTargetAngle(-30);     
     }
     if (cell == 2)
     {
        m1->gotoTargetAngle(110);
        m3->gotoTargetAngle(15);
        m2->gotoTargetAngle(60);
     }
     if (cell == 3)
     {
        m1->gotoTargetAngle(107);
        m3->gotoTargetAngle(80);
        m2->gotoTargetAngle(10);
        m3->gotoTargetAngle(60);
     }
     if (cell == 4)
     {
        m1->gotoTargetAngle(90);
        m3->gotoTargetAngle(-15);
        m2->gotoTargetAngle(110);
        m3->gotoTargetAngle(-30);
     }
     if (cell == 5)
     {
        m1->gotoTargetAngle(90);
        m3->gotoTargetAngle(15);
        m2->gotoTargetAngle(60);
        m3->gotoTargetAngle(-10);
     }     
     if (cell == 6)
     {
        m1->gotoTargetAngle(95);
        m3->gotoTargetAngle(90);
        m2->gotoTargetAngle(20);
        m3->gotoTargetAngle(50);
     } 
     if (cell == 7)
     {
        m1->gotoTargetAngle(65);
        m3->gotoTargetAngle(-30);
        m2->gotoTargetAngle(75);
     }
     if (cell == 8)
     {
        m1->gotoTargetAngle(70);
        m3->gotoTargetAngle(-10);
        m2->gotoTargetAngle(60);
        
     }
     if (cell == 9)
     {
        m1->gotoTargetAngle(75);
        m3->gotoTargetAngle(90);
        m2->gotoTargetAngle(0);
        
     } 
     dropObject();
     GoHome();     
    }
  } 
}

void GoHome()
{
  m2->gotoTargetAngle(90);
  m3->gotoTargetAngle(90);
  m1->gotoTargetAngle(90);
  clawClose();
}





