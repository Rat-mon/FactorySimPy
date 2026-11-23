# Intelligent-factory
31-segment Communication monitoring using FactirySimPy
Project Overview
This project is a Python based system for establishing communication between 1 spinal segments and modeling the processing of communication-check jobs using FactorySimPy

The system has four main parts:\
Segment logic: What is going to be done
Device interface/communication analysis: How the info is shared
Operator console: Who the info is shared to and seen by
Factory simulation: The simulation that is run for communication checks

Project Files
main.py: The entry point
device_readings.csv: Device input 
factory_simulation.py: The model
operator_console.py: The contact/information transfer
requirements.txt: Python dependencies
segment_logic.py: Generated segment results
test.py: automated logic tests

Setup
Install Python, then run: 
python -m pip install -r requirements.txt
Run the Application
python main.py
Run the Tests
python -m unittest test.py

Development Status
This is still an early prototype using these readings. The physical device has never been connected and will still require integration and validation.

Disclaimer:
The software is for a demonstration and is no way an actual medical diagnostic system

AI Generated Content Disclosure
AI was used is some parts of this project, mainly to fix errors in main.py and the .csv file specifically on how to delete the old one and replace it with a new one.
