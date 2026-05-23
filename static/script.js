const temperatura = document.getElementById("temperatura");

const luz = document.getElementById("luz");

const ocupacion = document.getElementById("ocupacion");

const ventilador = document.getElementById("ventilador");

const iluminacion = document.getElementById("iluminacion");

const prediccion = document.getElementById("prediccion");

const alerta = document.getElementById("alerta");

const ctx = document.getElementById('grafica');

let temperaturas = [];

let labels = [];

const grafica = new Chart(ctx, {

    type: 'line',

    data: {

        labels: labels,

        datasets: [{

            label: 'Temperatura',

            data: temperaturas,

            borderWidth: 3

        }]

    }

});

async function obtenerDatos(){

    const respuesta = await fetch("http://127.0.0.1:5000/datos");

    const datos = await respuesta.json();

    temperatura.innerHTML = datos.temperatura + " °C";

    luz.innerHTML = datos.luz;

    ocupacion.innerHTML = datos.ocupacion;

    ventilador.innerHTML = datos.ventilador;

    iluminacion.innerHTML = datos.iluminacion;

    prediccion.innerHTML = datos.prediccion + " °C";

    if(datos.temperatura > 32){

        alerta.style.display = "block";

    }else{

        alerta.style.display = "none";
    }

    temperaturas.push(datos.temperatura);

    labels.push("");

    if(temperaturas.length > 10){

        temperaturas.shift();

        labels.shift();
    }

    grafica.update();
}

setInterval(obtenerDatos,2000);

obtenerDatos();