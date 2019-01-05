import time
from io import BytesIO

import cv2
import requests
import numpy as np
from PIL import Image
from darkflow.net.build import TFNet

from server.utils import grab_img, obj_exists_in_img
from server.config.app import interested_objects

options = {
	'model': './setup/darkflow/cfg/tiny-yolo-voc.cfg',
	'load': './setup/darkflow/bin/tiny-yolo-voc.weights',
	'threshold': 0.1
}

tfnet = TFNet(options)

while True:

	img = grab_img()
	tfnet_result = tfnet.return_predict(img)

	for obj in interested_objects:
		if obj_exists_in_img(tfnet_result, obj):
			print('Found object "{}" in image'.format(obj))

	time.sleep(1)