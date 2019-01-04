from io import BytesIO

import cv2
import requests
import numpy as np
from PIL import Image

def grab_img() -> np.ndarray:
	''' Sends GET request to /image route on localhost '''
	response = requests.get('http://0.0.0.0:8000/image')
	img = Image.open(BytesIO(response.content))
	curr_img_cv2 = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
	return curr_img_cv2

def obj_exists_in_img(tfnet_result: list, obj: str) -> bool:
	''' See whether `obj` was detected in image '''
	return True if any(d['label'] == obj for d in tfnet_result) else False