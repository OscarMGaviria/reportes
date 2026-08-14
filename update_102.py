import json
import os

DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'src', 'data')

def load_json(name):
    path = os.path.join(DATA_DIR, name)
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_json(name, data):
    path = os.path.join(DATA_DIR, name)
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

presupuestos = load_json('presupuestos_y_cronograma_base.json')

circuit_102_acts = [
    {"id_actividad": "4.1.1", "cantidad_total": 25000, "valor_total_esperado": 18141304676}, # Estabilización
    {"id_actividad": "2.8", "cantidad_total": 102, "valor_total_esperado": 3567628925}, # Alcantarillas
    {"id_actividad": "8.13.1", "cantidad_total": 25000, "valor_total_esperado": 5624939000}, # Filtro para cunetas
    {"id_actividad": "6.2.50", "cantidad_total": 25000, "valor_total_esperado": 4163474519}, # Cunetas
    {"id_actividad": "4.1.9", "cantidad_total": 77, "valor_total_esperado": 524283533}, # Disipadores
    {"id_actividad": "4.1.2", "cantidad_total": 5000, "valor_total_esperado": 607318000}, # Bordillos
    {"id_actividad": "12.1", "cantidad_total": 25000, "valor_total_esperado": 367105625}, # Señalización vial
    {"id_actividad": "MACRO-PMA", "cantidad_total": 1, "valor_total_esperado": 232478312},
    {"id_actividad": "MACRO-PMT", "cantidad_total": 1, "valor_total_esperado": 236983041},
    {"id_actividad": "MACRO-CARAC", "cantidad_total": 1, "valor_total_esperado": 26399025}
]

for p in presupuestos:
    if p['id_circuito'] == 102:
        p['actividades_programadas'] = circuit_102_acts

save_json('presupuestos_y_cronograma_base.json', presupuestos)
print("Updated circuit 102 successfully.")
