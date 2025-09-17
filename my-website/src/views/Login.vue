<template>
  <div class="login-page">
    <div class="login-container">
      <div class="login-card">
        <div class="login-header">
          <h1 class="login-title">
            <span class="app-icon">🏢</span>
            License Manager
          </h1>
          <p class="login-subtitle">Вход в систему управления лицензиями</p>
        </div>
        
        <form @submit.prevent="handleLogin" class="login-form">
          <div class="form-group">
            <label for="login" class="form-label">Логин</label>
            <input
              id="login"
              v-model="formData.login"
              type="text"
              class="form-input"
              :class="{ error: errors.login }"
              placeholder="Введите ваш логин"
              required
            />
            <div v-if="errors.login" class="error-message">{{ errors.login }}</div>
          </div>
          
          <div class="form-group">
            <label for="password" class="form-label">Пароль</label>
            <input
              id="password"
              v-model="formData.password"
              type="password"
              class="form-input"
              :class="{ error: errors.password }"
              placeholder="Введите ваш пароль"
              required
            />
            <div v-if="errors.password" class="error-message">{{ errors.password }}</div>
          </div>
          
          <div v-if="authStore.error" class="error-message mb-2">
            {{ authStore.error }}
          </div>
          
          <button
            type="submit"
            class="btn btn-primary login-btn"
            :disabled="authStore.loading"
          >
            <span v-if="authStore.loading" class="loading-spinner">⟳</span>
            {{ authStore.loading ? 'Вход...' : 'Войти' }}
          </button>
        </form>
        
        <div class="register-link">
          <p>Нет аккаунта? <a href="#" @click="showRegister = !showRegister">Зарегистрироваться</a></p>
        </div>
        
        <!-- Форма регистрации -->
        <div v-if="showRegister" class="register-form">
          <h3>Регистрация</h3>
          <form @submit.prevent="handleRegister">
            <div class="form-group">
              <label for="regLogin" class="form-label">Логин</label>
              <input
                id="regLogin"
                v-model="registerData.login"
                type="text"
                class="form-input"
                placeholder="Введите логин"
                required
              />
            </div>
            
            <div class="form-group">
              <label for="regPassword" class="form-label">Пароль</label>
              <input
                id="regPassword"
                v-model="registerData.password"
                type="password"
                class="form-input"
                placeholder="Введите пароль"
                required
              />
            </div>
            
            <button
              type="submit"
              class="btn btn-success"
              :disabled="authStore.loading"
            >
              {{ authStore.loading ? 'Регистрация...' : 'Зарегистрироваться' }}
            </button>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { useToast } from 'vue-toastification'

export default {
  name: 'Login',
  setup() {
    const router = useRouter()
    const authStore = useAuthStore()
    const toast = useToast()
    
    const showRegister = ref(false)
    const errors = ref({})
    
    const formData = reactive({
      login: '',
      password: ''
    })
    
    const registerData = reactive({
      login: '',
      password: ''
    })
    
    const validateForm = () => {
      errors.value = {}
      
      if (!formData.login.trim()) {
        errors.value.login = 'Логин обязателен'
      }
      
      if (!formData.password.trim()) {
        errors.value.password = 'Пароль обязателен'
      }
      
      return Object.keys(errors.value).length === 0
    }
    
    const handleLogin = async () => {
      if (!validateForm()) return
      
      const result = await authStore.login(formData)
      
      if (result.success) {
        toast.success('Добро пожаловать!')
        router.push('/dashboard')
      } else {
        toast.error(result.error || 'Ошибка входа')
      }
    }
    
    const handleRegister = async () => {
      const result = await authStore.register(registerData)
      
      if (result.success) {
        toast.success('Регистрация успешна! Теперь войдите в систему')
        showRegister.value = false
        registerData.login = ''
        registerData.password = ''
      } else {
        toast.error(result.error || 'Ошибка регистрации')
      }
    }
    
    return {
      authStore,
      formData,
      registerData,
      errors,
      showRegister,
      handleLogin,
      handleRegister
    }
  }
}
</script>

<style scoped>
.login-page {
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 1rem;
}

.login-container {
  width: 100%;
  max-width: 400px;
}

.login-card {
  background: white;
  border-radius: 12px;
  box-shadow: 0 10px 25px rgba(0,0,0,0.2);
  padding: 2rem;
}

.login-header {
  text-align: center;
  margin-bottom: 2rem;
}

.login-title {
  font-size: 1.8rem;
  color: #2c3e50;
  margin-bottom: 0.5rem;
  display: flex;
  align-items: center;
  justify-content: center;
}

.app-icon {
  margin-right: 0.5rem;
  font-size: 2rem;
}

.login-subtitle {
  color: #7f8c8d;
  font-size: 0.9rem;
}

.login-form {
  margin-bottom: 1.5rem;
}

.login-btn {
  width: 100%;
  font-weight: 600;
}

.loading-spinner {
  animation: spin 1s linear infinite;
}

@keyframes spin {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

.register-link {
  text-align: center;
  margin-top: 1rem;
}

.register-link a {
  color: #3498db;
  text-decoration: none;
}

.register-link a:hover {
  text-decoration: underline;
}

.register-form {
  margin-top: 1.5rem;
  padding-top: 1.5rem;
  border-top: 1px solid #eee;
}

.register-form h3 {
  margin-bottom: 1rem;
  color: #2c3e50;
  text-align: center;
}

@media (max-width: 480px) {
  .login-card {
    padding: 1.5rem;
  }
  
  .login-title {
    font-size: 1.5rem;
  }
}
</style>
