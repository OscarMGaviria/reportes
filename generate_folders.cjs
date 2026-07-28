const fs = require('fs');
const path = require('path');

const geojsonPath = path.join(__dirname, 'src', 'data', 'Circuitos.geojson');
const imagesBaseDir = path.join(__dirname, 'public', 'images');

try {
  const data = JSON.parse(fs.readFileSync(geojsonPath, 'utf8'));
  const features = data.features;
  
  let createdCount = 0;
  
  features.forEach(feature => {
    if (feature.properties && feature.properties.SUBREGION && feature.properties.CIRCUITO) {
      // Clean up names to be folder friendly (remove special chars if needed, though they seem fine, maybe trim)
      const subregion = feature.properties.SUBREGION.trim();
      const circuito = feature.properties.CIRCUITO.trim().replace(/[\\/:\*\?"<>\|]/g, '');
      
      const targetDir = path.join(imagesBaseDir, subregion, circuito);
      
      if (!fs.existsSync(targetDir)) {
        fs.mkdirSync(targetDir, { recursive: true });
        createdCount++;
      }
    }
  });
  
  console.log(`Successfully created ${createdCount} new directories.`);
} catch (error) {
  console.error("Error creating directories:", error);
}
