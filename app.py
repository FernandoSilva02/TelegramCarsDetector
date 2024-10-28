import os
import numpy as np
from flask import Flask, render_template, request
from flask import jsonify
import functions
import random
import torch
import cv2
import mysql.connector
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
app=Flask(__name__,static_folder='static')

@app.route("/", methods=['GET', 'POST'])
def main():
	return render_template("index.html")


@app.route("/submit", methods=['GET', 'POST'])
def get_output():
    if request.method == 'POST':
        img = request.files['image']
        img_path = "static/" + img.filename
        img.save(img_path)
        img = cv2.imread(img_path)
        img = cv2.resize(img, (512, 512))
        label, bbox, confidence = functions.yolo(img_path)

		# Obtener la cantidad de clases detectadas
        num_classes_detected = len(label) if label else 0

		# Contar la cantidad de cada clase detectada
        classes_count = {}
        for l in label:
            if l not in classes_count:
                classes_count[l] = 1
            else:
                classes_count[l] += 1
		
        functions.yolo(img_path)  # Realizar detección y guardar la imagen procesada
        detected_img_path = "static/detected_image.jpg"  # Ruta relativa de la imagen detectada

        mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="iadb"
        )

        mycursor = mydb.cursor()

        # Suponiendo que tienes una tabla llamada 'detected_images' con columnas: 'id', 'image_path', 'classes_detected'
        sql = "INSERT INTO detected_images (image_path, classes_detected) VALUES (%s, %s)"
        val = ("static/detected_image.jpg", str(classes_count))
        mycursor.execute(sql, val)
        
        mydb.commit()

        # Recuperar datos de la base de datos para mostrar en HTML
        # Código para recuperar la información de la base de datos y enviarla al HTML
        sql = "SELECT * FROM detected_images ORDER BY id DESC LIMIT 1"
        mycursor.execute(sql)
        result = mycursor.fetchone()  # Obtener el último registro insertado

        # Obtener la información necesaria para mostrar en HTML
        detected_img_path = result[1]  # Ruta de la imagen detectada desde la base de datos
        num_classes_detected = len(eval(result[2]))  # Convertir la cadena de clases a lista y obtener la cantidad

        # Envía los datos al HTML para mostrar la imagen y las clases detectadas
        return jsonify({"detected_img_path": detected_img_path, "num_classes_detected": num_classes_detected, "classes_count": eval(result[2])})
        

if __name__=='__main__':
    app.run(debug=True)
