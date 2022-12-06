import cv2
import numpy as np
import torch
import dxcam

INPUT_WIDTH = 1024
INPUT_HEIGHT = 1024
CONFIDENCE_THRESHOLD = 0.85
# Text parameters.
FONT_FACE = cv2.FONT_HERSHEY_SIMPLEX
FONT_SCALE = 0.5
THICKNESS = 1


def draw_label(im, label, x, y, color):
    """Draw text onto image at location."""
    # Get text size.
    text_size = cv2.getTextSize(label, FONT_FACE, FONT_SCALE, THICKNESS)
    dim, baseline = text_size[0], text_size[1]
    # Use text size to create a BLACK rectangle.
    cv2.rectangle(im, (x,y - dim[1] - baseline), (x + dim[0], y), (0,0,0), cv2.FILLED)
    # Display text inside the rectangle.
    cv2.putText(im, label, (x, y - baseline), FONT_FACE, FONT_SCALE, color, THICKNESS, cv2.LINE_AA)

def draw_wrap_detection(input_image, outputs_2darr):
    image_width, image_height, _ = input_image.shape
    x_factor = image_width / INPUT_WIDTH
    y_factor = image_height / INPUT_HEIGHT

    for row in outputs_2darr:
        confidence = row[4]
        if confidence >= CONFIDENCE_THRESHOLD:
            clas_id = int(row[5])

            x, y, w, h = row[0], row[1], row[2], row[3]
            left = int(x * x_factor)
            top = int(y * y_factor)
            width = int(w * x_factor)
            height = int(h * y_factor)

            color = colors[int(clas_id) % len(colors)]
            # Draw bounding box.
            cv2.rectangle(frame, (left, top), (width, height), color, THICKNESS*3)
            # Class label.                      
            label = "{}:{:.2f}".format(class_list[clas_id], confidence)             
            # Draw label.  
            draw_label(input_image, label, left, top, color)

def format_yolo(frame):
    row, col, _ = frame.shape
    _max = max(col, row)
    result = np.zeros((_max, _max, 3), np.uint8)
    result[0:row, 0:col] = frame[:, :, :3]
    return result

# link to model: https://drive.google.com/file/d/1yMl9jUhqS9xfyBcZhjIXB1MoRcZ1mhfe/view?usp=sharing
model = torch.hub.load("WongKinYiu/yolov7", 'custom', 'config_files/yolov7_csgo_v1.pt') #download custom model
class_list = ["c","ch","t","th"]
colors = [(0, 0, 255), (0, 180, 255), (255, 0, 0), (255, 125, 0)]
monitor = (0, 26, 1024, 768+26)
camera = dxcam.create()

camera.start(region=monitor)
while True:
    frame = camera.get_latest_frame()
    frame = format_yolo(frame)
    results = model(frame)  # includes NMS
    
    # draw boxes
    draw_wrap_detection(frame, results.xyxy[0].cpu().numpy())

    # results.print() # info in console
    cv2.imshow("OpenCV", cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

camera.stop()
cv2.destroyAllWindows()
