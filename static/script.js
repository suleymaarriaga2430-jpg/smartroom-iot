const temperatura = document.getElementById("temperatura");
const luz = document.getElementById("luz");
const ocupacion = document.getElementById("ocupacion");
const ventilador = document.getElementById("ventilador");
const iluminacion = document.getElementById("iluminacion");
const prediccion = document.getElementById("prediccion");
const alerta = document.getElementById("alerta");

const ctx = document.getElementById('grafica').getContext('2d');

let temperaturas = [];
let predicciones = [];
let etiquetas = [];

const grafica = new Chart(ctx, {

    type: 'line',

    data: {

        labels: etiquetas,

        datasets: [

            {
                label: 'Temperatura',
                data: temperaturas,
                borderWidth: 3
            },

            {
                label: 'Predicción IA',
                data: predicciones,
                borderWidth: 3
            }

        ]

    },

    options: {

        responsive: true

    }

});

async function cargarDatos() {

    try {

        const response = await fetch("/datos");

        const data = await response.json();

        temperatura.textContent =
            data.temperatura + " °C";

        luz.textContent =
            data.luz;

        ocupacion.textContent =
            data.ocupacion;

        ventilador.textContent =
            data.ventilador;

        iluminacion.textContent =
            data.iluminacion;

        prediccion.textContent =
            data.prediccion + " °C";

        // ALERTA

        if (data.temperatura >= 32) {

            alerta.style.display = "block";

            alerta.innerHTML =
                "⚠️ Temperatura alta detectada";

        } else {

            alerta.style.display = "none";

        }

        // GRAFICA

        const hora = new Date().toLocaleTimeString();

        etiquetas.push(hora);

        temperaturas.push(data.temperatura);

        predicciones.push(data.prediccion);

        if (etiquetas.length > 10) {

            etiquetas.shift();

            temperaturas.shift();

            predicciones.shift();

        }

        grafica.update();

    } catch (error) {

        console.log(error);

    }

}

cargarDatos();

setInterval(cargarDatos, 3000);