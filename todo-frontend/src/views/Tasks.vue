<template>
  <div class="container mt-5">
    <h3 class="mb-4">Tus Tareas</h3>

    <!-- Formulario nueva tarea -->
    <form @submit.prevent="addTask" class="mb-4">
      <div class="row g-2">
        <div class="col-md-4">
          <input v-model="newTask.title" type="text" class="form-control" placeholder="Título" required />
        </div>
        <div class="col-md-6">
          <input v-model="newTask.description" type="text" class="form-control" placeholder="Descripción" />
        </div>
        <div class="col-md-2">
          <button class="btn btn-primary w-100" type="submit">Agregar</button>
        </div>
      </div>
    </form>

    <!-- Filtros -->
    <div class="mb-3">
      <button
        class="btn me-2"
        :class="filter === 'all' ? 'btn-secondary' : 'btn-outline-secondary'"
        @click="filter = 'all'"
      >
        Todas
      </button>
      <button
        class="btn me-2"
        :class="filter === 'pending' ? 'btn-secondary' : 'btn-outline-secondary'"
        @click="filter = 'pending'"
      >
        Pendientes
      </button>
      <button
        class="btn"
        :class="filter === 'completed' ? 'btn-secondary' : 'btn-outline-secondary'"
        @click="filter = 'completed'"
      >
        Completadas
      </button>
    </div>

    <!-- Lista de tareas -->
    <ul class="list-group">
      <li
        v-for="task in filteredTasks"
        :key="task.id"
        class="list-group-item d-flex justify-content-between align-items-center"
      >
        <div>
          <input
            type="checkbox"
            class="form-check-input me-2"
            :checked="task.status === 'completed'"
            @change="toggleStatus(task)"
          />
          <span :class="{ 'text-decoration-line-through text-muted': task.status === 'completed' }">
            <strong>{{ task.title }}</strong>: {{ task.description }}
          </span>
        </div>

        <div>
          <button class="btn btn-sm btn-warning me-2" @click="editTask(task)">Editar</button>
          <button class="btn btn-sm btn-danger" @click="deleteTask(task.id)">Eliminar</button>
        </div>
      </li>
    </ul>

    <!-- Modal edición -->
    <div v-if="editingTask" class="modal fade show d-block" style="background: rgba(0, 0, 0, 0.5);">
      <div class="modal-dialog">
        <div class="modal-content">
          <form @submit.prevent="updateTask">
            <div class="modal-header">
              <h5 class="modal-title">Editar Tarea</h5>
              <button type="button" class="btn-close" @click="editingTask = null"></button>
            </div>
            <div class="modal-body">
              <input v-model="editingTask.title" class="form-control mb-2" required />
              <input v-model="editingTask.description" class="form-control" />
            </div>
            <div class="modal-footer">
              <button type="submit" class="btn btn-success">Guardar</button>
              <button type="button" class="btn btn-secondary" @click="editingTask = null">Cancelar</button>
            </div>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { onMounted, ref, computed } from 'vue'
import axios from 'axios'

const tasks = ref([])
const newTask = ref({ title: '', description: '' })
const editingTask = ref(null)
const filter = ref('all')

// Obtener token desde localStorage
const token = localStorage.getItem('token')

// Axios config
const api = axios.create({
  baseURL: 'http://localhost:8000', // <-- Cambia si es necesario
  headers: {
    Authorization: `Bearer ${token}`,
  },
})

const fetchTasks = async () => {
  try {
    const response = await api.get('/tasks/')
    tasks.value = response.data
  } catch (err) {
    alert('Error al obtener tareas')
  }
}

onMounted(fetchTasks)

const filteredTasks = computed(() => {
  if (filter.value === 'all') return tasks.value
  return tasks.value.filter((task) => task.status === filter.value)
})

const addTask = async () => {
  if (!newTask.value.title.trim()) return

  try {
    const response = await api.post('/tasks/', {
      title: newTask.value.title,
      description: newTask.value.description,
    })
    tasks.value.push(response.data)
    newTask.value.title = ''
    newTask.value.description = ''
  } catch (err) {
    alert('Error al agregar tarea')
  }
}

const toggleStatus = async (task) => {
  try {
    const newStatus = task.status === 'completed' ? 'pending' : 'completed'
    const response = await api.put(`/tasks/${task.id}/`, {
      ...task,
      status: newStatus,
    })
    task.status = response.data.status
  } catch (err) {
    alert('Error al cambiar estado')
  }
}

const deleteTask = async (id) => {
  try {
    await api.delete(`/tasks/${id}/`)
    tasks.value = tasks.value.filter((task) => task.id !== id)
  } catch (err) {
    alert('Error al eliminar tarea')
  }
}

const editTask = (task) => {
  editingTask.value = { ...task }
}

const updateTask = async () => {
  try {
    const response = await api.put(`/tasks/${editingTask.value.id}/`, editingTask.value)
    const index = tasks.value.findIndex((t) => t.id === editingTask.value.id)
    if (index !== -1) {
      tasks.value[index] = response.data
    }
    editingTask.value = null
  } catch (err) {
    alert('Error al actualizar tarea')
  }
}
</script>