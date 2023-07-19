from flask import Flask, request,render_template
import cv2
import numpy as np
import math
from PIL import Image
import io
from torch.serialization import save
from ultralytics import YOLO

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
    
    img_bytes = file.read()
    file = Image.open(io.BytesIO(img_bytes))
    model=YOLO("cyclone_best.pt")
    results = model.predict(file, save=True,save_crop=True,name="predicted")
    x1,y1,x2,y2=results[0].boxes.xyxy[0]
    x1,y1,x2,y2=int(x1),int(y1),int(x2),int(y2)
    cv2.rectangle(file,(x1,y1),(x2,y2),[255,0,255],3,)
    conf=math.ceil((results[0].boxes.conf[0]*100))/100
    label=f'cyclone:{conf}'
    print("***************************")
    print("label")
    t_size = cv2.getTextSize(label, 0, fontScale=1, thickness=2)[0]
    c2 = x1 + t_size[0], y1 - t_size[1] - 3
    cv2.rectangle(file, (x1,y1), c2, [255,0,255], -1, cv2.LINE_AA)  # filled
    cv2.putText(file, label, (x1,y1-2),0, 1,[255,255,255], thickness=1,lineType=cv2.LINE_AA)
    cv2.imwrite("predicted_image.jpeg",file)
    return render_template("display_text.html",image_path=file)
    

if __name__ == '__main__':
    app.run()