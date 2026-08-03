<script setup>
import { ref, computed, watch } from 'vue'
import dbData from './data/db.json'
import ProgressSection from './components/ProgressSection.vue'
import Activities from './components/Activities.vue'
import PhotoGallery from './components/PhotoGallery.vue'
import Observations from './components/Observations.vue'

const showFilterModal = ref(false)
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
  if (!circuitoActual.value || !circuitoActual.value.cortes_semanales.length) return null
  // Obtener el corte con la semana mayor
  return [...circuitoActual.value.cortes_semanales].sort((a, b) => b.semana - a.semana)[0]
})

const formatCurrency = (value) => {
  return new Intl.NumberFormat('es-CO', { style: 'decimal', minimumFractionDigits: 0 }).format(value)
}
</script>

<template>
  <div class="dashboard-wrapper">
    <!-- FILTER MODAL -->
    <div v-if="showFilterModal" class="filter-modal-overlay" @click="showFilterModal = false">
      <div class="filter-modal" @click.stop>
        <div class="filter-modal-header bg-dark-green">
          <h3 style="color: white; margin: 0;">Filtros de Búsqueda</h3>
          <button class="close-modal-btn" @click="showFilterModal = false">✕</button>
        </div>
        <div class="filter-modal-body">
          <label class="filter-label">Subregión: 
            <select v-model="selectedSubregionName" class="filter-select">
              <option v-for="sub in subregiones" :key="sub.nombre" :value="sub.nombre">
                {{ sub.nombre }}
              </option>
            </select>
          </label>
          <label v-if="subregionActual" class="filter-label">Circuito: 
            <select v-model="selectedCircuitoId" class="filter-select">
              <option v-for="c in subregionActual.circuitos" :key="c.id" :value="c.id">
                {{ c.corredor_vial }}
              </option>
            </select>
          </label>
        </div>
        <div class="filter-modal-footer">
          <button class="apply-filter-btn bg-dark-green" @click="showFilterModal = false">Aplicar y Cerrar</button>
        </div>
      </div>
    </div>

    <!-- MAIN DASHBOARD -->
    <main v-if="corteActual" class="dashboard-container">
      <div class="dashboard-grid">
        
        <!-- COLUMNA IZQUIERDA -->
        <div class="left-column">
          <!-- HEADER -->
          <header class="main-header">
            <div class="header-titles">
              <h1>INFORME DE AVANCE DE OBRA</h1>
              <h2 class="text-green">Corredor vial {{ circuitoActual.corredor_vial }}</h2>
              <p class="subtitle">Resumen ejecutivo y avance de actividades</p>
            </div>
            <div class="header-logo">
              <button class="filter-btn" @click="showFilterModal = true" title="Filtrar">
                <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polygon points="22 3 2 3 10 12.46 10 19 14 21 14 12.46 22 3"></polygon></svg>
              </button>
              <img src="/Logo-gob-antioquia-ant.png" alt="Logo Gobernación de Antioquia" />
            </div>
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
          <div class="section-ribbon" style="margin-top: 4vh;">
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

/* Modal de filtros */
.filter-modal-overlay {
  position: fixed;
  top: 0; left: 0; right: 0; bottom: 0;
  background: rgba(0, 0, 0, 0.6);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 2000;
  backdrop-filter: blur(3px);
}

.filter-modal {
  background: white;
  width: 400px;
  max-width: 90vw;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 10px 25px rgba(0,0,0,0.2);
}

.filter-modal-header {
  padding: 1.5vh 1.5vw;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.close-modal-btn {
  background: none;
  border: none;
  color: white;
  font-size: 2vh;
  cursor: pointer;
}

.filter-modal-body {
  padding: 2vh 1.5vw;
  display: flex;
  flex-direction: column;
  gap: 2vh;
}

.filter-label {
  display: flex;
  flex-direction: column;
  font-size: 1.6vh;
  font-weight: bold;
  color: var(--color-text-main);
}

.filter-select {
  margin-top: 0.5vh;
  padding: 1vh;
  border: 1px solid var(--color-border);
  border-radius: 4px;
  font-size: 1.5vh;
  width: 100%;
}

.filter-modal-footer {
  padding: 1.5vh 1.5vw;
  background: var(--color-bg-light);
  display: flex;
  justify-content: flex-end;
}

.apply-filter-btn {
  color: white;
  border: none;
  padding: 1vh 2vw;
  border-radius: 4px;
  cursor: pointer;
  font-weight: bold;
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
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 2vw;
}

.header-titles {
  flex: 1;
}

.header-logo {
  flex: 0 0 auto;
  display: flex;
  align-items: center;
  gap: 1.5vw;
}

.filter-btn {
  background: var(--color-primary-dark);
  color: white;
  border: none;
  width: 5vh;
  height: 5vh;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  box-shadow: 0 2px 5px rgba(0,0,0,0.2);
  transition: transform 0.2s;
}

.filter-btn:hover {
  transform: scale(1.05);
}

.filter-btn svg {
  width: 2.5vh;
  height: 2.5vh;
}

.header-logo img {
  max-height: 8vh;
  object-fit: contain;
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
