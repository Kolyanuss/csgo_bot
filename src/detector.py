import numpy as np
import cv2
import torch

INPUT_WIDTH_HEIGHT = 1024
CONFIDENCE_THRESHOLD = 0.85
# Text parameters.
FONT_FACE = cv2.FONT_HERSHEY_SIMPLEX
FONT_SCALE = 0.5
THICKNESS = 1

CLASS_LIST = ["c", "ch", "t", "th"]
COLORS = [(0, 0, 255), (0, 180, 255), (255, 0, 0), (255, 125, 0)]

# link to model: https://drive.google.com/file/d/1yMl9jUhqS9xfyBcZhjIXB1MoRcZ1mhfe/view?usp=sharing
MODEL = torch.hub.load("WongKinYiu/yolov7", 'custom',
                       'config_files/yolov7_csgo_v1.pt')  # download custom model


def draw_label(im, label, x, y, color):
    """Draw text onto image at location."""
    # Get text size.
    text_size = cv2.getTextSize(label, FONT_FACE, FONT_SCALE, THICKNESS)
    dim, baseline = text_size[0], text_size[1]
    # Use text size to create a BLACK rectangle.
    cv2.rectangle(im, (x, y - dim[1] - baseline),
                  (x + dim[0], y), (0, 0, 0), cv2.FILLED)
    # Display text inside the rectangle.
    cv2.putText(im, label, (x, y - baseline), FONT_FACE,
                FONT_SCALE, color, THICKNESS, cv2.LINE_AA)


def draw_detection(input_image, outputs_2darr):
    image_width, image_height, _ = input_image.shape
    x_factor = image_width / INPUT_WIDTH_HEIGHT
    y_factor = image_height / INPUT_WIDTH_HEIGHT

    for row in outputs_2darr:
        confidence = row[4]
        if confidence >= CONFIDENCE_THRESHOLD:
            left = int(row[0] * x_factor)
            top = int(row[1] * y_factor)
            right = int(row[2] * x_factor)
            bottom = int(row[3] * y_factor)

            clas_id = int(row[5])

            color = COLORS[int(clas_id) % len(COLORS)]
            # Draw bounding box.
            cv2.rectangle(input_image, (left, top),
                          (right, bottom), color, THICKNESS*3)
            # Class label.
            label = "{}:{:.2f}".format(CLASS_LIST[clas_id], confidence)
            # Draw label.
            draw_label(input_image, label, left, top, color)


def convert_to_yolo_format(frame):
    row, col, _ = frame.shape
    _max = max(col, row)
    result = np.zeros((_max, _max, 3), np.uint8)
    result[0:row, 0:col] = frame[:, :, :3]
    return result


def detect(frame):
    return MODEL(frame)  # includes NMS


def get_detected_points(input_image, outputs_2darr):
    result_points = []
    image_width, image_height, _ = input_image.shape
    x_factor = image_width / INPUT_WIDTH_HEIGHT
    y_factor = image_height / INPUT_WIDTH_HEIGHT

    for row in outputs_2darr:
        confidence = row[4]
        if confidence >= CONFIDENCE_THRESHOLD:
            left = int(row[0] * x_factor)
            top = int(row[1] * y_factor)
            right = int(row[2] * x_factor)
            bottom = int(row[3] * y_factor)
            midl_x = abs(left - right)/2+left
            midl_y = abs(top - bottom)/2+top
            result_points.append((midl_x, midl_y, row[5]))

    return result_points
