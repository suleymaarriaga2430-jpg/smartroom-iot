from flask import Flask, jsonify, render_template
import random
from sklearn.linear_model import LinearRegression
import numpy as np

# FIREBASE
import firebase_admin
from firebase_admin import credentials, firestore
from datetime import datetime

app = Flask(__name__)

# --------------------------------
# FIREBASE
# --------------------------------

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

@app.route('/')

def home():

    return render_template('index.html')

@app.route('/datos')

def datos():

    # --------------------------------
    # DATOS IOT
    # --------------------------------

    temperatura = round(random.uniform(18,40),1)

    luz = random.randint(0,1023)

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

    X = np.array([[1],[2],[3],[4],[5]])

    y = np.array([20,22,24,26,28])

    modelo = LinearRegression()

    modelo.fit(X,y)

    prediccion = modelo.predict([[6]])

    prediccion = round(prediccion[0],1)

    # --------------------------------
    # GUARDAR EN FIREBASE
    # --------------------------------

    db.collection("lecturas").add({

        "temperatura": temperatura,

        "prediccion": prediccion,

        "luz": luz,

        "ocupacion": ocupacion,

        "ventilador": ventilador,

        "iluminacion": iluminacion,

        "timestamp": datetime.now()

    })

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

        "baja": round(baja,2),

        "media": round(media,2),

        "alta": round(alta,2)

    })


if __name__ == '__main__':
    app.run(debug=True)