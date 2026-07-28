<script setup>
import { ref, computed, watch } from 'vue'
import dbData from './data/db.json'
import ProgressSection from './components/ProgressSection.vue'
import Activities from './components/Activities.vue'
import PhotoGallery from './components/PhotoGallery.vue'
import Observations from './components/Observations.vue'

const data = ref(dbData)
const subregiones = computed(() => data.value.subregiones || [])

const selectedSubregionName = ref(subregiones.value.length > 0 ? subregiones.value[0].nombre : null)

const subregionActual = computed(() => {
  return subregiones.value.find(s => s.nombre === selectedSubregionName.value)
})

const selectedCircuitoId = ref(null)

watch(subregionActual, (newSubregion) => {
  if (newSubregion && newSubregion.circuitos.length > 0) {
    selectedCircuitoId.value = newSubregion.circuitos[0].id
  } else {
    selectedCircuitoId.value = null
  }
}, { immediate: true })

const circuitoActual = computed(() => {
  if (!subregionActual.value) return null
  return subregionActual.value.circuitos.find(c => c.id === selectedCircuitoId.value)
})

const corteActual = computed(() => {
  if (!circuitoActual.value) return null
  return circuitoActual.value.cortes_semanales[0]
})

const formatCurrency = (value) => {
  return new Intl.NumberFormat('es-CO', { style: 'decimal', minimumFractionDigits: 0 }).format(value)
}
</script>

<template>
  <div class="dashboard-wrapper">
    <!-- Controles DEV -->
    <div class="dev-controls">
      <label>Subregión: 
        <select v-model="selectedSubregionName">
          <option v-for="sub in subregiones" :key="sub.nombre" :value="sub.nombre">
            {{ sub.nombre }}
          </option>
        </select>
      </label>
      <label v-if="subregionActual">Circuito: 
        <select v-model="selectedCircuitoId">
          <option v-for="c in subregionActual.circuitos" :key="c.id" :value="c.id">
            {{ c.corredor_vial }}
          </option>
        </select>
      </label>
    </div>

    <!-- MAIN DASHBOARD -->
    <main v-if="corteActual" class="dashboard-container">
      <div class="dashboard-grid">
        
        <!-- COLUMNA IZQUIERDA -->
        <div class="left-column">
          <!-- HEADER -->
          <header class="main-header">
            <h1>INFORME DE AVANCE DE OBRA</h1>
            <h2 class="text-green">Corredor vial {{ circuitoActual.corredor_vial }}</h2>
            <p class="subtitle">Resumen ejecutivo y avance de actividades</p>
          </header>

          <!-- VALOR DEL CONTRATO -->
          <div class="contract-value bg-dark-green">
            <span class="icon">📄</span>
            <h2>Valor del contrato: $ {{ formatCurrency(circuitoActual.valor_contrato) }}</h2>
          </div>
          
          <!-- RIBBON PROGRESS -->
          <div style="display:flex; align-items:center; margin-top: 1vh;">
            <div class="section-ribbon">
              <span class="ribbon-icon">↗</span> Avance financiero y físico
            </div>
            <div class="ribbon-line"></div>
          </div>
          
          <!-- PROGRESO (Financiero / Físico) -->
          <ProgressSection :corte="corteActual" />
          
          <!-- RIBBON ACTIVIDADES -->
          <div class="section-ribbon" style="margin-top: 1vh;">
            <span class="ribbon-icon">✓</span> Avance de actividades ejecutadas
          </div>
          <!-- ACTIVIDADES -->
          <Activities :actividades="corteActual.actividades_ejecutadas" />
        </div>

        <!-- COLUMNA DERECHA -->
        <div class="right-column">
          <div class="top-right-decoration"></div>
          <!-- FOTOS -->
          <PhotoGallery :imagenes="corteActual.imagenes" />

          <!-- RIBBON OBSERVACIONES -->
          <div class="section-ribbon" style="margin-top: 1vh;">
            <span class="ribbon-icon">✓</span> Dificultades y observaciones técnicas
          </div>
          <!-- OBSERVACIONES -->
          <Observations :observaciones="corteActual.observaciones_tecnicas" :tipoEstructura="corteActual.tipo_estructura" />
        </div>

      </div>
    </main>
  </div>
</template>

<style scoped>
.dashboard-wrapper {
  height: 100vh;
  display: flex;
  flex-direction: column;
  background-color: white;
}

.dev-controls {
  flex: 0 0 auto;
  background: #eee;
  padding: 0.5vh 1vw;
  display: flex;
  gap: 1vw;
  font-size: 1.4vh;
}

.dashboard-container {
  flex: 1;
  padding: 1.5vh 2vw;
  border-radius: 4px;
  margin: 1vh 1vw;
  overflow: hidden;
  position: relative;
}

.top-right-decoration {
  position: absolute;
  top: -1.5vh;
  right: 2vw;
  width: 4vw;
  height: 3vh;
  background-color: var(--color-primary-dark);
  clip-path: polygon(20% 0%, 80% 0%, 100% 100%, 0% 100%);
}

.dashboard-grid {
  display: grid;
  grid-template-columns: 1.25fr 1fr;
  gap: 2vw;
  height: 100%;
}

.left-column, .right-column {
  display: flex;
  flex-direction: column;
  height: 100%;
}

.main-header {
  flex: 0 0 auto;
}

.main-header h1 {
  font-size: 4.2vh;
  color: #0b1f3a; 
  margin-bottom: 0.2vh;
}

.main-header h2 {
  font-size: 2.6vh;
  margin-bottom: 0.5vh;
}

.main-header .subtitle {
  font-style: italic;
  font-size: 1.6vh;
  color: var(--color-text-muted);
}

.contract-value {
  flex: 0 0 auto;
  display: flex;
  align-items: center;
  padding: 1.5vh 2vw;
  border-radius: 8px;
  gap: 1vw;
  margin-top: 1vh;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
}

.contract-value .icon {
  font-size: 3.5vh;
}

.contract-value h2 {
  color: white;
  margin: 0;
  font-size: 3.2vh;
}

.ribbon-line {
  flex: 1;
  height: 2px;
  background-color: var(--color-border);
  margin-left: -1vw;
  margin-bottom: 2vh;
}
</style>
