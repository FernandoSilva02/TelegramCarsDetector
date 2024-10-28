import numpy as np
import tensorflow as tf
import cv2
from tensorflow.keras.models import load_model
import torch
print(cv2.__version__)

model = torch.hub.load('ultralytics/yolov5', 'custom', path='last.pt')
classes=[]
f=open('classes.txt','r')
for line in f:
	classes.append(line.strip())

def yolo(img_path):
    img = cv2.imread(img_path)
    img = cv2.resize(img, (512, 512))
    results = model(img)
    Label, Bbox, Confidence = [], [], []
    for res in results.pandas().xyxy:
        for obj in range(len(res)):
            if res['confidence'][obj] > 0.2:
                (x1, y1, x2, y2) = (res['xmin'][obj], res['ymin'][obj], res['xmax'][obj], res['ymax'][obj])
                bbox = (x1, y1, x2, y2)
                className = classes[res['class'][obj]]
                Label.append(className)
                Bbox.append(bbox)
                Confidence.append(res['confidence'][obj])

                # Dibujar bounding box y etiquetas en la imagen
                cv2.rectangle(img, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 2)
                cv2.putText(img, f'{className} {res["confidence"][obj]:.2f}', (int(x1), int(y1) - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    # Guardar la imagen con las detecciones en la carpeta static
    cv2.imwrite('static/detected_image.jpg', img)

    return Label, Bbox, Confidence
