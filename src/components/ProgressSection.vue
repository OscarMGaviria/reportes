<script setup>
const props = defineProps({
  corte: { type: Object, required: true }
})

const formatCurrency = (value) => {
  return new Intl.NumberFormat('es-CO', { style: 'decimal', minimumFractionDigits: 0 }).format(value)
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
        <div class="data-row" v-if="corte.financiero.anticipo">
          <div class="label"><span class="dot dot-blue"></span> Anticipo</div>
          <div class="value">$ {{ formatCurrency(corte.financiero.anticipo.valor) }}</div>
          <div class="percentage text-blue font-bold">{{ corte.financiero.anticipo.porcentaje }}%</div>
        </div>
        <div class="data-row">
          <div class="label"><span class="dot dot-blue"></span> Programado</div>
          <div class="value">$ {{ formatCurrency(corte.financiero.programado.valor) }}</div>
          <div class="percentage text-blue font-bold">{{ corte.financiero.programado.porcentaje }}%</div>
        </div>
        <div class="data-row">
          <div class="label"><span class="dot dot-dark-green"></span> Ejecutado</div>
          <div class="value">$ {{ formatCurrency(corte.financiero.ejecutado.valor) }}</div>
          <div class="percentage text-dark-green font-bold">{{ corte.financiero.ejecutado.porcentaje }}%</div>
        </div>
        <div class="data-row">
          <div class="label"><span class="dot dot-light-green"></span> Avance</div>
          <div class="value">$ {{ formatCurrency(corte.financiero.avance.valor) }}</div>
          <div class="percentage text-light-green font-bold">{{ corte.financiero.avance.porcentaje }}%</div>
        </div>
      </div>
      
      <div class="card-bottom-badge">
        <span class="status-icon">✓</span> {{ corte.financiero.estado }}
      </div>
    </div>

    <!-- Físico -->
    <div class="card-container progress-card">
      <div class="card-top-badge">
        <div class="badge-icon">|||</div> FÍSICO
      </div>
      
      <div class="progress-data">
        <div class="data-row">
          <div class="label"><span class="dot dot-blue"></span> Programado</div>
          <div class="value percentage-only text-blue font-bold">{{ corte.fisico.programado }}%</div>
          <div class="bar-container">
            <div class="progress-bar-bg"><div class="progress-bar-fill progress-fill-blue" :style="{ width: corte.fisico.programado + '%' }"></div></div>
          </div>
        </div>
        <div class="data-row">
          <div class="label"><span class="dot dot-dark-green"></span> Ejecutado</div>
          <div class="value percentage-only text-dark-green font-bold">{{ corte.fisico.ejecutado }}%</div>
          <div class="bar-container">
            <div class="progress-bar-bg"><div class="progress-bar-fill progress-fill-dark-green" :style="{ width: corte.fisico.ejecutado + '%' }"></div></div>
          </div>
        </div>
        <div class="data-row">
          <div class="label"><span class="dot dot-light-green"></span> Avance</div>
          <div class="value percentage-only text-light-green font-bold">{{ corte.fisico.avance }}%</div>
          <div class="bar-container">
            <div class="progress-bar-bg"><div class="progress-bar-fill progress-fill-light-green" :style="{ width: corte.fisico.avance + '%' }"></div></div>
          </div>
        </div>
      </div>
      
      <div class="card-bottom-badge">
        <span class="status-icon">✓</span> {{ corte.fisico.estado }}
      </div>
    </div>
  </div>
</template>

<style scoped>
.progress-section {
  flex: 0 0 auto; 
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1.5vw;
}

.progress-card {
  padding-top: 5vh;
  padding-bottom: 3.5vh;
  min-height: 24vh;
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

.text-dark-green { color: var(--color-primary-dark); }
.text-light-green { color: #7AA980; }
</style>
