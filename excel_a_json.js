import fs from 'fs';
import path from 'path';
import * as xlsx from 'xlsx';

const excelPath = path.join(process.cwd(), 'Plantilla_Reportes_Circuitos_v10_Diligenciada.xlsx');
const dbPath = path.join(process.cwd(), 'src', 'data', 'db.json');

try {
  if (!fs.existsSync(excelPath)) {
    console.error("No se encontró el archivo Excel en la ruta especificada.");
    process.exit(1);
  }
  const fileData = fs.readFileSync(excelPath);
  const workbook = xlsx.read(fileData, { type: 'buffer' });

  let db = { subregiones: [] };
  if (fs.existsSync(dbPath)) {
    db = JSON.parse(fs.readFileSync(dbPath, 'utf8'));
  }

  // 1. Procesar "Avance_General"
  const generalSheet = workbook.Sheets["Avance_General"];
  if (!generalSheet) throw new Error("No se encontró la hoja Avance_General");
  const avanceData = xlsx.utils.sheet_to_json(generalSheet);

  avanceData.forEach(row => {
    const idCircuito = row.ID_Circuito; // Volvemos a ID_Circuito
    const semana = row.Semana;
    const lote = row.Lote_Subregion || "GENERAL";
    
    // Buscar o crear subregión
    let subregion = db.subregiones.find(s => s.nombre === lote);
    if (!subregion) {
      subregion = { nombre: lote, circuitos: [] };
      db.subregiones.push(subregion);
    }

    // Buscar o crear circuito
    let circuito = subregion.circuitos.find(c => c.id_circuito === idCircuito || c.id === idCircuito);
    if (!circuito) {
      circuito = {
        id: idCircuito, 
        id_circuito: idCircuito,
        corredor_vial: row.Corredor || "Nuevo Circuito",
        cortes_semanales: []
      };
      subregion.circuitos.push(circuito);
    }

    // Buscar o crear corte semanal
    let corte = circuito.cortes_semanales.find(c => c.semana === semana);
    if (!corte) {
      corte = {
        semana: semana,
        fecha_corte: row.Fecha_Corte,
        financiero: {
          anticipo: { valor: 0, porcentaje: 0 },
          programado: { valor: 0, porcentaje: row.Porcentaje_Financiero_Programado || 0 },
          ejecutado: { valor: 0, porcentaje: row.Porcentaje_Financiero_Ejecutado || 0 },
          avance: { valor: 0, porcentaje: 0 },
          estado: "En ejecución"
        },
        fisico: {
          programado: row.Porcentaje_Fisico_Programado || 0,
          ejecutado: row.Porcentaje_Fisico_Ejecutado || 0,
          avance: 0,
          estado: "En ejecución"
        },
        actividades_ejecutadas: [],
        insumos: [],
        imagenes: [],
        observaciones_tecnicas: []
      };
      circuito.cortes_semanales.push(corte);
    } else {
      corte.fecha_corte = row.Fecha_Corte || corte.fecha_corte;
      corte.financiero.programado.porcentaje = row.Porcentaje_Financiero_Programado ?? corte.financiero.programado.porcentaje;
      corte.financiero.ejecutado.porcentaje = row.Porcentaje_Financiero_Ejecutado ?? corte.financiero.ejecutado.porcentaje;
      corte.fisico.programado = row.Porcentaje_Fisico_Programado ?? corte.fisico.programado;
      corte.fisico.ejecutado = row.Porcentaje_Fisico_Ejecutado ?? corte.fisico.ejecutado;
    }
    
    // Escanear carpeta de imágenes de este circuito
    corte.imagenes = [];
    try {
      const sanitize = (name) => name.replace(/[<>:"/\\|?*]+/g, '-').trim();
      
      // Buscar la subregión a la que pertenece este circuito
      let subregionName = lote; // por defecto el lote
      const subObj = db.subregiones.find(s => s.circuitos.some(c => c.corredor_vial === circuito.corredor_vial));
      if (subObj) {
        subregionName = subObj.nombre;
      }
      
      const imgsPath = path.join(process.cwd(), 'public', 'images', sanitize(subregionName), sanitize(circuito.corredor_vial));
      
      if (fs.existsSync(imgsPath)) {
        // Función recursiva para buscar imágenes
        const getImages = (dir) => {
          let results = [];
          const list = fs.readdirSync(dir);
          list.forEach(file => {
            const filePath = path.join(dir, file);
            const stat = fs.statSync(filePath);
            if (stat && stat.isDirectory()) {
              results = results.concat(getImages(filePath));
            } else if (file.match(/\.(jpg|jpeg|png|gif|webp)$/i)) {
              results.push(filePath);
            }
          });
          return results;
        };

        const imageFiles = getImages(imgsPath);
        
        imageFiles.forEach((filePath, index) => {
          const relativePath = path.relative(path.join(process.cwd(), 'public'), filePath).replace(/\\/g, '/');
          const fileName = path.basename(filePath);
          corte.imagenes.push({
            id: index + 1,
            url: `/${relativePath}`,
            descripcion: fileName.split('.')[0].replace(/_/g, ' ')
          });
        });
      }
    } catch(err) {
      console.warn("Error leyendo imágenes del circuito:", circuito.corredor_vial, err.message);
    }
    
    // Asignar observación si existe
    if (row.Observacion_Semanal) {
      if (!corte.observaciones_tecnicas.includes(row.Observacion_Semanal)) {
        corte.observaciones_tecnicas.push(row.Observacion_Semanal);
      }
    }
  });

  // 2. Procesar Hojas de Detalle por Circuito
  const findCorteGlobal = (idCircuito) => {
    for (let sub of db.subregiones) {
      if (sub.circuitos) {
        let c = sub.circuitos.find(c => String(c.id_circuito) === String(idCircuito) || String(c.id) === String(idCircuito));
        if (c && c.cortes_semanales.length > 0) {
          // Obtener el corte más reciente
          return c.cortes_semanales.sort((a,b) => b.semana - a.semana)[0];
        }
      }
    }
    return null;
  };

  workbook.SheetNames.forEach(sheetName => {
    if (sheetName === "Avance_General") return; // Saltar la hoja maestra
    
    // Sheet name is "C-ID", we need to extract ID
    let circuitoId = sheetName;
    if (sheetName.startsWith("C-")) {
      circuitoId = sheetName.substring(2);
    }
    
    const corte = findCorteGlobal(circuitoId);
    if (!corte) {
      console.warn(`No se encontró corte semanal para el circuito ID ${circuitoId} reportado en la hoja de detalle.`);
      return;
    }

    const detailData = xlsx.utils.sheet_to_json(workbook.Sheets[sheetName]);
    
    // Limpiamos listas para reemplazarlas
    corte.actividades_ejecutadas = [];
    corte.insumos = [];

    detailData.forEach(row => {
      const tipo = row.Tipo || "Actividad";
      
      if (tipo === "Actividad") {
        corte.actividades_ejecutadas.push({
          nombre: row.Nombre_Actividad,
          unidad: row.Unidad,
          total: parseFloat(row.Total_Programado) || 0,
          completado: parseFloat(row.Completado) || 0
        });
      } else if (tipo === "Insumo") {
        corte.insumos.push({
          nombre: row.Nombre_Actividad,
          responsable: row.Responsable,
          fecha_presentacion: row.Fecha_Entregable,
          estado_observacion: ""
        });
      }
    });
  });

  // Guardar db.json actualizado
  fs.writeFileSync(dbPath, JSON.stringify(db, null, 2));
  console.log("Base de datos db.json actualizada exitosamente con el formato Híbrido V10.");

} catch (error) {
  console.error("Error procesando el archivo de Excel V6:", error);
}
