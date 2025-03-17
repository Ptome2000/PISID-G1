import json
import re
import paho.mqtt.client as mqtt
import pymongo
from pymongo import MongoClient
from datetime import datetime
import os

# Connect to MongoDB
client = MongoClient("localhost", 27017)

# Create a "logs" directory inside the project if it doesn't exist
log_dir = "logs"
if not os.path.exists(log_dir):
    os.makedirs(log_dir)

# Generate a log filename based on the current date and time (e.g., "logs/2025-03-17_14-45.txt")
log_filename = f"{log_dir}/{datetime.now().strftime('%Y-%m-%d_%H-%M')}.txt"

# Ensure the log file is created at the start of execution
with open(log_filename, "w") as log_file:
    log_file.write(f"Log file created at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

def log_error(error_message):
    """Logs errors to a text file with a timestamp"""
    with open(log_filename, "a") as log_file:
        timestamp = datetime.now().strftime("[%H:%M:%S]")  # Get current time
        log_file.write(f"{timestamp} {error_message}\n")  # Write the error message

def insertData(collectionName, message):
    """Processes and inserts MQTT message data into MongoDB"""
    db = client["labirinto_pisid"]  # Select database
    collection = db[collectionName]  # Select collection based on the topic

    try:
        # Decode the message from bytes to string and remove surrounding {}
        decoded_message = message.decode("utf-8").strip("{}")
        payload = {}  # Dictionary to store processed key-value pairs

        for field in decoded_message.split(", "):  # Split key-value pairs
            key, value = field.split(":", 1)  # Split key and value
            key = key.strip()  # Remove spaces
            value = value.strip()  # Remove spaces

            # Try to determine the correct data type for the value
            try:
                if value.startswith('"') and value.endswith('"'):
                    value = value.strip('"')  # Remove quotes (string)
                elif "." in value:
                    value = float(value)  # Convert to float (if it contains a dot)
                else:
                    value = int(value)  # Convert to integer

            except ValueError as e:
                # Handle conversion errors (e.g., if "abc" is provided instead of a number)
                error_msg = f"Error converting '{value}': {e}"
                print(error_msg)
                log_error(error_msg)  # Log the error
                continue  # Skip this field and move to the next one

            payload[key] = value  # Add to the dictionary

        # Try inserting the processed data into MongoDB
        try:
            res = collection.insert_one(payload)  # Insert data
            print("Inserted:", res)
        except pymongo.errors.PyMongoError as e:
            # Handle database errors (e.g., duplicate key, connection issues)
            error_msg = f"Error inserting into MongoDB: {e}"
            print(error_msg)
            log_error(error_msg)  # Log the error

    except Exception as e:
        # Handle any unexpected errors in the function
        error_msg = f"Error processing MQTT message: {e}"
        print(error_msg)
        log_error(error_msg)  # Log the error

# MQTT callback function: triggered when connected to the broker
def on_connect(client, userdata, flags, reason_code, properties):
    print(f"Connected with result code {reason_code}")
    
    # Subscribe to MQTT topics when connected
    client.subscribe("pisid_mazesound_1")
    client.subscribe("pisid_mazemov_1")

# MQTT callback function: triggered when a message is received
def on_message(client, userdata, msg):
    print(msg.topic + " " + str(msg.payload))  # Print received message
    
    # Process the message and insert it into the correct MongoDB collection
    if msg.topic == "pisid_mazemov_1":
        insertData("movimento", msg.payload)
    if msg.topic == "pisid_mazesound_1":
        insertData("ruido", msg.payload)

# Create MQTT client
mqttc = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)

# Assign callback functions
mqttc.on_connect = on_connect
mqttc.on_message = on_message

# Connect to the MQTT broker
mqttc.connect("broker.mqtt-dashboard.com", 1883, 60)

# Start an infinite loop to keep the script running and listening for messages
mqttc.loop_forever()
