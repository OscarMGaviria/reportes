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
catalogo = load_json('catalogo_actividades.json')

circuit_101_acts = [
    # ALCANTARILLAS
    {"id": "2.8", "und": "m3", "cant": 24.0, "vu": 230711.0, "vt": 5537064.0, "cat": "CONSTRUCCIÓN DE ALCANTARILLAS"},
    {"id": "2.14.1", "und": "m", "cant": 30.0, "vu": 60377.0, "vt": 1811310.0, "cat": "CONSTRUCCIÓN DE ALCANTARILLAS"},
    {"id": "4.1.8", "und": "m3", "cant": 204.0, "vu": 54161.0, "vt": 11048844.0, "cat": "CONSTRUCCIÓN DE ALCANTARILLAS"},
    {"id": "4.2.2", "und": "m3", "cant": 66.0, "vu": 32553.0, "vt": 2148498.0, "cat": "CONSTRUCCIÓN DE ALCANTARILLAS"},
    {"id": "5.1.7", "und": "m3", "cant": 24.0, "vu": 108602.0, "vt": 2606448.0, "cat": "CONSTRUCCIÓN DE ALCANTARILLAS"},
    {"id": "6.2.4", "und": "m3", "cant": 6.0, "vu": 841878.0, "vt": 5051268.0, "cat": "CONSTRUCCIÓN DE ALCANTARILLAS"},
    {"id": "6.2.24", "und": "m3", "cant": 53.0, "vu": 1239676.0, "vt": 65702828.0, "cat": "CONSTRUCCIÓN DE ALCANTARILLAS"},
    {"id": "8.1", "und": "m", "cant": 48.0, "vu": 140150.0, "vt": 6727200.0, "cat": "CONSTRUCCIÓN DE ALCANTARILLAS"},
    {"id": "8.27", "und": "m", "cant": 36.0, "vu": 2306859.0, "vt": 83046924.0, "cat": "CONSTRUCCIÓN DE ALCANTARILLAS"},
    {"id": "10.1", "und": "kg", "cant": 2904.0, "vu": 9487.0, "vt": 27550248.0, "cat": "CONSTRUCCIÓN DE ALCANTARILLAS"},
    {"id": "13.1", "und": "m3-Km", "cant": 1296.0, "vu": 2033.0, "vt": 2634768.0, "cat": "CONSTRUCCIÓN DE ALCANTARILLAS"},
    
    # CUNETAS
    {"id": "4.1.8_2", "real_id": "4.1.8", "und": "m3", "cant": 174.0, "vu": 54161.0, "vt": 9424014.0, "cat": "CONSTRUCCIÓN DE CUNETA"},
    {"id": "5.1.7_2", "real_id": "5.1.7", "und": "m3", "cant": 80.0, "vu": 108602.0, "vt": 8688160.0, "cat": "CONSTRUCCIÓN DE CUNETA"},
    {"id": "6.2.50", "und": "m3", "cant": 100.0, "vu": 1038976.0, "vt": 103897600.0, "cat": "CONSTRUCCIÓN DE CUNETA"},
    {"id": "10.1_2", "real_id": "10.1", "und": "kg", "cant": 2802.0, "vu": 9487.0, "vt": 26582574.0, "cat": "CONSTRUCCIÓN DE CUNETA"},
    {"id": "13.1_2", "real_id": "13.1", "und": "m3-Km", "cant": 4320.0, "vu": 2033.0, "vt": 8782560.0, "cat": "CONSTRUCCIÓN DE CUNETA"},
    
    # FILTRO PARA CUNETAS
    {"id": "8.13.1", "und": "m", "cant": 1000.0, "vu": 143027.0, "vt": 143027000.0, "cat": "CONSTRUCCIÓN DE FILTRO PARA CUNETAS"},
    {"id": "13.1_3", "real_id": "13.1", "und": "m3-Km", "cant": 19440.0, "vu": 2033.0, "vt": 39521520.0, "cat": "CONSTRUCCIÓN DE FILTRO PARA CUNETAS"},

    # BORDILLOS
    {"id": "4.1.2", "und": "m3", "cant": 16.0, "vu": 52282.0, "vt": 836512.0, "cat": "CONSTRUCCIÓN DE BORDILLOS"},
    {"id": "5.1.7_3", "real_id": "5.1.7", "und": "m3", "cant": 4.0, "vu": 108602.0, "vt": 434408.0, "cat": "CONSTRUCCIÓN DE BORDILLOS"},
    {"id": "14.3", "und": "m", "cant": 200.0, "vu": 115109.0, "vt": 23021800.0, "cat": "CONSTRUCCIÓN DE BORDILLOS"},
    
    # DISIPADORES
    {"id": "4.1.9", "und": "m3", "cant": 180.0, "vu": 33663.0, "vt": 6018540.0, "cat": "CONSTRUCCIÓN DE DISIPADORES"},
    {"id": "6.1.18.1", "und": "m2", "cant": 35.0, "vu": 41173.0, "vt": 1441055.0, "cat": "CONSTRUCCIÓN DE DISIPADORES"},
    {"id": "8.18", "und": "m3", "cant": 30.0, "vu": 1019967.0, "vt": 30599010.0, "cat": "CONSTRUCCIÓN DE DISIPADORES"},
    {"id": "10.1_3", "real_id": "10.1", "und": "kg", "cant": 170.0, "vu": 9487.0, "vt": 1612790.0, "cat": "CONSTRUCCIÓN DE DISIPADORES"},

    # ESTABILIZACION CON MATERIAL GRANULAR
    {"id": "4.1.1", "und": "m3", "cant": 105.0, "vu": 18728.0, "vt": 1966440.0, "cat": "ESTABILIZACION CON MATERIAL GRANULAR"},
    {"id": "5.1.2", "und": "m3", "cant": 105.0, "vu": 162146.0, "vt": 17025330.0, "cat": "ESTABILIZACION CON MATERIAL GRANULAR"},
    {"id": "5.2.16", "und": "m3", "cant": 1400.0, "vu": 59266.0, "vt": 82972400.0, "cat": "ESTABILIZACION CON MATERIAL GRANULAR"},
    {"id": "5.2.13", "und": "m3", "cant": 260.0, "vu": 54742.0, "vt": 14232920.0, "cat": "ESTABILIZACION CON MATERIAL GRANULAR"},
    {"id": "4.1.95", "und": "m3", "cant": 208.0, "vu": 27866.0, "vt": 5796128.0, "cat": "ESTABILIZACION CON MATERIAL GRANULAR"},
    {"id": "4.3.8", "und": "m3", "cant": 208.0, "vu": 11049.0, "vt": 2298192.0, "cat": "ESTABILIZACION CON MATERIAL GRANULAR"},
    {"id": "5.1.15", "und": "m3", "cant": 640.0, "vu": 115826.0, "vt": 74128640.0, "cat": "ESTABILIZACION CON MATERIAL GRANULAR"},
    {"id": "7.1.1", "und": "m2", "cant": 5000.0, "vu": 5399.0, "vt": 26995000.0, "cat": "ESTABILIZACION CON MATERIAL GRANULAR"},
    {"id": "7.1.12.2", "und": "m2", "cant": 5000.0, "vu": 22788.0, "vt": 113940000.0, "cat": "ESTABILIZACION CON MATERIAL GRANULAR"},
    {"id": "13.1_4", "real_id": "13.1", "und": "m3-Km", "cant": 86548.50, "vu": 2033.0, "vt": 175953101.0, "cat": "ESTABILIZACION CON MATERIAL GRANULAR"},
    {"id": "13.2", "und": "m3-Km", "cant": 1575.0, "vu": 2033.0, "vt": 3201975.0, "cat": "ESTABILIZACION CON MATERIAL GRANULAR"},

    # SEÑALIZACIÓN VIAL
    {"id": "12.1", "und": "m", "cant": 3000.0, "vu": 3444.0, "vt": 10332000.0, "cat": "SEÑALIZACIÓN VIAL"},
    {"id": "12.9", "und": "Und", "cant": 5.0, "vu": 870445.0, "vt": 4352225.0, "cat": "SEÑALIZACIÓN VIAL"}
]

for p in presupuestos:
    if p['id_circuito'] == 101:
        # Preserve MACRO activities
        macros = [act for act in p['actividades_programadas'] if act['id_actividad'].startswith('MACRO')]
        p['actividades_programadas'] = macros
        
        for a in circuit_101_acts:
            real_id = a.get('real_id', a['id'])
            unique_id = f"{real_id}_{a['cat'].replace(' ', '_')}" if a.get('real_id') else real_id
            
            p['actividades_programadas'].append({
                "id_actividad": unique_id,
                "cantidad_total": a['cant'],
                "valor_total_esperado": a['vt']
            })

save_json('presupuestos_y_cronograma_base.json', presupuestos)
print("Updated circuit 101 successfully.")
