import fs from 'fs';
import path from 'path';

const imagesDir = path.join(process.cwd(), 'public', 'images');
const dbPath = path.join(process.cwd(), 'src', 'data', 'db.json');

try {
  if (!fs.existsSync(dbPath)) {
    console.error("No se encontró db.json");
    process.exit(1);
  }
  
  const db = JSON.parse(fs.readFileSync(dbPath, 'utf8'));

  // Función para sanitizar nombres de carpetas en Windows
  const sanitize = (name) => name.replace(/[<>:"/\\|?*]+/g, '-').trim();

  // Diccionario: nombre de circuito -> nombre de subregion sanitizado
  const circuitToSubregion = {};
  
  db.subregiones.forEach(sub => {
    const safeSubName = sanitize(sub.nombre);
    
    // Si la subregion no existe como carpeta, crearla
    const subPath = path.join(imagesDir, safeSubName);
    if (!fs.existsSync(subPath)) {
      fs.mkdirSync(subPath, { recursive: true });
    }

    if (sub.circuitos) {
      sub.circuitos.forEach(c => {
        circuitToSubregion[sanitize(c.corredor_vial)] = safeSubName;
      });
    }
  });

  // Leer carpetas en public/images
  const items = fs.readdirSync(imagesDir);

  items.forEach(item => {
    const itemPath = path.join(imagesDir, item);
    const stat = fs.statSync(itemPath);

    if (stat.isDirectory()) {
      // Verificar si la carpeta (sanitizada) es el nombre de un circuito
      const safeItem = sanitize(item);
      if (circuitToSubregion[safeItem]) {
        const subregion = circuitToSubregion[safeItem];
        const newPath = path.join(imagesDir, subregion, safeItem);
        
        // Mover solo si no está ya dentro de su subregión
        if (safeItem !== subregion) {
          console.log(`Moviendo ${item} -> ${subregion}/${item}`);
          try {
            fs.cpSync(itemPath, newPath, { recursive: true });
            fs.rmSync(itemPath, { recursive: true, force: true });
          } catch(e) {
            console.error(`Error moviendo ${item}:`, e.message);
          }
        }
      }
    }
  });

  console.log("Organización de imágenes finalizada.");

} catch (error) {
  console.error("Error organizando fotos:", error);
}
