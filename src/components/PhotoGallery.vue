<script setup>
import { ref } from 'vue'

const props = defineProps({
  imagenes: { type: Array, required: true }
})

const selectedImageIndex = ref(null)

const openModal = (index) => {
  selectedImageIndex.value = index
}

const closeModal = () => {
  selectedImageIndex.value = null
}
</script>

<template>
  <div class="photo-gallery">
    <template v-if="imagenes && imagenes.length > 0">
      <div v-for="(img, index) in imagenes" :key="img.id" class="photo-card">
        <div class="img-wrapper" @click="openModal(index)">
          <img :src="`https://picsum.photos/seed/${img.id+index}/400/300`" :alt="img.descripcion" />
          <div class="photo-number">{{ index + 1 }}</div>
        </div>
        <div class="photo-caption bg-dark-green">
          <span class="photo-desc">{{ img.descripcion }}</span>
        </div>
      </div>
    </template>
    <template v-else>
      <div class="photo-card empty-card" style="grid-column: 1 / -1; display: flex; align-items: center; justify-content: center; background: #f3f4f6; padding: 2vh;">
        <span style="color: #6b7280; font-size: 1.6vh; font-style: italic;">Sin registro fotográfico reportado para esta semana.</span>
      </div>
    </template>


    <!-- Modal para imagen ampliada -->
    <div v-if="selectedImageIndex !== null" class="modal-overlay" @click="closeModal">
      <div class="modal-content" @click.stop>
        <button class="close-btn" @click="closeModal">✕</button>
        <img 
          :src="`https://picsum.photos/seed/${imagenes[selectedImageIndex].id+selectedImageIndex}/800/600`" 
          :alt="imagenes[selectedImageIndex].descripcion" 
          class="enlarged-img"
        />
        <div class="modal-caption bg-dark-green">
          <span class="photo-desc">{{ imagenes[selectedImageIndex].descripcion }}</span>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.photo-gallery {
  flex: 1.5; 
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  grid-template-rows: 1fr 1fr;
  gap: 1vw;
  overflow: hidden;
}

.photo-card {
  border-radius: 6px;
  overflow: hidden;
  display: flex;
  flex-direction: column;
}

.img-wrapper {
  flex: 1;
  position: relative;
  cursor: pointer;
  overflow: hidden;
}

.img-wrapper img {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.3s ease;
}

.img-wrapper:hover img {
  transform: scale(1.05);
}

.img-wrapper.no-cursor {
  cursor: default;
}

.img-wrapper.no-cursor:hover img {
  transform: none;
}

.photo-number {
  position: absolute;
  bottom: 0.5vh;
  left: 0.5vw;
  background-color: white;
  color: var(--color-primary-dark);
  border-radius: 50%;
  width: 2.8vh;
  height: 2.8vh;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: bold;
  font-size: 1.6vh;
  z-index: 2;
}

.photo-caption {
  flex: 0 0 auto;
  padding: 0.6vh 1vw 0.6vh 2.5vw;
  display: flex;
  align-items: center;
}

.photo-desc {
  font-size: 1.4vh;
  line-height: 1.2;
  color: white;
}

/* Modal Styles */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  background-color: rgba(0, 0, 0, 0.85);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.modal-content {
  position: relative;
  width: 80vw;
  max-width: 1000px;
  height: 80vh;
  display: flex;
  flex-direction: column;
  background-color: white;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 10px 30px rgba(0,0,0,0.5);
  animation: modalIn 0.3s ease-out;
}

@keyframes modalIn {
  from { opacity: 0; transform: scale(0.95); }
  to { opacity: 1; transform: scale(1); }
}

.close-btn {
  position: absolute;
  top: 15px;
  right: 15px;
  background: rgba(0,0,0,0.5);
  color: white;
  border: 2px solid white;
  font-size: 20px;
  width: 40px;
  height: 40px;
  border-radius: 50%;
  cursor: pointer;
  z-index: 10;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s ease;
}

.close-btn:hover {
  background: white;
  color: black;
}

.enlarged-img {
  width: 100%;
  flex: 1;
  object-fit: contain;
  background-color: #111;
}

.modal-caption {
  padding: 15px;
  text-align: center;
  font-size: 1.8vh;
}
</style>
