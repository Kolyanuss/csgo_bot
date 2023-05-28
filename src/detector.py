import numpy as np
import cv2
import torch

CONFIDENCE_THRESHOLD = 0.85
# Text parameters.
FONT_FACE = cv2.FONT_HERSHEY_SIMPLEX
FONT_SCALE = 0.5
THICKNESS = 1

CLASS_LIST = ["c", "ch", "t", "th"]
COLORS = [(0, 0, 255), (0, 180, 255), (255, 0, 0), (255, 125, 0)]

# link to model: https://drive.google.com/file/d/1yMl9jUhqS9xfyBcZhjIXB1MoRcZ1mhfe/view?usp=sharing
MODEL = torch.hub.load("WongKinYiu/yolov7", 'custom',
                       'config_files/yolov7_csgo_v1.pt')  # import custom model


def _draw_label(im, label, x, y, color):
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


def draw_detection(input_image, nn_results):
    for row in _get_filtered_detection(nn_results):
        left = int(row[0])
        top = int(row[1])
        right = int(row[2])
        bottom = int(row[3])
        confidence = row[4]
        clas_id = int(row[5])

        color = COLORS[int(clas_id) % len(COLORS)]
        # Draw bounding box.
        cv2.rectangle(input_image, (left, top),
                        (right, bottom), color, THICKNESS*3)
        # Class label.
        label = "{}:{:.2f}".format(CLASS_LIST[clas_id], confidence)
        # Draw label.
        _draw_label(input_image, label, left, top, color)


def get_big_detect_mid_point(nn_results):
    maxArea = 0
    maxPoint = None
    for row in _get_filtered_detection(nn_results):
        rectangle = (int(row[0]),int(row[1]),int(row[2]),int(row[3]))
        area = _get_area(*rectangle)
        if area > maxArea:
            maxArea = area
            maxPoint = (*_get_center_point(*rectangle), row[5])
    return maxPoint


# def convert_to_yolo_format(frame):
#     row, col, _ = frame.shape
#     _max = max(col, row)
#     result = np.zeros((_max, _max, 3), np.uint8)
#     result[0:row, 0:col] = frame[:, :, :3]
#     return result


def detect(frame):
    return MODEL(frame)  # includes NMS

def _get_center_point(left,top,right,bottom):
    mid_x = (left + right)/2
    mid_y = (top + bottom)/2
    return mid_x,mid_y

def _get_intersection_area(rectangle_1, rectangle_2):
    x_overlap = max(0, min(rectangle_1[2], rectangle_2[2]) - max(rectangle_1[0], rectangle_2[0]))
    y_overlap = max(0, min(rectangle_1[3], rectangle_2[3]) - max(rectangle_1[1], rectangle_2[1]))
    intersection_area = x_overlap * y_overlap
    return intersection_area

def _get_area(left,top,right,bottom):
    return abs(left - right) * abs(top - bottom)

def _get_filtered_detection(nn_results):
    confirmed_2darr = []
    for row in nn_results:
        confidence = row[4]
        if confidence >= CONFIDENCE_THRESHOLD:
            confirmed_2darr.append(row)

    result_points = []
    for row in confirmed_2darr:
        # [left, top, right, bottom]
        cur_rectangle = (int(row[0]),int(row[1]),int(row[2]),int(row[3]))
        class_name = row[5]
        # if class is head - add
        if class_name == 1 or class_name == 3: # head
            result_points.append(row)
            continue
        
        has_intersection_with_head = False
        # if not skipped - class is body / start find intersection with head
        for new_row in confirmed_2darr:
            class_name2 = new_row[5]
            if class_name2 == 1 or class_name2 == 3: # head
                rect2 = (int(new_row[0]),int(new_row[1]),int(new_row[2]),int(new_row[3]))
                if (_get_intersection_area(cur_rectangle,rect2) > 0.9*_get_area(*rect2)):
                    has_intersection_with_head = True
                    break # if body has intersection with head - we don`t add him to targets
        # add body to targets if has`t intersection with head
        if not has_intersection_with_head:
            result_points.append(row)

    return result_points
