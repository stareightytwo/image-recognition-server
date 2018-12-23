import time

from flask import (
    Flask,
    render_template,
    Response,
    jsonify,
    request
)

# Using the config settings decide to use opencv or picamera
from .configs import config
if config.USE_PICAMERA:
    from .pi_camera import Camera
else:
    from .opencv_camera import Camera


# Functions for getting camera frames
stop = False
frame_sleep = config.FRAME_SLEEP
def gen_image(camera):
    frame = camera.get_frame()
    yield frame


def gen(camera):
    """Video streaming generator function."""
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
            b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

        if not stop:
            time.sleep(frame_sleep)
        else:
            break


def add_app_routes(app):
    """Different routes for the flask app."""

    # Routes for demo pages to visit with a web browser
    @app.route('/')
    def index():
        return render_template('index.html')

    @app.route('/video_stream_demo')
    def video_stream_demo():
        """Video streaming demo page."""
        return render_template('video_stream_demo.html')

    @app.route('/image_capture_demo')
    def image_capture_demo():
        """Image capture demo page."""
        return render_template('image_capture_demo.html')



    # Routes to use to use for programmatic connectivity
    @app.route('/video_feed')
    def video_feed():
        """Video streaming route."""
        return Response(gen(Camera()),
                        mimetype='multipart/x-mixed-replace; boundary=frame')

    @app.route('/image')
    def image():
        """Image capture route."""
        return Response(gen_image(Camera()),
                        mimetype='image/jpeg')

    # TODO: Probably makes more sense to have a POST url 
    # so it'll be easier to set multiple settings
    @app.route('/settings')
    def settings():
        """Settings route"""
        stop_req = request.args.get('stop')
        frame_sleep_req = request.args.get('frame_sleep')

        global stop
        if stop_req == '1':
            stop = True
        elif stop_req == '0':
            stop = False

        global frame_sleep
        if frame_sleep_req:
            frame_sleep = int(frame_sleep_req)

        return jsonify({'message': 'Set settings: {}'.format(request.args)})


    return app
