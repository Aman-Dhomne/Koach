import flask
import os
from werkzeug.utils import secure_filename
import PoseModule as pm

app = flask.Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['ALLOWED_EXTENSIONS'] = {'mp4', 'avi', 'mov'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/')
def index():
    return flask.render_template('index.html')

@app.route('/process_video', methods=['POST'])
def process_video():
    if 'video' not in flask.request.files:
        return 'No video file uploaded', 400

    video_file = flask.request.files['video']

    if video_file.filename == '':
        return 'No selected video file', 400

    if video_file and allowed_file(video_file.filename):
        filename = secure_filename(video_file.filename)
        video_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        video_file.save(video_path)

        # Process the uploaded video using the pose estimation module
        #detector #= pm.poseDetector()

        # Your pose estimation processing logic here...
        import cv2
        import time
        import PoseModule as pm

        def process_video(video_path):
            cap = cv2.VideoCapture(video_path)
            detector = pm.poseDetector()
            pTime = 0
            while True:
                success, img = cap.read()
                img = detector.findPose(img)
                lmList = detector.findPosition(img, draw=False)
                if len(lmList) != 0:
                    print(lmList[14])
                    cv2.circle(img, (lmList[14][1], lmList[14][2]), 15, (0, 0, 255), cv2.FILLED)

                cTime = time.time()
                fps = 1 / (cTime - pTime)
                pTime = cTime

                cv2.putText(img, str(int(fps)), (70, 50), cv2.FONT_HERSHEY_PLAIN, 3,
                            (255, 0, 0), 3)

                cv2.imshow("Image", img)
                cv2.waitKey(1)

        if __name__ == "__main__":
            process_video('PoseVideos/1.mp4')

        # For now, just return the same video as output
        return flask.send_file(video_path, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
