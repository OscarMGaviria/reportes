<script setup>
import { ref, onMounted, watch } from 'vue'
import { calculateGanttData } from '../utils/constructionLogic'
import actividadesData from '../data/actividades.json'

const props = defineProps({
  circuitoNombre: {
    type: String,
    required: true
  }
})

const emit = defineEmits(['close'])

const processedData = ref([])
const circuitoFiltrado = ref(null)
const totalDays = 540 // 18 months

// Meses para el eje superior (Feb 2026 a Jul 2027)
const months = [
  'Feb', 'Mar', 'Abr', 'May', 'Jun', 'Jul', 'Ago', 'Sept', 'Oct', 'Nov', 'Dic', 
  'Ene<br>2027', 'Feb', 'Mar', 'Abr', 'May', 'Jun', 'Jul'
]

// Posicion Hoy simulada (ej. Agosto = mes 6 => ~33%)
const todayPercentage = 35; 

onMounted(() => {
  if (actividadesData && actividadesData.circuitos) {
    processedData.value = calculateGanttData(actividadesData.circuitos)
    filtrarCircuito()
  }
})

watch(() => props.circuitoNombre, () => {
  filtrarCircuito()
})

const filtrarCircuito = () => {
  if (!props.circuitoNombre || processedData.value.length === 0) return
  
  // Fuzzy matching: buscar si comparten al menos 2 palabras clave significativas
  const normalize = (str) => str.toLowerCase().normalize("NFD").replace(/[\u0300-\u036f]/g, "").replace(/[^a-z0-9 ]/g, " ");
  
  const searchWords = normalize(props.circuitoNombre).split(' ').filter(w => w.length > 3);
  
  const found = processedData.value.find(c => {
    const targetWords = normalize(c.nombre).split(' ');
    // Contar cuantas searchWords estan en targetWords
    const matches = searchWords.filter(sw => targetWords.includes(sw));
    return matches.length >= 2 || (searchWords.length === 1 && matches.length === 1);
  })
  
  if (found) {
    circuitoFiltrado.value = found
  } else {
    // Si no encuentra por nombre exacto, por defecto mostramos el primero o null
    circuitoFiltrado.value = processedData.value[0]
  }
}

const formatName = (name) => {
  if (name.includes('ESTABILIZACION')) return 'Estabilización';
  if (name.includes('ALCANTARILLAS')) return 'Alcantarillas';
  if (name.includes('DISIPADORES')) return 'Disipadores';
  if (name.includes('FILTRO')) return 'Filtros para Cunetas';
  if (name.includes('CUNETA')) return 'Cunetas';
  if (name.includes('BORDILLOS')) return 'Bordillos';
  if (name.includes('SEÑALIZACIÓN')) return 'Señalización Vial';
  
  // Fallback genérico
  let short = name.replace('CONSTRUCCIÓN DE ', '').replace('CONSTRUCCION DE ', '');
  return short.charAt(0).toUpperCase() + short.slice(1).toLowerCase();
}
</script>

<template>
  <div class="gantt-overlay" @click.self="$emit('close')">
    <div class="gantt-container">
      
      <header class="gantt-header">
        <div class="header-content">
          <h1>Plan de Obra - 18 Meses ({{ props.circuitoNombre }})</h1>
        </div>
        <button class="close-btn" @click="$emit('close')">X</button>
      </header>

      <div class="gantt-content">
        <div v-if="!circuitoFiltrado" class="loading">Cargando cronograma para {{ props.circuitoNombre }}...</div>
        
        <div v-else class="circuit-gantt">
          
          <div class="gantt-chart">
            
            <!-- EJE SUPERIOR DE MESES -->
            <div class="gantt-axis">
              <div class="axis-empty-space"></div> <!-- Espacio para las etiquetas izquierdas -->
              <div class="axis-months">
                <div v-for="(m, i) in months" :key="i" class="month-marker">
                  <span v-html="m"></span>
                </div>
                
                <!-- LINEA DE HOY -->
                <div class="today-line-container" :style="{ left: todayPercentage + '%' }">
                  <div class="today-badge">Hoy</div>
                  <div class="today-line"></div>
                </div>
              </div>
            </div>

            <!-- FILAS DEL GANTT -->
            <div class="gantt-rows-container">
              <div v-for="(fase, index) in circuitoFiltrado.fases" :key="fase.id" class="gantt-row" :class="{ 'bg-gray': index % 2 !== 0 }">
                
                <!-- COLUMNA IZQUIERDA: Nombre de actividad -->
                <div class="phase-label">
                  <span class="phase-number">{{ fase.id }}</span>
                  <strong class="phase-name" :title="fase.name">{{ formatName(fase.name) }}</strong>
                </div>
                
                <!-- COLUMNA DERECHA: Pistas de barras -->
                <div class="bar-track-area">
                  <div class="bar-capsule" 
                       :style="{
                         left: (fase.startDay / totalDays * 100) + '%', 
                         width: ((fase.endDay - fase.startDay) / totalDays * 100) + '%'
                       }">
                       
                       <div class="bar-fill" :style="{ width: fase.progress + '%' }"></div>
                       <div class="progress-badge" v-if="fase.progress > 0" :style="{ left: fase.progress + '%' }">
                         {{ fase.progress }}%
                       </div>
                  </div>
                </div>
              </div>
            </div>

          </div>
        </div>
        
      </div>
    </div>
  </div>
</template>

<style scoped>
.gantt-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.4);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 9999;
  padding: 2vh 2vw;
}

.gantt-container {
  background: #ffffff;
  border-radius: 8px;
  width: 95vw;
  height: 90vh;
  display: flex;
  flex-direction: column;
  box-shadow: 0 15px 30px rgba(0, 0, 0, 0.2);
  overflow: hidden;
  font-family: 'Inter', 'Segoe UI', sans-serif;
}

.gantt-header {
  background: white;
  padding: 2vh 2.5vw;
  display: flex;
  justify-content: space-between;
  align-items: center;
  border-bottom: 1px solid #e5e7eb;
}

.header-content h1 {
  margin: 0;
  color: #1f2937;
  font-size: 2.5vh;
  font-weight: 700;
}

.close-btn {
  background: none;
  border: none;
  color: #6b7280;
  font-size: 2.5vh;
  cursor: pointer;
  transition: color 0.2s;
}

.close-btn:hover {
  color: #ef4444;
}

.gantt-content {
  flex: 1;
  overflow-y: auto;
  padding: 2vh 2.5vw;
  background: #ffffff;
}

.circuit-gantt {
  padding-top: 1vh;
}

.gantt-chart {
  background: white;
  margin-bottom: 4vh;
}

/* EJE SUPERIOR */
.gantt-axis {
  display: flex;
  position: relative;
  border-bottom: 1px solid #e5e7eb;
  padding-bottom: 1vh;
  margin-bottom: 1vh;
}

.axis-empty-space {
  width: 25%;
}

.axis-months {
  width: 75%;
  display: flex;
  position: relative;
}

.month-marker {
  flex: 1;
  text-align: center;
  color: #6b7280;
  font-size: 1.2vh;
  font-weight: 700;
  position: relative;
}

.month-marker::after {
  content: '';
  position: absolute;
  bottom: -1vh;
  left: 50%;
  width: 1px;
  height: 0.5vh;
  background: #d1d5db;
}

/* HOY LINE */
.today-line-container {
  position: absolute;
  top: -2.5vh;
  bottom: -50vh;
  width: 1px;
  z-index: 10;
}

.today-badge {
  background: #f59e0b;
  color: white;
  font-size: 1.1vh;
  font-weight: bold;
  padding: 0.2vh 0.6vw;
  border-radius: 12px;
  position: absolute;
  top: 0;
  left: 50%;
  transform: translateX(-50%);
  white-space: nowrap;
}

.today-line {
  position: absolute;
  top: 2vh;
  left: 50%;
  width: 2px;
  height: 50vh;
  background: #f59e0b;
  transform: translateX(-50%);
}

/* FILAS */
.gantt-rows-container {
  position: relative;
  overflow: hidden;
}

.gantt-row {
  display: flex;
  align-items: center;
  padding: 1.5vh 0;
  position: relative;
}

.gantt-row.bg-gray {
  background-color: #f9fafb;
}

.bar-track-area::before {
  content: '';
  position: absolute;
  top: 0; left: 0; right: 0; bottom: 0;
  background-image: linear-gradient(to right, #f3f4f6 1px, transparent 1px);
  background-size: calc(100% / 18) 100%;
  z-index: 0;
  pointer-events: none;
}

.phase-label {
  width: 25%;
  display: flex;
  align-items: center;
  gap: 1vw;
  padding-left: 1vw;
  z-index: 1;
}

.phase-number {
  background: #e6f4ea;
  color: #1e4620;
  width: 2.5vh;
  height: 2.5vh;
  display: flex;
  justify-content: center;
  align-items: center;
  border-radius: 50%;
  font-size: 1.2vh;
  font-weight: 800;
  flex-shrink: 0;
}

.phase-name {
  color: #374151;
  font-size: 1.4vh;
  font-weight: 600;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.bar-track-area {
  width: 75%;
  position: relative;
  height: 3vh;
  z-index: 1;
}

/* CAPSULA Y BARRAS */
.bar-capsule {
  position: absolute;
  top: 10%;
  height: 80%;
  background: #e6e9e6;
  border: 1px solid #d1d5db;
  border-radius: 12px;
  display: flex;
  align-items: center;
}

.bar-fill {
  height: 100%;
  background: #2f6e4a;
  border-radius: 12px;
  transition: width 0.5s ease;
}

.progress-badge {
  position: absolute;
  background: #4ade80;
  color: white;
  font-size: 1.1vh;
  font-weight: 800;
  padding: 0.1vh 0.4vw;
  border-radius: 10px;
  transform: translateX(-110%);
  pointer-events: none;
}

.gantt-content::-webkit-scrollbar {
  width: 8px;
}
.gantt-content::-webkit-scrollbar-track {
  background: #f1f1f1; 
}
.gantt-content::-webkit-scrollbar-thumb {
  background: #c1c1c1; 
  border-radius: 4px;
}
.gantt-content::-webkit-scrollbar-thumb:hover {
  background: #a8a8a8; 
}
</style>
