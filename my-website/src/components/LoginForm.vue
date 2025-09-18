<template>
  <div class="login-container">
    <div class="login-form">
      <h2>Вход в систему</h2>
      
      <form @submit.prevent="handleLogin">
        <div class="form-group">
          <label for="username">Логин:</label>
          <input
            type="text"
            id="username"
            v-model="username"
            placeholder="Введите логин"
            required
          />
        </div>
        
        <div class="form-group">
          <label for="password">Пароль:</label>
          <input
            type="password"
            id="password"
            v-model="password"
            placeholder="Введите пароль"
            required
          />
        </div>
        
        <button type="submit" class="login-btn">Войти</button>
        
        <div v-if="errorMessage" class="error-message">
          {{ errorMessage }}
        </div>
      </form>
      
      <div class="login-hint">
        <p>Подсказка: логин: <strong>admin</strong>, пароль: <strong>123</strong></p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'

// Определяем событие для родительского компонента
const emit = defineEmits(['login-success'])

// Реактивные данные
const username = ref('')
const password = ref('')
const errorMessage = ref('')

// Функция обработки входа
const handleLogin = () => {
  // Простая проверка логина и пароля
  if (username.value === 'admin' && password.value === '123') {
    errorMessage.value = ''
    emit('login-success', { username: username.value })
  } else {
    errorMessage.value = 'Неверный логин или пароль!'
  }
}
</script>

<style scoped>
.login-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.login-form {
  background: white;
  padding: 2rem;
  border-radius: 10px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
  width: 100%;
  max-width: 400px;
}

h2 {
  text-align: center;
  color: #333;
  margin-bottom: 1.5rem;
}

.form-group {
  margin-bottom: 1rem;
}

label {
  display: block;
  margin-bottom: 0.5rem;
  color: #555;
  font-weight: bold;
}

input {
  width: 100%;
  padding: 0.75rem;
  border: 2px solid #ddd;
  border-radius: 5px;
  font-size: 1rem;
  transition: border-color 0.3s;
}

input:focus {
  outline: none;
  border-color: #667eea;
}

.login-btn {
  width: 100%;
  padding: 0.75rem;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border: none;
  border-radius: 5px;
  font-size: 1rem;
  font-weight: bold;
  cursor: pointer;
  transition: transform 0.2s;
}

.login-btn:hover {
  transform: translateY(-2px);
}

.error-message {
  margin-top: 1rem;
  padding: 0.5rem;
  background: #fee;
  color: #c33;
  border-radius: 5px;
  text-align: center;
  border: 1px solid #fcc;
}

.login-hint {
  margin-top: 1.5rem;
  padding: 1rem;
  background: #f0f8ff;
  border-radius: 5px;
  border-left: 4px solid #667eea;
}

.login-hint p {
  margin: 0;
  color: #555;
  font-size: 0.9rem;
}
</style>