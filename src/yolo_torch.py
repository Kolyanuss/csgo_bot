import cv2
import numpy as np
import torch
import dxcam

INPUT_WIDTH = 1024
INPUT_HEIGHT = 1024
SCORE_THRESHOLD = 0.8
NMS_THRESHOLD = 0.8
CONFIDENCE_THRESHOLD = 0.8
# Text parameters.
FONT_FACE = cv2.FONT_HERSHEY_SIMPLEX
FONT_SCALE = 0.7
THICKNESS = 1


def drawRectangles(image, dfResults):
    for _, row in dfResults.iterrows():
        print((row['xmin'], row['ymin']))
        image = cv2.rectangle(image, (row['xmin'], row['ymin']), (row['xmax'], row['ymax']), (255, 0, 0), 2)

def draw_label(im, label, x, y, color):
    """Draw text onto image at location."""
    # Get text size.
    text_size = cv2.getTextSize(label, FONT_FACE, FONT_SCALE, THICKNESS)
    dim, baseline = text_size[0], text_size[1]
    # Use text size to create a BLACK rectangle.
    cv2.rectangle(im, (x,y), (x + dim[0], y + dim[1] + baseline), (0,0,0), cv2.FILLED)
    # Display text inside the rectangle.
    cv2.putText(im, label, (x, y + dim[1]), FONT_FACE, FONT_SCALE, color, THICKNESS, cv2.LINE_AA)


def draw_wrap_detection(input_image, outputs_2darr):
    class_ids = []
    confidences = []
    boxes = []

    image_width, image_height, _ = input_image.shape
    x_factor = image_width / INPUT_WIDTH
    y_factor = image_height / INPUT_HEIGHT

    for row in outputs_2darr:
        confidence = row[4]
        if confidence >= CONFIDENCE_THRESHOLD:
            classes_scores = row[5:]
            class_id = np.argmax(classes_scores)
            if (classes_scores[class_id] > SCORE_THRESHOLD):
                confidences.append(confidence)
                class_ids.append(class_id)

                x, y, w, h = row[0], row[1], row[2], row[3]
                left = int((x - 0.5 * w) * x_factor)
                top = int((y - 0.5 * h) * y_factor)
                width = int(w * x_factor)
                height = int(h * y_factor)
                box = np.array([left, top, width, height])
                boxes.append(box)

    # indexes = cv2.dnn.NMSBoxes(boxes, confidences, 
    #         CONFIDENCE_THRESHOLD, NMS_THRESHOLD)

    for i in range(len(boxes)):
        box = boxes[i]
        left,top,width,height = box[0],box[1],box[2],box[3]
        color = colors[int(class_ids[i]) % len(colors)]
        # Draw bounding box.
        #  cv2.rectangle(frame, box, color, 2)
        cv2.rectangle(frame, (left, top), (left + width, top + height), color, THICKNESS*3)
        # cv2.putText(frame, class_list[class_ids[i]], (box[0], box[1] - 10), cv2.FONT_HERSHEY_SIMPLEX, .5, (0,0,0))
        # Class label.                      
        label = "{}:{:.2f}".format(class_list[class_ids[i]], confidences[i])             
        # Draw label.  
        draw_label(input_image, label, left, top, color)


def format_yolov5(frame):
    row, col, _ = frame.shape
    _max = max(col, row)
    result = np.zeros((_max, _max, 3), np.uint8)
    result[0:row, 0:col] = frame[:, :, :3]
    return result


# model = torch.hub.load('ultralytics/yolov5', 'yolov5s')
# model = torch.hub.load("ultralytics/yolov5", 'custom', path='config_files/yolov5s.pt') #+
# model = torch.hub.load("WongKinYiu/yolov7", 'yolov7', force_reload=True)
# model = torch.hub.load("WongKinYiu/yolov7", 'custom', 'config_files/yolov7.pt') #+
model = torch.hub.load("WongKinYiu/yolov7", 'custom', 'config_files/yolov7_csgo_v1.pt')
class_list = []
with open("config_files/classes.txt", "r") as f:
    class_list = [cname.strip() for cname in f.readlines()]
colors = [(255, 255, 0), (0, 255, 0), (0, 255, 255), (255, 0, 0)]
monitor = (0, 26, 640, 640+26)
camera = dxcam.create()

camera.start(region=monitor)
while True:
    frame = camera.get_latest_frame()
    # frame = format_yolov5(frame)  # todo: check
    results = model(frame)  # includes NMS
    
    # draw boxes variant 1
    # dfResults = results.pandas().xyxy[0]
    # drawRectangles(frame, dfResults[['xmin', 'ymin', 'xmax', 'ymax']].astype(int))

    # draw boxes variant 2
    draw_wrap_detection(frame, results.xyxy[0].cpu().numpy()) # some draw problem

    results.print() # info in console
    cv2.imshow("OpenCV", cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

camera.stop()
cv2.destroyAllWindows()
