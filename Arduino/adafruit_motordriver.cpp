/**
 * @file adafruit_motor_driver.h
 * @brief Motor device driver for the Adafruit motor shield.
 * @author 
 */

#include "motordriver.h"


ArmMotor::ArmMotor (Adafruit_DCMotor *motor, int potPin)
{
    this->motor = motor;
    this->potPin = potPin;
    Serial.print("From constructor ");
    Serial.println();
}

void ArmMotor::setSpeed(int speed)
{
    this->motorSpeed = speed;
}

int ArmMotor::getSpeed()
{
    return this->motorSpeed;
}

void ArmMotor::setMinAngle (int degrees)
{
  this->minAngle = degrees;
}

void ArmMotor::setMaxAngle (int degrees)
{
  this->maxAngle = degrees;
}

void ArmMotor::setTargetAngle (int degrees)
{
  if ( (degrees >= this->minAngle) & (degrees <= this->maxAngle))
  {
    this->targetAngle = degrees;
  }
}

int ArmMotor::getCurrentAngle()
{
  return this->currentAngle;
}
//Algorithm
/* Formula to calculate: Srikanth Ranganathan
 * Implementation: Me 
 */

void ArmMotor::calibratePotentiometer(float voltage1, float degree1, float voltage2, float degree2)
{
  Serial.println(voltage1); 
   Serial.println(degree1);  
     Serial.println(voltage2); 
       Serial.println(degree2); 
  // calculate slope and y intercept
  this->slope = (voltage2-voltage1)/(degree2-degree1);

  //y=ax+b
  //y1=x1*slope + b
  // b = y1 - (x1*slope)
  this->yIntercept = voltage1 - (this->slope*degree1);
  Serial.println("Slope is"); 
  Serial.println(this->slope);
  Serial.println("Yintercept is ");
  Serial.println(this->yIntercept);
}

int ArmMotor::gotoTargetAngle(int degree)
{
  int angleToUse = degree;
  if (angleToUse <= minAngle) angleToUse = minAngle;
  if (angleToUse >= maxAngle) angleToUse = maxAngle;
  // calculate the voltage from the degrees and call moveMotorToTarget
  int targetVoltageLevel = getVoltageFromDegree(angleToUse);
  int upperLimit = getVoltageFromDegree(angleToUse + this->thresholdInDegrees);
  int lowerLimit = getVoltageFromDegree(angleToUse - this->thresholdInDegrees);
  this->moveMotorToTarget(targetVoltageLevel,upperLimit, lowerLimit);
  return 1;
}

int ArmMotor::getVoltageFromDegree(int degree)
{
    Serial.println();
    Serial.print("Input degree is ");
    Serial.println(degree);
    int voltage = this->slope * degree + this->yIntercept ;
    Serial.print("voltage is ");
    Serial.println(voltage);
    Serial.println("");
    return voltage;
}

void ArmMotor::moveMotorToTarget(int voltageLevel, int upperLimit,int lowerLimit) 
{
  targetReached = false;
  this->motor->setSpeed(motorSpeed);
  Serial.print("Motor num = "); Serial.print(motorNum);Serial.println();
  boolean mObject = false;
  if (this->motor) mObject = true;
  Serial.print("Motor Object = "); Serial.print(mObject); Serial.println();
  printObject();
  int val=0;
  int lowerBand = lowerLimit;
  int upperBand = upperLimit;
  if (upperLimit <= lowerLimit)
  {
    lowerBand = upperBand;
    upperBand = lowerLimit;
  }
  while (targetReached == false)
  {
    val = analogRead(potPin);
    Serial.print(val);Serial.println();
  
    if (val >= lowerBand & val <= upperBand )
//    if (val== voltageLevel)
    {
      this->motor->run(BRAKE);
      this->motor->run(RELEASE);
      this->motor->setSpeed(0);
      Serial.println("Done");
      targetReached = true;
    }
    if (val > voltageLevel)
    {
        this->motor->run(BACKWARD);
        Serial.println("Going backward");
    }
    else
    {
        this->motor->run(FORWARD);
        Serial.println("Going forward");
    }
  }
}

void ArmMotor::setThreshold(int degrees)
{
  this->thresholdInDegrees<-degrees;
}

void ArmMotor::printObject()
{
    Serial.print("MotorNum "); Serial.print(this->motorNum);
    Serial.print(" potPin "); Serial.print(this->potPin);
    Serial.print(" MotorSpeed "); Serial.print(this->motorSpeed);
    Serial.print(" TargetAngle ");Serial.print( this->targetAngle);
    Serial.print(" CurrentAngle "); Serial.print( this->currentAngle);
    Serial.print(" yIntercept "); Serial.print(this->yIntercept);
    Serial.print(" slope "); Serial.print(this->slope);
    Serial.print(" minAngle "); Serial.print(this->minAngle);
    Serial.print(" maxAngle ");Serial.print( this->maxAngle);  
    Serial.println();
}

