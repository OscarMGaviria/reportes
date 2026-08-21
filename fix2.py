import re
with open('src/App.vue', 'r', encoding='utf-8') as f:
    c = f.read()

# Fix the injection to use descripcion
old_injection = '''        } else if (catName.includes('MANEJO DE TRANSITO') || catName.includes('MANEJO AMBIENTAL') || catName.includes('CARACTERIZACION VIAL') || catName.includes('CARACTERIZACIÓN VIAL')) {
          categoriasProg[catName] = {
            nombre_categoria: catName,
            id_actividad: ap.id_actividad,
            unidad: 'GLB',
            total: 0,
            completado: 0,
            valor_total: (ap.valor_total_esperado || 0)
          };
        }'''

new_injection = '''        } else if (ap.id_actividad === 'MACRO-PMA' || ap.id_actividad === 'MACRO-PMT' || ap.id_actividad === 'MACRO-CARAC') {
          const mName = catObj.descripcion;
          categoriasProg[mName] = {
            nombre_categoria: mName,
            id_actividad: ap.id_actividad,
            unidad: 'GLB',
            total: 0,
            completado: 0,
            valor_total: (ap.valor_total_esperado || 0)
          };
        }'''
c = c.replace(old_injection, new_injection)

# Also fix the execution loop
old_exec = '''          if (categoriasProg[catName].subItems && sa.subItems_ejecutados) {'''
new_exec = '''        } else if (sa.id_actividad === 'MACRO-PMA' || sa.id_actividad === 'MACRO-PMT' || sa.id_actividad === 'MACRO-CARAC') {
          const mName = catObj.descripcion;
          if (categoriasProg[mName]) {
            categoriasProg[mName].completado = sa.cantidad_ejecutada || 0;
            categoriasProg[mName].id_actividad = sa.id_actividad;
          }
        }
        if (categoriasProg[catName] && categoriasProg[catName].subItems && sa.subItems_ejecutados) {'''
c = c.replace(old_exec, new_exec)

# Excel-like styles
excel_style = '''
<style scoped>
.excel-table {
  width: 100%;
  border-collapse: collapse;
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  font-size: 13px;
}
.excel-table th, .excel-table td {
  border: 1px solid #d4d4d4;
  padding: 4px 8px;
}
.excel-table th {
  background-color: #f3f3f3;
  color: #333;
  font-weight: 600;
  text-align: center;
  border-bottom: 2px solid #a0a0a0;
}
.excel-table input {
  width: 100%;
  box-sizing: border-box;
  border: 1px solid transparent;
  padding: 4px;
  background-color: transparent;
  outline: none;
  text-align: right;
  font-family: inherit;
}
.excel-table input:focus {
  border: 2px solid #217346;
  background-color: #fff;
}
.excel-table input[type="number"]::-webkit-inner-spin-button, 
.excel-table input[type="number"]::-webkit-outer-spin-button { 
  -webkit-appearance: none; 
  margin: 0; 
}
.excel-table tr:nth-child(even) {
  background-color: #fafafa;
}
.excel-table tr:hover {
  background-color: #e5f1eb;
}
'''

c = c.replace('<table style="width: 100%; border-collapse: collapse;">', '<table class="excel-table">')
c = c.replace('style="padding: 8px; border: 1px solid #ddd; text-align: left;"', '')
c = c.replace('style="padding: 8px; border: 1px solid #ddd; text-align: right;"', '')
c = c.replace('style="padding: 8px; border: 1px solid #ddd;"', '')
c = c.replace('style="width: 50px;"', '')
c = c.replace('style="width: 60px;"', '')
c = c.replace('style="width: 120px;"', '')
c = c.replace('style="background: #f5f5f5;"', '')
if '.excel-table {' not in c:
    c = c.replace('<style scoped>', excel_style)

with open('src/App.vue', 'w', encoding='utf-8') as f:
    f.write(c)
