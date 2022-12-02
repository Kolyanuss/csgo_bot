import cv2
import torch
# Model
model = torch.hub.load('ultralytics/yolov5', 'yolov5s')
# Image
img = cv2.imread('test/T/2562925089_preview_tm_phoenix_varianti.jpg')
# Inference
results = model(img, size=640)  # includes NMS
# Results
results.print()  
results.save()