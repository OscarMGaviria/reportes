<script setup>
const props = defineProps({
  actividades: { type: Array, required: true }
})

const formatNumber = (num) => {
  return new Intl.NumberFormat('es-CO', { minimumFractionDigits: 2, maximumFractionDigits: 2 }).format(num)
}
</script>

<template>
  <div class="card-container activities-card">
    <div class="activities-grid">
      <div v-for="(act, index) in actividades" :key="index" class="activity-item">
        <div class="check-icon">✓</div>
        <div class="act-icon-wrapper">
          <div class="act-icon-placeholder"></div>
        </div>
        <div class="act-details">
          <div class="act-name">{{ act.nombre }}: <span v-if="act.porcentaje !== undefined" class="text-green font-bold">{{ act.porcentaje }}%</span></div>
          <div v-if="act.completado !== undefined" class="act-progress">
            <span class="text-blue font-bold">{{ formatNumber(act.completado) }} {{ act.unidad }}</span> / {{ formatNumber(act.total) }} {{ act.unidad }}
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.activities-card {
  flex: 1; 
  padding: 1.5vh;
  overflow: hidden;
}

.activities-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  row-gap: 1.5vh;
  column-gap: 2vw;
  height: 100%;
  align-content: start;
}

.activity-item {
  display: flex;
  align-items: center;
  gap: 1vw;
  padding: 0.5vh 0;
  border-bottom: 1px solid #f0f0f0;
}

.activity-item:nth-child(odd) {
  border-right: 2px solid var(--color-border);
  padding-right: 1.5vw;
}

.check-icon {
  background-color: var(--color-primary);
  color: white;
  border-radius: 50%;
  width: 2.2vh;
  height: 2.2vh;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.2vh;
  flex-shrink: 0;
}

.act-icon-wrapper {
  width: 3vh;
  height: 3vh;
  display: flex;
  align-items: center;
  justify-content: center;
}

.act-icon-placeholder {
  width: 100%;
  height: 100%;
  background-image: repeating-linear-gradient(45deg, #1f4287 0, #1f4287 2px, transparent 2px, transparent 4px);
  border: 1px solid #1f4287;
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
</style>
