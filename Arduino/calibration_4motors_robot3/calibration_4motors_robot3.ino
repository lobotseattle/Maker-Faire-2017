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
  m2->calibratePotentiometer(136,0,491,90) ;
  m2->setMinAngle(-30);
  m2->setMaxAngle(120);
  m2->printObject();

  m3 = new ArmMotor (AFMS.getMotor(m3Num), m3PotPin);
  m3->setSpeed(motorSpeed);
  m3->calibratePotentiometer(171,0,505,90) ;
  m3->setMinAngle(-15);
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

void loop()
{
  if (Serial.available() > 0 )
  {
     String motorStr = Serial.readStringUntil(':');
     int degree = Serial.parseInt();
     if (motorStr.compareTo("m1") == 0 )
     {
        m1->gotoTargetAngle(degree);
     }
     if (motorStr.compareTo("m2") == 0 )
     {
        m2->gotoTargetAngle(degree);
     }
     if (motorStr.compareTo("m3") == 0 )
     {
        m3->gotoTargetAngle(degree);
     }
     if (motorStr.compareTo("m4") == 0 )
     {
        m4->gotoTargetAngle(degree);
     }
     
     if (motorStr.compareTo("home")==0)
     { 
        m1->gotoTargetAngle(degree);
        m2->gotoTargetAngle(degree);
        m3->gotoTargetAngle(degree);
        m4->gotoTargetAngle(degree);  
     }

//    if (motorStr.compareTo("beaker1")==0)
//     { 
//        m1->gotoTargetAngle(120);
//        m2->gotoTargetAngle(45);
//        m3->gotoTargetAngle(35);  
//        m4->gotoTargetAngle(40);
//        m4->gotoTargetAngle(60);
//        m3->gotoTargetAngle(90);  
//     }
//
//    
//    if (motorStr.compareTo("vial1")==0)
//     { 
//        //m1->gotoTargetAngle(67);
//        m2->gotoTargetAngle(45);
//        m3->gotoTargetAngle(35);  
//        m4->gotoTargetAngle(40);
//        delay(1000);
//        m4->gotoTargetAngle(60);
//        m3->gotoTargetAngle(90);
//     }
//    if (motorStr.compareTo("vial2")==0)
//     { 
//       // m1->gotoTargetAngle(70);
//        m2->gotoTargetAngle(110);
//        m3->gotoTargetAngle(0);  
//        m4->gotoTargetAngle(40);
//        delay(500);
//        m4->gotoTargetAngle(60);
//        m3->gotoTargetAngle(90);
//      }
       if (motorStr.compareTo("test")==0)
         { 
            m1->gotoTargetAngle(90);
            m2->gotoTargetAngle(90);
            m3->gotoTargetAngle(90);
            m2->gotoTargetAngle(0);
            m3->gotoTargetAngle(180);
            m3->gotoTargetAngle(90);
            m2->gotoTargetAngle(90);
            m4->gotoTargetAngle(degree);  
         }
//          
     }
   }
 



