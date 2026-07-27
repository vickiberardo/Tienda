<script setup>
defineProps({
  carrito: Array,
  total: Number
})

const emit = defineEmits(['finalizar'])
</script>

<template>

<section>

<h2>Carrito</h2>

<div id="carrito">

<div
v-for="item in carrito"
:key="item.id"
class="item-carrito"
>

<h3>{{ item.nombre }}</h3>

<p>Cantidad: {{ item.cantidad }}</p>

<p>Precio: ${{ item.precio }}</p>

</div>

</div>

<h3 id="total">
Total: ${{ total }}
</h3>

<button
id="btnFinalizar"
@click="emit('finalizar')"
>

Finalizar Compra

</button>

</section>

</template>