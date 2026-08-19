import json
import os

DATA_DIR = os.path.join('src', 'data')

def load_json(name):
    path = os.path.join(DATA_DIR, name)
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_json(name, data):
    path = os.path.join(DATA_DIR, name)
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

# 1. Update metas_fisicas.json targets
metas = load_json('metas_fisicas.json')
if "105" in metas:
    metas["105"]["Topografia"] = {"total": 35.0, "unidad": "Km"}
    metas["105"]["Exploracion de campo"] = {"total": 140.0, "unidad": "und"}
    
    # Alcantarillas subitems targets
    metas["105"]["Construcción de alcantarillas"]["subItems"] = [
      { "nombre": "Limpieza", "completado": 0, "total": 319.0 },
      { "nombre": "Remplazar", "completado": 0, "total": 0.0 },
      { "nombre": "Nuevas", "completado": 0, "total": 11.0 }
    ]

save_json('metas_fisicas.json', metas)

# 2. Create cortes_circuito_105.json
corte_105 = [
  {
    "semana": 1,
    "fecha_corte": "2024-05-15",
    "seguimiento_general": {
      "cronograma": {
        "estado": "En ejecución"
      },
      "financiero": {
        "porcentaje_programado": 100.0,
        "porcentaje_ejecutado": 0.0
      },
      "fisico": {
        "porcentaje_programado": 100.0,
        "porcentaje_ejecutado": 0.0
      }
    },
    "seguimiento_actividades": [
      {
        "id_actividad": "MACRO-CARAC-TOPO",
        "cantidad_ejecutada": 7.0
      },
      {
        "id_actividad": "MACRO-CARAC-EXPL",
        "cantidad_ejecutada": 40.0
      },
      {
        "id_actividad": "4.1.1", 
        "cantidad_ejecutada": 35.19
      },
      {
        "id_actividad": "2.8",
        "cantidad_ejecutada": 0,
        "subItems_ejecutados": {
            "Limpieza": 319,
            "Remplazar": 0,
            "Nuevas": 9
        }
      },
      {
        "id_actividad": "8.13.1",
        "cantidad_ejecutada": 1500.0 
      }
    ],
    "registro_fotografico": [],
    "dificultades_y_observaciones": []
  }
]

cortes_path = os.path.join(DATA_DIR, 'cortes_semanales', 'cortes_circuito_105.json')
with open(cortes_path, 'w', encoding='utf-8') as f:
    json.dump(corte_105, f, indent=2, ensure_ascii=False)

print("Updated 105 successfully.")
