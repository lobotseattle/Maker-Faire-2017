/*
 * Adafruit motordriver shield library
 * 
 */
#include <Wire.h>
#include <Adafruit_MotorShield.h>
#include "utility/Adafruit_MS_PWMServoDriver.h"
/**
 * @file motor_driver.h
 * @brief Motor device driver definition for the Edge ARM robot.
 * @author 
 */


//Srikanth Ranganathan
class ArmMotor
{
  public:
       /**
       * @brief Constructor
       * @param Motor number and the potentiometer pin
       */
      ArmMotor();
      ArmMotor (Adafruit_DCMotor *motor, int potPin);
      void setMinAngle(int degrees);
      void setMaxAngle(int degrees);
  
      /**
       * @brief Change the speed of the motor.
       * @param speed The new speed of the motor.
       *  Valid values are between 0 and 255. 
       */
      void setSpeed(int speed);

      /**
       * @brief Return the current speed of the motor.
       * @return The current speed of the motor with range -255 to 255.
       */
      int getSpeed();


      /**
       * @brief Return the current speed of the motor.
       * @return The current speed of the motor with range -255 to 255.
       */
      void setTargetAngle(int degrees);

      int gotoTargetAngle(int degrees);

      /**
       * @brief This will cailbtrate the potentiometer so that it can be used for slope calculations
       * @param x1 voltage 1, y1 is the degree at voltage 1, x2 is voltage 2 and y2 is degrees at voltage 2
       *  Valid values are between 0 and 255. 
       */
       // Me
      void calibratePotentiometer(float voltage1, float degree1, float voltage2, float degree2); 

      int getCurrentAngle();

      void printObject();

      void setThreshold(int degrees);

  private:
  //Srikanth Ranganathan
    void moveMotorToTarget(int voltageLevel, int upperLimit, int lowerLimit) ;
    int getVoltageFromDegree(int degree) ;
  
    int motorNum=1;
    int potPin=0;
    int motorSpeed=0;
    int targetAngle = 90;
    int currentAngle = 90;
    float yIntercept = 0;
    float slope = 0;
    boolean targetReached = false;
    int minAngle=45;
    int maxAngle=135;
    int thresholdInDegrees=2;
    Adafruit_DCMotor *motor;     
      
  };
