const temperatura = document.getElementById("temperatura");
const luz = document.getElementById("luz");
const ocupacion = document.getElementById("ocupacion");
const ventilador = document.getElementById("ventilador");
const iluminacion = document.getElementById("iluminacion");
const prediccion = document.getElementById("prediccion");

async function cargarDatos() {

    try {

        const response = await fetch("/datos");

        if (!response.ok) {
            throw new Error("No se pudieron obtener los datos");
        }

        const data = await response.json();

        console.log("Datos recibidos:", data);

        temperatura.textContent = data.temperatura + " °C";

        luz.textContent = data.luz;

        ocupacion.textContent = data.ocupacion;

        ventilador.textContent = data.ventilador;

        iluminacion.textContent = data.iluminacion;

        prediccion.textContent = data.prediccion + " °C";

    } catch (error) {

        console.error("Error:", error);

    }

}

cargarDatos();

setInterval(cargarDatos, 3000);