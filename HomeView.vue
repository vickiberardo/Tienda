<script setup>
import { ref, onMounted } from 'vue'
import api from '../services/api'
import Swal from 'sweetalert2'

import ProductoCard from '../components/ProductoCard.vue'
import Carrito from '../components/Carrito.vue'

const productos = ref([])
const carrito = ref([])
const total = ref(0)

const cargarProductos = async () => {

  const respuesta = await api.get('/productos')

  productos.value = respuesta.data

}

const cargarCarrito = async () => {

  const respuesta = await api.get('/carrito')

  carrito.value = respuesta.data

  total.value = carrito.value.reduce((acum, item) => {

    return acum + item.precio * item.cantidad

  },0)

}

const agregarAlCarrito = async(id)=>{

  await api.post('/carrito/agregar',{

    id_producto:id,
    cantidad:1

  })

  Swal.fire({
    icon:'success',
    title:'Producto agregado'
  })

  cargarCarrito()

}

const finalizarCompra = async()=>{

  await api.post('/carrito/finalizar')

  Swal.fire({
    icon:'success',
    title:'Compra realizada'
  })

  cargarProductos()
  cargarCarrito()

}

onMounted(()=>{

  cargarProductos()
  cargarCarrito()

})
</script>

<template>

<h1 class="titulo">
Tienda Online
</h1>

<section>

<h2>Productos</h2>

<div class="contenedor-productos">

<ProductoCard

v-for="producto in productos"

:key="producto.id"

:producto="producto"

@agregar="agregarAlCarrito"

/>

</div>

</section>

<hr>

<Carrito

:carrito="carrito"

:total="total"

@finalizar="finalizarCompra"

/>

</template>