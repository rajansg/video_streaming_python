from flask import Flask, render_template, Response
from video_capture import VideoCapture
import config

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html', 
        frame_size_w = config.frame_size_w,
        frame_size_h = config.frame_size_h)

@app.route('/video_feed')
def video_feed():
    return Response(generate(), mimetype='multipart/x-mixed-replace; boundary=frame')

def generate():
    while True:
        frame = video_capture.frame
        yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

if __name__ == '__main__':
    video_capture = VideoCapture()   
    video_capture.start()
    app.run(host='0.0.0.0', port=8080, debug=True, threaded=True)