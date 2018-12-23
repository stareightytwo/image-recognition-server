# camera-server

\*Tested using python 3.6.7

## Setup

1. Install python virtualenv (`pip install virtualenv`) then run `make init-venv` to initialize a python virtual environment.

2. Activate the virtual env:

        `source venv/bin/activate`

3. If running the server using a webcam install opencv:

        `pip install opencv-python==3.4.4.19`

    or if using a raspberry pi with picamera:

        `pip install picamera==1.13`

## Run

Use the runner `run.sh` to start the camera server.

Navigate to `http://localhost:8000/` in a browser.

## Settings

Update the values in the [config.py](server/configs/config.py) file directly or as environment variables. When the app is running the `/settings` url can be used to change settings.

parameters:

    stop: Stops a direct video feed (like from the video streaming page)
    frame_sleep: Sleeps the app for n number of seconds before getting another frame.

example:
    
    curl "http://localhost:8000/settings?stop=0&frame_sleep=1"