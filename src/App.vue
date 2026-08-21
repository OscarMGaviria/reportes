<script setup>
import localforage from 'localforage'
import { ref, computed, watch, onMounted } from 'vue'
import subregionesData from './data/subregiones.json'
import circuitosData from './data/circuitos_maestros.json'
import presupuestosData from './data/presupuestos_y_cronograma_base.json'
import catalogoData from './data/catalogo_actividades.json'
import metasData from './data/metas_fisicas.json'
import VueMultiselect from 'vue-multiselect'
import 'vue-multiselect/dist/vue-multiselect.css'
import { CalendarRange, Filter, TrendingUp, Check } from 'lucide-vue-next'
import ProgressSection from './components/ProgressSection.vue'
import Activities from './components/Activities.vue'
import PhotoGallery from './components/PhotoGallery.vue'
import Observations from './components/Observations.vue'
import GanttDashboard from './components/GanttDashboard.vue'

// Import all weekly reports
const cortesModules = import.meta.glob('./data/cortes_semanales/*.json', { eager: true, import: 'default' })

const showGanttModal = ref(false)
const pendingSyncs = ref([])
const isLocalhost = computed(() => window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1')

const subregiones = computed(() => {
  return subregionesData.map(sub => {
    const circuitos = circuitosData.filter(c => c.id_subregion === sub.id_subregion).map(c => {
      const cortes = cortesModules[`./data/cortes_semanales/cortes_circuito_${c.id_circuito}.json`] || []
      return {
        ...c,
        id: c.id_circuito,
        valor_contrato: c.contrato.valor_total,
        cortes_semanales: cortes
      }
    })
    return { ...sub, circuitos }
  })
})

const subregionActual = ref(subregiones.value.length > 0 ? subregiones.value[0] : null)

const circuitoActual = ref(null)
const corteSeleccionado = ref(null)

watch(subregionActual, (val) => {
  if (val) sessionStorage.setItem('subregion', val.id_subregion);
});
watch(circuitoActual, (val) => {
  if (val) sessionStorage.setItem('circuito', val.id);
});
watch(corteSeleccionado, (val) => {
  if (val) sessionStorage.setItem('semana', val.semana);
});

onMounted(() => {
  localforage.getItem('pending_syncs').then(val => { if(val) pendingSyncs.value = val });
  const savedSub = sessionStorage.getItem('subregion');
  const savedCirc = sessionStorage.getItem('circuito');
  const savedSem = sessionStorage.getItem('semana');
  
  if (savedSub && subregiones.value) {
    const sub = subregiones.value.find(s => s.id_subregion === savedSub);
    if (sub) {
      subregionActual.value = sub;
      if (savedCirc) {
        const circ = sub.circuitos.find(c => c.id.toString() === savedCirc.toString());
        if (circ) {
          circuitoActual.value = circ;
          if (savedSem) {
            const sem = circ.cortes_semanales.find(c => c.semana.toString() === savedSem.toString());
            if (sem) corteSeleccionado.value = sem;
          }
        }
      }
    }
  }
});


watch(circuitoActual, () => {
  corteSeleccionado.value = null
})

watch(subregionActual, (newSubregion) => {
  if (newSubregion && newSubregion.circuitos && newSubregion.circuitos.length > 0) {
    circuitoActual.value = newSubregion.circuitos[0]
  } else {
    circuitoActual.value = null
  }
}, { immediate: true })

const weekLabel = (corte) => `Semana ${corte.semana} (${corte.fecha_corte})`


const showEditModal = ref(false);

const flatIndex = (actIdx, subIdx) => {
  if (!corteActual.value || !corteActual.value.actividades_ejecutadas) return 0;
  let index = 0;
  for (let i = 0; i < actIdx; i++) {
    const a = corteActual.value.actividades_ejecutadas[i];
    index += (a.subItems && a.subItems.length > 0) ? a.subItems.length : 1;
  }
  return index + subIdx;
};


const modalTotalCost = computed(() => {
  if (!corteActual.value || !corteActual.value.actividades_ejecutadas) return 0;
  return corteActual.value.actividades_ejecutadas.reduce((sum, act) => sum + (parseFloat(act.valor_total) || 0), 0);
});

const handlePaste = (event, colIndex, startRowIndex) => {
  const pasteData = event.clipboardData.getData('text');
  if (!pasteData) return;
  
  const rows = pasteData.split(/[\r\n]+/).filter(r => r.trim() !== '');
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


const saveModal = async () => {
  const payload = {
    id_circuito: circuitoActual.value.id_circuito || circuitoActual.value.id,
    semana: corteSeleccionado.value ? corteSeleccionado.value.semana : 1,
    actividades: corteActual.value.actividades_ejecutadas.flatMap(act => {
      if (act.subItems && act.subItems.length > 0) {
        return act.subItems.map(sub => ({
           id_actividad: act.id_actividad,
           nombre_categoria: act.nombre_categoria || act.nombre,
           unidad: sub.unidad,
           total: sub.total,
           ejecutado: sub.completado,
           presupuesto: act.valor_total,
           subitem_nombre: sub.nombre
        }));
      } else {
        return [{
           id_actividad: act.id_actividad,
           nombre_categoria: act.nombre_categoria || act.nombre,
           unidad: act.unidad,
           total: act.total,
           ejecutado: act.completado,
           presupuesto: act.valor_total
        }];
      }
    })
  };
  try {
    const existing = (await localforage.getItem('pending_syncs')) || [];
    const filtered = existing.filter(p => !(p.id_circuito === payload.id_circuito && p.semana === payload.semana));
    filtered.push(payload);
    await localforage.setItem('pending_syncs', filtered);
    pendingSyncs.value = filtered;
    showEditModal.value = false;
    alert('Borrador guardado localmente en el navegador. Recuerda sincronizar.');
  } catch (e) {
    console.error(e);
    alert('Error guardando localmente');
  }
};

const corteActual = computed(() => {

  if (!circuitoActual.value) return null
  
  let corteRaw = corteSeleccionado.value
  
  if (!corteRaw) {
    if (circuitoActual.value.cortes_semanales && circuitoActual.value.cortes_semanales.length > 0) {
      corteRaw = [...circuitoActual.value.cortes_semanales].sort((a, b) => b.semana - a.semana)[0]
    } else {
      corteRaw = {
        semana: 0,
        fecha_corte: 'Línea Base',
        seguimiento_general: {
          financiero: { porcentaje_programado: 0, porcentaje_ejecutado: 0 },
          fisico: { porcentaje_programado: 0, porcentaje_ejecutado: 0 },
          cronograma: { estado: 'Sin iniciar' }
        },
        seguimiento_actividades: [],
        registro_fotografico: [],
        dificultades_y_observaciones: []
      }
    }
  }
  
  // Extraemos las actividades directamente del presupuesto base
  const idCircuito = circuitoActual.value.id;
  const presupuestoBase = presupuestosData.find(p => p.id_circuito === idCircuito);
  const actividadesProgramadas = presupuestoBase ? presupuestoBase.actividades_programadas : [];

  // Calcular "Programado" como la suma del presupuesto base de todas las actividades
  const valorProgramadoTotal = actividadesProgramadas.reduce((sum, ap) => sum + (ap.valor_total_esperado || 0), 0);
  
  // Financial calculations
  const valorAnticipo = 0.15 * valorProgramadoTotal;
  const anticipoPorc = 15.0; // Siempre es 15% del total programado
  
  // Ejecutado: "valor ingresado por acta (ahora miramos como lo agregamos)"
  // Por ahora lo dejamos en 0 para la semana 0, o usamos el porcentaje reportado
  const porcEjecFin = corteRaw.seguimiento_general?.financiero?.porcentaje_ejecutado || 0;
  const valorEjecFin = (porcEjecFin / 100) * valorProgramadoTotal; 
  
  const avanceFinPorc = valorProgramadoTotal > 0 ? (valorEjecFin / valorProgramadoTotal) * 100 : 0;
  
  const corteProcesado = {
    semana: corteRaw.semana,
    fecha_corte: corteRaw.fecha_corte,
    financiero: {
      programado: { porcentaje: "100.0", valor: valorProgramadoTotal },
      ejecutado: { porcentaje: porcEjecFin.toFixed(1), valor: valorEjecFin },
      anticipo: { porcentaje: anticipoPorc.toFixed(1), valor: valorAnticipo },
      avance: { porcentaje: avanceFinPorc.toFixed(1), valor: valorEjecFin }
    },
    fisico: {
      programado: (corteRaw.seguimiento_general?.fisico?.porcentaje_programado || 0).toFixed(1),
      ejecutado: (corteRaw.seguimiento_general?.fisico?.porcentaje_ejecutado || 0).toFixed(1),
      avance: ((corteRaw.seguimiento_general?.fisico?.porcentaje_programado || 0) > 0 
                ? ((corteRaw.seguimiento_general?.fisico?.porcentaje_ejecutado || 0) / (corteRaw.seguimiento_general?.fisico?.porcentaje_programado || 1) * 100) 
                : 0).toFixed(1),
      estado: corteRaw.seguimiento_general?.cronograma?.estado || 'En ejecución'
    },
    actividades_ejecutadas: [],
    imagenes: corteRaw.registro_fotografico || [],
    observaciones_tecnicas: (corteRaw.dificultades_y_observaciones || []).map(obs => obs.descripcion)
  }

  // Base definition
  const categoriasProg = {
    'Topografía': { nombre: 'Topografía', unidad: 'Glb', total: 100, completado: 0, valor_total: 0 },
    'Exploración de campo': { nombre: 'Exploración de campo', unidad: 'Glb', total: 100, completado: 0, valor_total: 0 },
    'CONSTRUCCIÓN DE ALCANTARILLAS': { nombre: 'Construcción de alcantarillas', unidad: 'Glb', total: 100, completado: 0, valor_total: 0 },
    'CONSTRUCCIÓN DE DISIPADORES': { nombre: 'Construcción de disipadores', unidad: 'Glb', total: 100, completado: 0, valor_total: 0 },
    'CONSTRUCCIÓN DE FILTROS PARA CUNETAS': { nombre: 'Construcción de filtros para cunetas', unidad: 'Glb', total: 100, completado: 0, valor_total: 0 },
    'ESTABILIZACION CON MATERIAL GRANULAR': { nombre: 'Estabilización con material granular', unidad: 'Glb', total: 100, completado: 0, valor_total: 0 },
    'CONSTRUCCIÓN DE CUNETAS': { nombre: 'Construcción de cunetas', unidad: 'Glb', total: 100, completado: 0, valor_total: 0 },
    'CONSTRUCCIÓN DE BORDILLOS': { nombre: 'Construcción de bordillos', unidad: 'Glb', total: 100, completado: 0, valor_total: 0 },
    'SEÑALIZACIÓN VIAL': { nombre: 'Señalización vial', unidad: 'Glb', total: 100, completado: 0, valor_total: 0 }
  };
  
  // Custom quantities per circuit
  const metasCircuito = metasData[idCircuito.toString()];
  
  if (metasCircuito) {
    if (metasCircuito['Topografia']) {
      categoriasProg['Topografía'].total = metasCircuito['Topografia'].total;
      categoriasProg['Topografía'].unidad = metasCircuito['Topografia'].unidad;
    }
    if (metasCircuito['Exploracion de campo']) {
      categoriasProg['Exploración de campo'].total = metasCircuito['Exploracion de campo'].total;
      categoriasProg['Exploración de campo'].unidad = metasCircuito['Exploracion de campo'].unidad;
    }
    if (metasCircuito['Construcción de alcantarillas']) {
      categoriasProg['CONSTRUCCIÓN DE ALCANTARILLAS'].total = metasCircuito['Construcción de alcantarillas'].total;
      categoriasProg['CONSTRUCCIÓN DE ALCANTARILLAS'].unidad = metasCircuito['Construcción de alcantarillas'].unidad;
      if (metasCircuito['Construcción de alcantarillas'].subItems) {
        categoriasProg['CONSTRUCCIÓN DE ALCANTARILLAS'].subItems = metasCircuito['Construcción de alcantarillas'].subItems;
      } else {
        // Fallback or explicit subitems as requested by user
        if (idCircuito === 101) {
          categoriasProg['CONSTRUCCIÓN DE ALCANTARILLAS'].subItems = [
            { nombre: 'Limpieza', completado: 0, total: 6 },
            { nombre: 'Remplazar', completado: 0, total: 6 },
            { nombre: 'Nuevas', completado: 0, total: 6 }
          ];
        }
      }
    }
    if (metasCircuito['Construcción de disipadores']) {
      categoriasProg['CONSTRUCCIÓN DE DISIPADORES'].total = metasCircuito['Construcción de disipadores'].total;
      categoriasProg['CONSTRUCCIÓN DE DISIPADORES'].unidad = metasCircuito['Construcción de disipadores'].unidad;
    }
    if (metasCircuito['Construcción de filtro para cunetas']) {
      categoriasProg['CONSTRUCCIÓN DE FILTROS PARA CUNETAS'].total = metasCircuito['Construcción de filtro para cunetas'].total;
      categoriasProg['CONSTRUCCIÓN DE FILTROS PARA CUNETAS'].unidad = metasCircuito['Construcción de filtro para cunetas'].unidad;
    }
    if (metasCircuito['Estabilización con material granular']) {
      categoriasProg['ESTABILIZACION CON MATERIAL GRANULAR'].total = metasCircuito['Estabilización con material granular'].total;
      categoriasProg['ESTABILIZACION CON MATERIAL GRANULAR'].unidad = metasCircuito['Estabilización con material granular'].unidad;
    }
    if (metasCircuito['Construcción de cunetas']) {
      categoriasProg['CONSTRUCCIÓN DE CUNETAS'].total = metasCircuito['Construcción de cunetas'].total;
      categoriasProg['CONSTRUCCIÓN DE CUNETAS'].unidad = metasCircuito['Construcción de cunetas'].unidad;
    }
    if (metasCircuito['Construcción de bordillos']) {
      categoriasProg['CONSTRUCCIÓN DE BORDILLOS'].total = metasCircuito['Construcción de bordillos'].total;
      categoriasProg['CONSTRUCCIÓN DE BORDILLOS'].unidad = metasCircuito['Construcción de bordillos'].unidad;
    }
    if (metasCircuito['Señalización vial']) {
      categoriasProg['SEÑALIZACIÓN VIAL'].total = metasCircuito['Señalización vial'].total;
      categoriasProg['SEÑALIZACIÓN VIAL'].unidad = metasCircuito['Señalización vial'].unidad;
    }
  }

  if (actividadesProgramadas) {
    actividadesProgramadas.forEach(ap => {
      const catObj = catalogoData.find(c => c.id_actividad === ap.id_actividad);
      if (catObj) {
        let catName = catObj.categoria;
        if (catName === 'CONSTRUCCIÓN DE CUNETA') catName = 'CONSTRUCCIÓN DE CUNETAS';
        if (catName === 'CONSTRUCCIÓN DE FILTRO PARA CUNETAS') catName = 'CONSTRUCCIÓN DE FILTROS PARA CUNETAS';
        
        if (categoriasProg[catName]) {
          categoriasProg[catName].valor_total += (ap.valor_total_esperado || 0);
          categoriasProg[catName].id_actividad = ap.id_actividad;
        } else if (ap.id_actividad === 'MACRO-PMA' || ap.id_actividad === 'MACRO-PMT' || ap.id_actividad === 'MACRO-CARAC') {
          const mName = catObj.descripcion;
          categoriasProg[mName] = {
            nombre: mName,
            nombre_categoria: mName,
            id_actividad: ap.id_actividad,
            unidad: 'GLB',
            total: 0,
            completado: 0,
            valor_total: (ap.valor_total_esperado || 0)
          };
        }
      }
    });
  }

  // Ahora procesamos el progreso de la semana actual
  if (corteRaw.seguimiento_actividades && corteRaw.seguimiento_actividades.length > 0) {
    corteRaw.seguimiento_actividades.forEach(sa => {
      const catObj = catalogoData.find(c => c.id_actividad === sa.id_actividad);
      if (catObj) {
        let catName = catObj.categoria;
        if (catName === 'CONSTRUCCIÓN DE CUNETA') catName = 'CONSTRUCCIÓN DE CUNETAS';
        if (catName === 'CONSTRUCCIÓN DE FILTRO PARA CUNETAS') catName = 'CONSTRUCCIÓN DE FILTROS PARA CUNETAS';
        
        if (categoriasProg[catName]) {
          categoriasProg[catName].completado = sa.cantidad_ejecutada || 0;
        categoriasProg[catName].id_actividad = sa.id_actividad;
          
          if (sa.subItems_ejecutados && categoriasProg[catName].subItems) {
            categoriasProg[catName].subItems.forEach(sub => {
              if (sa.subItems_ejecutados[sub.nombre] !== undefined) {
                sub.completado = sa.subItems_ejecutados[sub.nombre];
              }
            });
            // Update total completado for parent based on subitems if parent was 0
            if (!sa.cantidad_ejecutada) {
               categoriasProg[catName].completado = categoriasProg[catName].subItems.reduce((sum, item) => sum + item.completado, 0);
            }
          }
        }
      }
    });
  }
  
  
  // Asignar id_actividad por defecto basado en catalogo_actividades
  Object.keys(categoriasProg).forEach(catName => {

    const normalizeString = (str) => {
      return str.normalize('NFD').replace(/[\u0300-\u036f]/g, '').toUpperCase();
    };
    let searchName = normalizeString(catName);
    if (searchName === 'CONSTRUCCION DE CUNETAS') searchName = 'CONSTRUCCION DE CUNETA';
    if (searchName === 'CONSTRUCCION DE FILTROS PARA CUNETAS') searchName = 'CONSTRUCCION DE FILTRO PARA CUNETAS';
    
    const catObj = catalogoData.find(c => c.categoria && normalizeString(c.categoria) === searchName);

    if (catObj && !categoriasProg[catName].id_actividad) {
      categoriasProg[catName].id_actividad = catObj.id_actividad;
    }
  });

  
  // Sobrescribir con cambios pendientes locales
  const pending = pendingSyncs.value.find(p => p.id_circuito === (circuitoActual.value.id_circuito || circuitoActual.value.id) && p.semana === corteSeleccionado.value.semana);
  if (pending && pending.actividades) {
    pending.actividades.forEach(act => {
       const catName = Object.keys(categoriasProg).find(k => categoriasProg[k].id_actividad === act.id_actividad || categoriasProg[k].nombre === act.nombre_categoria);
       if (catName && categoriasProg[catName]) {
          categoriasProg[catName].total = parseFloat(act.total) || 0;
          categoriasProg[catName].unidad = act.unidad;
          categoriasProg[catName].valor_total = parseFloat(act.presupuesto) || 0;
          if (act.subitem_nombre && categoriasProg[catName].subItems) {
              const sub = categoriasProg[catName].subItems.find(s => s.nombre === act.subitem_nombre);
              if (sub) {
                  sub.completado = parseFloat(act.ejecutado) || 0;
                  sub.total = parseFloat(act.total) || 0;
                  sub.unidad = act.unidad;
              }
              categoriasProg[catName].completado = categoriasProg[catName].subItems.reduce((sum, item) => sum + (item.completado || 0), 0);
          } else {
              categoriasProg[catName].completado = parseFloat(act.ejecutado) || 0;
          }
       }
    });
  }

  corteProcesado.actividades_ejecutadas = Object.values(categoriasProg).filter(act => act.total > 0 || act.valor_total > 0 || act.completado > 0 || act.id_actividad || (act.subItems && act.subItems.length > 0));

  return corteProcesado
})

const formatCurrency = (value) => {
  return new Intl.NumberFormat('es-CO', { style: 'decimal', minimumFractionDigits: 0, maximumFractionDigits: 0 }).format(value)
}
</script>

<template>
  <div class="dashboard-wrapper">
    <!-- APP TOPBAR -->
    <header class="app-topbar bg-dark-green">
      <div class="topbar-logo-area">
        <span class="topbar-title">Contrato de Estabilización Vial</span>
      </div>
      
      <div class="topbar-filters">
        <div class="header-filter-item">
          <VueMultiselect
            v-model="subregionActual"
            :options="subregiones"
            track-by="nombre"
            label="nombre"
            placeholder="Subregión"
            :searchable="true"
            :show-labels="false"
            :close-on-select="true"
            class="header-multiselect"
          />
        </div>
        <div v-if="subregionActual" class="header-filter-item">
          <VueMultiselect
            v-model="circuitoActual"
            :options="subregionActual.circuitos"
            track-by="id"
            label="corredor_vial"
            placeholder="Circuito"
            :searchable="true"
            :show-labels="false"
            :close-on-select="true"
            class="header-multiselect"
          />
        </div>
        <div v-if="circuitoActual" class="header-filter-item">
          <VueMultiselect
            v-model="corteSeleccionado"
            :options="circuitoActual.cortes_semanales"
            :custom-label="weekLabel"
            track-by="semana"
            placeholder="Semana de Corte"
            :searchable="false"
            :show-labels="false"
            :close-on-select="true"
            class="header-multiselect"
          />
        </div>
      </div>

      
      <div class="topbar-actions">
        <button v-if="isLocalhost && pendingSyncs.length > 0" class="topbar-btn sync-btn" @click="syncAllPending" :disabled="isSyncing" title="Sincronizar cambios">
          ☁️ {{ isSyncing ? '...' : pendingSyncs.length }}
        </button>
        <button v-if="isLocalhost" class="topbar-btn publish-btn" @click="deployToGithub" :disabled="isDeploying" title="Publicar en GitHub">
          🚀 {{ isDeploying ? '...' : 'Publicar' }}
        </button>
        <button class="topbar-btn" @click="showGanttModal = true" title="Ver Gantt 18 Meses">

          <CalendarRange :size="20" />
        </button>
      </div>
    </header>

    <!-- MAIN DASHBOARD -->
    <main v-if="corteActual" class="dashboard-container">
      <div class="dashboard-grid">

        <!-- FILA 1 IZQUIERDA: header + contrato + progreso -->
        <div class="grid-cell grid-top-left">
          <!-- HEADER -->
          <header class="main-header">
            <div class="header-titles">
              <h1>INFORME DE AVANCE DE OBRA</h1>
              <h2 class="text-green">Corredor vial {{ circuitoActual.corredor_vial }}</h2>
            </div>
            <div class="header-logo">
              <img src="/Logo-gob-antioquia-ant.png" alt="Logo Gobernación de Antioquia" />
            </div>
          </header>

          <!-- VALOR DEL CONTRATO -->
          <div class="contract-value bg-dark-green">
            <h2>Valor del contrato: $ {{ formatCurrency(circuitoActual.valor_contrato) }}</h2>
          </div>

          <!-- RIBBON ACTIVIDADES -->
          <div class="ribbon-row">
            <div class="section-ribbon">
              <span class="ribbon-icon">📈</span> Avance de actividades ejecutadas <span v-if="isLocalhost" @click="showEditModal = true" style="cursor: pointer; padding: 2px 5px; background: #fff; color: #4caf50; border-radius: 4px; font-size: 0.8em; margin-left: 10px; font-weight: bold;">✏️</span>
            </div>
            <div class="ribbon-line"></div>
          </div>

          <!-- ACTIVIDADES -->
          <Activities :actividades="corteActual.actividades_ejecutadas" />
        </div>

        <!-- FILA 2 IZQUIERDA: ribbon progreso -->
        <div class="section-ribbon grid-cell grid-ribbon-left">
          <span class="ribbon-icon">↗</span> Avance financiero y físico
        </div>

        <!-- FILA 3 IZQUIERDA: progreso -->
        <div class="grid-cell grid-bottom-left">
          <ProgressSection :corte="corteActual" />
        </div>

        <!-- FILA 1 DERECHA: fotos -->
        <div class="grid-cell grid-top-right">
          <div class="top-right-decoration"></div>
          <PhotoGallery :imagenes="corteActual.imagenes" />
        </div>

        <!-- FILA 2 DERECHA: ribbon observaciones -->
        <div class="section-ribbon grid-cell grid-ribbon-right">
          <span class="ribbon-icon"><Check :size="14" /></span> Dificultades y observaciones técnicas
        </div>

        <!-- FILA 3 DERECHA: observaciones -->
        <div class="grid-cell grid-bottom-right">
          <Observations :observaciones="corteActual.observaciones_tecnicas" :tipoEstructura="corteActual.tipo_estructura || []" />
        </div>

      </div>
    </main>

    <!-- GANTT MODAL -->
    <GanttDashboard 
      v-if="showGanttModal && circuitoActual" 
      :circuitoNombre="circuitoActual.corredor_vial"
      @close="showGanttModal = false" 
    />

    <!-- EDIT MODAL -->
    <div v-if="showEditModal" class="modal-overlay">
      <div class="modal-content">
        <div class="modal-header">
          <h2>Editar Actividades - {{ selectedCircuito?.label }}</h2>
          <button @click="showEditModal = false" class="close-btn">✕</button>
        </div>
        <div class="modal-body" style="max-height: 70vh; overflow-y: auto;">
          <table class="excel-table">
            <thead>
              <tr >
                <th >Actividad</th>
                <th >Unidad</th>
                <th >Ejecutado</th>
                <th >Total Programado</th>
                <th >Costo Base ($)</th>
              </tr>
            </thead>
            <tbody>
              <template v-for="(act, idx) in corteActual.actividades_ejecutadas" :key="idx">
                <template v-if="act.subItems && act.subItems.length > 0">
                  <tr v-for="(sub, sidx) in act.subItems" :key="'s'+idx+'-'+sidx">
                    <td >{{ act.nombre_categoria || act.nombre }} - {{ sub.nombre }}</td>
                    <td ><input type="text" v-model="sub.unidad"  /></td>
                    <td ><input type="number" v-model="sub.completado"  /></td>
                    <td ><input type="number" v-model="sub.total"  /></td>
                    <td ><input type="number" v-model="act.valor_total"  v-if="sidx === 0" /></td>
                  </tr>
                </template>
                <template v-else>
                  <tr>
                    <td >{{ act.nombre_categoria || act.nombre }}</td>
                    <td ><input type="text" v-model="act.unidad"  /></td>
                    <td ><input type="number" v-model="act.completado"  /></td>
                    <td ><input type="number" v-model="act.total"  /></td>
                    <td ><input type="number" v-model="act.valor_total"  /></td>
                  </tr>
                </template>
              </template>
            
            </tbody>
            <tfoot>
              <tr style="background-color: #e5f1eb; font-weight: bold; border-top: 2px solid #217346;">
                <td colspan="4" style="text-align: right; padding: 8px;">TOTAL COSTO DEL TRAMO:</td>
                <td style="text-align: right; padding: 8px; font-size: 14px;">$ {{ formatCurrency(modalTotalCost) }}</td>
              </tr>
            </tfoot>
          </table>

        </div>
        <div class="modal-footer" style="padding: 15px; text-align: right; border-top: 1px solid #ddd; margin-top: 15px;">
          <button @click="saveModal()" style="background: #4caf50; color: white; padding: 10px 20px; border: none; border-radius: 4px; cursor: pointer; font-weight: bold;">Guardar Cambios</button>
        </div>
      </div>
    </div>
  </div>
</template>




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

.dashboard-wrapper {
  height: 100vh;
  min-width: 1200px;
  min-height: 700px;
  overflow: auto;
  display: flex;
  flex-direction: column;
  background-color: white;
}



.dashboard-container {
  flex: 1;
  padding: 1.5vh 2vw;
  border-radius: 4px;
  margin: 1vh 1vw;
  overflow: hidden;
  position: relative;
}

.top-right-decoration {
  position: absolute;
  top: -1.5vh;
  right: 2vw;
  width: 4vw;
  height: 3vh;
  background-color: var(--color-primary-dark);
  clip-path: polygon(20% 0%, 80% 0%, 100% 100%, 0% 100%);
}

/* Grid de 2 columnas x 3 filas compartidas: las filas de "ribbon" y de
   contenido inferior quedan alineadas entre columna izquierda y derecha
   porque ambas usan las mismas pistas de fila (grid-row), no un cálculo
   de flex independiente por columna. */
.dashboard-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  grid-template-rows: auto auto minmax(0, 1fr);
  column-gap: 2vw;
  row-gap: 1vh;
  height: 100%;
}

.grid-top-left { grid-column: 1; grid-row: 1; }
.grid-ribbon-left { grid-column: 1; grid-row: 2; }
.grid-bottom-left { grid-column: 1; grid-row: 3; }

.grid-top-right { grid-column: 2; grid-row: 1; }
.grid-ribbon-right { grid-column: 2; grid-row: 2; }
.grid-bottom-right { grid-column: 2; grid-row: 3; }

.grid-bottom-left {
  overflow: visible; /* Allow overlapping badges */
}

.grid-cell {
  min-height: 0;
  min-width: 0;
  overflow: hidden;
}

.grid-bottom-left, .grid-bottom-right {
  padding-top: 2vh;
}

.grid-top-left, .grid-top-right, .grid-bottom-left, .grid-bottom-right {
  display: flex;
  flex-direction: column;
}

.grid-top-right {
  position: relative;
}

.grid-ribbon-left, .grid-ribbon-right {
  margin: 0;
}

.ribbon-row {
  display: flex;
  align-items: center;
  margin-top: 1vh;
}

.main-header {
  flex: 0 0 auto;
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 2vw;
}

.header-titles {
  flex: 1;
}

/* ===== APP TOPBAR ===== */
.app-topbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.8vh 2vw; /* Altura reducida */
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
  color: white;
  z-index: 10;
}

.topbar-logo-area {
  display: flex;
  align-items: center;
  gap: 1vw;
  flex: 0 0 auto;
}

.topbar-filters {
  display: flex;
  gap: 1vw;
  flex: 1;
  justify-content: flex-end;
  margin-right: 2vw;
}

.header-filter-item {
  width: 18vw;
  min-width: 180px;
}

/* Custom styling to make VueMultiselect fit in the dark green header */
.header-multiselect :deep(.multiselect__tags) {
  min-height: 4vh;
  padding: 0.6vh 2.5vw 0 1.2vw;
  border-radius: 50px;
  background: white;
  border: 1px solid #e2e8f0;
  color: #1e293b;
  transition: all 0.2s ease;
  cursor: pointer;
  box-shadow: 0 1px 3px rgba(0,0,0,0.1);
}
.header-multiselect:hover :deep(.multiselect__tags) {
  border-color: #cbd5e1;
  box-shadow: 0 2px 5px rgba(0,0,0,0.15);
}
.header-multiselect :deep(.multiselect__select) {
  height: 4vh;
  padding: 0;
}
.header-multiselect :deep(.multiselect__select::before) {
  border-color: #64748b transparent transparent;
}
.header-multiselect :deep(.multiselect__placeholder) {
  margin-bottom: 0;
  padding-top: 0.2vh;
  font-size: 1.4vh;
  color: #64748b;
  font-weight: 500;
}
.header-multiselect :deep(.multiselect__single),
.header-multiselect :deep(.multiselect__input) {
  margin-bottom: 0;
  padding-top: 0.2vh;
  font-size: 1.4vh;
  color: #1e293b;
  font-weight: 600;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  display: block;
  background: transparent;
}

.header-logo {
  flex: 0 0 auto;
  display: flex;
  align-items: center;
  gap: 1.5vw;
}

.header-logo img {
  max-height: 8vh;
  object-fit: contain;
}

.topbar-title {
  font-weight: bold;
  font-size: 1.8vh;
  letter-spacing: 0.5px;
}

.topbar-actions {
  display: flex;
  gap: 1vw;
}

.topbar-btn {
  background: rgba(255, 255, 255, 0.15);
  color: white;
  border: 1px solid rgba(255, 255, 255, 0.2);
  padding: 0.8vh;
  border-radius: 6px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s;
}

.topbar-btn:hover {
  background: rgba(255, 255, 255, 0.25);
  transform: translateY(-1px);
}

.main-header h1 {
  font-size: 4.2vh;
  color: #0b1f3a; 
  margin-bottom: 0.2vh;
}

.main-header h2 {
  font-size: 2.6vh;
  margin-bottom: 0.5vh;
}

.main-header .subtitle {
  font-style: italic;
  font-size: 1.6vh;
  color: var(--color-text-muted);
}

.week-badge {
  display: inline-block;
  margin-top: 0.5vh;
  padding: 0.3vh 1vw;
  background-color: var(--color-bg-light);
  color: var(--color-primary-dark);
  border-radius: 4px;
  font-size: 1.4vh;
  font-weight: bold;
  border: 1px solid var(--color-border);
}

.contract-value {
  flex: 0 0 auto;
  display: flex;
  align-items: center;
  padding: 1.5vh 2vw;
  border-radius: 8px;
  gap: 1vw;
  margin-top: 1vh;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
}

.contract-value .icon {
  font-size: 3.5vh;
}

.contract-value h2 {
  color: white;
  margin: 0;
  font-size: 3.2vh;
}

.ribbon-line {
  flex: 1;
  height: 2px;
  background-color: var(--color-border);
  margin-left: -1vw;
  margin-bottom: 2vh;
}


</style>
