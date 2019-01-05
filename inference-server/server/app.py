import time
from io import BytesIO

import cv2
import requests
import numpy as np
from PIL import Image
from darkflow.net.build import TFNet

from server.utils import grab_img, search_tfnet_result_for_object, draw_bounding_box, create_filename
from server.config.app import interested_objects

options = {
	'model': './setup/darkflow/cfg/tiny-yolo-voc.cfg',
	'load': './setup/darkflow/bin/tiny-yolo-voc.weights',
	'threshold': 0.35
}

tfnet = TFNet(options)

while True:

	img_cv2 = grab_img()
	tfnet_result = tfnet.return_predict(img_cv2)

	for obj in interested_objects:
		# See if that object (`obj`) appears at all
		search = search_tfnet_result_for_object(tfnet_result, obj)
		
		if search:
			print('Found object "{}" in image'.format(obj))

			# Show where in the image the object exists and label
			img_annotated = draw_bounding_box(img_cv2, search)
			
			# Save annotated image
			filename = create_filename(obj)
			cv2.imwrite(filename, img_annotated)

	time.sleep(5)