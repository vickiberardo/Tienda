let productos = [];

async function cargarProductos() {

    const respuesta = await fetch(
        "http://127.0.0.1:8000/productos"
    );

    productos = await respuesta.json();

    mostrarProductos();
}

function mostrarProductos() {

    const contenedorProductos =
        document.getElementById("productos");

    contenedorProductos.innerHTML = "";

    productos.forEach(producto => {

        contenedorProductos.innerHTML += `
            <div class="card">
                <h3>${producto.nombre}</h3>
                <p>Precio: $${producto.precio}</p>
                <p>Stock: ${producto.stock}</p>

                <button onclick="agregarAlCarrito(${producto.id})">
                    Agregar al carrito
                </button>
            </div>
        `;
    });
}

async function agregarAlCarrito(id) {

    await fetch(
        "http://127.0.0.1:8000/carrito/agregar",
        {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                id_producto: id,
                cantidad: 1
            })
        }
    );

    Swal.fire({
        icon: "success",
        title: "Producto agregado"
    });

    cargarCarrito();
}


async function cargarCarrito() {

    const respuesta = await fetch(
        "http://127.0.0.1:8000/carrito"
    );

    const carrito = await respuesta.json();

    const contenedorCarrito =
        document.getElementById("carrito");

    const totalHTML =
        document.getElementById("total");

    contenedorCarrito.innerHTML = "";

    let total = 0;

    carrito.forEach(item => {

        total += item.precio * item.cantidad;

        contenedorCarrito.innerHTML += `
            <div class="item-carrito">
                <h3>${item.nombre}</h3>
                <p>Cantidad: ${item.cantidad}</p>
                <p>Precio: $${item.precio}</p>
            </div>
        `;
    });

    totalHTML.innerText =
        `Total: $${total}`;
}


async function finalizarCompra() {

    await fetch(
        "http://127.0.0.1:8000/carrito/finalizar",
        {
            method: "POST"
        }
    );

    Swal.fire({
        icon: "success",
        title: "Compra realizada"
    });

    cargarCarrito();
    cargarProductos();
}


document
    .getElementById("btnFinalizar")
    .addEventListener(
        "click",
        finalizarCompra
    );


cargarProductos();
cargarCarrito();