<script setup>
const props = defineProps({
  observaciones: { type: Array, required: true },
  tipoEstructura: { type: Array, required: true }
})
</script>

<template>
  <div class="card-container obs-card">
    <ul class="obs-list">
      <li v-for="(obs, index) in observaciones" :key="index">
        <span class="bullet dot-green"></span>
        <span>{{ obs }}</span>
      </li>
    </ul>
  </div>
</template>

<style scoped>
.obs-card {
  flex: 0.8;
  padding: 2vh 1.5vw;
  display: flex;
  flex-direction: column;
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

@media (max-width: 1024px) {
  .obs-card {
    padding: 2vh 4vw;
  }

  .obs-list li {
    font-size: clamp(0.85rem, 2vw, 1rem);
  }
}
</style>
