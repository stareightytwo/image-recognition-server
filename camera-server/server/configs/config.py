import os

USE_PICAMERA = int(os.environ.get('USE_PICAMERA', 0))
FRAME_SLEEP = float(os.getenv('FRAME_SLEEP', 0))