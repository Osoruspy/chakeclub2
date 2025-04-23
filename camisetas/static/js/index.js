
let confecciones = [];

const listarDetalles = async (idconfecciones) => {
    try {
        const response = await fetch(`./detalles/${idconfecciones}`);
        const data = await response.json();
        if (data.message === "Success") {
            detalles = data.detalles;
            //console.log('detalles');
            //console.log(detalles);
            let detaconf = ``;
            detalles.forEach((detalles, index) => {
                detaconf += `
                <tr>
                    <td>${index + 1}</td>
                    <td>${detalles.item}</td>
                    <td>${detalles.nombre}</td>
                    <td>${detalles.tamano}</td>
                    <td>${detalles.genero}</td>
                    <td>${detalles.item_adicional}</td>
                    <td>${detalles.numero}</td>
                    <td>${detalles.obs}</td>
                    <td class="centrado"><a href="edicionDetalle/${detalles.id}/" class="btn btn-sm btn-block btn-info"><i class="fa fa-pencil-alt"></i> Editar</a></td>
                    <td class="centrado"><a href="eliminacionDetalle/${detalles.id}/" class="btn btn-sm btn-block btn-danger btnEliminacion"><i class="fa fa-trash-alt"></i> Eliminar</a></td>
                </tr>
            `;
            });
            tbDetalles.innerHTML = detaconf;
        } else {
            tbDetalles.innerHTML = `Confecciones sin detalles`;
        }
    } catch (error) {
        console.log(error);
    }
};

const listarConfecciones = async (idClientes) => {
    try {
        const response = await fetch(`./confecciones/${idClientes}`);
        const data = await response.json();
        if (data.message === "Success") {
            confecciones = data.confecciones;
            //console.log('confecciones');
            //console.log(confecciones);
            let opciones = ``;
            let datosclientes = ``;
            let datosconfecciones = ``;
            confecciones.forEach((confecciones, index) => {
                opciones += `<option value='${confecciones.id}'>${confecciones.contacto}</option>`;
                datosclientes += `
                <tr>
                    <td>${index + 1}</td>
                    <td>${confecciones.telcontacto}</td>
                    <td>Deuda</td>
                    <td>Pagado</td>
                    <td>${confecciones.obs}</td>
                    <td class="centrado"><a href="edicionCliente/${confecciones.cliente_id}" class="btn btn-sm btn-block btn-info"><i class="fa fa-pencil-alt"></i> Editar</a></td>
                    <td class="centrado"><a href="eliminarCliente/${confecciones.cliente_id}" class="btn btn-sm btn-block btn-danger btnEliminacion"><i class="fa fa-trash-alt"></i> Eliminar</a></td>
                </tr>
                `;
            });
            cboConfecciones.innerHTML = opciones;
            tbConfecciones.innerHTML = datosclientes;
            const primeraConfeccionId = cboConfecciones.options.length > 0 ? cboConfecciones.options[0].value : null;
            aNuevoDetalle.href = primeraConfeccionId ? `nuevoDetalle/${primeraConfeccionId}/` : '#';
            /*datosconfecciones = `href="nuevaConfeccion/${confecciones.cliente_id}/"`;
            aNuevaConfeccion.href = datosconfecciones;*/
            listarDetalles(confecciones[0].id)
        } else {
            cboConfecciones.innerHTML = `<option'>Cliente sin confecciones</option>`;
            tbConfecciones.innerHTML = "Clientes sin confecciones";
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
            listarConfecciones(data.clientes[0].id);
        } else {
            alert("Clientes no encontrados ...");
        }
    } catch (error) {
        console.log(error);
    }
};

const cargaInicial = async () => {
    await listarClientes();

    cboClientes.addEventListener("change", (event) => {
        let cliente_id = event.target.value;
        datosconfecciones = `href="nuevaConfeccion/${cliente_id}/"`;
        aNuevaConfeccion.href = datosconfecciones;

        /*datosdetalles = `href="nuevoDetalle/${cliente_id}/"`;
        aNuevoDetalle.href = datosdetalles;*/

        listarConfecciones(event.target.value);
    });

    cboConfecciones.addEventListener("change", (event) => {
        let confecciones_id = event.target.value;
        datosdetalles = `href="nuevoDetalle/${confecciones_id}/"`;
        aNuevoDetalle.href = datosdetalles;
        ListarDetalles(event.target.value);
    });

};

window.addEventListener("load", async () => {
    await cargaInicial();
});

function getSelectedId() {
    const select = document.getElementById('selectItem');
    return select.value;
}

function abrirModal(url) {
    const modal = document.getElementById("popupModal");
    const iframe = document.getElementById("popupIframe");
    iframe.src = url;
    modal.style.display = "block";
}

function cerrarModal() {
    const modal = document.getElementById("popupModal");
    const iframe = document.getElementById("popupIframe");
    iframe.src = "";
    modal.style.display = "none";
}

function accionConSeleccionado(tipo) {
    const id = getSelectedId();
    if (id) {
        abrirModal(`/items/${tipo}/${id}/`);
    } else {
        alert("Selecciona un registro primero.");
    }
}

// Cerrar modal si se hace clic fuera
window.onclick = function(event) {
    const modal = document.getElementById("popupModal");
    if (event.target == modal) cerrarModal();
}
