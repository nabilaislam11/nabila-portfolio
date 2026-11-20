# Advanced Fire and Smoke Detection System

**Course project:** CSE360  
**Focus:** Fire and smoke detection, alarms, Arduino-based hardware integration

An academic embedded-systems project addressing fire and smoke detection through a sensing and warning workflow. The group project is documented through the CSE360 report and supporting Arduino project archives.

## Academic project materials

- [Original CSE360 project repository](https://github.com/Khandaker-Atik/CSE360)
- [CSE360 Project Report — Group 5 (PDF)](materials/CSE360%20Project%20Report%20-%20Group%205.pdf)
- [Arduino fire/smoke system sketch](arduino/code.ino)
- [Arduino serial prototype sketch](arduino/B_proto.ino)
- [Original Project V1 archive](materials/Project%20V1.zip)
- [Arduino LCD library archive](https://github.com/Khandaker-Atik/CSE360/blob/main/LiquidCrystal_I2C.zip)
- [Project overview on the portfolio website](index.html)

## System design

The Arduino source configures a flame detector on digital input 6 and smoke sensor input on analog A0. It includes a buzzer on pin 13, red and green indicator LEDs on pins 3 and 4, a 16×2 I²C LCD interface, and serial communication. The sketches implement the detection and alert workflow described by the course project.

The [project report](materials/CSE360%20Project%20Report%20-%20Group%205.pdf), [Arduino source](arduino/code.ino), and [original source archive](materials/Project%20V1.zip) are included for direct inspection.

## Related software work

[PyroWatch](../03-pyrowatch/README.md) is a separate Python/Flask image-analysis application exploring fire-and-smoke computer-vision workflows.
