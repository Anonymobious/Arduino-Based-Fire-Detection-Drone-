import cv2
import matplotlib.pyplot as plt
import cvlib as cv
import urllib.request
import numpy as np
from cvlib.object_detection import draw_bbox
import concurrent.futures

url = 'http://192.168.0.104/cam-hi.jpg'

def run1():
    cv2.namedWindow("live transmission", cv2.WINDOW_AUTOSIZE)
    while True:
        try:
            img_resp = urllib.request.urlopen(url)
            imgnp = np.array(bytearray(img_resp.read()), dtype=np.uint8)
            im = cv2.imdecode(imgnp, -1)
        except Exception as e:
            print(f"Error in fetching or decoding image: {e}")
            continue

        cv2.imshow('live transmission', im)
        key = cv2.waitKey(5)
        if key == ord('q'):
            break
            
    cv2.destroyAllWindows()

def run2():
    cv2.namedWindow("detection", cv2.WINDOW_AUTOSIZE)
    while True:
        try:
            img_resp = urllib.request.urlopen(url)
            imgnp = np.array(bytearray(img_resp.read()), dtype=np.uint8)
            im = cv2.imdecode(imgnp, -1)
        except Exception as e:
            print(f"Error in fetching or decoding image: {e}")
            continue

        bbox, label, conf = cv.detect_common_objects(im)
        im = draw_bbox(im, bbox, label, conf)

        cv2.imshow('detection', im)
        key = cv2.waitKey(5)
        if key == ord('q'):
            break
            
    cv2.destroyAllWindows()

if __name__ == '__main__':
    print("started")
    with concurrent.futures.ThreadPoolExecutor() as executor:
        f1 = executor.submit(run1)
        f2 = executor.submit(run2)
        concurrent.futures.wait([f1, f2])
