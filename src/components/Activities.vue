<script setup>
import { computed } from 'vue'
import { Check, AlertCircle } from 'lucide-vue-next'

const props = defineProps({
  actividades: { type: Array, required: true }
})

const displayActivities = computed(() => {
  return (props.actividades || [])
    .filter(act => {
      const nom = act.nombre.toLowerCase().normalize("NFD").replace(/[\u0300-\u036f]/g, "")
      return !nom.includes('caracterizacion vial') 
          && !nom.includes('manejo ambiental')
          && !nom.includes('manejo de transito')
    })
    .map(act => {
      const isObrasTransversales = act.nombre.includes('Obras Transversales')
      return {
        ...act,
        displayName: act.nombre,
        isObrasTransversales,
        isMocked: act.total === 0 && act.completado === 0 && !act.valor_total
      }
    })
})

const formatNumber = (num) => {
  return new Intl.NumberFormat('es-CO', { minimumFractionDigits: 2, maximumFractionDigits: 2 }).format(num)
}

const getStatus = (act) => {
  if (act.isMocked) return 'pending'
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
      <div v-for="(act, index) in displayActivities" :key="index" class="activity-item">
        <div class="status-icon" :class="getStatus(act) === 'exceeded' ? 'completed' : getStatus(act)">
          <Check v-if="getStatus(act) === 'completed' || getStatus(act) === 'exceeded'" :size="14" />
          <AlertCircle v-else :size="14" />
        </div>

        <div class="act-details">
          <template v-if="act.isObrasTransversales">
            <div class="act-name">{{ act.displayName }}<span v-if="!act.isMocked">: <span class="text-green font-bold">{{ act.porcentaje }}</span></span></div>
            <div class="act-progress-group">
              <div class="act-progress">
                <span class="font-bold" :class="getStatus(act) === 'exceeded' ? 'text-red' : 'text-blue'">
                  {{ act.isMocked ? '0,00' : formatNumber(act.completado) }} {{ act.unidad }}
                </span> / {{ act.isMocked ? '0,00' : formatNumber(act.total) }} {{ act.unidad }} - Limpieza
                <span v-if="!act.isMocked && getStatus(act) === 'exceeded'" class="exceeded-badge">¡Supera la meta!</span>
              </div>
              <div class="act-progress">
                <span class="font-bold text-blue">0,00 und</span> / 0,00 und - Remplazo
              </div>
              <div class="act-progress">
                <span class="font-bold text-blue">0,00 und</span> / 0,00 und - Nuevas
              </div>
            </div>
          </template>
          
          <template v-else>
            <div class="act-name">{{ act.displayName }}<span v-if="!act.isMocked">: <span class="text-green font-bold">{{ act.porcentaje }}</span></span></div>
            <div class="act-progress">
              <span class="font-bold" :class="getStatus(act) === 'exceeded' ? 'text-red' : 'text-blue'">
                {{ act.isMocked ? '0,00' : formatNumber(act.completado) }} {{ act.unidad }}
              </span> / {{ act.isMocked ? '0,00' : formatNumber(act.total) }} {{ act.unidad }}
              <span v-if="!act.isMocked && getStatus(act) === 'exceeded'" class="exceeded-badge">¡Supera la meta!</span>
            </div>
          </template>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.activities-card {
  flex: 1;
  min-height: 0;
  padding: 1vh;
  overflow: hidden;
}

.activities-grid {
  column-count: 2;
  column-gap: 2vw;
  column-rule: 2px solid var(--color-border);
  height: 100%;
}

.activity-item {
  display: flex;
  align-items: center;
  gap: 0.8vw;
  padding: 0.5vh 0;
  border-bottom: 1px solid #f0f0f0;
  break-inside: avoid;
  margin-bottom: 1.2vh;
}

.status-icon {
  border-radius: 50%;
  width: 2vh;
  height: 2vh;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1vh;
  flex-shrink: 0;
  color: white;
  font-weight: bold;
}

.status-icon.completed {
  background-color: #16a34a; /* Verde */
}

.status-icon.in-progress {
  background-color: #f59e0b; /* Naranja */
}

.status-icon.not-started,
.status-icon.pending {
  background-color: #9ca3af; /* Gris */
}

.status-icon.exceeded {
  background-color: #16a34a; /* Verde */
  font-size: 1vh;
}



.act-progress-group {
  display: flex;
  flex-direction: column;
  gap: 0.2vh;
}

.act-details {
  font-size: 1.35vh;
  line-height: 1.3;
}

.act-name {
  color: var(--color-text-main);
}

.act-progress {
  color: var(--color-text-muted);
  font-size: 1.2vh;
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


</style>
