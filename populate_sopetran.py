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

# Sopetran-Belmira-Horizontes acts (Circuit 105)
sopetran_acts = [
    # ALCANTARILLAS
    {"id": "2.8", "und": "m3", "cant": 34.0, "vu": 230711.0, "vt": 7844174.0, "cat": "CONSTRUCCIÓN DE ALCANTARILLAS"},
    {"id": "2.14.1", "und": "m", "cant": 210.0, "vu": 60377.0, "vt": 12679170.0, "cat": "CONSTRUCCIÓN DE ALCANTARILLAS"},
    {"id": "4.1.8", "und": "m3", "cant": 5984.0, "vu": 54161.0, "vt": 324099424.0, "cat": "CONSTRUCCIÓN DE ALCANTARILLAS"},
    {"id": "4.2.2", "und": "m3", "cant": 1936.0, "vu": 32553.0, "vt": 63022608.0, "cat": "CONSTRUCCIÓN DE ALCANTARILLAS"},
    {"id": "5.1.7", "und": "m3", "cant": 704.0, "vu": 108602.0, "vt": 76455808.0, "cat": "CONSTRUCCIÓN DE ALCANTARILLAS"},
    {"id": "6.2.4", "und": "m3", "cant": 176.0, "vu": 841878.0, "vt": 148170528.0, "cat": "CONSTRUCCIÓN DE ALCANTARILLAS"},
    {"id": "6.2.24", "und": "m3", "cant": 1551.0, "vu": 1239676.0, "vt": 1922737476.0, "cat": "CONSTRUCCIÓN DE ALCANTARILLAS"},
    {"id": "8.1", "und": "m", "cant": 1056.0, "vu": 140150.0, "vt": 147998400.0, "cat": "CONSTRUCCIÓN DE ALCANTARILLAS"},
    {"id": "8.27", "und": "m", "cant": 1056.0, "vu": 2306859.0, "vt": 2436043104.0, "cat": "CONSTRUCCIÓN DE ALCANTARILLAS"},
    {"id": "10.1", "und": "kg", "cant": 85184.0, "vu": 9487.0, "vt": 808140608.0, "cat": "CONSTRUCCIÓN DE ALCANTARILLAS"},
    {"id": "13.1", "und": "m3-Km", "cant": 30131.0, "vu": 2033.0, "vt": 61256323.0, "cat": "CONSTRUCCIÓN DE ALCANTARILLAS"},
    
    # CUNETA
    {"id": "4.1.8_2", "real_id": "4.1.8", "und": "m3", "cant": 6116.0, "vu": 54161.0, "vt": 331248676.0, "cat": "CONSTRUCCIÓN DE CUNETA"},
    {"id": "5.1.7_3", "real_id": "5.1.7", "und": "m3", "cant": 2815.0, "vu": 108602.0, "vt": 305714630.0, "cat": "CONSTRUCCIÓN DE CUNETA"},
    {"id": "6.2.50", "und": "m3", "cant": 3519.0, "vu": 1038976.0, "vt": 3656156544.0, "cat": "CONSTRUCCIÓN DE CUNETA"},
    {"id": "10.1_2", "real_id": "10.1", "und": "kg", "cant": 98534.0, "vu": 9487.0, "vt": 934792058.0, "cat": "CONSTRUCCIÓN DE CUNETA"},
    {"id": "13.1_3", "real_id": "13.1", "und": "m3-Km", "cant": 120482.0, "vu": 2033.0, "vt": 244939906.0, "cat": "CONSTRUCCIÓN DE CUNETA"},
    
    # FILTRO PARA CUNETAS
    {"id": "8.13.1", "und": "m", "cant": 35190.0, "vu": 143027.0, "vt": 5033120130.0, "cat": "CONSTRUCCIÓN DE FILTRO PARA CUNETAS"},
    {"id": "13.1_4", "real_id": "13.1", "und": "m3-Km", "cant": 542207.52, "vu": 2033.0, "vt": 1102307888.0, "cat": "CONSTRUCCIÓN DE FILTRO PARA CUNETAS"},

    # BORDILLOS
    {"id": "4.1.2", "und": "m3", "cant": 563.0, "vu": 52282.0, "vt": 29434766.0, "cat": "CONSTRUCCIÓN DE BORDILLOS"},
    {"id": "5.1.7_4", "real_id": "5.1.7", "und": "m3", "cant": 141.0, "vu": 108602.0, "vt": 15312882.0, "cat": "CONSTRUCCIÓN DE BORDILLOS"},
    {"id": "14.3", "und": "m", "cant": 7038.0, "vu": 115109.0, "vt": 810137142.0, "cat": "CONSTRUCCIÓN DE BORDILLOS"},
    
    # DISIPADORES
    {"id": "4.1.9", "und": "m3", "cant": 2772.0, "vu": 33663.0, "vt": 93314516.0, "cat": "CONSTRUCCIÓN DE DISIPADORES"},
    {"id": "6.1.18.1", "und": "m2", "cant": 924.0, "vu": 41173.0, "vt": 38043852.0, "cat": "CONSTRUCCIÓN DE DISIPADORES"},
    {"id": "8.18", "und": "m3", "cant": 792.0, "vu": 1019967.0, "vt": 807813864.0, "cat": "CONSTRUCCIÓN DE DISIPADORES"},
    {"id": "10.1_3", "real_id": "10.1", "und": "kg", "cant": 4488.0, "vu": 9487.0, "vt": 42577656.0, "cat": "CONSTRUCCIÓN DE DISIPADORES"},
    
    # ESTABILIZACION CON MATERIAL GRANULAR
    {"id": "4.1.1", "und": "m3", "cant": 3695.0, "vu": 18728.0, "vt": 69199960.0, "cat": "ESTABILIZACION CON MATERIAL GRANULAR"},
    {"id": "5.1.2", "und": "m3", "cant": 3695.0, "vu": 162146.0, "vt": 599129470.0, "cat": "ESTABILIZACION CON MATERIAL GRANULAR"},
    {"id": "5.2.16", "und": "m3", "cant": 49266.0, "vu": 59266.0, "vt": 2919798756.0, "cat": "ESTABILIZACION CON MATERIAL GRANULAR"},
    {"id": "5.2.13", "und": "m3", "cant": 9149.0, "vu": 54742.0, "vt": 500834558.0, "cat": "ESTABILIZACION CON MATERIAL GRANULAR"},
    {"id": "4.1.95", "und": "m3", "cant": 7320.0, "vu": 27866.0, "vt": 203979120.0, "cat": "ESTABILIZACION CON MATERIAL GRANULAR"},
    {"id": "4.3.8", "und": "m3", "cant": 7320.0, "vu": 11049.0, "vt": 80878680.0, "cat": "ESTABILIZACION CON MATERIAL GRANULAR"},
    {"id": "5.1.15", "und": "m3", "cant": 22521.0, "vu": 115826.0, "vt": 2608517346.0, "cat": "ESTABILIZACION CON MATERIAL GRANULAR"},
    {"id": "7.1.1", "und": "m2", "cant": 175950.0, "vu": 5399.0, "vt": 949954050.0, "cat": "ESTABILIZACION CON MATERIAL GRANULAR"},
    {"id": "7.1.12.2", "und": "m2", "cant": 175950.0, "vu": 22788.0, "vt": 4009548600.0, "cat": "ESTABILIZACION CON MATERIAL GRANULAR"},
    {"id": "13.1_5", "real_id": "13.1", "und": "m3-Km", "cant": 1269269.20, "vu": 2033.0, "vt": 2580424284.0, "cat": "ESTABILIZACION CON MATERIAL GRANULAR"},
    {"id": "13.2", "und": "m3-Km", "cant": 55425.0, "vu": 2033.0, "vt": 112679025.0, "cat": "ESTABILIZACION CON MATERIAL GRANULAR"},
    
    # SEÑALIZACIÓN VIAL
    {"id": "12.1", "und": "m", "cant": 105570.0, "vu": 3444.0, "vt": 363583080.0, "cat": "SEÑALIZACIÓN VIAL"},
    {"id": "12.9", "und": "Und", "cant": 175.0, "vu": 870445.0, "vt": 152327875.0, "cat": "SEÑALIZACIÓN VIAL"}
]

for p in presupuestos:
    if p['id_circuito'] == 105: # Sopetran - Belmira - Horizontes
        for a in sopetran_acts:
            real_id = a.get('real_id', a['id'])
            unique_id = f"{real_id}_{a['cat'].replace(' ', '_')}" if a.get('real_id') else real_id
            
            # Update catalog
            if not any(c['id_actividad'] == unique_id for c in catalogo):
                cat_item = next((c for c in catalogo if c['id_actividad'] == real_id), None)
                catalogo.append({
                    "id_actividad": unique_id,
                    "categoria": a['cat'],
                    "descripcion": cat_item['descripcion'] if cat_item else "Descripción...",
                    "unidad": a['und'],
                    "valor_unitario": a['vu']
                })
                
            if not any(act['id_actividad'] == unique_id for act in p['actividades_programadas']):
                p['actividades_programadas'].append({
                    "id_actividad": unique_id,
                    "cantidad_total": a['cant'],
                    "valor_total_esperado": a['vt']
                })
        
        p['meta_financiera_total'] = sum(a['valor_total_esperado'] for a in p['actividades_programadas'])

save_json('presupuestos_y_cronograma_base.json', presupuestos)
save_json('catalogo_actividades.json', catalogo)

print("Páginas 9 y 10 (Sopetran-Belmira) inyectadas con éxito.")
