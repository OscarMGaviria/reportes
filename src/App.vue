<script setup>
import { ref, computed, watch } from 'vue'
import dbData from './data/db.json'
import plantilla from './data/plantilla.json'
import VueMultiselect from 'vue-multiselect'
import 'vue-multiselect/dist/vue-multiselect.css'
import { CalendarRange, Filter, TrendingUp, Check } from 'lucide-vue-next'
import ProgressSection from './components/ProgressSection.vue'
import Activities from './components/Activities.vue'
import PhotoGallery from './components/PhotoGallery.vue'
import Observations from './components/Observations.vue'
import GanttDashboard from './components/GanttDashboard.vue'

const showGanttModal = ref(false)
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
  const baseTemplate = JSON.parse(JSON.stringify(plantilla))
  const corteProcesado = JSON.parse(JSON.stringify(corte))

  // MERGE ESTRUCTURAL
  const norm = (str) => str ? str.toLowerCase().normalize("NFD").replace(/[\u0300-\u036f]/g, "") : ""
  
  if (corteProcesado.actividades_ejecutadas) {
    baseTemplate.actividades_ejecutadas.forEach(baseAct => {
      let match = null
      if (baseAct.nombre === 'Obras Transversales') {
        match = corteProcesado.actividades_ejecutadas.find(a => norm(a.nombre).includes('obras transversales'))
      } else if (baseAct.nombre === 'Estabilización') {
        match = corteProcesado.actividades_ejecutadas.find(a => norm(a.nombre).includes('estabilizacion'))
      } else {
        match = corteProcesado.actividades_ejecutadas.find(a => norm(a.nombre).includes(norm(baseAct.nombre)))
      }
      
      if (match) {
        Object.assign(baseAct, match)
      }
    })
  }
  
  corteProcesado.actividades_ejecutadas = baseTemplate.actividades_ejecutadas
  
  if (!corteProcesado.financiero) corteProcesado.financiero = baseTemplate.financiero
  if (!corteProcesado.fisico) corteProcesado.fisico = baseTemplate.fisico
  if (!corteProcesado.observaciones_tecnicas || corteProcesado.observaciones_tecnicas.length === 0) {
    corteProcesado.observaciones_tecnicas = baseTemplate.observaciones_tecnicas
  }

  // Calcular avance físico dinámico si hay valores
  let sumaProgramadoTotal = 0
  let sumaBaseAnticipo = 0
  let sumaEjecutada = 0

  if (corteProcesado.actividades_ejecutadas && corteProcesado.actividades_ejecutadas.length > 0) {
    corteProcesado.actividades_ejecutadas.forEach(act => {
      if (act.valor_total) {
        sumaProgramadoTotal += act.valor_total
        
        const esCaracterizacion = act.nombre.toLowerCase().normalize("NFD").replace(/[\u0300-\u036f]/g, "").includes('caracterizacion vial')
        
        if (!esCaracterizacion) {
          sumaBaseAnticipo += act.valor_total
        }
        
        if (act.total > 0 && act.completado > 0 && !esCaracterizacion) {
          const proporcion = Math.min(act.completado / act.total, 1)
          sumaEjecutada += proporcion * act.valor_total
        }
      }
    })

    if (sumaBaseAnticipo > 0) {
      const avanceFisico = (sumaEjecutada / sumaBaseAnticipo) * 100
      corteProcesado.fisico.ejecutado = parseFloat(avanceFisico.toFixed(1))
      corteProcesado.fisico.avance = parseFloat(avanceFisico.toFixed(1))
    }
    
    // Regla de Negocio: Programado es la sumatoria de todas las actividades (incluyendo Caracterización)
    corteProcesado.financiero.programado.valor = sumaProgramadoTotal
    // Regla de Negocio: Anticipo es el 15% del Programado, excluyendo Caracterización Vial
    corteProcesado.financiero.anticipo.valor = sumaBaseAnticipo * 0.15
    
    const valorContrato = circuitoActual.value.valor_contrato || 1
    corteProcesado.financiero.programado.porcentaje = parseFloat(((sumaProgramadoTotal / valorContrato) * 100).toFixed(1))
    corteProcesado.financiero.anticipo.porcentaje = parseFloat(((corteProcesado.financiero.anticipo.valor / valorContrato) * 100).toFixed(1))
  }

  return corteProcesado
})

const formatCurrency = (value) => {
  return new Intl.NumberFormat('es-CO', { style: 'decimal', minimumFractionDigits: 0 }).format(value)
}
</script>

<template>
  <div class="dashboard-wrapper">
    <!-- APP TOPBAR -->
    <header class="app-topbar bg-dark-green">
      <div class="topbar-logo-area">
        <span class="topbar-title">Reportes de Obras</span>
      </div>
      
      <div class="topbar-filters">
        <div class="header-filter-item">
          <VueMultiselect
            v-model="subregionActual"
            :options="subregiones"
            track-by="nombre"
            label="nombre"
            placeholder="Subregión"
            :searchable="true"
            :show-labels="false"
            :close-on-select="true"
            class="header-multiselect"
          />
        </div>
        <div v-if="subregionActual" class="header-filter-item">
          <VueMultiselect
            v-model="circuitoActual"
            :options="subregionActual.circuitos"
            track-by="id"
            label="corredor_vial"
            placeholder="Circuito"
            :searchable="true"
            :show-labels="false"
            :close-on-select="true"
            class="header-multiselect"
          />
        </div>
        <div v-if="circuitoActual" class="header-filter-item">
          <VueMultiselect
            v-model="corteSeleccionado"
            :options="circuitoActual.cortes_semanales"
            :custom-label="weekLabel"
            track-by="semana"
            placeholder="Semana de Corte"
            :searchable="false"
            :show-labels="false"
            :close-on-select="true"
            class="header-multiselect"
          />
        </div>
      </div>

      <div class="topbar-actions">
        <button class="topbar-btn" @click="showGanttModal = true" title="Ver Gantt 18 Meses">
          <CalendarRange :size="20" />
        </button>
      </div>
    </header>

    <!-- MAIN DASHBOARD -->
    <main v-if="corteActual" class="dashboard-container">
      <div class="dashboard-grid">

        <!-- FILA 1 IZQUIERDA: header + contrato + progreso -->
        <div class="grid-cell grid-top-left">
          <!-- HEADER -->
          <header class="main-header">
            <div class="header-titles">
              <h1>INFORME DE AVANCE DE OBRA</h1>
              <h2 class="text-green">Corredor vial {{ circuitoActual.corredor_vial }}</h2>
            </div>
            <div class="header-logo">
              <img src="/Logo-gob-antioquia-ant.png" alt="Logo Gobernación de Antioquia" />
            </div>
          </header>

          <!-- VALOR DEL CONTRATO -->
          <div class="contract-value bg-dark-green">
            <h2>Valor del contrato: $ {{ formatCurrency(circuitoActual.valor_contrato) }}</h2>
          </div>

          <!-- RIBBON ACTIVIDADES -->
          <div class="ribbon-row">
            <div class="section-ribbon">
              <span class="ribbon-icon">✓</span> Avance de actividades ejecutadas
            </div>
            <div class="ribbon-line"></div>
          </div>

          <!-- ACTIVIDADES -->
          <Activities :actividades="corteActual.actividades_ejecutadas" />
        </div>

        <!-- FILA 2 IZQUIERDA: ribbon progreso -->
        <div class="section-ribbon grid-cell grid-ribbon-left">
          <span class="ribbon-icon">↗</span> Avance financiero y físico
        </div>

        <!-- FILA 3 IZQUIERDA: progreso -->
        <div class="grid-cell grid-bottom-left">
          <ProgressSection :corte="corteActual" />
        </div>

        <!-- FILA 1 DERECHA: fotos -->
        <div class="grid-cell grid-top-right">
          <div class="top-right-decoration"></div>
          <PhotoGallery :imagenes="corteActual.imagenes" />
        </div>

        <!-- FILA 2 DERECHA: ribbon observaciones -->
        <div class="section-ribbon grid-cell grid-ribbon-right">
          <span class="ribbon-icon"><Check :size="14" /></span> Dificultades y observaciones técnicas
        </div>

        <!-- FILA 3 DERECHA: observaciones -->
        <div class="grid-cell grid-bottom-right">
          <Observations :observaciones="corteActual.observaciones_tecnicas" :tipoEstructura="corteActual.tipo_estructura || []" />
        </div>

      </div>
    </main>

    <!-- GANTT MODAL -->
    <GanttDashboard 
      v-if="showGanttModal && circuitoActual" 
      :circuitoNombre="circuitoActual.corredor_vial"
      @close="showGanttModal = false" 
    />
  </div>
</template>

<style scoped>
.dashboard-wrapper {
  height: 100vh;
  min-width: 1200px;
  min-height: 700px;
  overflow: auto;
  display: flex;
  flex-direction: column;
  background-color: white;
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

/* Grid de 2 columnas x 3 filas compartidas: las filas de "ribbon" y de
   contenido inferior quedan alineadas entre columna izquierda y derecha
   porque ambas usan las mismas pistas de fila (grid-row), no un cálculo
   de flex independiente por columna. */
.dashboard-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  grid-template-rows: auto auto minmax(0, 1fr);
  column-gap: 2vw;
  row-gap: 1vh;
  height: 100%;
}

.grid-top-left { grid-column: 1; grid-row: 1; }
.grid-ribbon-left { grid-column: 1; grid-row: 2; }
.grid-bottom-left { grid-column: 1; grid-row: 3; }

.grid-top-right { grid-column: 2; grid-row: 1; }
.grid-ribbon-right { grid-column: 2; grid-row: 2; }
.grid-bottom-right { grid-column: 2; grid-row: 3; }

.grid-bottom-left {
  overflow: visible; /* Allow overlapping badges */
}

.grid-cell {
  min-height: 0;
  min-width: 0;
  overflow: hidden;
}

.grid-bottom-left, .grid-bottom-right {
  padding-top: 2vh;
}

.grid-top-left, .grid-top-right, .grid-bottom-left, .grid-bottom-right {
  display: flex;
  flex-direction: column;
}

.grid-top-right {
  position: relative;
}

.grid-ribbon-left, .grid-ribbon-right {
  margin: 0;
}

.ribbon-row {
  display: flex;
  align-items: center;
  margin-top: 1vh;
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

/* ===== APP TOPBAR ===== */
.app-topbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.8vh 2vw; /* Altura reducida */
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
  color: white;
  z-index: 10;
}

.topbar-logo-area {
  display: flex;
  align-items: center;
  gap: 1vw;
  flex: 0 0 auto;
}

.topbar-filters {
  display: flex;
  gap: 1vw;
  flex: 1;
  justify-content: flex-end;
  margin-right: 2vw;
}

.header-filter-item {
  width: 12vw;
  min-width: 130px;
}

/* Custom styling to make VueMultiselect fit in the dark green header */
.header-multiselect :deep(.multiselect__tags) {
  min-height: 3.5vh;
  padding: 0.5vh 3vw 0 1vw;
  border-radius: 6px;
  background: rgba(255, 255, 255, 0.15);
  border: 1px solid rgba(255, 255, 255, 0.2);
  color: white;
  transition: all 0.2s;
  cursor: pointer;
}
.header-multiselect:hover :deep(.multiselect__tags) {
  background: rgba(255, 255, 255, 0.25);
}
.header-multiselect :deep(.multiselect__select) {
  height: 3.5vh;
  padding: 0;
}
.header-multiselect :deep(.multiselect__select::before) {
  border-color: rgba(255, 255, 255, 0.8) transparent transparent;
}
.header-multiselect :deep(.multiselect__placeholder) {
  margin-bottom: 0;
  padding-top: 0.2vh;
  font-size: 1.4vh;
  color: rgba(255, 255, 255, 0.7);
  font-weight: 500;
}
.header-multiselect :deep(.multiselect__single),
.header-multiselect :deep(.multiselect__input) {
  margin-bottom: 0;
  padding-top: 0.2vh;
  font-size: 1.4vh;
  color: #ffffff;
  font-weight: 600;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  display: block;
}

.header-logo {
  flex: 0 0 auto;
  display: flex;
  align-items: center;
  gap: 1.5vw;
}

.header-logo img {
  max-height: 8vh;
  object-fit: contain;
}

.topbar-title {
  font-weight: bold;
  font-size: 2.2vh;
  letter-spacing: 0.5px;
}

.topbar-actions {
  display: flex;
  gap: 1vw;
}

.topbar-btn {
  background: rgba(255, 255, 255, 0.15);
  color: white;
  border: 1px solid rgba(255, 255, 255, 0.2);
  padding: 0.8vh;
  border-radius: 6px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s;
}

.topbar-btn:hover {
  background: rgba(255, 255, 255, 0.25);
  transform: translateY(-1px);
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
