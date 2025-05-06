import serial
import time
import threading
import csv
import tkinter as tk
from tkinter import messagebox
import pandas as pd
import matplotlib.pyplot as plt

# Set up serial connection
port = "/dev/tty.usbmodem101"  # ------------> CHANGE BASED ON PERSONAL COMPUTER PORT
baudrate = 57600 # BE SURE MATCHES ARDUINO CODE BAUD RATE
ser = serial.Serial(port, baudrate, timeout=2)
time.sleep(2)  # Allow Arduino to reset

# Create/open CSV file
filename = "thrust_data.csv" # FEEL FREE TO CHANGE NAME OF FILE TO PREFERENCE
file = open(filename, "w", newline="")
csv_writer = csv.writer(file)
csv_writer.writerow(["Time(ms)", "Thrust (kg)", "Torque (N*m)", "PWM", "RPM", "Cell2", "Cell3"])

# Lock for serial access
serial_lock = threading.Lock()
logging_enabled = False
start_time = None  # Variable to track the time when logging starts
latest_rpm = 0.0  # Store the latest RPM value for continuous display

def send_command(command):
    def _send():
        with serial_lock:
            ser.write((command + "\n").encode())
            time.sleep(0.1)
            response = ser.readline().decode().strip()
            if response:
                print("Arduino:", response)
            else:
                print("⚠️ Warning: No response from Arduino.")

    threading.Thread(target=_send, daemon=True).start()

def read_serial():
    global logging_enabled, start_time, latest_rpm
    while True:
        try:
            with serial_lock:
                data = ser.readline().decode("utf-8", errors="ignore").strip()
            if data:
                if "," in data:
                    values = data.split(",")
                    if len(values) == 7:
                        try:
                            latest_rpm = float(values[4])
                        except ValueError:
                            latest_rpm = 0.0
                        print(f"Current RPM: {latest_rpm:.1f}", end="\r")
                        if logging_enabled:
                            print("\nDATA:", data)
                            current_time_ms = int(values[0])
                            if start_time is None:
                                start_time = current_time_ms
                            elapsed_time = current_time_ms - start_time
                            csv_writer.writerow([elapsed_time] + values[1:])
                            file.flush()
        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f"Error reading serial data: {e}")

def set_pwm():
    try:
        pwm_value = int(pwm_entry.get())
        send_command(f"PWM:{pwm_value}")
    except ValueError:
        messagebox.showerror("Invalid Input", "Enter a valid PWM value.")

def start_logging():
    global logging_enabled, start_time
    logging_enabled = True
    start_time = None
    send_command("START")

def stop_logging():
    global logging_enabled
    logging_enabled = False
    send_command("STOP")

def on_close():
    file.close()
    ser.close()
    root.destroy()

def plot_data():
    # Load CSV data into a pandas DataFrame
    df = pd.read_csv(filename)

    # Convert time column to seconds
    df['Time(s)'] = df['Time(ms)'] / 1000

    # Create a figure with three subplots
    fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(10, 10), sharex=True)

    # First subplot: Thrust vs PWM
    ax1.set_ylabel('Thrust (kg)', color='tab:blue')
    ax1.plot(df['Time(s)'], df['Thrust (kg)'], color='tab:blue', label='Thrust')
    ax1.tick_params(axis='y', labelcolor='tab:blue')
    ax1.grid(True)

    # Add PWM to first subplot (right y-axis)
    ax1_twin = ax1.twinx()
    ax1_twin.set_ylabel('PWM (µs)', color='tab:orange')
    ax1_twin.plot(df['Time(s)'], df['PWM'], color='tab:orange', label='PWM')
    ax1_twin.set_ylim([1000, max(df['PWM']) + 100])
    ax1_twin.tick_params(axis='y', labelcolor='tab:orange')

    # Second subplot: Torque vs PWM
    ax2.set_ylabel('Torque (N*m)', color='tab:red')
    ax2.plot(df['Time(s)'], df['Torque (N*m)'], color='tab:red', label='Torque')
    ax2.tick_params(axis='y', labelcolor='tab:red')
    ax2.grid(True)

    # Add PWM to second subplot (right y-axis)
    ax2_twin = ax2.twinx()
    ax2_twin.set_ylabel('PWM (µs)', color='tab:orange')
    ax2_twin.plot(df['Time(s)'], df['PWM'], color='tab:orange', label='PWM')
    ax2_twin.set_ylim([1000, max(df['PWM']) + 100])
    ax2_twin.tick_params(axis='y', labelcolor='tab:orange')

    # Third subplot: RPM vs PWM
    ax3.set_xlabel('Time (s)')
    ax3.set_ylabel('RPM', color='tab:green')
    ax3.plot(df['Time(s)'], df['RPM'], color='tab:green', label='RPM')
    ax3.tick_params(axis='y', labelcolor='tab:green')
    ax3.grid(True)

    # Add PWM to third subplot (right y-axis)
    ax3_twin = ax3.twinx()
    ax3_twin.set_ylabel('PWM (µs)', color='tab:orange')
    ax3_twin.plot(df['Time(s)'], df['PWM'], color='tab:orange', label='PWM')
    ax3_twin.set_ylim([1000, max(df['PWM']) + 100])
    ax3_twin.tick_params(axis='y', labelcolor='tab:orange')

    # Titles and layout
    ax1.set_title('Thrust vs PWM')
    ax2.set_title('Torque vs PWM')
    ax3.set_title('RPM vs PWM')
    plt.tight_layout()
    plt.show()

# Start a separate thread to read and log serial data
threading.Thread(target=read_serial, daemon=True).start()

# Create GUI window
root = tk.Tk()
root.title("Thrust Stand Control")
root.geometry("400x250")
root.configure(bg="#f0f0f0")

# PWM Entry
pwm_label = tk.Label(root, text="Enter PWM:", font=("Arial", 12), bg="#f0f0f0")
pwm_label.pack(pady=5)
pwm_entry = tk.Entry(root, font=("Arial", 12))
pwm_entry.pack(pady=5)
pwm_button = tk.Button(root, text="Set PWM", font=("Arial", 12), command=set_pwm, bg="#007BFF")
pwm_button.pack(pady=5)

# Logging Buttons
start_button = tk.Button(root, text="Start Logging", font=("Arial", 12), command=start_logging, bg="#28A745")
start_button.pack(pady=5)
stop_button = tk.Button(root, text="Stop Logging", font=("Arial", 12), command=stop_logging, bg="#DC3545")
stop_button.pack(pady=5)

# Plot Button
plot_button = tk.Button(root, text="Plot Data", font=("Arial", 12), command=plot_data, bg="#FFC107", fg="black")
plot_button.pack(pady=5)

# Handle window close
root.protocol("WM_DELETE_WINDOW", on_close)

# Run GUI
root.mainloop()
