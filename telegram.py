import telebot
import requests
import numpy as np
import tensorflow as tf
import cv2
from tensorflow.keras.models import load_model
import torch

# Cargar el modelo y las clases
model = torch.hub.load('ultralytics/yolov5', 'custom', path='last.pt')
classes = []
with open('classes.txt', 'r') as f:
    for line in f:
        classes.append(line.strip())

TOKEN = '6742866921:AAHVjdEXLKuI9sc1KUO7juxeQDIkGZL_Tdg'
bot = telebot.TeleBot(TOKEN)

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

def send_detection_image(chat_id):
    # Enviar la imagen con las detecciones al usuario de Telegram
    img_with_text = open('static/detected_image.jpg', 'rb')
    bot.send_photo(chat_id=chat_id, photo=img_with_text)
    img_with_text.close()

def send_classes_message(chat_id, response_text):
    # Enviar el mensaje con las clases detectadas y la cantidad al usuario de Telegram
    bot.send_message(chat_id=chat_id, text=response_text)

@bot.message_handler(content_types=['photo'])
def handle_image(message):
    file_id = message.photo[-1].file_id
    file_info = bot.get_file(file_id)
    
    # Obtener la URL de la imagen sin necesidad de descargarla localmente
    file_url = f'https://api.telegram.org/file/bot{TOKEN}/{file_info.file_path}'
    
    # Descargar la imagen localmente para procesarla
    img_data = requests.get(file_url)
    with open('input_image.jpg', 'wb') as img_file:
        img_file.write(img_data.content)
    
    # Realizar la detección de objetos en la imagen
    labels, boxes, confidences = yolo('input_image.jpg')
    
    # Contar las clases detectadas y sus recuentos
    classes_count = {}
    for label in labels:
        if label not in classes_count:
            classes_count[label] = 1
        else:
            classes_count[label] += 1
    
    # Preparar el texto con las clases detectadas y sus recuentos
    response_text = "Clases detectadas y sus recuentos:\n"
    for key, value in classes_count.items():
        response_text += f"{key}: {value}\n"
    
    # Enviar la imagen con las detecciones al usuario de Telegram
    img = open('static/detected_image.jpg', 'rb')
    bot.send_photo(chat_id=message.chat.id, photo=img, caption=response_text)
    img.close()

bot.polling()
