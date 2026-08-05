<script setup>
import { ref, computed, watch } from 'vue'
import dbData from './data/db.json'
import VueMultiselect from 'vue-multiselect'
import 'vue-multiselect/dist/vue-multiselect.css'
import ProgressSection from './components/ProgressSection.vue'
import Activities from './components/Activities.vue'
import PhotoGallery from './components/PhotoGallery.vue'
import Observations from './components/Observations.vue'

const showFilterModal = ref(false)
const data = ref(dbData)
const subregiones = computed(() => data.value.subregiones || [])

const subregionActual = ref(subregiones.value.length > 0 ? subregiones.value[0] : null)

const circuitoActual = ref(null)
const corteSeleccionado = ref(null)

watch(circuitoActual, () => {
  corteSeleccionado.value = null
})

watch(subregionActual, (newSubregion) => {
  if (newSubregion && newSubregion.circuitos && newSubregion.circuitos.length > 0) {
    circuitoActual.value = newSubregion.circuitos[0]
  } else {
    circuitoActual.value = null
  }
}, { immediate: true })

const weekLabel = (corte) => `Semana ${corte.semana} (${corte.fecha_corte})`

const corteActual = computed(() => {
  if (!circuitoActual.value || !circuitoActual.value.cortes_semanales || !circuitoActual.value.cortes_semanales.length) return null
  
  // Obtener el corte seleccionado o el de la semana mayor por defecto
  let corte = null
  if (corteSeleccionado.value) {
    corte = corteSeleccionado.value
  } else {
    corte = [...circuitoActual.value.cortes_semanales].sort((a, b) => b.semana - a.semana)[0]
  }
  
  // Clonar para poder modificar los valores calculados
  const corteProcesado = JSON.parse(JSON.stringify(corte))

  // Calcular avance físico dinámico si hay valores
  let sumaObraDirecta = 0
  let sumaEjecutada = 0

  if (corteProcesado.actividades_ejecutadas && corteProcesado.actividades_ejecutadas.length > 0) {
    corteProcesado.actividades_ejecutadas.forEach(act => {
      if (act.valor_total) {
        sumaObraDirecta += act.valor_total
        if (act.total > 0 && act.completado > 0) {
          const proporcion = Math.min(act.completado / act.total, 1)
          sumaEjecutada += proporcion * act.valor_total
        }
      }
    })

    if (sumaObraDirecta > 0) {
      const avanceFisico = (sumaEjecutada / sumaObraDirecta) * 100
      corteProcesado.fisico.ejecutado = parseFloat(avanceFisico.toFixed(1))
      corteProcesado.fisico.avance = parseFloat(avanceFisico.toFixed(1))
    }
  }

  return corteProcesado
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
          <div class="filter-label">Subregión: 
            <VueMultiselect
              v-model="subregionActual"
              :options="subregiones"
              track-by="nombre"
              label="nombre"
              placeholder="Selecciona una subregión"
              :searchable="true"
              :show-labels="false"
              :close-on-select="true"
              class="custom-multiselect"
            />
          </div>
          <div v-if="subregionActual" class="filter-label">Circuito: 
            <VueMultiselect
              v-model="circuitoActual"
              :options="subregionActual.circuitos"
              track-by="id"
              label="corredor_vial"
              placeholder="Selecciona un circuito"
              :searchable="true"
              :show-labels="false"
              :close-on-select="true"
              class="custom-multiselect"
            />
          </div>
          <div v-if="circuitoActual" class="filter-label">Semana de Corte: 
            <VueMultiselect
              v-model="corteSeleccionado"
              :options="circuitoActual.cortes_semanales"
              :custom-label="weekLabel"
              track-by="semana"
              placeholder="Última semana por defecto"
              :searchable="false"
              :show-labels="false"
              :close-on-select="true"
              class="custom-multiselect"
            />
          </div>
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
          <div style="display: flex; flex-direction: column; flex: 1.5; overflow: hidden;">
            <!-- HEADER -->
            <header class="main-header">
              <div class="header-titles">
                <h1>INFORME DE AVANCE DE OBRA</h1>
                <h2 class="text-green">Corredor vial {{ circuitoActual.corredor_vial }}</h2>
                <p class="subtitle">Resumen ejecutivo y avance de actividades</p>
                <div v-if="corteActual" class="week-badge">
                  Corte: Semana {{ corteActual.semana }} ({{ corteActual.fecha_corte }})
                </div>
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
          </div>
          
          <!-- RIBBON ACTIVIDADES -->
          <div class="section-ribbon" style="margin-top: 1vh;">
            <span class="ribbon-icon">✓</span> Avance de actividades ejecutadas
          </div>
          <!-- ACTIVIDADES -->
          <Activities :actividades="corteActual.actividades_ejecutadas" />
        </div>

        <!-- COLUMNA DERECHA -->
        <div class="right-column">
          <div style="display: flex; flex-direction: column; flex: 1.5; overflow: hidden; position: relative;">
            <div class="top-right-decoration"></div>
            <!-- FOTOS -->
            <PhotoGallery :imagenes="corteActual.imagenes" />
          </div>

          <!-- RIBBON OBSERVACIONES -->
          <div class="section-ribbon" style="margin-top: 1vh;">
            <span class="ribbon-icon">✓</span> Dificultades y observaciones técnicas
          </div>
          <!-- OBSERVACIONES -->
          <div style="display: flex; flex-direction: column; flex: 1; overflow: hidden;">
            <Observations :observaciones="corteActual.observaciones_tecnicas" :tipoEstructura="corteActual.tipo_estructura" />
          </div>
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
  /* overflow: hidden; removed to allow vue-multiselect dropdown to show outside */
  box-shadow: 0 10px 25px rgba(0,0,0,0.2);
}

.filter-modal-header {
  border-top-left-radius: 8px;
  border-top-right-radius: 8px;

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

.filter-modal-footer {
  padding: 1.5vh 1.5vw;
  background: var(--color-bg-light);
  display: flex;
  justify-content: flex-end;
  border-bottom-left-radius: 8px;
  border-bottom-right-radius: 8px;
}

.custom-multiselect {
  margin-top: 0.5vh;
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

.week-badge {
  display: inline-block;
  margin-top: 0.5vh;
  padding: 0.3vh 1vw;
  background-color: var(--color-bg-light);
  color: var(--color-primary-dark);
  border-radius: 4px;
  font-size: 1.4vh;
  font-weight: bold;
  border: 1px solid var(--color-border);
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
