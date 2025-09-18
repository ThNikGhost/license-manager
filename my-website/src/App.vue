<template>
  <div id="app">
    <!-- Login Screen -->
    <div class="login-container" v-if="currentScreen === 'login'">
      <div class="main-container">
        <div class="content">
          <h1 class="main-title">License Manager</h1>
          <h2 class="subtitle">Добро пожаловать, Барабулька</h2>
          
          <form class="login-form" @submit.prevent="login">
            <div class="form-group">
              <label for="login">Логин:</label>
              <input type="text" id="login" v-model="loginForm.username" required>
            </div>
            
            <div class="form-group">
              <label for="password">Пароль:</label>
              <input type="password" id="password" v-model="loginForm.password" required>
            </div>
            
            <button type="submit" class="btn btn-primary">Вход</button>
            
            <div class="login-links">
              <a href="#">Регистрация</a>
              <a href="#">Забыли пароль?</a>
            </div>
          </form>
        </div>
      </div>
    </div>
    
    <!-- Main Dashboard -->
    <div class="dashboard" v-if="currentScreen === 'dashboard'">
      <!-- Sidebar -->
      <div class="sidebar">
        <div class="user-profile">
          <div class="user-avatar">ВБ</div>
          <div class="user-name">Вика Барабулька!</div>
        </div>
        
        <ul class="nav-menu">
          <li class="nav-item" :class="{ active: currentView === 'status' }" @click="currentView = 'status'">
            <i class="fas fa-chart-bar"></i> Состояние
          </li>
          <li class="nav-item" :class="{ active: currentView === 'licenses' }" @click="currentView = 'licenses'">
            <i class="fas fa-key"></i> Лицензии
          </li>
          <li class="nav-item" :class="{ active: currentView === 'settings' }" @click="currentView = 'settings'">
            <i class="fas fa-cog"></i> Настройки
          </li>
          <li class="nav-item" @click="logout">
            <i class="fas fa-sign-out-alt"></i> Выход
          </li>
        </ul>
      </div>
      
      <!-- Main Content -->
      <div class="main-content">
        <!-- Status View -->
        <div v-if="currentView === 'status'">
          <div class="header-section">
            <h1>ВБ</h1>
            <h2>Вика Барабулька</h2>
          </div>

          <div class="welcome-section">
            <h3>Здравствуйте, Вика</h3>
            <p>Состояние ваших лицензий</p>
          </div>

          <div class="stats-grid">
            <div class="stat-card">
              <div class="stat-title">Работают</div>
              <div class="stat-value">60</div>
            </div>
            <div class="stat-card">
              <div class="stat-title">Лицензии истекают</div>
              <div class="stat-value">10</div>
            </div>
            <div class="stat-card">
              <div class="stat-title">Лицензии истекли</div>
              <div class="stat-value">2</div>
            </div>
            <div class="stat-card total">
              <div class="stat-title">Всего лицензий</div>
              <div class="stat-value">72</div>
            </div>
          </div>
        </div>
        
        <!-- Licenses View -->
        <div v-if="currentView === 'licenses'">
          <h2 class="page-title">Управление лицензиями</h2>
          <p>Здесь будет таблица лицензий...</p>
        </div>
        
        <!-- Settings View -->
        <div v-if="currentView === 'settings'">
          <h2 class="page-title">Настройки системы</h2>
          <p>Здесь будут настройки...</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'App',
  data() {
    return {
      currentScreen: 'login',
      currentView: 'status',
      loginForm: {
        username: '',
        password: ''
      }
    }
  },
  methods: {
    login() {
      if (this.loginForm.username && this.loginForm.password) {
        this.currentScreen = 'dashboard';
      }
    },
    logout() {
      this.currentScreen = 'login';
      this.loginForm.username = '';
      this.loginForm.password = '';
    }
  }
}
</script>

<style>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

html, body, #app {
  margin: 0;
  height: 100%;
  font-family: Arial, 'Inter', sans-serif;
}

body {
  background: linear-gradient(180deg, #041628 0%, #032d4a 100%);
  min-height: 100vh;
}

#app {
  width: 100vw;
  height: 100vh;
  overflow: hidden;
}

/* Login Screen Styles */
.login-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  width: 100vw;
}

.main-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  width: 100vw;
  text-align: center;
}

.content {
  max-width: 960px;
  padding: 20px;
}

/* Main Title */
.main-title {
  font-size: 56px;
  font-weight: 800;
  color: #FFFFFF;
  text-shadow: 0 6px 18px rgba(0, 0, 0, 0.65);
  margin: 0;
  line-height: 1.05;
  letter-spacing: -0.5px;
  font-family: Arial, 'Inter', sans-serif;
}

/* Subtitle */
.subtitle {
  font-size: 24px;
  font-weight: 600;
  color: #66E0FF;
  text-shadow: 0 3px 10px rgba(0, 0, 0, 0.55);
  margin-top: 16px;
  line-height: 1.3;
  font-family: Arial, 'Inter', sans-serif;
}

/* Login Form */
.login-form {
  width: 400px;
  margin: 40px auto 0;
  background: rgba(255, 255, 255, 0.95);
  padding: 30px;
  border-radius: 12px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
}

.form-group {
  margin-bottom: 25px;
  width: 100%;
  text-align: left;
}

.form-group label {
  display: block;
  margin-bottom: 10px;
  font-weight: 600;
  color: #2d3748;
  font-size: 16px;
}

.form-group input {
  width: 100%;
  padding: 16px;
  border: 2px solid #e1e5eb;
  border-radius: 10px;
  font-size: 16px;
  transition: border 0.3s;
  background: white;
}

.form-group input:focus {
  border-color: #4361ee;
  outline: none;
  box-shadow: 0 0 0 3px rgba(67, 97, 238, 0.1);
}

.btn {
  padding: 16px;
  border: none;
  border-radius: 10px;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s;
  width: 100%;
}

.btn-primary {
  background: #4361ee;
  color: white;
}

.btn-primary:hover {
  background: #3a56d4;
  transform: translateY(-2px);
  box-shadow: 0 5px 15px rgba(67, 97, 238, 0.3);
}

.login-links {
  display: flex;
  justify-content: space-between;
  width: 100%;
  margin-top: 20px;
}

.login-links a {
  color: #4361ee;
  text-decoration: none;
  font-size: 15px;
  font-weight: 500;
}

.login-links a:hover {
  text-decoration: underline;
}

/* Main Content Area */
.main-content-area {
  width: 100%;
  max-width: 960px;
  margin-top: 40px;
  min-height: 200px;
}

/* Dashboard Styles */
.dashboard {
  display: flex;
  width: 100vw;
  height: 100vh;
}

.sidebar {
  width: 280px;
  background: #2d3748;
  color: white;
  padding: 30px 0;
  flex-shrink: 0;
  height: 100vh;
}

.user-profile {
  text-align: center;
  padding: 25px;
  border-bottom: 1px solid #4a5568;
}

.user-avatar {
  width: 80px;
  height: 80px;
  border-radius: 50%;
  background: #4361ee;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 32px;
  margin: 0 auto 15px;
  color: white;
  font-weight: 600;
}

.user-name {
  font-weight: 600;
  font-size: 18px;
  color: white;
}

.nav-menu {
  list-style: none;
  padding: 25px 0;
}

.nav-item {
  padding: 16px 25px;
  cursor: pointer;
  transition: background 0.3s;
  display: flex;
  align-items: center;
  font-size: 16px;
  border-left: 4px solid transparent;
}

.nav-item:hover {
  background: #4a5568;
  border-left-color: #4361ee;
}

.nav-item i {
  margin-right: 15px;
  width: 20px;
  text-align: center;
  font-size: 18px;
}

.nav-item.active {
  background: #4361ee;
  border-left-color: white;
}

.main-content {
  flex: 1;
  padding: 40px;
  background: #f7fafc;
  overflow-y: auto;
  height: 100vh;
  width: calc(100vw - 280px);
}

/* Status View Styles */
.header-section {
  margin-bottom: 40px;
}

.header-section h1 {
  font-size: 48px;
  font-weight: 700;
  color: #2d3748;
  margin-bottom: 10px;
}

.header-section h2 {
  font-size: 24px;
  color: #718096;
  font-weight: 500;
}

.info-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 25px;
  margin-bottom: 40px;
}

.info-card {
  background: white;
  border-radius: 12px;
  padding: 25px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
}

.info-card h3 {
  font-size: 20px;
  font-weight: 600;
  color: #2d3748;
  margin-bottom: 20px;
  padding-bottom: 15px;
  border-bottom: 2px solid #e2e8f0;
}

.info-list {
  list-style: none;
}

.info-list li {
  padding: 12px 0;
  font-size: 16px;
  color: #4a5568;
  border-bottom: 1px solid #f1f5f9;
}

.info-list li:last-child {
  border-bottom: none;
}

.welcome-section {
  margin-bottom: 35px;
}

.welcome-section h3 {
  font-size: 28px;
  font-weight: 600;
  color: #2d3748;
  margin-bottom: 10px;
}

.welcome-section p {
  font-size: 18px;
  color: #718096;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 25px;
  margin-bottom: 40px;
}

.stat-card {
  background: white;
  border-radius: 12px;
  padding: 30px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
  text-align: center;
  transition: transform 0.3s;
}

.stat-card:hover {
  transform: translateY(-5px);
}

.stat-card.total {
  border-top: 4px solid #4361ee;
  background: linear-gradient(135deg, #4361ee 0%, #3a56d4 100%);
  color: white;
}

.stat-title {
  font-size: 16px;
  color: #718096;
  margin-bottom: 15px;
  font-weight: 500;
}

.stat-card.total .stat-title {
  color: rgba(255, 255, 255, 0.9);
}

.stat-value {
  font-size: 42px;
  font-weight: 700;
  margin-bottom: 5px;
}

.stat-card.total .stat-value {
  color: white;
}

.details-section {
  background: white;
  border-radius: 12px;
  padding: 30px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
}

.details-section h3 {
  font-size: 24px;
  font-weight: 600;
  color: #2d3748;
  margin-bottom: 20px;
}

.details-btn {
  padding: 15px 30px;
  background: #4361ee;
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s;
}

.details-btn:hover {
  background: #3a56d4;
  transform: translateY(-2px);
  box-shadow: 0 5px 15px rgba(67, 97, 238, 0.3);
}

/* Table Styles */
.licenses-table {
  background: white;
  border-radius: 12px;
  overflow-x: auto;
  box-shadow: 0 6px 12px rgba(0, 0, 0, 0.08);
  margin-top: 20px;
}

table {
  width: auto;
  min-width: 100%;
  border-collapse: collapse;
}

th, td {
  padding: 18px;
  text-align: left;
  border-bottom: 1px solid #e2e8f0;
  font-size: 15px;
}

th {
  background: #f7fafc;
  font-weight: 600;
  color: #4a5568;
  font-size: 16px;
  padding: 20px;
}

.status-badge {
  padding: 8px 16px;
  border-radius: 20px;
  font-size: 14px;
  font-weight: 500;
  display: inline-block;
  min-width: 120px;
  text-align: center;
}

.status-ok {
  background: #c6f6d5;
  color: #276749;
}

.status-warning {
  background: #fefcbf;
  color: #744210;
}

.status-error {
  background: #fed7d7;
  color: #c53030;
}

.room-header {
  background: #edf2f7;
  font-weight: 600;
  font-size: 16px;
}

/* Settings Styles */
.settings-container {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 30px;
  margin-top: 20px;
}

.settings-card {
  background: white;
  border-radius: 12px;
  padding: 30px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
}

.page-title {
  font-size: 28px;
  font-weight: 600;
  margin-bottom: 25px;
  color: #2d3748;
}
</style>