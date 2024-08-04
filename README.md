# Dock Visibility Controller

## About
A Python utility for macOS that automatically adjusts Dock visibility based on external display connection and laptop lid state. Designed to run in the background as a service.

## Installation
- Requires macOS and Python 3.9>= (tested on Python 3.12).
- Clone or download from GitHub.
- Run `pip install -r requirements.txt` in the project directory.

## Usage
To ensure the utility runs continuously in the background, it should be started as a background process or set up as a service.

### Running in Background
`nohup python main.py [-i INTERVAL] [-l] &`
- `-i INTERVAL`: Check interval in seconds (default in script).
- `-l`: Show Dock only when the laptop's lid is closed.

### Setting Up as a Service
For persistent usage, consider setting up the script as a system service using `launchd` or another service manager.

## License
See LICENSE file.

## Future??
I might make macOS mac if won't be lazy