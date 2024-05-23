from ultralytics import YOLO
import cv2

model = YOLO("yolov8x.pt")

image = cv2.imread(r"faces\classroom.jpg")

results = model.predict(source=image, save=True, save_txt=True)
