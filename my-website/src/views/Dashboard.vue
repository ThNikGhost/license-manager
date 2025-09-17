<template>
  <div class="dashboard">
    <div class="dashboard-header">
      <h1>Панель управления</h1>
      <p>Обзор системы управления лицензиями</p>
    </div>
    
    <!-- Статистические карточки -->
    <div class="stats-grid">
      <div class="stat-card">
        <div class="stat-icon">📄</div>
        <div class="stat-content">
          <h3>{{ totalLicenses }}</h3>
          <p>Всего лицензий</p>
        </div>
      </div>
      
      <div class="stat-card">
        <div class="stat-icon">✅</div>
        <div class="stat-content">
          <h3>{{ activeLicenses }}</h3>
          <p>Активных лицензий</p>
        </div>
      </div>
      
      <div class="stat-card">
        <div class="stat-icon">⚠️</div>
        <div class="stat-content">
          <h3>{{ expiredLicenses }}</h3>
          <p>Истекших лицензий</p>
        </div>
      </div>
      
      <div class="stat-card">
        <div class="stat-icon">💻</div>
        <div class="stat-content">
          <h3>{{ totalComputers }}</h3>
          <p>Компьютеров</p>
        </div>
      </div>
      
      <div class="stat-card">
        <div class="stat-icon">💰</div>
        <div class="stat-content">
          <h3>${{ totalBudget.toLocaleString() }}</h3>
          <p>Общий бюджет</p>
        </div>
      </div>
    </div>
    
    <!-- Быстрые действия -->
    <div class="quick-actions">
      <h2>Быстрые действия</h2>
      <div class="actions-grid">
        <router-link to="/licenses" class="action-card">
          <div class="action-icon">📄</div>
          <h3>Управление лицензиями</h3>
          <p>Добавить, редактировать или удалить лицензии</p>
        </router-link>
        
        <router-link to="/computers" class="action-card">
          <div class="action-icon">💻</div>
          <h3>Управление компьютерами</h3>
          <p>Добавить или удалить компьютеры</p>
        </router-link>
        
        <a href="#" @click="searchExpiring" class="action-card">
          <div class="action-icon">⏰</div>
          <h3>Лицензии истекают</h3>
          <p>Посмотреть лицензии, которые скоро истекут</p>
        </a>
      </div>
    </div>
    
    <!-- Последние лицензии -->
    <div class="recent-licenses" v-if="recentLicenses.length">
      <h2>Последние добавленные лицензии</h2>
      <div class="card">
        <table class="table">
          <thead>
            <tr>
              <th>ПО</th>
              <th>Компьютер</th>
              <th>Дата начала</th>
              <th>Дата окончания</th>
              <th>Бюджет</th>
              <th>Статус</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="license in recentLicenses" :key="license.id">
              <td>{{ license.software }}</td>
              <td>{{ getComputerName(license.computer_id) }}</td>
              <td>{{ formatDate(license.license_start) }}</td>
              <td>{{ formatDate(license.license_end) }}</td>
              <td>${{ license.budget?.toLocaleString() || 0 }}</td>
              <td>
                <span :class="['status', getStatusClass(license)]">
                  {{ getStatusText(license) }}
                </span>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useLicensesStore } from '@/stores/licenses'
import { useComputersStore } from '@/stores/computers'
import { format } from 'date-fns'
import { ru } from 'date-fns/locale'

export default {
  name: 'Dashboard',
  setup() {
    const router = useRouter()
    const licensesStore = useLicensesStore()
    const computersStore = useComputersStore()
    
    const loading = ref(true)
    
    const totalLicenses = computed(() => licensesStore.licenses.length)
    const activeLicenses = computed(() => licensesStore.activeLicenses.length)
    const expiredLicenses = computed(() => licensesStore.expiredLicenses.length)
    const totalComputers = computed(() => computersStore.computers.length)
    const totalBudget = computed(() => licensesStore.totalBudget)
    
    const recentLicenses = computed(() => {
      return [...licensesStore.licenses]
        .sort((a, b) => new Date(b.license_start) - new Date(a.license_start))
        .slice(0, 5)
    })
    
    const getComputerName = (computerId) => {
      const computer = computersStore.getComputerById(computerId)
      return computer ? `${computer.computer_name} (${computer.room_number})` : 'Неизвестно'
    }
    
    const formatDate = (dateString) => {
      if (!dateString) return '-'
      try {
        return format(new Date(dateString), 'dd.MM.yyyy', { locale: ru })
      } catch {
        return dateString
      }
    }
    
    const getStatusClass = (license) => {
      const today = new Date().toISOString().split('T')[0]
      if (license.license_end < today) return 'status-expired'
      
      const daysUntilExpiry = Math.ceil((new Date(license.license_end) - new Date()) / (1000 * 60 * 60 * 24))
      if (daysUntilExpiry <= 30) return 'status-warning'
      
      return 'status-active'
    }
    
    const getStatusText = (license) => {
      const today = new Date().toISOString().split('T')[0]
      if (license.license_end < today) return 'Истекла'
      
      const daysUntilExpiry = Math.ceil((new Date(license.license_end) - new Date()) / (1000 * 60 * 60 * 24))
      if (daysUntilExpiry <= 30) return `Истекает (${daysUntilExpiry} дн.)`
      
      return 'Активна'
    }
    
    const searchExpiring = () => {
      // Переходим на страницу лицензий с фильтром по истекающим
      router.push({ path: '/licenses', query: { filter: 'expiring' } })
    }
    
    const loadData = async () => {
      loading.value = true
      try {
        await Promise.all([
          licensesStore.fetchLicenses(),
          computersStore.fetchComputers()
        ])
      } catch (error) {
        console.error('Ошибка загрузки данных:', error)
      } finally {
        loading.value = false
      }
    }
    
    onMounted(() => {
      loadData()
    })
    
    return {
      loading,
      totalLicenses,
      activeLicenses,
      expiredLicenses,
      totalComputers,
      totalBudget,
      recentLicenses,
      getComputerName,
      formatDate,
      getStatusClass,
      getStatusText,
      searchExpiring
    }
  }
}
</script>

<style scoped>
.dashboard {
  max-width: 1200px;
  margin: 0 auto;
}

.dashboard-header {
  margin-bottom: 2rem;
}

.dashboard-header h1 {
  font-size: 2rem;
  color: #2c3e50;
  margin-bottom: 0.5rem;
}

.dashboard-header p {
  color: #7f8c8d;
  font-size: 1.1rem;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1rem;
  margin-bottom: 2rem;
}

.stat-card {
  background: white;
  border-radius: 8px;
  padding: 1.5rem;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
  display: flex;
  align-items: center;
  transition: transform 0.2s ease;
}

.stat-card:hover {
  transform: translateY(-2px);
}

.stat-icon {
  font-size: 2rem;
  margin-right: 1rem;
}

.stat-content h3 {
  font-size: 1.8rem;
  color: #2c3e50;
  margin: 0;
}

.stat-content p {
  color: #7f8c8d;
  margin: 0;
  font-size: 0.9rem;
}

.quick-actions {
  margin-bottom: 2rem;
}

.quick-actions h2 {
  color: #2c3e50;
  margin-bottom: 1rem;
}

.actions-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1rem;
}

.action-card {
  background: white;
  border-radius: 8px;
  padding: 1.5rem;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
  text-decoration: none;
  color: inherit;
  transition: all 0.2s ease;
  border: 2px solid transparent;
}

.action-card:hover {
  transform: translateY(-2px);
  border-color: #3498db;
  color: inherit;
  text-decoration: none;
}

.action-icon {
  font-size: 2.5rem;
  margin-bottom: 1rem;
}

.action-card h3 {
  color: #2c3e50;
  margin-bottom: 0.5rem;
}

.action-card p {
  color: #7f8c8d;
  margin: 0;
  font-size: 0.9rem;
}

.recent-licenses h2 {
  color: #2c3e50;
  margin-bottom: 1rem;
}

.status {
  padding: 0.25rem 0.5rem;
  border-radius: 12px;
  font-size: 0.8rem;
  font-weight: 500;
}

.status-active {
  background: #d5f4e6;
  color: #27ae60;
}

.status-warning {
  background: #fcf3cd;
  color: #f39c12;
}

.status-expired {
  background: #fadbd8;
  color: #e74c3c;
}

@media (max-width: 768px) {
  .stats-grid {
    grid-template-columns: 1fr;
  }
  
  .actions-grid {
    grid-template-columns: 1fr;
  }
  
  .stat-card {
    flex-direction: column;
    text-align: center;
  }
  
  .stat-icon {
    margin-right: 0;
    margin-bottom: 0.5rem;
  }
}
</style>
