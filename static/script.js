async function cargarDatos() {

    try {

        const respuesta = await fetch('/datos');

        const datos = await respuesta.json();

        document.getElementById('temperatura').innerHTML =
            datos.temperatura + " °C";

        document.getElementById('luz').innerHTML =
            datos.luz;

        document.getElementById('ocupacion').innerHTML =
            datos.ocupacion;

        document.getElementById('ventilador').innerHTML =
            datos.ventilador;

        document.getElementById('iluminacion').innerHTML =
            datos.iluminacion;

        document.getElementById('prediccion').innerHTML =
            datos.prediccion + " °C";

        console.log(datos);

    } catch(error) {

        console.log("Error:", error);

    }

}

cargarDatos();

setInterval(cargarDatos, 5000);