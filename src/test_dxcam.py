import dxcam
import cv2
camera = dxcam.create()
monitor = (27, 0, 1024, 500)

camera.start(region=monitor)
while camera.is_capturing:
    image = camera.get_latest_frame()
    cv2.imshow("OpenCV", image)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        cv2.destroyAllWindows()
        break
camera.stop()
