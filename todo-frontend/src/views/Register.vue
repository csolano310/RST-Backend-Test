<template>
  <div class="container mt-5" style="max-width: 400px;">
    <h3 class="mb-4">Registro</h3>
    <form @submit.prevent="register">
      <div class="mb-3">
        <label>Nombre</label>
        <input v-model="name" type="text" class="form-control" required />
      </div>
      <div class="mb-3">
        <label>Email</label>
        <input v-model="email" type="email" class="form-control" required />
      </div>
      <div class="mb-3">
        <label>Contraseña</label>
        <input v-model="password" type="password" class="form-control" required />
      </div>
      <button class="btn btn-success w-100" type="submit">Registrar</button>
    </form>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import axios from 'axios'

const name = ref('')
const email = ref('')
const password = ref('')

const register = async () => {
  try {
    await axios.post('http://localhost:8000/auth/register', {
      name: name.value,
      email: email.value,
      password: password.value
    })
    alert('Registro exitoso')
  } catch (err) {
    alert('Error al registrar')
  }
}
</script>