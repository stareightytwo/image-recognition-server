import datetime
import os
from io import BytesIO
from os import listdir
from os.path import isfile, join
import logging
import sys
logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

import numpy as np
import requests
from PIL import Image, ImageDraw
import cv2

from server.config import app


class Imager():
    """
    Handles image fetching/storing/other prep for interacting with the
    predict.Predictor class
    """
    
    @staticmethod
    def get_image_from_camera_server(url=''):
        """
        Get a cv2 image from a camera server.
        Returns a tuple of the request object and the cv2 image,
        (requests.models.Response, numpy.ndarray)
        """

        if not url:
            url = config.camera_server_image_url

        r = requests.get(url)
        detection_image = Image.open(BytesIO(r.content))
        detection_image_cv2 = cv2.cvtColor(np.array(detection_image), cv2.COLOR_RGB2BGR)

        return detection_image, detection_image_cv2

    @staticmethod
    def get_image_camera_server(url=''):
        """
        Get a cv2 image from a camera server.
        Returns the cv2 image, numpy.ndarray.
        """

        r = Imager.get_request_from_image_camera_server(config.camera_server_image_url)
        return Imager.get_image_from_request(r)
        
    @staticmethod
    def get_request_from_image_camera_server(url=''):
        """
        Requests an image from the camera server using the url.
        Returns the request object, requests.models.Response.
        """

        if not url:
            url = config.camera_server_image_url

        return requests.get(url)

    @staticmethod
    def get_image_from_request(r):
        """
        Get the cv2 image that was sent as part of a response from
        the camera server.
        Return the cv2 image. numpy.ndarray
        """
        detection_image = Image.open(BytesIO(r.content))
        return cv2.cvtColor(np.array(detection_image), cv2.COLOR_RGB2BGR)

    @staticmethod
    def get_file_strings_from_local(local_path=''):
        """
        Gets a list of files names from a local path.
        Returns a list of string file names.
        """
        if not local_path:
            local_path = config.local_image_path
        
        files = [f for f in listdir(local_path) if isfile(join(local_path, f))]
        logging.debug('local files: {}'.format(files))
    
        return files

    @staticmethod
    def get_image_from_local(local_image_path):
        """
        Get an image from a local directory.
        Returns a cv2 image, numpy.ndarray
        """

        detection_image = Image.open(local_image_path).convert('RGB')
        return cv2.cvtColor(np.array(detection_image), cv2.COLOR_RGB2BGR)

    @staticmethod
    def draw_boxes_and_labels(detections, detection_image_cv2):
        """
        Draws boxes and labels the different detections for a given cv2 image.
        Returns the drawn on cv2 image, numpy.ndarray
        """

        logging.debug('drawing boxes and labels')
        for detection in detections:
            detection_image_cv2 = Imager.draw_box(detection, detection_image_cv2)
            detection_image_cv2 = Imager.draw_label(detection, detection_image_cv2)

        return detection_image_cv2
        
    @staticmethod
    def draw_box(detection, detection_image_cv2):
        """
        Draws a box on the given cv2 image using the specified
        points in the given detection.
        Returns the drawn on cv2 image, numpy.ndarray
        """

        logging.debug('drawing box for {}'.format(detection['label'].upper()))
        scale = 2
        color = (0, 0, 255)
        cv2.rectangle(
            detection_image_cv2,
            (detection['topleft']['x'], detection['topleft']['y']),
            (detection['bottomright']['x'], detection['bottomright']['y']),
            color,
            scale
        ) 

        return detection_image_cv2

    @staticmethod
    def draw_label(detection, detection_image_cv2):
        """
        Draws a label on the given cv2 image using the specified
        lable in the given detection.
        Returns the drawn on cv2 image, numpy.ndarray
        """

        logging.debug('drawing label for {}'.format(detection['label'].upper()))
        scale = 2
        font_scale = 1
        color = (0, 0, 255)
        cv2.putText(
            detection_image_cv2,
            detection['label'].upper(),
            (detection['topleft']['x'], detection['topleft']['y'] - 5),
            cv2.FONT_HERSHEY_COMPLEX_SMALL,
            font_scale,
            color,
            scale
        )

        return detection_image_cv2

    @staticmethod
    def save_image(base_path, detection_image_cv2, use_date=False):
        """
        Saves an image based on some supplied filepath options.
        """

        logging.debug('save_image')
        if use_date:
            now = datetime.datetime.now()
            save_path = '{}/{}/{}/{}'.format(base_path, now.year, now.month, now.day)

        else:
            save_path = '{}'.format(base_path)

        try:
            path, dirs, files = next(os.walk(save_path))

        # Path not created yet so make it
        except StopIteration:
            os.makedirs(save_path)
    
        path, dirs, files = next(os.walk(save_path))
        file_count = len(files)
        image_filename = '{}/{}.jpg'.format(save_path, file_count)
        logging.debug('saving image to {}'.format(image_filename))
        cv2.imwrite(image_filename, detection_image_cv2)