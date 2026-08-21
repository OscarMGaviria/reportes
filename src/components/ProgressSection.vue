<script setup>
import { Check } from 'lucide-vue-next'

const props = defineProps({
  corte: { type: Object, required: true }
})

const formatCurrency = (value) => {
  return new Intl.NumberFormat('es-CO', { style: 'decimal', minimumFractionDigits: 0, maximumFractionDigits: 0 }).format(value)
}
</script>

<template>
  <div class="progress-section">
    <!-- Financiero -->
    <div class="card-container progress-card">
      <div class="card-top-badge">
        <div class="badge-icon">$</div> FINANCIERO
      </div>
      
      <div class="progress-data">
        <div class="data-row">
          <div class="label"><span class="dot dot-gray"></span> Valor del tramo</div>
          <div class="value">$ {{ formatCurrency(corte.financiero.programado.valor) }}</div>
          <div class="percentage font-bold">{{ corte.financiero.programado.porcentaje }}%</div>
        </div>
        <div class="data-row" v-if="corte.financiero.anticipo">
          <div class="label"><span class="dot dot-gray"></span> Anticipo</div>
          <div class="value">$ {{ formatCurrency(corte.financiero.anticipo.valor) }}</div>
          <div class="percentage font-bold">{{ corte.financiero.anticipo.porcentaje }}%</div>
        </div>
        <div class="data-row">
          <div class="label"><span class="dot dot-gray"></span> Ejecutado</div>
          <div class="value">$ {{ formatCurrency(corte.financiero.ejecutado.valor) }}</div>
          <div class="percentage font-bold">{{ corte.financiero.ejecutado.porcentaje }}%</div>
        </div>
      </div>
      

    </div>

    <!-- Físico -->
    <div class="card-container progress-card">
      <div class="card-top-badge">
        <div class="badge-icon">|||</div> FÍSICO
      </div>
      
      <div class="progress-data">
        <div class="data-row">
          <div class="label"><span class="dot dot-gray"></span> Programado</div>
          <div class="percentage-only font-bold">{{ corte.fisico.programado }}%</div>
          <div class="bar-container">
            <div class="progress-bar-bg"><div class="progress-bar-fill progress-fill-dark-green" :style="{ width: corte.fisico.programado + '%' }"></div></div>
          </div>
        </div>
        <div class="data-row">
          <div class="label"><span class="dot dot-gray"></span> Ejecutado</div>
          <div class="percentage-only font-bold">{{ corte.fisico.ejecutado }}%</div>
          <div class="bar-container">
            <div class="progress-bar-bg"><div class="progress-bar-fill progress-fill-dark-green" :style="{ width: corte.fisico.ejecutado + '%' }"></div></div>
          </div>
        </div>
        <div class="data-row">
          <div class="label"><span class="dot dot-gray"></span> Avance</div>
          <div class="percentage-only font-bold">{{ corte.fisico.avance }}%</div>
          <div class="bar-container">
            <div class="progress-bar-bg"><div class="progress-bar-fill progress-fill-dark-green" :style="{ width: corte.fisico.avance + '%' }"></div></div>
          </div>
        </div>
      </div>
      

    </div>
  </div>
</template>

<style scoped>
.progress-section {
  flex: 1; 
  min-height: 0;
  display: flex;
  gap: 1.5vw;
}

.progress-card {
  flex: 1;
  padding-top: 5vh;
  padding-bottom: 3.5vh;
  display: flex;
  flex-direction: column;
  justify-content: center;
}

.progress-data {
  display: flex;
  flex-direction: column;
  gap: 2vh;
}

.data-row {
  display: flex;
  align-items: center;
  font-size: 1.6vh;
}

.label {
  flex: 1;
  display: flex;
  align-items: center;
  gap: 0.5vw;
  color: var(--color-text-main);
}

.value {
  flex: 1;
  text-align: right;
  white-space: nowrap;
}

.percentage {
  width: 4vw;
  text-align: right;
}

.percentage-only {
  width: 3vw;
  text-align: left;
  flex: none;
}

.bar-container {
  flex: 1;
  margin-left: 1vw;
}

.dot {
  width: 1vh;
  height: 1vh;
  border-radius: 50%;
  display: inline-block;
}

.dot-blue { background-color: var(--color-accent-blue); }
.dot-dark-green { background-color: var(--color-primary-dark); }
.dot-light-green { background-color: #7AA980; }
.dot-gray { background-color: #6b7280; }

.text-dark-green { color: var(--color-primary-dark); }
.text-light-green { color: #7AA980; }


</style>
