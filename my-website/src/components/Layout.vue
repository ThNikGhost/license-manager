<template>
  <div class="layout">
    <Header />
    <div class="main-content">
      <nav class="sidebar">
        <div class="nav-menu">
          <router-link to="/dashboard" class="nav-item" :class="{ active: $route.name === 'Dashboard' }">
            <span class="nav-icon">📊</span>
            Панель управления
          </router-link>
          <router-link to="/licenses" class="nav-item" :class="{ active: $route.name === 'Licenses' }">
            <span class="nav-icon">📄</span>
            Лицензии
          </router-link>
          <router-link to="/computers" class="nav-item" :class="{ active: $route.name === 'Computers' }">
            <span class="nav-icon">💻</span>
            Компьютеры
          </router-link>
        </div>
      </nav>
      <main class="content">
        <slot />
      </main>
    </div>
  </div>
</template>

<script>
import Header from './Header.vue'

export default {
  name: 'Layout',
  components: {
    Header
  }
}
</script>

<style scoped>
.layout {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

.main-content {
  display: flex;
  flex: 1;
}

.sidebar {
  width: 250px;
  background: #2c3e50;
  color: white;
  padding: 1rem 0;
}

.nav-menu {
  display: flex;
  flex-direction: column;
}

.nav-item {
  display: flex;
  align-items: center;
  padding: 1rem 1.5rem;
  color: #bdc3c7;
  text-decoration: none;
  transition: all 0.3s ease;
}

.nav-item:hover {
  background: #34495e;
  color: white;
}

.nav-item.active {
  background: #3498db;
  color: white;
}

.nav-icon {
  margin-right: 0.5rem;
  font-size: 1.2rem;
}

.content {
  flex: 1;
  padding: 2rem;
  background: #f8f9fa;
  overflow-y: auto;
}

@media (max-width: 768px) {
  .main-content {
    flex-direction: column;
  }
  
  .sidebar {
    width: 100%;
  }
  
  .nav-menu {
    flex-direction: row;
    justify-content: space-around;
  }
  
  .nav-item {
    flex: 1;
    justify-content: center;
    padding: 0.75rem;
  }
  
  .nav-icon {
    margin-right: 0.25rem;
  }
}
</style>
