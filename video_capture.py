import cv2
import base64
import threading
import config
import datetime


class VideoCapture(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.frame = None
        self.off_air_frame = cv2.imread('off_air.jpg')
        self.off_air_frame = cv2.resize(self.off_air_frame, (config.frame_size_w, config.frame_size_h))
        
    def run(self):
        cap = cv2.VideoCapture(config.camera_path)
                
        while True:
            ret, frame = cap.read()

            if ret:
                frame = self.draw_stuffs(frame)
                self.set_frame(frame)

                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
            else:
                break

        self.set_frame(self.off_air_frame)
        cap.release()
        cv2.destroyAllWindows()

    def draw_stuffs(self, image):
        frame_h, frame_w, _ = image.shape
        image = cv2.flip(image,1)
        cv2.circle(image,(15,20), 7, (0,0,255), -1)
        cv2.putText(image, "Live", (25, 32), 0, 1e-2 * 100, (255, 0, 0), 2)
        now = datetime.datetime.now()
        strnow = "{}:{}:{}".format(now.hour, now.minute, now.second)
        cv2.putText(image, strnow, (frame_w - 150, 50), 0, 1e-2 * 100, (255, 255, 255), 2)
        image = cv2.resize(image, (config.frame_size_w, config.frame_size_h))
        return image

    def set_frame(self, frame):
        _, buffer = cv2.imencode('.jpg', frame)
        self.frame = buffer.tostring()

if __name__ == "__main__":
    video_capture = VideoCapture()
    video_capture.run()
