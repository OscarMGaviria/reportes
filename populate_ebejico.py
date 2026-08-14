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

# Ebejico-Heliconia acts (Circuit 103)
ebejico_acts = [
    # ALCANTARILLAS
    {"id": "2.8", "und": "m3", "cant": 179.0, "vu": 230711.0, "vt": 41297269.0, "cat": "CONSTRUCCIÓN DE ALCANTARILLAS"},
    {"id": "2.14.1", "und": "m", "cant": 228.0, "vu": 60377.0, "vt": 13765956.0, "cat": "CONSTRUCCIÓN DE ALCANTARILLAS"},
    {"id": "4.1.8", "und": "m3", "cant": 5202.0, "vu": 54161.0, "vt": 281745522.0, "cat": "CONSTRUCCIÓN DE ALCANTARILLAS"},
    {"id": "4.2.2", "und": "m3", "cant": 1683.0, "vu": 32553.0, "vt": 54786699.0, "cat": "CONSTRUCCIÓN DE ALCANTARILLAS"},
    {"id": "5.1.7", "und": "m3", "cant": 612.0, "vu": 108602.0, "vt": 66464424.0, "cat": "CONSTRUCCIÓN DE ALCANTARILLAS"},
    {"id": "6.2.4", "und": "m3", "cant": 153.0, "vu": 841878.0, "vt": 128807334.0, "cat": "CONSTRUCCIÓN DE ALCANTARILLAS"},
    {"id": "6.2.24", "und": "m3", "cant": 1348.0, "vu": 1239676.0, "vt": 1671083248.0, "cat": "CONSTRUCCIÓN DE ALCANTARILLAS"},
    {"id": "8.1", "und": "m", "cant": 828.0, "vu": 140150.0, "vt": 116044200.0, "cat": "CONSTRUCCIÓN DE ALCANTARILLAS"},
    {"id": "8.27", "und": "m", "cant": 918.0, "vu": 2306859.0, "vt": 2117696562.0, "cat": "CONSTRUCCIÓN DE ALCANTARILLAS"},
    {"id": "10.1", "und": "kg", "cant": 74052.0, "vu": 9487.0, "vt": 702531324.0, "cat": "CONSTRUCCIÓN DE ALCANTARILLAS"},
    {"id": "13.1", "und": "m3-Km", "cant": 39780.0, "vu": 2033.0, "vt": 80872740.0, "cat": "CONSTRUCCIÓN DE ALCANTARILLAS"},
    
    # CUNETA
    {"id": "4.1.8_2", "real_id": "4.1.8", "und": "m3", "cant": 4999.0, "vu": 54161.0, "vt": 270750839.0, "cat": "CONSTRUCCIÓN DE CUNETA"},
    {"id": "5.1.7_3", "real_id": "5.1.7", "und": "m3", "cant": 2301.0, "vu": 108602.0, "vt": 249893202.0, "cat": "CONSTRUCCIÓN DE CUNETA"},
    {"id": "6.2.50", "und": "m3", "cant": 2876.0, "vu": 1038976.0, "vt": 2988094976.0, "cat": "CONSTRUCCIÓN DE CUNETA"},
    {"id": "10.1_2", "real_id": "10.1", "und": "kg", "cant": 80530.0, "vu": 9487.0, "vt": 763988110.0, "cat": "CONSTRUCCIÓN DE CUNETA"},
    {"id": "13.1_3", "real_id": "13.1", "und": "m3-Km", "cant": 149565.0, "vu": 2033.0, "vt": 304065645.0, "cat": "CONSTRUCCIÓN DE CUNETA"},
    
    # FILTRO PARA CUNETAS
    {"id": "8.13.1", "und": "m", "cant": 28760.0, "vu": 143027.0, "vt": 4113456520.0, "cat": "CONSTRUCCIÓN DE FILTRO PARA CUNETAS"},
    {"id": "13.1_4", "real_id": "13.1", "und": "m3-Km", "cant": 672984.0, "vu": 2033.0, "vt": 1368176472.0, "cat": "CONSTRUCCIÓN DE FILTRO PARA CUNETAS"},

    # BORDILLOS
    {"id": "4.1.2", "und": "m3", "cant": 460.0, "vu": 52282.0, "vt": 24049720.0, "cat": "CONSTRUCCIÓN DE BORDILLOS"},
    {"id": "5.1.7_4", "real_id": "5.1.7", "und": "m3", "cant": 115.0, "vu": 108602.0, "vt": 12489230.0, "cat": "CONSTRUCCIÓN DE BORDILLOS"},
    {"id": "14.3", "und": "m", "cant": 5752.0, "vu": 115109.0, "vt": 662106968.0, "cat": "CONSTRUCCIÓN DE BORDILLOS"},
    
    # DISIPADORES
    {"id": "4.1.9", "und": "m3", "cant": 603.0, "vu": 33663.0, "vt": 20298212.0, "cat": "CONSTRUCCIÓN DE DISIPADORES"},
    {"id": "6.1.18.1", "und": "m2", "cant": 805.0, "vu": 41173.0, "vt": 33144265.0, "cat": "CONSTRUCCIÓN DE DISIPADORES"},
    {"id": "8.18", "und": "m3", "cant": 690.0, "vu": 1019967.0, "vt": 703777230.0, "cat": "CONSTRUCCIÓN DE DISIPADORES"},
    {"id": "10.1_3", "real_id": "10.1", "und": "kg", "cant": 3910.0, "vu": 9487.0, "vt": 37094170.0, "cat": "CONSTRUCCIÓN DE DISIPADORES"},
    
    # ESTABILIZACION CON MATERIAL GRANULAR
    {"id": "4.1.1", "und": "m3", "cant": 3020.0, "vu": 18728.0, "vt": 56558560.0, "cat": "ESTABILIZACION CON MATERIAL GRANULAR"},
    {"id": "5.1.2", "und": "m3", "cant": 3020.0, "vu": 162146.0, "vt": 489680920.0, "cat": "ESTABILIZACION CON MATERIAL GRANULAR"},
    {"id": "5.2.16", "und": "m3", "cant": 40264.0, "vu": 59266.0, "vt": 2386286224.0, "cat": "ESTABILIZACION CON MATERIAL GRANULAR"},
    {"id": "5.2.13", "und": "m3", "cant": 7478.0, "vu": 54742.0, "vt": 409360676.0, "cat": "ESTABILIZACION CON MATERIAL GRANULAR"},
    {"id": "4.1.95", "und": "m3", "cant": 5982.0, "vu": 27866.0, "vt": 166694412.0, "cat": "ESTABILIZACION CON MATERIAL GRANULAR"},
    {"id": "4.3.8", "und": "m3", "cant": 5982.0, "vu": 11049.0, "vt": 66095118.0, "cat": "ESTABILIZACION CON MATERIAL GRANULAR"},
    {"id": "5.1.15", "und": "m3", "cant": 18406.0, "vu": 115826.0, "vt": 2131893356.0, "cat": "ESTABILIZACION CON MATERIAL GRANULAR"},
    {"id": "7.1.1", "und": "m2", "cant": 143800.0, "vu": 5399.0, "vt": 776376200.0, "cat": "ESTABILIZACION CON MATERIAL GRANULAR"},
    {"id": "7.1.12.2", "und": "m2", "cant": 143800.0, "vu": 22788.0, "vt": 3276914400.0, "cat": "ESTABILIZACION CON MATERIAL GRANULAR"},
    {"id": "13.1_5", "real_id": "13.1", "und": "m3-Km", "cant": 1575423.85, "vu": 2033.0, "vt": 3202836687.0, "cat": "ESTABILIZACION CON MATERIAL GRANULAR"},
    {"id": "13.2", "und": "m3-Km", "cant": 45300.0, "vu": 2033.0, "vt": 92094900.0, "cat": "ESTABILIZACION CON MATERIAL GRANULAR"},
    
    # SEÑALIZACIÓN VIAL
    {"id": "12.1", "und": "m", "cant": 86280.0, "vu": 3444.0, "vt": 297148320.0, "cat": "SEÑALIZACIÓN VIAL"},
    {"id": "12.9", "und": "Und", "cant": 145.0, "vu": 870445.0, "vt": 126214525.0, "cat": "SEÑALIZACIÓN VIAL"}
]

for p in presupuestos:
    if p['id_circuito'] == 103: # Ebejico - Heliconia - Medellin
        for a in ebejico_acts:
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

print("Páginas 5 y 6 (Ebejico-Heliconia) inyectadas con éxito.")
