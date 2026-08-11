<script setup>
const props = defineProps({
  actividades: { type: Array, required: true }
})

const formatNumber = (num) => {
  return new Intl.NumberFormat('es-CO', { minimumFractionDigits: 2, maximumFractionDigits: 2 }).format(num)
}

const getStatus = (act) => {
  if (act.completado === undefined || act.total === undefined || act.total === 0) return 'not-started'
  if (act.completado > act.total) return 'exceeded'
  if (act.completado === act.total) return 'completed'
  if (act.completado > 0) return 'in-progress'
  return 'not-started'
}
</script>

<template>
  <div class="card-container activities-card">
    <div class="activities-grid">
      <div v-for="(act, index) in actividades" :key="index" class="activity-item">
        <div class="status-icon" :class="getStatus(act) === 'exceeded' ? 'completed' : getStatus(act)">
          {{ (getStatus(act) === 'completed' || getStatus(act) === 'exceeded') ? '✓' : '!' }}
        </div>

        <div class="act-details">
          <div class="act-name">{{ act.nombre }}: <span v-if="act.porcentaje !== undefined" class="text-green font-bold">{{ act.porcentaje }}%</span></div>
          <div v-if="act.completado !== undefined" class="act-progress">
            <span class="font-bold" :class="getStatus(act) === 'exceeded' ? 'text-red' : 'text-blue'">{{ formatNumber(act.completado) }} {{ act.unidad }}</span> / {{ formatNumber(act.total) }} {{ act.unidad }}
            <span v-if="getStatus(act) === 'exceeded'" class="exceeded-badge">¡Supera la meta!</span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.activities-card {
  flex: 1;
  min-height: 0;
  padding: 1.5vh;
  overflow: hidden;
}

.activities-grid {
  column-count: 2;
  column-gap: 3.5vw;
  column-rule: 2px solid var(--color-border);
  height: 100%;
}

.activity-item {
  display: flex;
  align-items: center;
  gap: 1vw;
  padding: 0.5vh 0;
  border-bottom: 1px solid #f0f0f0;
  break-inside: avoid;
  margin-bottom: 1.5vh;
}

.status-icon {
  border-radius: 50%;
  width: 2.2vh;
  height: 2.2vh;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.2vh;
  flex-shrink: 0;
  color: white;
  font-weight: bold;
}

.status-icon.completed {
  background-color: var(--color-primary);
}

.status-icon.in-progress {
  background-color: #f59e0b; /* Amarillo/Naranja */
}

.status-icon.not-started {
  background-color: #ef4444; /* Rojo */
}

.status-icon.exceeded {
  background-color: #dc2626; /* Rojo Oscuro */
  font-size: 1vh;
}



.act-details {
  font-size: 1.5vh;
  line-height: 1.3;
}

.act-name {
  color: var(--color-text-main);
}

.act-progress {
  color: var(--color-text-muted);
  font-size: 1.35vh;
}

.text-red {
  color: #dc2626;
}

.exceeded-badge {
  background-color: #fef2f2;
  color: #dc2626;
  font-size: 1vh;
  padding: 0.2vh 0.6vh;
  border-radius: 1vh;
  font-weight: bold;
  margin-left: 0.5vw;
  border: 1px solid #fca5a5;
}

@media (max-width: 1024px) {
  .activities-card {
    overflow: visible;
  }

  .activities-grid {
    column-count: 1;
    height: auto;
  }

  .act-details {
    font-size: clamp(0.85rem, 2vw, 1rem);
  }

  .act-progress {
    font-size: clamp(0.75rem, 1.8vw, 0.9rem);
  }
}
</style>
