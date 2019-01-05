import time
from io import BytesIO
from typing import Union

import cv2
import requests
import numpy as np
from PIL import Image

def grab_img() -> np.ndarray:
	''' Sends GET request to /image route on localhost '''
	response = requests.get('http://0.0.0.0:8000/image')
	img = Image.open(BytesIO(response.content))
	img_cv2 = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
	return img_cv2

def search_tfnet_result_for_object(tfnet_result: list, obj: str) -> Union[None, dict]:
	''' See whether `obj` was detected in image '''
	for detection in tfnet_result:
		if detection['label'] == obj:
			return detection
	else:
		return None

def draw_bounding_box(img_cv2: np.ndarray, detection: dict):
	'''
	Given detection and an image, draw bounding box
	
	https://github.com/thtrieu/darkflow/issues/571#issuecomment-365831589
	'''

	img_cv2 = cv2.rectangle(
		img_cv2,
		(detection['topleft']['x'], detection['topleft']['y']),
		(detection['bottomright']['x'], detection['bottomright']['y']),
		(0, 255, 0),
		4
	)
	
	text_x, text_y = detection['topleft']['x'] - 10, detection['topleft']['y'] - 10

	img_cv2 = cv2.putText(
		img_cv2,
		detection['label'],
		(text_x, text_y),
		cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0),
		2,
		cv2.LINE_AA
	)

	return img_cv2

def create_filename(obj: str) -> str:
	return './imgs/{}_{}.png'.format(obj, int(time.time()))