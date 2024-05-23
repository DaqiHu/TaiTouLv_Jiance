import cv2
import config
from rects import *

def __inference_image_rects_cv2_internal(image):
    color = (0, 255, 0)
    grey = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    classfier = cv2.CascadeClassifier(config.classifier_data)
    scaled_rects = classfier.detectMultiScale(grey, scaleFactor=1.2, minNeighbors=3, minSize=(32, 32))
    return scaled_rects

def inference_image_rects_cv2(image_path: str) -> list[RectScaled]:
    image = cv2.imread(image_path)
    
    # cv2.image.shape is (height, width, channel). e.g. (720, 1280, 3). NOT (width, height, channel)! CAUTION!
    height, width, channel = image.shape
    raw_rects = __inference_image_rects_cv2_internal(image)
    
    scaled_rects = []
    for rect in raw_rects:
        x, y, w, h = rect
        scaled_rects.append(RectScaled(x, y, w, h, width, height))
        
    return scaled_rects

def __inference_image_rects_yolo_internal(txt_path: str):
    with open(txt_path, encoding="utf-8", mode="r") as f:
        file_lines = f.readlines()
        unit_rects = []
        
        for line in file_lines:
            
            # "0 0.231226 0.243774 0.0466695 0.119245": str -> [0.231226, 0.243774, 0.0466695, 0.119245]: list[float]
            result = line.split(" ")
            
            # Added check `if result[0] != "0"`. In yolov8x model, 0 stands for "person".
            if result[0] != "0":
                continue
            
            # convert and store pos-x, pos-y, width and height (relative).
            xywh = [float(num) for num in result[1:]]
            
            # add one 
            unit_rects.append(xywh)
            
        return unit_rects

def inference_image_rects_yolo(image_txt: str) -> list[RectUnit]:
    raw_rects = __inference_image_rects_yolo_internal(image_txt)
    unit_rects = []
    
    for rect in raw_rects:
        x, y, w, h = rect
        unit_rects.append(RectUnit(x, y, w, h))
        
    return unit_rects

def inference_video_rects_cv2(video_path: str):
    pass