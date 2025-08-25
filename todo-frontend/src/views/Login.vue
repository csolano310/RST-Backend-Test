<template>
  <div class="container mt-5" style="max-width: 400px;">
    <h3 class="mb-4">Iniciar sesión</h3>
    <form @submit.prevent="login">
      <div class="mb-3">
        <label>Email</label>
        <input v-model="email" type="email" class="form-control" required />
      </div>
      <div class="mb-3">
        <label>Contraseña</label>
        <input v-model="password" type="password" class="form-control" required />
      </div>
      <button class="btn btn-primary w-100" type="submit">Entrar</button>
    </form>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import axios from 'axios'

const email = ref('')
const password = ref('')

const login = async () => {
  try {
    const response = await axios.post('http://localhost:8000/auth/login', {
      email: email.value,
      password: password.value
    })
    localStorage.setItem('token', response.data.token)
    alert('Login exitoso')
  } catch (err) {
    alert('Error al iniciar sesión')
  }
}
</script>