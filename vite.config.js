import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import fs from 'fs'
import path from 'path'
import { exec } from 'child_process'

const apiPlugin = () => {
  return {
    name: 'api-plugin',
    configureServer(server) {
      server.middlewares.use(async (req, res, next) => {
        if (req.url === '/api/save-activities' && req.method === 'POST') {
          let body = '';
          req.on('data', chunk => { body += chunk.toString(); });
          req.on('end', () => {
            try {
              const payload = JSON.parse(body);
              const dataDir = path.resolve(__dirname, 'src/data');
              const { id_circuito, semana, actividades } = payload;
              
              const metasPath = path.join(dataDir, 'metas_fisicas.json');
              const presupuestosPath = path.join(dataDir, 'presupuestos_y_cronograma_base.json');
              
              const metas = JSON.parse(fs.readFileSync(metasPath, 'utf-8'));
              const presupuestos = JSON.parse(fs.readFileSync(presupuestosPath, 'utf-8'));
              
              if (!metas[id_circuito]) metas[id_circuito] = {};
              const circuitoPres = presupuestos.find(p => p.id_circuito == id_circuito);
              
              const weekPath = path.join(dataDir, 'cortes_semanales', `cortes_circuito_${id_circuito}.json`);
              let cortes = [];
              if (fs.existsSync(weekPath)) {
                cortes = JSON.parse(fs.readFileSync(weekPath, 'utf-8'));
              }
              let corteData = cortes.find(c => c.semana === semana);
              if (!corteData) {
                corteData = { semana: semana, fecha_corte: new Date().toISOString().split('T')[0], seguimiento_actividades: [] };
                cortes.push(corteData);
              }

              actividades.forEach(act => {
                const { id_actividad, nombre_categoria, unidad, total, ejecutado, presupuesto, subitem_nombre } = act;
                
                // 1. Update Metas
                if (!metas[id_circuito][nombre_categoria]) {
                  metas[id_circuito][nombre_categoria] = { total: 0, unidad, subItems: [] };
                }
                if (subitem_nombre) {
                  if (!metas[id_circuito][nombre_categoria].subItems) metas[id_circuito][nombre_categoria].subItems = [];
                  let sub = metas[id_circuito][nombre_categoria].subItems.find(s => s.nombre === subitem_nombre);
                  if (!sub) {
                    sub = { nombre: subitem_nombre, total: 0, unidad };
                    metas[id_circuito][nombre_categoria].subItems.push(sub);
                  }
                  sub.total = parseFloat(total);
                  metas[id_circuito][nombre_categoria].total = metas[id_circuito][nombre_categoria].subItems.reduce((acc, s) => acc + (parseFloat(s.total)||0), 0);
                } else {
                  metas[id_circuito][nombre_categoria].total = parseFloat(total);
                }

                // 2. Update Presupuesto
                if (circuitoPres && id_actividad) {
                  let pAct = circuitoPres.actividades_programadas.find(ap => ap.id_actividad === id_actividad);
                  if (!pAct) {
                    pAct = { id_actividad, valor_total_esperado: 0 };
                    circuitoPres.actividades_programadas.push(pAct);
                  }
                  pAct.valor_total_esperado = parseFloat(presupuesto);
                }
                
                // 3. Update Corte (Ejecutado)
                if (id_actividad) {
                  let sAct = corteData.seguimiento_actividades.find(sa => sa.id_actividad === id_actividad);
                  if (!sAct) {
                    sAct = { id_actividad, cantidad_ejecutada: 0, subItems_ejecutados: {} };
                    corteData.seguimiento_actividades.push(sAct);
                  }
                  if (subitem_nombre) {
                    if (!sAct.subItems_ejecutados) sAct.subItems_ejecutados = {};
                    sAct.subItems_ejecutados[subitem_nombre] = parseFloat(ejecutado);
                    sAct.cantidad_ejecutada = Object.values(sAct.subItems_ejecutados).reduce((a, b) => a + b, 0);
                  } else {
                    sAct.cantidad_ejecutada = parseFloat(ejecutado);
                  }
                }
              });
              
              fs.writeFileSync(metasPath, JSON.stringify(metas, null, 2), 'utf-8');
              fs.writeFileSync(presupuestosPath, JSON.stringify(presupuestos, null, 2), 'utf-8');
              fs.writeFileSync(weekPath, JSON.stringify(cortes, null, 2), 'utf-8');
              
              res.statusCode = 200;
              res.setHeader('Content-Type', 'application/json');
              res.end(JSON.stringify({ success: true }));
            } catch (err) {
              console.error(err);
              res.statusCode = 500;
              res.end(JSON.stringify({ success: false, error: err.toString() }));
            }
          });
        } else if (req.url === '/api/deploy' && req.method === 'POST') {
          const dataDir = path.resolve(__dirname, 'src/data');
          exec('git add "src/data/*.json" && git commit -m "Auto-update data" && git push', { cwd: __dirname }, (error, stdout, stderr) => {
            if (error) {
              console.error(error);
              res.statusCode = 500;
              res.end(JSON.stringify({ success: false, error: stderr }));
              return;
            }
            res.statusCode = 200;
            res.setHeader('Content-Type', 'application/json');
            res.end(JSON.stringify({ success: true, stdout }));
          });
        } else {
          next();
        }
      });
    }
  }
}

export default defineConfig({
  plugins: [vue(), apiPlugin()],
  base: './'
})
