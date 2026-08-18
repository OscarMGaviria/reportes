<script setup>
import { ref, computed, watch } from 'vue'
import subregionesData from './data/subregiones.json'
import circuitosData from './data/circuitos_maestros.json'
import presupuestosData from './data/presupuestos_y_cronograma_base.json'
import catalogoData from './data/catalogo_actividades.json'
import metasData from './data/metas_fisicas.json'
import VueMultiselect from 'vue-multiselect'
import 'vue-multiselect/dist/vue-multiselect.css'
import { CalendarRange, Filter, TrendingUp, Check } from 'lucide-vue-next'
import ProgressSection from './components/ProgressSection.vue'
import Activities from './components/Activities.vue'
import PhotoGallery from './components/PhotoGallery.vue'
import Observations from './components/Observations.vue'
import GanttDashboard from './components/GanttDashboard.vue'

// Import all weekly reports
const cortesModules = import.meta.glob('./data/cortes_semanales/*.json', { eager: true, import: 'default' })

const showGanttModal = ref(false)

const subregiones = computed(() => {
  return subregionesData.map(sub => {
    const circuitos = circuitosData.filter(c => c.id_subregion === sub.id_subregion).map(c => {
      const cortes = cortesModules[`./data/cortes_semanales/cortes_circuito_${c.id_circuito}.json`] || []
      return {
        ...c,
        id: c.id_circuito,
        valor_contrato: c.contrato.valor_total,
        cortes_semanales: cortes
      }
    })
    return { ...sub, circuitos }
  })
})

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
  if (!circuitoActual.value) return null
  
  let corteRaw = corteSeleccionado.value
  
  if (!corteRaw) {
    if (circuitoActual.value.cortes_semanales && circuitoActual.value.cortes_semanales.length > 0) {
      corteRaw = [...circuitoActual.value.cortes_semanales].sort((a, b) => b.semana - a.semana)[0]
    } else {
      corteRaw = {
        semana: 0,
        fecha_corte: 'Línea Base',
        seguimiento_general: {
          financiero: { porcentaje_programado: 0, porcentaje_ejecutado: 0 },
          fisico: { porcentaje_programado: 0, porcentaje_ejecutado: 0 },
          cronograma: { estado: 'Sin iniciar' }
        },
        seguimiento_actividades: [],
        registro_fotografico: [],
        dificultades_y_observaciones: []
      }
    }
  }
  
  // Extraemos las actividades directamente del presupuesto base
  const idCircuito = circuitoActual.value.id;
  const presupuestoBase = presupuestosData.find(p => p.id_circuito === idCircuito);
  const actividadesProgramadas = presupuestoBase ? presupuestoBase.actividades_programadas : [];

  // Calcular "Programado" como la suma del presupuesto base de todas las actividades
  const valorProgramadoTotal = actividadesProgramadas.reduce((sum, ap) => sum + (ap.valor_total_esperado || 0), 0);
  
  // Financial calculations
  const valorAnticipo = 0.15 * valorProgramadoTotal;
  const anticipoPorc = 15.0; // Siempre es 15% del total programado
  
  // Ejecutado: "valor ingresado por acta (ahora miramos como lo agregamos)"
  // Por ahora lo dejamos en 0 para la semana 0, o usamos el porcentaje reportado
  const porcEjecFin = corteRaw.seguimiento_general?.financiero?.porcentaje_ejecutado || 0;
  const valorEjecFin = (porcEjecFin / 100) * valorProgramadoTotal; 
  
  const avanceFinPorc = valorProgramadoTotal > 0 ? (valorEjecFin / valorProgramadoTotal) * 100 : 0;
  
  const corteProcesado = {
    semana: corteRaw.semana,
    fecha_corte: corteRaw.fecha_corte,
    financiero: {
      programado: { porcentaje: "100.0", valor: valorProgramadoTotal },
      ejecutado: { porcentaje: porcEjecFin.toFixed(1), valor: valorEjecFin },
      anticipo: { porcentaje: anticipoPorc.toFixed(1), valor: valorAnticipo },
      avance: { porcentaje: avanceFinPorc.toFixed(1), valor: valorEjecFin }
    },
    fisico: {
      programado: (corteRaw.seguimiento_general?.fisico?.porcentaje_programado || 0).toFixed(1),
      ejecutado: (corteRaw.seguimiento_general?.fisico?.porcentaje_ejecutado || 0).toFixed(1),
      avance: ((corteRaw.seguimiento_general?.fisico?.porcentaje_programado || 0) > 0 
                ? ((corteRaw.seguimiento_general?.fisico?.porcentaje_ejecutado || 0) / (corteRaw.seguimiento_general?.fisico?.porcentaje_programado || 1) * 100) 
                : 0).toFixed(1),
      estado: corteRaw.seguimiento_general?.cronograma?.estado || 'En ejecución'
    },
    actividades_ejecutadas: [],
    imagenes: corteRaw.registro_fotografico || [],
    observaciones_tecnicas: (corteRaw.dificultades_y_observaciones || []).map(obs => obs.descripcion)
  }

  // Base definition
  const categoriasProg = {
    'Topografía': { nombre: 'Topografía', unidad: 'Glb', total: 100, completado: 0, valor_total: 0 },
    'Exploración de campo': { nombre: 'Exploración de campo', unidad: 'Glb', total: 100, completado: 0, valor_total: 0 },
    'CONSTRUCCIÓN DE ALCANTARILLAS': { nombre: 'Construcción de alcantarillas', unidad: 'Glb', total: 100, completado: 0, valor_total: 0 },
    'CONSTRUCCIÓN DE DISIPADORES': { nombre: 'Construcción de disipadores', unidad: 'Glb', total: 100, completado: 0, valor_total: 0 },
    'CONSTRUCCIÓN DE FILTROS PARA CUNETAS': { nombre: 'Construcción de filtros para cunetas', unidad: 'Glb', total: 100, completado: 0, valor_total: 0 },
    'ESTABILIZACION CON MATERIAL GRANULAR': { nombre: 'Estabilización con material granular', unidad: 'Glb', total: 100, completado: 0, valor_total: 0 },
    'CONSTRUCCIÓN DE CUNETAS': { nombre: 'Construcción de cunetas', unidad: 'Glb', total: 100, completado: 0, valor_total: 0 },
    'CONSTRUCCIÓN DE BORDILLOS': { nombre: 'Construcción de bordillos', unidad: 'Glb', total: 100, completado: 0, valor_total: 0 },
    'SEÑALIZACIÓN VIAL': { nombre: 'Señalización vial', unidad: 'Glb', total: 100, completado: 0, valor_total: 0 }
  };
  
  // Custom quantities per circuit
  const metasCircuito = metasData[idCircuito.toString()];
  
  if (metasCircuito) {
    if (metasCircuito['Topografia']) {
      categoriasProg['Topografía'].total = metasCircuito['Topografia'].total;
      categoriasProg['Topografía'].unidad = metasCircuito['Topografia'].unidad;
    }
    if (metasCircuito['Exploracion de campo']) {
      categoriasProg['Exploración de campo'].total = metasCircuito['Exploracion de campo'].total;
      categoriasProg['Exploración de campo'].unidad = metasCircuito['Exploracion de campo'].unidad;
    }
    if (metasCircuito['Construcción de alcantarillas']) {
      categoriasProg['CONSTRUCCIÓN DE ALCANTARILLAS'].total = metasCircuito['Construcción de alcantarillas'].total;
      categoriasProg['CONSTRUCCIÓN DE ALCANTARILLAS'].unidad = metasCircuito['Construcción de alcantarillas'].unidad;
      if (metasCircuito['Construcción de alcantarillas'].subItems) {
        categoriasProg['CONSTRUCCIÓN DE ALCANTARILLAS'].subItems = metasCircuito['Construcción de alcantarillas'].subItems;
      } else {
        // Fallback or explicit subitems as requested by user
        if (idCircuito === 101) {
          categoriasProg['CONSTRUCCIÓN DE ALCANTARILLAS'].subItems = [
            { nombre: 'Limpieza', completado: 0, total: 6 },
            { nombre: 'Remplazar', completado: 0, total: 6 },
            { nombre: 'Nuevas', completado: 0, total: 6 }
          ];
        }
      }
    }
    if (metasCircuito['Construcción de disipadores']) {
      categoriasProg['CONSTRUCCIÓN DE DISIPADORES'].total = metasCircuito['Construcción de disipadores'].total;
      categoriasProg['CONSTRUCCIÓN DE DISIPADORES'].unidad = metasCircuito['Construcción de disipadores'].unidad;
    }
    if (metasCircuito['Construcción de filtro para cunetas']) {
      categoriasProg['CONSTRUCCIÓN DE FILTROS PARA CUNETAS'].total = metasCircuito['Construcción de filtro para cunetas'].total;
      categoriasProg['CONSTRUCCIÓN DE FILTROS PARA CUNETAS'].unidad = metasCircuito['Construcción de filtro para cunetas'].unidad;
    }
    if (metasCircuito['Estabilización con material granular']) {
      categoriasProg['ESTABILIZACION CON MATERIAL GRANULAR'].total = metasCircuito['Estabilización con material granular'].total;
      categoriasProg['ESTABILIZACION CON MATERIAL GRANULAR'].unidad = metasCircuito['Estabilización con material granular'].unidad;
    }
    if (metasCircuito['Construcción de cunetas']) {
      categoriasProg['CONSTRUCCIÓN DE CUNETAS'].total = metasCircuito['Construcción de cunetas'].total;
      categoriasProg['CONSTRUCCIÓN DE CUNETAS'].unidad = metasCircuito['Construcción de cunetas'].unidad;
    }
    if (metasCircuito['Construcción de bordillos']) {
      categoriasProg['CONSTRUCCIÓN DE BORDILLOS'].total = metasCircuito['Construcción de bordillos'].total;
      categoriasProg['CONSTRUCCIÓN DE BORDILLOS'].unidad = metasCircuito['Construcción de bordillos'].unidad;
    }
    if (metasCircuito['Señalización vial']) {
      categoriasProg['SEÑALIZACIÓN VIAL'].total = metasCircuito['Señalización vial'].total;
      categoriasProg['SEÑALIZACIÓN VIAL'].unidad = metasCircuito['Señalización vial'].unidad;
    }
  }

  if (actividadesProgramadas) {
    actividadesProgramadas.forEach(ap => {
      const catObj = catalogoData.find(c => c.id_actividad === ap.id_actividad);
      if (catObj) {
        let catName = catObj.categoria;
        if (catName === 'CONSTRUCCIÓN DE CUNETA') catName = 'CONSTRUCCIÓN DE CUNETAS';
        
        if (categoriasProg[catName]) {
          categoriasProg[catName].valor_total += (ap.valor_total_esperado || 0);
        }
      }
    });
  }

  // Ahora procesamos el progreso de la semana actual
  if (corteRaw.seguimiento_actividades && corteRaw.seguimiento_actividades.length > 0) {
    corteRaw.seguimiento_actividades.forEach(sa => {
      const catObj = catalogoData.find(c => c.id_actividad === sa.id_actividad);
      if (catObj) {
        let catName = catObj.categoria;
        if (catName === 'CONSTRUCCIÓN DE CUNETA') catName = 'CONSTRUCCIÓN DE CUNETAS';
        
        if (categoriasProg[catName]) {
          // Weighted completion based on value could be calculated here.
        }
      }
    });
  }
  
  corteProcesado.actividades_ejecutadas = Object.values(categoriasProg);

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
        <span class="topbar-title">Contrato de Estabilización Vial</span>
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
  width: 18vw;
  min-width: 180px;
}

/* Custom styling to make VueMultiselect fit in the dark green header */
.header-multiselect :deep(.multiselect__tags) {
  min-height: 4vh;
  padding: 0.6vh 2.5vw 0 1.2vw;
  border-radius: 50px;
  background: white;
  border: 1px solid #e2e8f0;
  color: #1e293b;
  transition: all 0.2s ease;
  cursor: pointer;
  box-shadow: 0 1px 3px rgba(0,0,0,0.1);
}
.header-multiselect:hover :deep(.multiselect__tags) {
  border-color: #cbd5e1;
  box-shadow: 0 2px 5px rgba(0,0,0,0.15);
}
.header-multiselect :deep(.multiselect__select) {
  height: 4vh;
  padding: 0;
}
.header-multiselect :deep(.multiselect__select::before) {
  border-color: #64748b transparent transparent;
}
.header-multiselect :deep(.multiselect__placeholder) {
  margin-bottom: 0;
  padding-top: 0.2vh;
  font-size: 1.4vh;
  color: #64748b;
  font-weight: 500;
}
.header-multiselect :deep(.multiselect__single),
.header-multiselect :deep(.multiselect__input) {
  margin-bottom: 0;
  padding-top: 0.2vh;
  font-size: 1.4vh;
  color: #1e293b;
  font-weight: 600;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  display: block;
  background: transparent;
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
  font-size: 1.8vh;
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
