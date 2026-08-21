import re
with open('src/App.vue', 'r', encoding='utf-8') as f:
    c = f.read()

logic = '''
const isSyncing = ref(false)
const syncAllPending = async () => {
  if (pendingSyncs.value.length === 0) return;
  isSyncing.value = true;
  try {
    for (const payload of pendingSyncs.value) {
      const res = await fetch('/api/save-activities', { 
          method: 'POST', 
          body: JSON.stringify(payload) 
      });
      if (!res.ok) throw new Error('Error saving ' + payload.id_circuito);
    }
    await localforage.setItem('pending_syncs', []);
    pendingSyncs.value = [];
    alert('Sincronización exitosa con el servidor local.');
  } catch(e) {
    console.error(e);
    alert('Ocurrió un error al sincronizar. Algunos datos pudieron no guardarse.');
  } finally {
    isSyncing.value = false;
  }
}

const isDeploying = ref(false)
const deployToGithub = async () => {
  if(!confirm('¿Estás seguro de subir todos los cambios al repositorio público de GitHub?')) return;
  isDeploying.value = true;
  try {
    const res = await fetch('/api/deploy', { method: 'POST' });
    if(res.ok) {
      alert('Cambios publicados exitosamente en GitHub!');
    } else {
      alert('Error al publicar en GitHub.');
    }
  } catch(e) {
    alert('Error al contactar con el servidor local para publicar.');
  } finally {
    isDeploying.value = false;
  }
}
'''

idx = c.find('const saveModal = async () => {')
c = c[:idx] + logic + '\n\n' + c[idx:]

ui = '''
      <div class="topbar-actions">
        <button v-if="isLocalhost && pendingSyncs.length > 0" class="topbar-btn sync-btn" @click="syncAllPending" :disabled="isSyncing" title="Sincronizar cambios">
          ☁️ {{ isSyncing ? '...' : pendingSyncs.length }}
        </button>
        <button v-if="isLocalhost" class="topbar-btn publish-btn" @click="deployToGithub" :disabled="isDeploying" title="Publicar en GitHub">
          🚀 {{ isDeploying ? '...' : 'Publicar' }}
        </button>
        <button class="topbar-btn" @click="showGanttModal = true" title="Ver Gantt 18 Meses">
'''

c = c.replace('<div class="topbar-actions">\n        <button class="topbar-btn" @click="showGanttModal = true" title="Ver Gantt 18 Meses">', ui)

with open('src/App.vue', 'w', encoding='utf-8') as f:
    f.write(c)
