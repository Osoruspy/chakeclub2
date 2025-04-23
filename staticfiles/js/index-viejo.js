let confecciones = [];

const listarDetalles = async (idconfecciones) => {
    try {
        const response = await fetch(`./confecciones_detalles/${idconfecciones}`);
        const data = await response.json();
        console.log(data);

        if (data.message === 'Success') {
            $('#tabla-detalles').DataTable({
                "ajax": {
                    "url": "confecciones_detalles/<int:confecciones_id>",
                    "dataSrc": "data"
                },
                "columns": [
                    { "data": "id" },
                    { "data": "nombre" },
                    { "data": "item" },
                    { "data": "tamano" },
                    { "data": "genero" },
                    { "data": "numero" },
                    { "data": "fecha" },
                    { "data": "estado" },
                    { "data": "obs" }
                ],
                "language": {
                    "url": "//cdn.datatables.net/plug-ins/1.13.6/i18n/es-ES.json"
                }
            });
        }
    }catch (error) {
        console.log(error);
    }
};

const listarConfecciones = async (idCliente) => {
    try {
        const response = await fetch(`./confecciones/${idCliente}`);
        const data = await response.json();
        /*console.log(data);*/

        if (data.message === "Success") {
            confecciones = data.confecciones;
            let opciones = ``;
            confecciones.forEach((confecciones) => {
                opciones += `<option value='${confecciones.id}'>${confecciones.obs}</option>`;
            });
            cboConfecciones.innerHTML = opciones;
            listarDetalles(confecciones[0].id);
        } else {
            alert("Confecciones no encontrados ...")
        }
    } catch (error) {
        console.log(error);
    }

};

const listarClientes = async () => {
    try {
        const response = await fetch("./clientes");
        const data = await response.json();

        if (data.message === "Success") {
            let opciones = ``;
            data.clientes.forEach((cliente) => {
                opciones += `<option value='${cliente.id}'>${cliente.nombre}</option>`;
            });
            cboClientes.innerHTML = opciones;
            /*spContacto.innerHTML = data.cliente.;*/
            listarConfecciones(data.clientes[0].id);
        } else {
            alert("Clientes no encontrados ...")
        }
    } catch (error) {
        console.log(error);
    }
};

const cargaInicial = async () => {
    await listarClientes();

    cboClientes.addEventListener("change", (event) => {
        /*console.log(event);*/
        listarConfecciones(event.target.value);
    });

    cboConfecciones.addEventListener("change", (event) => {
        console.log(event);
        listarConfecciones(event.target.value);
    });
};

window.addEventListener("load", async () => {
    await cargaInicial();
});