# Arduino Thrust Stand Project

This project is an Arduino-based thrust stand for testing brushless motor performance, measuring thrust, torque, RPM, voltage, and current. It’s designed for drone development in the ACE Lab at Auburn Univerisity, under the guidance of Dr. Eshan Taheri.

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
  - HX711 load cell amplifier with 10kg load cell
  - Holybro PM06 power sensor (for voltage/current)
  - Optical RPM sensor
  - Brushless motor with ESC and propeller
  - Power supply (e.g., LiPo battery or bench supply)
- **Wiring**:
  - HX711: Connect to Arduino digital pins.
  - PM06: Connect to analog pins A3 (voltage), A4 (current).
  - RPM sensor: Connect to digital pin 2.
  - ESC: Connect to digital pin 11 (PWM via Servo library).
- **Schematic**: ![Thrust Stand Setup](docs/schematic.png)
- **Safety**:
  - Secure the motor and propeller to avoid vibration or detachment.
  - Use a stable power supply to prevent ESC damage.
  - Keep clear of the propeller during testing.

## License
This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.
