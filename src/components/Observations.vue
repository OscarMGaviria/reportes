<script setup>
import { computed } from 'vue'

const props = defineProps({
  observaciones: { type: Array, required: true },
  tipoEstructura: { type: Array, required: false }
})

const splitObservaciones = computed(() => {
  if (!props.observaciones) return []
  let result = []
  props.observaciones.forEach(obs => {
    if (typeof obs === 'string') {
      // Dividir primero por saltos de línea
      let lines = obs.split(/\n+/)
      lines.forEach(line => {
        // Luego dividir por punto seguido de un espacio y una letra mayúscula
        let sentences = line.split(/(?<=\.)\s+(?=[A-Z¿¡])/)
        sentences.forEach(s => {
          let trimmed = s.trim()
          if (trimmed) {
            result.push(trimmed)
          }
        })
      })
    }
  })
  return result
})
</script>

<template>
  <div class="card-container obs-card">
    <ul class="obs-list">
      <li v-for="(obs, index) in splitObservaciones" :key="index">
        <span class="bullet dot-green"></span>
        <span>{{ obs }}</span>
      </li>
    </ul>
  </div>
</template>

<style scoped>
.obs-card {
  flex: 1;
  min-height: 0;
  padding: 2vh 1.5vw;
  display: flex;
  flex-direction: column;
  overflow-y: auto;
}

.obs-list {
  flex: 1; 
  display: flex;
  flex-direction: column;
  gap: 1.2vh;
  margin-bottom: 2vh;
}

.obs-list li {
  display: flex;
  align-items: flex-start;
  gap: 0.8vw;
  font-size: 1.5vh;
  line-height: 1.3;
}

.bullet {
  width: 0.8vh;
  height: 0.8vh;
  border-radius: 50%;
  flex-shrink: 0;
  margin-top: 0.4vh;
}
.dot-green { background-color: var(--color-primary); }


</style>
