import cv2
import numpy as np
import time
import mss
import torch

INPUT_WIDTH = 640
INPUT_HEIGHT = 640
SCORE_THRESHOLD = 0.2
NMS_THRESHOLD = 0.4
CONFIDENCE_THRESHOLD = 0.4


def drawRectangles(image, dfResults):
    for _, row in dfResults.iterrows():
        print((row['xmin'], row['ymin']))
        image = cv2.rectangle(image, (row['xmin'], row['ymin']), (row['xmax'], row['ymax']), (255, 0, 0), 2)
    # cv2.imshow("OpenCV", image)


def wrap_detection(input_image, output_data):
    class_ids = []
    confidences = []
    boxes = []

    image_width, image_height, _ = input_image.shape

    x_factor = image_width / INPUT_WIDTH
    y_factor = image_height / INPUT_HEIGHT

    for row in output_data:
        confidence = row[4]
        if confidence >= 0.4:

            classes_scores = row[5:]
            class_id = np.argmax(classes_scores)
            confidence = classes_scores[class_id]
            if (confidence > .25):

                confidences.append(confidence)

                class_ids.append(class_id)

                x, y, w, h = row[0].item(), row[1].item(), row[2].item(), row[3].item() 
                left = int((x - 0.5 * w) * x_factor)
                top = int((y - 0.5 * h) * y_factor)
                width = int(w * x_factor)
                height = int(h * y_factor)
                box = np.array([left, top, width, height])
                boxes.append(box)

    indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.25, 0.45)

    result_class_ids = []
    result_confidences = []
    result_boxes = []

    for i in indexes:
        result_confidences.append(confidences[i])
        result_class_ids.append(class_ids[i])
        result_boxes.append(boxes[i])

    return result_class_ids, result_confidences, result_boxes


def format_yolov5(frame):
    row, col, _ = frame.shape
    _max = max(col, row)
    result = np.zeros((_max, _max, 3), np.uint8)
    result[0:row, 0:col] = frame[:, :, :3]
    return result


# model = torch.hub.load('ultralytics/yolov5', 'yolov5s')
model = torch.hub.load("ultralytics/yolov5", 'custom',
                       path='config_files/yolov5s.pt')
class_list = []
with open("config_files/classes.txt", "r") as f:
    class_list = [cname.strip() for cname in f.readlines()]
colors = [(255, 255, 0), (0, 255, 0), (0, 255, 255), (255, 0, 0)]
monitor = {"top": 26, "left": 0, "width": 640, "height": 640}

i = 0
start_time = time.time()
while True:
    frame = np.array(mss.mss().grab(monitor))
    # frame = format_yolov5(frame)  # todo: check
    results = model(frame, size=INPUT_WIDTH)  # includes NMS
    results.print()  # can be hide

    # draw boxes variant 1
    dfResults = results.pandas().xyxy[0]
    drawRectangles(frame, dfResults[['xmin', 'ymin', 'xmax', 'ymax']].astype(int))

    # draw boxes variant 2
    # class_ids, confidences, boxes = wrap_detection(frame, results.xyxy[0]) # trouble with dimentions
    # for (classid, confidence, box) in zip(class_ids, confidences, boxes):
    #      color = colors[int(classid) % len(colors)]
    #      cv2.rectangle(frame, box, color, 2)
    #      cv2.rectangle(frame, (box[0], box[1] - 20), (box[0] + box[2], box[1]), color, -1)
    #      cv2.putText(frame, class_list[classid], (box[0], box[1] - 10), cv2.FONT_HERSHEY_SIMPLEX, .5, (0,0,0))

    cv2.imshow("OpenCV", frame)
    # ending
    i += 1
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

mytime = time.time() - start_time
cv2.destroyAllWindows()
print("avg fps is: ", 1/(mytime/i))
