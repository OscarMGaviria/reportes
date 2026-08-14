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

# Titiribi-Armenia acts (Circuit 104)
titiribi_acts = [
    # ALCANTARILLAS
    {"id": "2.8", "und": "m3", "cant": 24.0, "vu": 230711.0, "vt": 5537064.0, "cat": "CONSTRUCCIÓN DE ALCANTARILLAS"},
    {"id": "2.14.1", "und": "m", "cant": 30.0, "vu": 60377.0, "vt": 1811310.0, "cat": "CONSTRUCCIÓN DE ALCANTARILLAS"},
    {"id": "4.1.8", "und": "m3", "cant": 680.0, "vu": 54161.0, "vt": 36829480.0, "cat": "CONSTRUCCIÓN DE ALCANTARILLAS"},
    {"id": "4.2.2", "und": "m3", "cant": 220.0, "vu": 32553.0, "vt": 7161660.0, "cat": "CONSTRUCCIÓN DE ALCANTARILLAS"},
    {"id": "5.1.7", "und": "m3", "cant": 80.0, "vu": 108602.0, "vt": 8688160.0, "cat": "CONSTRUCCIÓN DE ALCANTARILLAS"},
    {"id": "6.2.4", "und": "m3", "cant": 20.0, "vu": 841878.0, "vt": 16837560.0, "cat": "CONSTRUCCIÓN DE ALCANTARILLAS"},
    {"id": "6.2.24", "und": "m3", "cant": 176.0, "vu": 1239676.0, "vt": 218182976.0, "cat": "CONSTRUCCIÓN DE ALCANTARILLAS"},
    {"id": "8.1", "und": "m", "cant": 120.0, "vu": 140150.0, "vt": 16818000.0, "cat": "CONSTRUCCIÓN DE ALCANTARILLAS"},
    {"id": "8.27", "und": "m", "cant": 120.0, "vu": 2306859.0, "vt": 276823080.0, "cat": "CONSTRUCCIÓN DE ALCANTARILLAS"},
    {"id": "10.1", "und": "kg", "cant": 9660.0, "vu": 9487.0, "vt": 91634160.0, "cat": "CONSTRUCCIÓN DE ALCANTARILLAS"},
    {"id": "13.1", "und": "m3-Km", "cant": 4616.0, "vu": 2033.0, "vt": 9384328.0, "cat": "CONSTRUCCIÓN DE ALCANTARILLAS"},
    
    # CUNETA
    {"id": "4.1.8_2", "real_id": "4.1.8", "und": "m3", "cant": 869.0, "vu": 54161.0, "vt": 47065909.0, "cat": "CONSTRUCCIÓN DE CUNETA"},
    {"id": "5.1.7_3", "real_id": "5.1.7", "und": "m3", "cant": 400.0, "vu": 108602.0, "vt": 43440800.0, "cat": "CONSTRUCCIÓN DE CUNETA"},
    {"id": "6.2.50", "und": "m3", "cant": 500.0, "vu": 1038976.0, "vt": 519488000.0, "cat": "CONSTRUCCIÓN DE CUNETA"},
    {"id": "10.1_2", "real_id": "10.1", "und": "kg", "cant": 14002.0, "vu": 9487.0, "vt": 132836974.0, "cat": "CONSTRUCCIÓN DE CUNETA"},
    {"id": "13.1_3", "real_id": "13.1", "und": "m3-Km", "cant": 23080.0, "vu": 2033.0, "vt": 46921640.0, "cat": "CONSTRUCCIÓN DE CUNETA"},
    
    # FILTRO PARA CUNETAS
    {"id": "8.13.1", "und": "m", "cant": 5000.0, "vu": 143027.0, "vt": 715135000.0, "cat": "CONSTRUCCIÓN DE FILTRO PARA CUNETAS"},
    {"id": "13.1_4", "real_id": "13.1", "und": "m3-Km", "cant": 103860.0, "vu": 2033.0, "vt": 211147380.0, "cat": "CONSTRUCCIÓN DE FILTRO PARA CUNETAS"},

    # BORDILLOS
    {"id": "4.1.2", "und": "m3", "cant": 80.0, "vu": 52282.0, "vt": 4182560.0, "cat": "CONSTRUCCIÓN DE BORDILLOS"},
    {"id": "5.1.7_4", "real_id": "5.1.7", "und": "m3", "cant": 20.0, "vu": 108602.0, "vt": 2172040.0, "cat": "CONSTRUCCIÓN DE BORDILLOS"},
    {"id": "14.3", "und": "m", "cant": 1000.0, "vu": 115109.0, "vt": 115109000.0, "cat": "CONSTRUCCIÓN DE BORDILLOS"},
    
    # DISIPADORES
    {"id": "4.1.9", "und": "m3", "cant": 79.0, "vu": 33663.0, "vt": 2659377.0, "cat": "CONSTRUCCIÓN DE DISIPADORES"},
    {"id": "6.1.18.1", "und": "m2", "cant": 105.0, "vu": 41173.0, "vt": 4323165.0, "cat": "CONSTRUCCIÓN DE DISIPADORES"},
    {"id": "8.18", "und": "m3", "cant": 90.0, "vu": 1019967.0, "vt": 91797030.0, "cat": "CONSTRUCCIÓN DE DISIPADORES"},
    {"id": "10.1_3", "real_id": "10.1", "und": "kg", "cant": 170.0, "vu": 9487.0, "vt": 1612790.0, "cat": "CONSTRUCCIÓN DE DISIPADORES"},
    
    # ESTABILIZACION CON MATERIAL GRANULAR
    {"id": "4.1.1", "und": "m3", "cant": 525.0, "vu": 18728.0, "vt": 9832200.0, "cat": "ESTABILIZACION CON MATERIAL GRANULAR"},
    {"id": "5.1.2", "und": "m3", "cant": 525.0, "vu": 162146.0, "vt": 85126650.0, "cat": "ESTABILIZACION CON MATERIAL GRANULAR"},
    {"id": "5.2.16", "und": "m3", "cant": 7000.0, "vu": 59266.0, "vt": 414862000.0, "cat": "ESTABILIZACION CON MATERIAL GRANULAR"},
    {"id": "5.2.13", "und": "m3", "cant": 1300.0, "vu": 54742.0, "vt": 71164600.0, "cat": "ESTABILIZACION CON MATERIAL GRANULAR"},
    {"id": "4.1.95", "und": "m3", "cant": 1040.0, "vu": 27866.0, "vt": 28980640.0, "cat": "ESTABILIZACION CON MATERIAL GRANULAR"},
    {"id": "4.3.8", "und": "m3", "cant": 1040.0, "vu": 11049.0, "vt": 11490960.0, "cat": "ESTABILIZACION CON MATERIAL GRANULAR"},
    {"id": "5.1.15", "und": "m3", "cant": 3200.0, "vu": 115826.0, "vt": 370643200.0, "cat": "ESTABILIZACION CON MATERIAL GRANULAR"},
    {"id": "7.1.1", "und": "m2", "cant": 25000.0, "vu": 5399.0, "vt": 134975000.0, "cat": "ESTABILIZACION CON MATERIAL GRANULAR"},
    {"id": "7.1.12.2", "und": "m2", "cant": 25000.0, "vu": 22788.0, "vt": 569700000.0, "cat": "ESTABILIZACION CON MATERIAL GRANULAR"},
    {"id": "13.1_5", "real_id": "13.1", "und": "m3-Km", "cant": 243135.39, "vu": 2033.0, "vt": 494294162.0, "cat": "ESTABILIZACION CON MATERIAL GRANULAR"},
    {"id": "13.2", "und": "m3-Km", "cant": 7875.0, "vu": 2033.0, "vt": 16009875.0, "cat": "ESTABILIZACION CON MATERIAL GRANULAR"},
    
    # SEÑALIZACIÓN VIAL
    {"id": "12.1", "und": "m", "cant": 15000.0, "vu": 3444.0, "vt": 51660000.0, "cat": "SEÑALIZACIÓN VIAL"},
    {"id": "12.9", "und": "Und", "cant": 25.0, "vu": 870445.0, "vt": 21761125.0, "cat": "SEÑALIZACIÓN VIAL"}
]

for p in presupuestos:
    if p['id_circuito'] == 104: # Titiribi-Armenia
        for a in titiribi_acts:
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

print("Páginas 7 y 8 (Titiribi-Armenia) inyectadas con éxito.")
