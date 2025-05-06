# Arduino Thrust Stand Project

This project is an Arduino-based thrust stand for testing brushless motor performance, measuring thrust, torque, RPM, voltage, and current. It’s designed for drone or RC enthusiasts to optimize motor and propeller combinations.

## Software
- **Code Overview**: `ThrustStand.ino` controls the thrust stand, reading data from an HX711 load cell (thrust), Holybro PM06 power sensor (voltage/current), and an RPM sensor. It sends data via serial to a Python GUI for logging and visualization.
- **Dependencies**:
  - Arduino libraries: `HX711.h`, `Servo.h` (install via Arduino IDE Library Manager).
  - Python libraries: `pyserial`, `matplotlib` (install via `pip install pyserial matplotlib`).
- **Setup**:
  1. Open `ThrustStand.ino` in Arduino IDE (version 2.0+ recommended).
  2. Connect Arduino (e.g., Uno) to your computer.
  3. Upload the sketch to your Arduino.
  4. Run `plot_data.py` on your computer to visualize real-time data.
- **Usage**:
  - Control ESC via PWM (set in Arduino code or Python GUI).
  - View thrust, torque, RPM, voltage, and current on the Python GUI or Serial Monitor (9600 baud).
  - Log data to CSV files for analysis (see `data/sample_data.csv`).
- **Python GUI**: `plot_data.py` plots Thrust vs. PWM, Torque vs. PWM, and RPM vs. PWM in real-time. Run with `python plot_data.py`.

## Hardware
- **Components**:
  - Arduino Uno (or compatible board)
  - HX711 load cell amplifier with 5kg or 10kg load cell
  - Holybro PM06 power sensor (for voltage/current)
  - Optical or hall-effect RPM sensor
  - Brushless motor with ESC and propeller
  - Power supply (e.g., LiPo battery or bench supply)
- **Wiring**:
  - HX711: Connect to Arduino pins A0 (CLK), A1 (DOUT).
  - PM06: Connect to analog pins A3 (voltage), A4 (current).
  - RPM sensor: Connect to digital pin 2 (interrupt).
  - ESC: Connect to digital pin 9 (PWM via Servo library).
- **Schematic**: ![Thrust Stand Setup](docs/schematic.png)
- **Safety**:
  - Secure the motor and propeller to avoid vibration or detachment.
  - Use a stable power supply to prevent ESC damage.
  - Keep clear of the propeller during testing.

## Future Development
- **Planned Improvements**:
  - Implement Kalman filtering in Arduino code to smooth thrust and RPM data (early tests in `kalman_test.ino`).
  - Add Wi-Fi module (e.g., ESP8266) for wireless data logging.
  - Support multiple motor sizes with adjustable mounts.
- **Ideas**:
  - Integrate with a mobile app for remote control and data display.
  - Add torque sensor calibration for higher accuracy.
  - Develop a 3D-printed enclosure for portability.
- **Contributing**:
  - Open an Issue to report bugs or suggest features.
  - Fork the repository and submit pull requests for code improvements.

## License
This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.
