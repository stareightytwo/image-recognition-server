import time
from io import BytesIO

import cv2
import requests
import numpy as np
from PIL import Image
from darkflow.net.build import TFNet

options = {
	'model': 'cfg/tiny-yolo-voc.cfg',
	'load': 'bin/tiny-yolo-voc.weights',
	'threshold': 0.1
}

tfnet = TFNet(options)

interested_object = 'bird'

while True:
	response = requests.get('http://0.0.0.0:8000/image')
	img = Image.open(BytesIO(response.content))

	curr_img_cv2 = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)

	result = tfnet.return_predict(curr_img_cv2)

	for detection in result:
		if detection['label'] == interested_object:
			curr_img.save('birds/%i.jpg' % birdsSeen)

	time.sleep(4)