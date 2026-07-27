<script setup>
defineProps({
  producto: Object
})

const emit = defineEmits(['agregar'])
</script>

<template>
  <div class="card">

    <h3>{{ producto.nombre }}</h3>

    <p>Precio: ${{ producto.precio }}</p>

    <p>Stock: {{ producto.stock }}</p>

    <button @click="emit('agregar', producto.id)">
      Agregar al carrito
    </button>

  </div>
</template>