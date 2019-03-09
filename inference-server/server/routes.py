import time
import sys
from threading import Thread

from flask import (
    Flask,
    render_template,
    Response,
    jsonify,
    request
)
import cv2

from server.images import Imager
from server.predict import Predictor
from server.configs import config

p = Predictor()


stop_inference_loop = False
def inference_loop():

    global stop_inference_loop
    stop_inference_loop = False
    while not stop_inference_loop:
        
        time_start = time.time()
        
        # Get image from camera server and predict on it
        frame = Imager.get_image_camera_server()
        detections = p.predict(frame)
        print('Made inference in {} seconds.'.format(time.time() - time_start))

        # Draw boxes around detected objects
        frame = Imager.draw_boxes_and_labels(detections, frame)

        # Save image to file system
        Imager.save_image(config.base_image_path, frame, use_date=True)

        # Wait for a bit to get next frame
        print('Sleeping for {} seconds.'.format(config.inference_sleep_time))
        time.sleep(config.inference_sleep_time)
        print('awake')


def single_inference():

    frame = Imager.get_image_camera_server()
    detections = p.predict(frame)
    frame = Imager.draw_boxes_and_labels(detections, frame) 
    bytes_string = cv2.imencode('.jpg', frame)[1].tostring()
    yield bytes_string


def add_app_routes(app):
    """Different routes for the flask app."""

    @app.route('/start_inference_loop')
    def start_inference_loop():
        th = Thread(target=inference_loop)
        th.start()
        return jsonify({'message': 'Started inference loop. Make GET request to /stop_inference_loop to stop.'})

    @app.route('/stop_inference_loop')
    def stop_inference_loop():

        global stop_inference_loop
        stop_inference_loop = True
        return jsonify({'message': 'Stopped inference loop. Make GET request to /start_inference_loop to restart.'})

    @app.route('/image')
    def image():
        """Image capture route."""
        return Response(single_inference(),
                        mimetype='image/jpeg')


    return app