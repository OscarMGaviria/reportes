import json

corte_101 = [
  {
    "semana": 1,
    "fecha_corte": "2024-05-15",
    "seguimiento_general": {
      "cronograma": { "estado": "En ejecución" },
      "financiero": { "porcentaje_programado": 100.0, "porcentaje_ejecutado": 0.0 },
      "fisico": { "porcentaje_programado": 100.0, "porcentaje_ejecutado": 0.0 }
    },
    "seguimiento_actividades": [
      { "id_actividad": "MACRO-CARAC-TOPO", "cantidad_ejecutada": 0.0 },
      { "id_actividad": "MACRO-CARAC-EXPL", "cantidad_ejecutada": 4.0 },
      { "id_actividad": "4.1.1", "cantidad_ejecutada": 0.0 },
      { "id_actividad": "2.8", "cantidad_ejecutada": 0, "subItems_ejecutados": { "Limpieza": 0, "Remplazar": 0, "Nuevas": 0 } },
      { "id_actividad": "8.13.1", "cantidad_ejecutada": 0.0 },
      { "id_actividad": "6.2.50", "cantidad_ejecutada": 0.0 },
      { "id_actividad": "4.1.9", "cantidad_ejecutada": 0.0 },
      { "id_actividad": "4.1.2", "cantidad_ejecutada": 0.0 },
      { "id_actividad": "12.1", "cantidad_ejecutada": 0.0 }
    ],
    "registro_fotografico": [],
    "dificultades_y_observaciones": []
  }
]

with open('src/data/cortes_semanales/cortes_circuito_101.json', 'w', encoding='utf-8') as f:
    json.dump(corte_101, f, indent=2, ensure_ascii=False)

print('Updated cortes')
