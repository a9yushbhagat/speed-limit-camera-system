# Speed Limit Camera System

A Python-based mathematical modelling project that uses two camera checkpoints and timestamps to estimate a vehicle's average speed and identify vehicles travelling above a speed limit.

## Project Overview

The system records a vehicle at two known camera locations and uses the distance between the cameras together with the time difference between the two observations.

The average speed is calculated using:

**Average Speed = Distance / Time**

The project connects this calculation to the Mean Value Theorem. If a vehicle's average speed over an interval exceeds the speed limit, then at some point during that interval its instantaneous speed must have reached or exceeded that average speed.

## Features

- Stores camera locations and vehicle readings
- Matches vehicle readings using license plates
- Calculates average vehicle speed
- Detects vehicles travelling above a chosen speed limit
- Writes speeding results to a ticket output file
- Includes an experimental camera and license-plate-reading extension

## Main Files

- `core.py` — main mathematical and vehicle-speed logic
- `plate_reader.py` — reads license plate text from images
- `server.py` — connects camera input with the speed-detection system
- `camera_phone.html` — simple phone-camera interface
- `tickets.txt` — example speeding output

## Core Mathematics

Suppose two cameras are separated by a known distance.

If a vehicle passes the first camera at time `t1` and the second camera at time `t2`:

**Travel Time = t2 - t1**

**Average Speed = Distance Between Cameras / Travel Time**

The program converts the travel time from seconds into hours so that the final speed is measured in kilometres per hour.

## Example

Suppose the cameras are **10 km apart** and a vehicle travels between them in **240 seconds**.

240 seconds is approximately **0.0667 hours**.

Therefore:

**Average Speed = 10 / 0.0667 ≈ 150 km/h**

If the speed limit is **100 km/h**, the program identifies the vehicle as speeding.

## Technologies and Concepts

- Python
- Object-oriented programming
- Mathematical modelling
- File input/output
- Mean Value Theorem
- OpenCV
- Tesseract OCR
- HTML

## Example Output

When a vehicle is detected travelling above the selected speed limit, the program can write the result to `tickets.txt`.

Example:

`ABC123,150.0`

This means the vehicle with plate `ABC123` was calculated to be travelling at approximately **150 km/h**.

## Status

**Completed**

The core mathematical and Python implementation calculates vehicle speeds from camera readings and detects vehicles exceeding a specified speed limit. Camera input and OCR functionality were explored as an additional extension.
