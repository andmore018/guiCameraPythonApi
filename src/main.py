# coding=utf-8

from flask import Flask, jsonify, request
import camera
import reportLog

app = Flask(__name__)

runCamera = None  # Variable global para almacenar la instancia de runCamera
logReport = None  # Variable global para almacenar la instancia de logReport


@app.route('/initCamera')
def initCamera():
    global runCamera  # Declarar que estás utilizando la variable global runCamera
    logReport = reportLog.LogReport()
    runCamera = camera.Runcamera(0, "CameraUsb_1")
    runCamera.start()
    if logReport is not None:
        logReport.logger.info("init runCamera function")
    if (runCamera.stream is not None and runCamera.grabbed):
        return jsonify("201")
    jsonify("402")


@app.route('/getFrame')
def getFrame():
    if runCamera is not None and len(runCamera.frame) > 0:
        return jsonify("202")
    return jsonify("402")


@app.route('/stopCamera')
def stopCamera():
    runCamera.stop()
    if runCamera.grabbed == False and runCamera.stream is None:
        jsonify("203")
    return jsonify("403")


if __name__ == "__main__":
    app.run(host='0.0.0.0')
