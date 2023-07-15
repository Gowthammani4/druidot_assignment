from flask import Flask, request,render_template
import cv2
from py_assignment import OCR
import numpy as np

app = Flask(__name__, template_folder='template')
@app.route("/")
def index():
    return render_template("upload.html",)
@app.route("/upload", methods=['POST'])
def upload():
    # Check if a file was submitted
    if 'file' not in request.files:
        return 'No file uploaded', 400
    file = request.files['file']
    print(file)
    print(type(file),"file type")
    # Check if the file is of allowed type
    if not file.filename.endswith(('.jpg', '.jpeg', '.png')):
        return 'Invalid file type', 400
    file = request.files['file']
    file_bytes = np.fromfile(file, np.uint8)
    file = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
    text__=OCR()
    text_=text__.extract(file)
    return render_template("display_text.html",text=text_)
    

if __name__ == '__main__':
    app.run()