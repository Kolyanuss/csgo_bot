import cv2
import dxcam
import detector

PRINT_MODE = False
# DRAW_MODE = True

monitor = (0, 26, 1024, 768+26)
camera = dxcam.create()

camera.start(region=monitor)
print("Start capture")
while True:
    # take screen shot
    frame = camera.get_latest_frame()
    # resize img to yolo format
    frame = detector.convert_to_yolo_format(frame)
    # show img to model and get result
    results = detector.detect(frame)

    # AIM section
    

    # info in console (optional)
    if PRINT_MODE:
        results.print()
    
    # draw boxes in other window
    detector.draw_detection(frame, results.xyxy[0].cpu().numpy())
    cv2.imshow("OpenCV", cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
    
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

camera.stop()
cv2.destroyAllWindows()
