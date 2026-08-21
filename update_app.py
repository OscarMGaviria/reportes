import re

with open('src/App.vue', 'r', encoding='utf-8') as f:
    c = f.read()

if 'const showEditModal' not in c:
    c = c.replace('const corteProcesado = computed(() => {', 'const showEditModal = ref(false);\n\nconst saveModal = async () => {\n  const payload = {\n    id_circuito: idCircuito.value,\n    semana: semanaIndex.value,\n    actividades: corteProcesado.value.actividades_ejecutadas.flatMap(act => {\n      if (act.subItems && act.subItems.length > 0) {\n        // Just sum the executed and return the parent act to save. Wait, if they edit subItems, we only save the parent total executed, but the UI shows subitems.\n        return { \n           id_actividad: act.id_actividad,\n           nombre_categoria: act.nombre_categoria || act.nombre,\n           unidad: act.subItems[0].unidad,\n           total: act.subItems.reduce((acc, sub) => acc + parseFloat(sub.total), 0),\n           ejecutado: act.subItems.reduce((acc, sub) => acc + parseFloat(sub.completado), 0),\n           presupuesto: act.valor_total\n        };\n      } else {\n        return {\n           id_actividad: act.id_actividad,\n           nombre_categoria: act.nombre_categoria || act.nombre,\n           unidad: act.unidad,\n           total: act.total,\n           ejecutado: act.completado,\n           presupuesto: act.valor_total\n        };\n      }\n    })\n  };\n  const res = await fetch("/api/save-activities", { method: "POST", body: JSON.stringify(payload) });\n  if(res.ok) { showEditModal.value = false; window.location.reload(); }\n};\n\nconst corteProcesado = computed(() => {')

modal_code = '''
    <!-- EDIT MODAL -->
    <div v-if="showEditModal" class="modal-overlay">
      <div class="modal-content">
        <div class="modal-header">
          <h2>Editar Actividades - {{ selectedCircuito?.label }}</h2>
          <button @click="showEditModal = false" class="close-btn">✕</button>
        </div>
        <div class="modal-body" style="max-height: 70vh; overflow-y: auto;">
          <table style="width: 100%; border-collapse: collapse;">
            <thead>
              <tr style="background: #f5f5f5;">
                <th style="padding: 8px; border: 1px solid #ddd; text-align: left;">Actividad</th>
                <th style="padding: 8px; border: 1px solid #ddd; text-align: right;">Unidad</th>
                <th style="padding: 8px; border: 1px solid #ddd; text-align: right;">Ejecutado</th>
                <th style="padding: 8px; border: 1px solid #ddd; text-align: right;">Total Programado</th>
                <th style="padding: 8px; border: 1px solid #ddd; text-align: right;">Costo Base ($)</th>
              </tr>
            </thead>
            <tbody>
              <template v-for="(act, idx) in corteProcesado.actividades_ejecutadas" :key="idx">
                <template v-if="act.subItems && act.subItems.length > 0">
                  <tr v-for="(sub, sidx) in act.subItems" :key="'s'+idx+'-'+sidx">
                    <td style="padding: 8px; border: 1px solid #ddd;">{{ act.nombre_categoria || act.nombre }} - {{ sub.nombre }}</td>
                    <td style="padding: 8px; border: 1px solid #ddd; text-align: right;"><input type="text" v-model="sub.unidad" style="width: 50px;" /></td>
                    <td style="padding: 8px; border: 1px solid #ddd; text-align: right;"><input type="number" v-model="sub.completado" style="width: 60px;" /></td>
                    <td style="padding: 8px; border: 1px solid #ddd; text-align: right;"><input type="number" v-model="sub.total" style="width: 60px;" /></td>
                    <td style="padding: 8px; border: 1px solid #ddd; text-align: right;"><input type="number" v-model="act.valor_total" style="width: 120px;" v-if="sidx === 0" /></td>
                  </tr>
                </template>
                <template v-else>
                  <tr>
                    <td style="padding: 8px; border: 1px solid #ddd;">{{ act.nombre_categoria || act.nombre }}</td>
                    <td style="padding: 8px; border: 1px solid #ddd; text-align: right;"><input type="text" v-model="act.unidad" style="width: 50px;" /></td>
                    <td style="padding: 8px; border: 1px solid #ddd; text-align: right;"><input type="number" v-model="act.completado" style="width: 60px;" /></td>
                    <td style="padding: 8px; border: 1px solid #ddd; text-align: right;"><input type="number" v-model="act.total" style="width: 60px;" /></td>
                    <td style="padding: 8px; border: 1px solid #ddd; text-align: right;"><input type="number" v-model="act.valor_total" style="width: 120px;" /></td>
                  </tr>
                </template>
              </template>
            </tbody>
          </table>
        </div>
        <div class="modal-footer" style="padding: 15px; text-align: right; border-top: 1px solid #ddd; margin-top: 15px;">
          <button @click="saveModal()" style="background: #4caf50; color: white; padding: 10px 20px; border: none; border-radius: 4px; cursor: pointer; font-weight: bold;">Guardar Cambios</button>
        </div>
      </div>
    </div>
  </div>
</template>
'''

if 'modal-overlay' not in c:
    c = c.replace('  </div>\n</template>', modal_code)

style = '''
<style scoped>
.modal-overlay {
  position: fixed;
  top: 0; left: 0; right: 0; bottom: 0;
  background: rgba(0,0,0,0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 9999;
}
.modal-content {
  background: white;
  border-radius: 8px;
  width: 90vw;
  max-width: 1000px;
  padding: 20px;
  box-shadow: 0 4px 12px rgba(0,0,0,0.15);
}
.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}
.close-btn {
  background: none; border: none; font-size: 20px; cursor: pointer;
}
'''
if '.modal-overlay' not in c:
    c = c.replace('<style scoped>', style)

if '✎ Editar' not in c:
    c = c.replace('<h2 class="section-title">Avance de actividades ejecutadas</h2>', '<h2 class="section-title cursor-pointer" @click="showEditModal = true" style="cursor: pointer; padding: 5px; background: #e8f5e9; border-radius: 4px; display: inline-block;">Avance de actividades ejecutadas <span style="font-size: 0.8em; color: #4caf50;">✎ Editar</span></h2>')

with open('src/App.vue', 'w', encoding='utf-8') as f:
    f.write(c)
