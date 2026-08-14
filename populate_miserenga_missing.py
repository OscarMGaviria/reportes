import json
import os

DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'src', 'data')

def load_json(name):
    path = os.path.join(DATA_DIR, name)
    if not os.path.exists(path):
        return []
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_json(name, data):
    path = os.path.join(DATA_DIR, name)
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

presupuestos = load_json('presupuestos_y_cronograma_base.json')
catalogo = load_json('catalogo_actividades.json')

# Missing from Miserenga-Ebejico (page 1)
missing_acts = [
    # ALCANTARILLAS (Items 8 to 11)
    {"id": "8.1", "und": "m", "cant": 48.0, "vu": 140150.0, "vt": 6727200.0, "cat": "CONSTRUCCIÓN DE ALCANTARILLAS"},
    {"id": "8.27", "und": "m", "cant": 36.0, "vu": 2306859.0, "vt": 83046924.0, "cat": "CONSTRUCCIÓN DE ALCANTARILLAS"},
    {"id": "10.1", "und": "kg", "cant": 2904.0, "vu": 9487.0, "vt": 27550248.0, "cat": "CONSTRUCCIÓN DE ALCANTARILLAS"},
    {"id": "13.1", "und": "m3-Km", "cant": 1296.0, "vu": 2033.0, "vt": 2634768.0, "cat": "CONSTRUCCIÓN DE ALCANTARILLAS"},
    
    # CUNETA (Items 12 to 16)
    {"id": "4.1.8_C", "real_id": "4.1.8", "und": "m3", "cant": 174.0, "vu": 54161.0, "vt": 9424014.0, "cat": "CONSTRUCCIÓN DE CUNETA"},
    {"id": "5.1.7_C", "real_id": "5.1.7", "und": "m3", "cant": 80.0, "vu": 108602.0, "vt": 8688160.0, "cat": "CONSTRUCCIÓN DE CUNETA"},
    {"id": "6.2.50_C", "real_id": "6.2.50", "und": "m3", "cant": 100.0, "vu": 1038976.0, "vt": 103897600.0, "cat": "CONSTRUCCIÓN DE CUNETA"},
    {"id": "10.1_C", "real_id": "10.1", "und": "kg", "cant": 2802.0, "vu": 9487.0, "vt": 26582574.0, "cat": "CONSTRUCCIÓN DE CUNETA"},
    {"id": "13.1_C", "real_id": "13.1", "und": "m3-Km", "cant": 4320.0, "vu": 2033.0, "vt": 8782560.0, "cat": "CONSTRUCCIÓN DE CUNETA"},
    
    # FILTRO PARA CUNETAS (Items 17 to 18)
    {"id": "8.13.1_F", "real_id": "8.13.1", "und": "m", "cant": 1000.0, "vu": 143027.0, "vt": 143027000.0, "cat": "CONSTRUCCIÓN DE FILTRO PARA CUNETAS"},
    {"id": "13.1_F", "real_id": "13.1", "und": "m3-Km", "cant": 19440.0, "vu": 2033.0, "vt": 39521520.0, "cat": "CONSTRUCCIÓN DE FILTRO PARA CUNETAS"}
]

for a in missing_acts:
    real_id = a.get('real_id', a['id'])
    
    # find desc
    desc = "VERIFICAR_DESCRIPCION"
    cat_item = next((c for c in catalogo if c['id_actividad'] == real_id), None)
    if cat_item:
        desc = cat_item['descripcion']
    
    unique_id = f"{real_id}_{a['cat'].replace(' ', '_')}" if a.get('real_id') else real_id
    
    if not any(c['id_actividad'] == unique_id for c in catalogo):
        catalogo.append({
            "id_actividad": unique_id,
            "categoria": a['cat'],
            "descripcion": desc,
            "unidad": a['und'],
            "valor_unitario": a['vu']
        })

for p in presupuestos:
    if p['id_circuito'] == 101: # Miserenga - Ebejico
        for a in missing_acts:
            real_id = a.get('real_id', a['id'])
            unique_id = f"{real_id}_{a['cat'].replace(' ', '_')}" if a.get('real_id') else real_id
            
            if not any(act['id_actividad'] == unique_id for act in p['actividades_programadas']):
                p['actividades_programadas'].append({
                    "id_actividad": unique_id,
                    "cantidad_total": a['cant'],
                    "valor_total_esperado": a['vt']
                })
        
        p['meta_financiera_total'] = sum(a['valor_total_esperado'] for a in p['actividades_programadas'])

save_json('presupuestos_y_cronograma_base.json', presupuestos)
save_json('catalogo_actividades.json', catalogo)

print("Items faltantes de Miserenga-Ebejico inyectados con éxito.")
