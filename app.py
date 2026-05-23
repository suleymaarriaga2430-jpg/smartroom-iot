from flask import Flask, jsonify, render_template
import random
from sklearn.linear_model import LinearRegression
import numpy as np

# FIREBASE
import firebase_admin
from firebase_admin import credentials, firestore
from datetime import datetime
import os

app = Flask(__name__)

# --------------------------------
# FIREBASE
# --------------------------------

if not firebase_admin._apps:

    cred = credentials.Certificate("firebase-key.json")

    firebase_admin.initialize_app(cred)

db = firestore.client()

# --------------------------------
# IA DIFUSA
# --------------------------------

def temp_baja(t):

    if t <= 15:
        return 1

    elif t < 25:
        return (25 - t) / 10

    return 0


def temp_media(t):

    if t <= 15 or t >= 35:
        return 0

    elif t < 25:
        return (t - 15) / 10

    return (35 - t) / 10


def temp_alta(t):

    if t <= 25:
        return 0

    elif t < 35:
        return (t - 25) / 10

    return 1

# --------------------------------
# HOME
# --------------------------------

@app.route('/')

def home():

    return render_template('index.html')

# --------------------------------
# API DATOS
# --------------------------------

@app.route('/datos')

def datos():

    # --------------------------------
    # DATOS IOT
    # --------------------------------

    temperatura = round(random.uniform(18, 40), 1)

    luz = random.randint(0, 1023)

    ocupacion = random.choice([
        "Ocupado",
        "Actividad Baja",
        "Ausente"
    ])

    # --------------------------------
    # IA DIFUSA
    # --------------------------------

    baja = temp_baja(temperatura)

    media = temp_media(temperatura)

    alta = temp_alta(temperatura)

    if alta > 0.7:
        ventilador = "Máximo"

    elif media > 0.5:
        ventilador = "Medio"

    elif baja > 0.5:
        ventilador = "Apagado"

    else:
        ventilador = "Lento"

    # --------------------------------
    # ILUMINACIÓN
    # --------------------------------

    if luz < 300:
        iluminacion = "Alta"

    elif luz < 700:
        iluminacion = "Media"

    else:
        iluminacion = "Apagada"

    # --------------------------------
    # MACHINE LEARNING
    # --------------------------------

    X = np.array([[1], [2], [3], [4], [5]])

    y = np.array([20, 22, 24, 26, 28])

    modelo = LinearRegression()

    modelo.fit(X, y)

    prediccion = modelo.predict([[6]])

    prediccion = round(prediccion[0], 1)

    # --------------------------------
    # GUARDAR EN FIREBASE
    # --------------------------------

    try:

        db.collection("lecturas").add({

            "temperatura": temperatura,

            "prediccion": prediccion,

            "luz": luz,

            "ocupacion": ocupacion,

            "ventilador": ventilador,

            "iluminacion": iluminacion,

            "timestamp": datetime.now()

        })

    except Exception as e:

        print("Error Firebase:", e)

    # --------------------------------
    # RESPUESTA API
    # --------------------------------

    return jsonify({

        "temperatura": temperatura,

        "prediccion": prediccion,

        "luz": luz,

        "ocupacion": ocupacion,

        "ventilador": ventilador,

        "iluminacion": iluminacion,

        "baja": round(baja, 2),

        "media": round(media, 2),

        "alta": round(alta, 2)

    })

# --------------------------------
# MAIN
# --------------------------------

if __name__ == '__main__':

    port = int(os.environ.get("PORT", 5000))

    app.run(host='0.0.0.0', port=port)