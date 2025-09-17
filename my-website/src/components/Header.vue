<template>
  <header class="header">
    <div class="header-left">
      <h1 class="app-title">
        <span class="app-icon">🏢</span>
        License Manager
      </h1>
    </div>
    
    <div class="header-right">
      <div class="user-info" v-if="authStore.currentUser">
        <span class="user-name">{{ authStore.currentUser.login }}</span>
        <button @click="handleLogout" class="logout-btn">
          <span class="logout-icon">🚪</span>
          Выход
        </button>
      </div>
    </div>
  </header>
</template>

<script>
import { useAuthStore } from '@/stores/auth'
import { useToast } from 'vue-toastification'

export default {
  name: 'Header',
  setup() {
    const authStore = useAuthStore()
    const toast = useToast()

    const handleLogout = () => {
      authStore.logout()
      toast.success('Вы успешно вышли из системы')
      // Роутер автоматически перенаправит на /login через navigation guard
    }

    return {
      authStore,
      handleLogout
    }
  }
}
</script>

<style scoped>
.header {
  background: #34495e;
  color: white;
  padding: 1rem 2rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.header-left {
  display: flex;
  align-items: center;
}

.app-title {
  margin: 0;
  font-size: 1.5rem;
  font-weight: 600;
  display: flex;
  align-items: center;
}

.app-icon {
  margin-right: 0.5rem;
  font-size: 1.8rem;
}

.header-right {
  display: flex;
  align-items: center;
}

.user-info {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.user-name {
  font-weight: 500;
  color: #ecf0f1;
}

.logout-btn {
  background: #e74c3c;
  color: white;
  border: none;
  padding: 0.5rem 1rem;
  border-radius: 4px;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 0.25rem;
  font-size: 0.9rem;
  transition: background-color 0.3s ease;
}

.logout-btn:hover {
  background: #c0392b;
}

.logout-icon {
  font-size: 1rem;
}

@media (max-width: 768px) {
  .header {
    padding: 1rem;
  }
  
  .app-title {
    font-size: 1.2rem;
  }
  
  .user-name {
    display: none;
  }
  
  .logout-btn {
    padding: 0.4rem 0.8rem;
    font-size: 0.8rem;
  }
}
</style>
