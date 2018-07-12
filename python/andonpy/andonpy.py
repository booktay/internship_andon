from flask import Flask, render_template, Response
# from lib.andon_camera import AndonCamera

app = Flask(__name__)

@app.route('/')
def index():
    # AndonCamera().faceRecognition()
    return render_template('index.html')


def gen():
    """Video streaming generator function."""
    while True:
        yield (b'--frame\r\n'
            b'Content-Type: image/jpeg\r\n\r\n' + open('a.jpg', 'rb').read() + b'\r\n')


@app.route('/video_feed')
def video_feed():
    """Video streaming route. Put this in the src attribute of an img tag."""
    return Response(gen(),
            mimetype = 'multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(host='0.0.0.0')
