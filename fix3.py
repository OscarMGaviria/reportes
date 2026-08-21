import re
with open('src/App.vue', 'r', encoding='utf-8') as f:
    c = f.read()

# Add computed for Total Cost
total_cost_computed = '''
const modalTotalCost = computed(() => {
  if (!corteActual.value || !corteActual.value.actividades_ejecutadas) return 0;
  return corteActual.value.actividades_ejecutadas.reduce((sum, act) => sum + (parseFloat(act.valor_total) || 0), 0);
});

const handlePaste = (event, colIndex, startRowIndex) => {
  const pasteData = event.clipboardData.getData('text');
  if (!pasteData) return;
  
  const rows = pasteData.split(/[\\r\\n]+/).filter(r => r.trim() !== '');
  if (rows.length <= 1) return; // standard single paste is fine natively
  
  event.preventDefault();
  
  const flatInputs = [];
  corteActual.value.actividades_ejecutadas.forEach(act => {
    if (act.subItems && act.subItems.length > 0) {
      act.subItems.forEach((sub, sidx) => {
        flatInputs.push({ act, sub, isFirst: sidx === 0 });
      });
    } else {
      flatInputs.push({ act, sub: act, isFirst: true });
    }
  });
  
  let dataIndex = 0;
  for (let i = startRowIndex; i < flatInputs.length && dataIndex < rows.length; i++) {
    const item = flatInputs[i];
    const val = rows[dataIndex];
    if (colIndex === 'unidad') item.sub.unidad = val;
    else if (colIndex === 'completado') item.sub.completado = parseFloat(val) || 0;
    else if (colIndex === 'total') item.sub.total = parseFloat(val) || 0;
    else if (colIndex === 'valor_total' && item.isFirst) item.act.valor_total = parseFloat(val) || 0;
    
    if (!(colIndex === 'valor_total' && !item.isFirst)) {
      dataIndex++;
    }
  }
};
'''

if 'const modalTotalCost = computed' not in c:
    c = c.replace('const showEditModal = ref(false);', 'const showEditModal = ref(false);\n' + total_cost_computed)

# Add tfoot
tfoot = '''
            </tbody>
            <tfoot>
              <tr style="background-color: #e5f1eb; font-weight: bold; border-top: 2px solid #217346;">
                <td colspan="4" style="text-align: right; padding: 8px;">TOTAL COSTO DEL TRAMO:</td>
                <td style="text-align: right; padding: 8px; font-size: 14px;">$ {{ formatCurrency(modalTotalCost) }}</td>
              </tr>
            </tfoot>
          </table>
'''
c = c.replace('</tbody>\n          </table>', tfoot)

# Add paste handlers
c = c.replace('v-model="sub.unidad" style="width: 50px;" />', 'v-model="sub.unidad" @paste="handlePaste($event, \'unidad\', flatIndex(idx, sidx))" />')
c = c.replace('v-model="sub.completado" style="width: 60px;" />', 'v-model="sub.completado" @paste="handlePaste($event, \'completado\', flatIndex(idx, sidx))" />')
c = c.replace('v-model="sub.total" style="width: 60px;" />', 'v-model="sub.total" @paste="handlePaste($event, \'total\', flatIndex(idx, sidx))" />')
c = c.replace('v-model="act.valor_total" style="width: 120px;" v-if="sidx === 0" />', 'v-model="act.valor_total" v-if="sidx === 0" @paste="handlePaste($event, \'valor_total\', flatIndex(idx, sidx))" />')

c = c.replace('v-model="act.unidad" style="width: 50px;" />', 'v-model="act.unidad" @paste="handlePaste($event, \'unidad\', flatIndex(idx, 0))" />')
c = c.replace('v-model="act.completado" style="width: 60px;" />', 'v-model="act.completado" @paste="handlePaste($event, \'completado\', flatIndex(idx, 0))" />')
c = c.replace('v-model="act.total" style="width: 60px;" />', 'v-model="act.total" @paste="handlePaste($event, \'total\', flatIndex(idx, 0))" />')
c = c.replace('v-model="act.valor_total" style="width: 120px;" />', 'v-model="act.valor_total" @paste="handlePaste($event, \'valor_total\', flatIndex(idx, 0))" />')

# Also replace for the newly added styles without inline styles
c = c.replace('v-model="sub.unidad" />', 'v-model="sub.unidad" @paste="handlePaste($event, \'unidad\', flatIndex(idx, sidx))" />')
c = c.replace('v-model="sub.completado" />', 'v-model="sub.completado" @paste="handlePaste($event, \'completado\', flatIndex(idx, sidx))" />')
c = c.replace('v-model="sub.total" />', 'v-model="sub.total" @paste="handlePaste($event, \'total\', flatIndex(idx, sidx))" />')
c = c.replace('v-model="act.valor_total" v-if="sidx === 0" />', 'v-model="act.valor_total" v-if="sidx === 0" @paste="handlePaste($event, \'valor_total\', flatIndex(idx, sidx))" />')

c = c.replace('v-model="act.unidad" />', 'v-model="act.unidad" @paste="handlePaste($event, \'unidad\', flatIndex(idx, 0))" />')
c = c.replace('v-model="act.completado" />', 'v-model="act.completado" @paste="handlePaste($event, \'completado\', flatIndex(idx, 0))" />')
c = c.replace('v-model="act.total" />', 'v-model="act.total" @paste="handlePaste($event, \'total\', flatIndex(idx, 0))" />')
c = c.replace('v-model="act.valor_total" />', 'v-model="act.valor_total" @paste="handlePaste($event, \'valor_total\', flatIndex(idx, 0))" />')

# clean up duplicate handlers if any
c = c.replace('@paste="handlePaste($event, \'unidad\', flatIndex(idx, sidx))" @paste="handlePaste($event, \'unidad\', flatIndex(idx, sidx))"', '@paste="handlePaste($event, \'unidad\', flatIndex(idx, sidx))"')
c = c.replace('@paste="handlePaste($event, \'completado\', flatIndex(idx, sidx))" @paste="handlePaste($event, \'completado\', flatIndex(idx, sidx))"', '@paste="handlePaste($event, \'completado\', flatIndex(idx, sidx))"')
c = c.replace('@paste="handlePaste($event, \'total\', flatIndex(idx, sidx))" @paste="handlePaste($event, \'total\', flatIndex(idx, sidx))"', '@paste="handlePaste($event, \'total\', flatIndex(idx, sidx))"')

c = c.replace('@paste="handlePaste($event, \'unidad\', flatIndex(idx, 0))" @paste="handlePaste($event, \'unidad\', flatIndex(idx, 0))"', '@paste="handlePaste($event, \'unidad\', flatIndex(idx, 0))"')
c = c.replace('@paste="handlePaste($event, \'completado\', flatIndex(idx, 0))" @paste="handlePaste($event, \'completado\', flatIndex(idx, 0))"', '@paste="handlePaste($event, \'completado\', flatIndex(idx, 0))"')
c = c.replace('@paste="handlePaste($event, \'total\', flatIndex(idx, 0))" @paste="handlePaste($event, \'total\', flatIndex(idx, 0))"', '@paste="handlePaste($event, \'total\', flatIndex(idx, 0))"')
c = c.replace('@paste="handlePaste($event, \'valor_total\', flatIndex(idx, 0))" @paste="handlePaste($event, \'valor_total\', flatIndex(idx, 0))"', '@paste="handlePaste($event, \'valor_total\', flatIndex(idx, 0))"')

flat_index = '''
const flatIndex = (actIdx, subIdx) => {
  if (!corteActual.value || !corteActual.value.actividades_ejecutadas) return 0;
  let index = 0;
  for (let i = 0; i < actIdx; i++) {
    const a = corteActual.value.actividades_ejecutadas[i];
    index += (a.subItems && a.subItems.length > 0) ? a.subItems.length : 1;
  }
  return index + subIdx;
};
'''
if 'const flatIndex = ' not in c:
    c = c.replace('const showEditModal = ref(false);', 'const showEditModal = ref(false);\n' + flat_index)

with open('src/App.vue', 'w', encoding='utf-8') as f:
    f.write(c)
