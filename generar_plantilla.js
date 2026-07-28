import fs from 'fs';
import path from 'path';
import * as xlsx from 'xlsx';

const dbPath = path.join(process.cwd(), 'src', 'data', 'db.json');
let db = { subregiones: [] };
if (fs.existsSync(dbPath)) {
  db = JSON.parse(fs.readFileSync(dbPath, 'utf8'));
}

const workbook = xlsx.utils.book_new();

// ==========================================
// 1. Hoja "Avance_General"
// ==========================================
const headersAvance = [
  "Lote_Subregion",
  "ID_Circuito",
  "Corredor",
  "Semana",
  "Fecha_Corte",
  "Porcentaje_Fisico_Programado",
  "Porcentaje_Fisico_Ejecutado",
  "Porcentaje_Financiero_Programado",
  "Porcentaje_Financiero_Ejecutado",
  "Observacion_Semanal"
];

const dataAvance = [];
const sheetsData = [];

db.subregiones.forEach(sub => {
  if (sub.circuitos) {
    sub.circuitos.forEach(c => {
      // Add to Avance General
      dataAvance.push([
        sub.nombre,
        c.id, // Using the actual ID from DB
        c.corredor_vial,
        1, // Semana por defecto
        "2026-07-24", // Fecha por defecto
        0, 0, 0, 0, ""
      ]);

      // Prepare data for individual sheets
      sheetsData.push({
        id: c.id,
        corredor: c.corredor_vial
      });
    });
  }
});

const wsAvance = xlsx.utils.aoa_to_sheet([headersAvance, ...dataAvance]);
wsAvance['!cols'] = [
  {wch: 18}, {wch: 15}, {wch: 40}, {wch: 10}, {wch: 15},
  {wch: 25}, {wch: 25}, {wch: 30}, {wch: 30}, {wch: 60}
];
xlsx.utils.book_append_sheet(workbook, wsAvance, "Avance_General");


// ==========================================
// Función para crear Hojas de Circuito
// ==========================================
const headersDetalle = [
  "Corredor",
  "Nombre_Actividad",
  "Tipo",
  "Responsable",
  "Unidad",
  "Total_Programado",
  "Completado",
  "Fecha_Entregable"
];

const crearHojaDetalle = (corredor, actividadesData) => {
  const dataConCorredor = actividadesData.map(row => [corredor, ...row]);
  
  const ws = xlsx.utils.aoa_to_sheet([headersDetalle, ...dataConCorredor]);
  ws['!cols'] = [
    {wch: 40}, {wch: 40}, {wch: 15}, {wch: 15}, {wch: 10}, 
    {wch: 20}, {wch: 15}, {wch: 20}
  ];
  return ws;
};

// Datos base por defecto para rellenar (pueden ser editados por el usuario)
const actividadesBase = [
  ["Topografía", "Actividad", "CONTRATISTA", "km", 0, 0, ""],
  ["Exploración Geotécnica", "Actividad", "CONTRATISTA", "km", 0, 0, ""],
  ["Limpieza de Obras Transversales", "Actividad", "CONTRATISTA", "und", 0, 0, ""],
  ["Construcción de filtros", "Actividad", "CONTRATISTA", "km", 0, 0, ""],
  ["Construcción de Cuneta", "Actividad", "CONTRATISTA", "km", 0, 0, ""],
  ["Conformación y adecuación", "Actividad", "CONTRATISTA", "km", 0, 0, ""],
  ["Perfil Topográfico", "Insumo", "CONTRATISTA", "Entregable", 1, 0, ""],
  ["Estudios de tránsito", "Insumo", "CONTRATISTA", "Entregable", 1, 0, ""],
  ["Presentación diseño estructura", "Insumo", "CONTRATISTA", "Entregable", 1, 0, ""]
];

// Generar una hoja por cada circuito
sheetsData.forEach(c => {
  let sheetName = `C-${c.id}`; 
  // Opcional: Para evitar nombres muy largos, usamos C-ID o un nombre corto.
  // Excel no permite nombres de >31 caracteres ni caracteres especiales.
  const ws = crearHojaDetalle(c.corredor, actividadesBase);
  xlsx.utils.book_append_sheet(workbook, ws, sheetName);
});

// Guardar archivo
const outputPath = path.join(process.cwd(), 'Plantilla_Reportes_Circuitos_v10.xlsx');
xlsx.writeFile(workbook, outputPath);

console.log(`Plantilla Híbrida V10 creada exitosamente en: ${outputPath}`);
