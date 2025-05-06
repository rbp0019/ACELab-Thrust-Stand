#include <HX711_ADC.h>
#if defined(ESP8266) || defined(ESP32) || defined(AVR)
#include <EEPROM.h>
#endif
#include <Servo.h>

Servo esc;

// Pins
const int HX711_dout_1 = 4, HX711_sck_1 = 5;
const int HX711_dout_2 = 6, HX711_sck_2 = 7;
const int HX711_dout_3 = 8, HX711_sck_3 = 9;
const int RPM_Sensor = 2;  

// HX711 Constructor
HX711_ADC LoadCell_1(HX711_dout_1, HX711_sck_1);
HX711_ADC LoadCell_2(HX711_dout_2, HX711_sck_2);
HX711_ADC LoadCell_3(HX711_dout_3, HX711_sck_3);

// RPM variables
volatile unsigned long pulseCount = 0;
unsigned long lastRPMCalcTime = 0;
float rpm = 0.0;
const int pulsesPerRevolution = 1;  // Adjust based on your sensor
const unsigned long rpmInterval = 1000;  // Calculate RPM every 1 second

unsigned long t = 0;
int throttle;
unsigned long Current_Time;
bool loggingEnabled = false;
unsigned long startLoggingTime = 0;

// Interrupt handler for RPM sensor
void countPulse() {
    pulseCount++;
}

void setup() {
    Serial.begin(57600);
    Serial.println("Starting...");

    // RPM sensor setup
    pinMode(RPM_Sensor, INPUT);
    attachInterrupt(digitalPinToInterrupt(RPM_Sensor), countPulse, FALLING);  // Adjust FALLING/RISING based on your sensor

    // Load cell calibration values. ------> CHANGE IF LOAD CELLS ARE CHANGED FOR CALIBRATION
    float calibrationValue_1 = 109.56;
    float calibrationValue_2 = 109.56;
    float calibrationValue_3 = 109.56;

    LoadCell_1.begin();
    LoadCell_2.begin();
    LoadCell_3.begin();

    unsigned long stabilizingtime = 2000;
    boolean _tare = true;
    byte loadcell_1_rdy = 0, loadcell_2_rdy = 0, loadcell_3_rdy = 0;

    while ((loadcell_1_rdy + loadcell_2_rdy + loadcell_3_rdy) < 2) {
        if (!loadcell_1_rdy) loadcell_1_rdy = LoadCell_1.startMultiple(stabilizingtime, _tare);
        if (!loadcell_2_rdy) loadcell_2_rdy = LoadCell_2.startMultiple(stabilizingtime, _tare);
        if (!loadcell_3_rdy) loadcell_3_rdy = LoadCell_3.startMultiple(stabilizingtime, _tare);
    }

    LoadCell_1.setCalFactor(calibrationValue_1);
    LoadCell_2.setCalFactor(calibrationValue_2);
    LoadCell_3.setCalFactor(calibrationValue_3);
    Serial.println("Startup complete");

    esc.attach(11); // ---------------> ESC MUST BE PLUGGED INTO DIGITAL PIN #11
    throttle = 800;
    esc.writeMicroseconds(throttle);
    delay(2000);
}

void calculateRPM() {
    unsigned long currentTime = millis();
    if (currentTime - lastRPMCalcTime >= rpmInterval) {
        noInterrupts();  // Disable interrupts while calculating
        unsigned long pulses = pulseCount;
        pulseCount = 0;  // Reset counter
        interrupts();    // Re-enable interrupts

        float timeElapsed = (currentTime - lastRPMCalcTime) / 1000.0;  // Convert to seconds
        rpm = (pulses * 60.0) / (timeElapsed * pulsesPerRevolution);
        lastRPMCalcTime = currentTime;
    }
}

void loop() {
    Current_Time = millis();
    static boolean newDataReady = false;

    // Update RPM calculation
    calculateRPM();

    // Check for new data from load cells
    if (LoadCell_1.update()) newDataReady = true;
    LoadCell_2.update();
    LoadCell_3.update();

    // Read and print values if logging is enabled
    if (newDataReady && loggingEnabled) {
        if (millis() > t) {
            float a = LoadCell_1.getData();
            float b = LoadCell_2.getData();
            float c = LoadCell_3.getData();

            // Torque Calculations
            float Torque_add = abs(a) + abs(c);                
            float Torque = Torque_add * 9.81 * 0.03 / 1000;    
            float Thrust_kg = b / 1000;

            unsigned long elapsedTime = Current_Time - startLoggingTime;

            // Send data as CSV format with RPM added
            Serial.print(elapsedTime);     // Elapsed time (ms)
            Serial.print(",");
            Serial.print(Thrust_kg, 4);    // Thrust (kg)
            Serial.print(",");
            Serial.print(Torque, 4);       // Torque (Nm)
            Serial.print(",");
            Serial.print(throttle);        // Throttle value
            Serial.print(",");
            Serial.print(rpm, 1);          // RPM
            Serial.print(",");
            Serial.print(a, 4);           // Torque Load cell (Left, beind motor)
            Serial.print(",");
            Serial.println(c, 4);         // Torque Load cell (Right, behind motor)

            newDataReady = false;
            t = millis();
        }
    }

    // Handle incoming serial commands
    if (Serial.available() > 0) {
        String command = Serial.readStringUntil('\n');

        if (command.startsWith("PWM:")) {
            int newThrottle = command.substring(4).toInt();
            throttle = constrain(newThrottle, 0, 2000);
            esc.writeMicroseconds(throttle);
            Serial.print("Throttle Set: ");
            Serial.println(throttle);
        } 
        else if (command == "TARE") {
            LoadCell_1.tareNoDelay();
            LoadCell_2.tareNoDelay();
            LoadCell_3.tareNoDelay();
            Serial.println("Tare Command Received");
        } 
        else if (command == "START") {
            loggingEnabled = true;
            startLoggingTime = millis();
            Serial.println("Logging Started");
        } 
        else if (command == "STOP") {
            loggingEnabled = false;
            Serial.println("Logging Stopped");
        }
    }
}
