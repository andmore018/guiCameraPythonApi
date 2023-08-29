import threading
import cv2
import time
import reportLog
import numpy as np


class Runcamera():
    def __init__(self, src=0, name="cameraThread"):
        try:
            self.name = name
            self.src = src
            self.logReport = reportLog.LogReport()
            self.stopped = False
            self.grabbed = False
            self.stream = None
            self.frame = []
            self.logReport.logger.info("Init runCamera process")

        except Exception as e:
            self.logReport.logger.error("error runCamera process: " + str(e))

    def start(self):
        try:
            self.stream = cv2.VideoCapture(self.src)
            time.sleep(1)
            self.grabbed, self.frame = self.stream.read()
            if (self.stream.isOpened()):
                self.my_thread = threading.Thread(
                    target=self.get, name=self.name)
                self.my_thread.start()  # no es lo mismo que nombre de clase
            else:
                self.logReport.logger.info("Camera is not opened")
        except Exception as e:
            self.logReport.logger.error("error runCamera start: " + str(e))

    def get(self):
        while not self.stopped:
            if (not self.grabbed):
                pass
            else:
                try:
                    self.grabbed, self.frame = self.stream.read()
                    cv2.waitKey(1)
                except Exception as e:
                    self.logReport.logger.error(
                        "error runCamera get: " + str(e))

    def stop(self):
        try:
            self.grabbed = False
            self.stopped = True
            self.my_thread.join()
            if (self.stream != None):
                self.stream.release()
                self.stream = None

        except Exception as e:
            self.logReport.logger.error("Error runCamera stop:" + str(e))

    def roiImg(self, img, x1, y1, x2, y2):
        roiImage = img[y1:y2, x1:x2]
        return roiImage

    def limites(self, limInferior, limSuperior):
        limInfe = np.array(limInferior, np.uint8)
        limSuper = np.array(limSuperior, np.uint8)
        return limInfe, limSuper
