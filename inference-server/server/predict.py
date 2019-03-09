import logging
import sys
logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

# from darkflow.net.build import TFNet

from configs import config

from fastai.vision import (
    ImageDataBunch,
    create_cnn,
    # open_image,
    get_transforms,
    models,
    imagenet_stats
)
# import torch
from pathlib import Path
# from io import BytesIO
# import sys
# import uvicorn
# import aiohttp
# import asyncio
# import numpy as np
# import json 


class Predictor():
    """
    Used to get predictions for detected objects in images.
    """

    def __init__(self, model_options={}):

        # if not model_options:
        #     model_options = config.model_options

        # self.model_options = model_options
        # self.tfnet = TFNet(model_options)
        # logging.debug('tfnet initiated with options: {}'.format(model_options))


        path = Path(__file__).parent
        data =  ImageDataBunch.single_from_classes(
            path,
            classes,
            ds_tfms=get_transforms(),
            size=299,
        ).normalize(imagenet_stats)

        self.model = create_cnn(data, models.resnet50)
        self.model.load("/home/scott/developer/git/stareightytwo/image-recognition-server/inference-server/models/resnet50-stage2")

    def set_model_options(self, model_options):
        """Creates a new tfnet model instance using the supplied model_options.

        model_options -> {'model': '<path>', 'load': '<path>', 'threshold': [0.0, 1.0]}
        """
        self.model_options = model_options
        self.tfnet = TFNet(model_options)
        logging.debug('new tfnet model instance created with options: {}'.format(model_options))

    def predict(self, detection_image_cv2):
        """Use the tfnet to predict on an image.
        
        :param detection_image_cv2: cv2 image to get an object detection prediction on
        :type detection_image_cv2: np.array
        """
        prediction = self.tfnet.return_predict(detection_image_cv2)
        logging.debug('predicted: {}'.format(prediction))
        return prediction