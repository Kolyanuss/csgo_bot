import numpy as np
import cv2
import torch
import math
from ultralytics import YOLO
import supervision as sv

CONFIDENCE_THRESHOLD = 0.85
# Text parameters.
FONT_FACE = cv2.FONT_HERSHEY_SIMPLEX
FONT_SCALE = 0.5
THICKNESS = 1

CLASS_LIST = ["c", "ch", "t", "th"]
ID_HEAD = [1,3]
COLORS = [(0, 0, 255), (0, 180, 255), (255, 0, 0), (255, 125, 0)]

# customize the bounding box
box_annotator = sv.BoxAnnotator(
    thickness=2,
    text_thickness=2,
    text_scale=1
)

# link to model: https://drive.google.com/file/d/1yMl9jUhqS9xfyBcZhjIXB1MoRcZ1mhfe/view?usp=sharing
# MODEL = torch.hub.load("WongKinYiu/yolov7", 'custom',
#                        'config_files/yolov7_csgo_v1.pt')  # import custom model
MODEL = YOLO('config_files/yolov8s_csgo_mirage-320-v62-pal-gen-bg-head.pt')


def get_closest_object(nn_results):
    # detect closest target
    closest = 1000000
    aim_rect = None
    for row in _get_filtered_detection(nn_results):
        rectangle = row[0]
        dist = math.dist([960, 540], [*_get_center_point(*rectangle)])
        if dist < closest:
            closest = dist
            aim_rect = rectangle
    return aim_rect


def detect(frame):
    result = MODEL(frame, agnostic_nms=True)[0]  # includes NMS
    return sv.Detections.from_yolov8(result)

def new_draw_detection(frame, detections):
    labels = [
        f"{MODEL.model.names[class_id]} {confidence:0.2f}"
        for _,_, confidence, class_id, _
        in detections
    ]
    frame = box_annotator.annotate(
        scene=frame, 
        detections=detections, 
        labels=labels
    )
    return frame

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
    confirmed_2darr = nn_results
    # for row in nn_results:
    #     confidence = row[4]
    #     if confidence >= CONFIDENCE_THRESHOLD:
    #         confirmed_2darr.append(row)

    result_points = []
    for row in confirmed_2darr:
        # [left, top, right, bottom]
        cur_rectangle = row[0]
        class_id = row[3]
        # if class is head - add
        if class_id == ID_HEAD[0] or class_id == ID_HEAD[1]: # head
            result_points.append(row)
            continue
        
        has_intersection_with_head = False
        # if not skipped - class is body
        # skip if object is very low
        if cur_rectangle[3]<1040:
            continue
        # start find intersection with head
        for new_row in confirmed_2darr:
            class_id2 = new_row[3]
            if class_id2 == ID_HEAD[0] or class_id2 == ID_HEAD[1]: # head
                rect2 = new_row[0]
                if (_get_intersection_area(cur_rectangle,rect2) > 0.9*_get_area(*rect2)):
                    has_intersection_with_head = True
                    break # if body has intersection with head - we don`t add him to targets
        # add body to targets if has`t intersection with head
        if not has_intersection_with_head:
            result_points.append(row)

    return result_points
