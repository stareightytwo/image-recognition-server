import time
from io import BytesIO

import cv2
import requests
import numpy as np
from PIL import Image
from darkflow.net.build import TFNet

from utils import grab_img, obj_exists_in_img
from config.app import interested_objects

options = {
	'model': 'cfg/tiny-yolo-voc.cfg',
	'load': 'bin/tiny-yolo-voc.weights',
	'threshold': 0.1
}

tfnet = TFNet(options)

while True:
	img = grab_img()
	tfnet_result = tfnet.return_predict(img)

	for obj in interested_objects:
		if obj_exists_in_img(tfnet_result, obj):
			pass

	time.sleep(5)