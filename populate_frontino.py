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

# Frontino-Nutibara acts
frontino_acts = [
    # ALCANTARILLAS
    {"id": "2.8", "und": "m3", "cant": 9.00, "vu": 230711.00, "vt": 2076399.00, "cat": "CONSTRUCCIÓN DE ALCANTARILLAS"},
    {"id": "2.14.1", "und": "m", "cant": 12.00, "vu": 60377.00, "vt": 724524.00, "cat": "CONSTRUCCIÓN DE ALCANTARILLAS"},
    {"id": "4.1.8", "und": "m3", "cant": 3468.00, "vu": 54161.00, "vt": 187830346.00, "cat": "CONSTRUCCIÓN DE ALCANTARILLAS"},
    {"id": "4.2.2", "und": "m3", "cant": 1122.00, "vu": 32553.00, "vt": 36524466.00, "cat": "CONSTRUCCIÓN DE ALCANTARILLAS"},
    {"id": "5.1.7", "und": "m3", "cant": 408.00, "vu": 108602.00, "vt": 44309616.00, "cat": "CONSTRUCCIÓN DE ALCANTARILLAS"},
    {"id": "6.2.4", "und": "m3", "cant": 102.00, "vu": 841878.00, "vt": 85871556.00, "cat": "CONSTRUCCIÓN DE ALCANTARILLAS"},
    {"id": "6.2.24", "und": "m3", "cant": 899.00, "vu": 1239676.00, "vt": 1114468724.00, "cat": "CONSTRUCCIÓN DE ALCANTARILLAS"},
    {"id": "8.1", "und": "m", "cant": 876.00, "vu": 140150.00, "vt": 122771400.00, "cat": "CONSTRUCCIÓN DE ALCANTARILLAS"},
    {"id": "8.27", "und": "m", "cant": 612.00, "vu": 2306859.00, "vt": 1411797708.00, "cat": "CONSTRUCCIÓN DE ALCANTARILLAS"},
    {"id": "10.1", "und": "kg", "cant": 49368.00, "vu": 9487.00, "vt": 468354216.00, "cat": "CONSTRUCCIÓN DE ALCANTARILLAS"},
    {"id": "13.1", "und": "m3-Km", "cant": 45696.00, "vu": 2033.00, "vt": 92899968.00, "cat": "CONSTRUCCIÓN DE ALCANTARILLAS"},
    
    # CUNETA
    {"id": "4.1.8_2", "real_id": "4.1.8", "und": "m3", "cant": 4345.00, "vu": 54161.00, "vt": 235328545.00, "cat": "CONSTRUCCIÓN DE CUNETA"},
    {"id": "5.1.7_3", "real_id": "5.1.7", "und": "m3", "cant": 2000.00, "vu": 108602.00, "vt": 217204000.00, "cat": "CONSTRUCCIÓN DE CUNETA"},
    {"id": "6.2.50", "und": "m3", "cant": 2500.00, "vu": 1038976.00, "vt": 2597440000.00, "cat": "CONSTRUCCIÓN DE CUNETA"},
    {"id": "10.1_2", "real_id": "10.1", "und": "kg", "cant": 70002.00, "vu": 9487.00, "vt": 664108974.00, "cat": "CONSTRUCCIÓN DE CUNETA"},
    {"id": "13.1_3", "real_id": "13.1", "und": "m3-Km", "cant": 224000.00, "vu": 2033.00, "vt": 455392000.00, "cat": "CONSTRUCCIÓN DE CUNETA"},
    
    # FILTRO PARA CUNETAS
    {"id": "8.13.1", "und": "m", "cant": 25000.00, "vu": 143027.00, "vt": 3575675000.00, "cat": "CONSTRUCCIÓN DE FILTRO PARA CUNETAS"},
    {"id": "13.1_4", "real_id": "13.1", "und": "m3-Km", "cant": 1008000.00, "vu": 2033.00, "vt": 2049264000.00, "cat": "CONSTRUCCIÓN DE FILTRO PARA CUNETAS"},

    # BORDILLOS
    {"id": "4.1.2", "und": "m3", "cant": 400.00, "vu": 52282.00, "vt": 20912800.00, "cat": "CONSTRUCCIÓN DE BORDILLOS"},
    {"id": "5.1.7_4", "real_id": "5.1.7", "und": "m3", "cant": 100.00, "vu": 108602.00, "vt": 10860200.00, "cat": "CONSTRUCCIÓN DE BORDILLOS"},
    {"id": "14.3", "und": "m", "cant": 5000.00, "vu": 115109.00, "vt": 575545000.00, "cat": "CONSTRUCCIÓN DE BORDILLOS"},
    
    # DISIPADORES
    {"id": "4.1.9", "und": "m3", "cant": 180.00, "vu": 33663.00, "vt": 6048540.00, "cat": "CONSTRUCCIÓN DE DISIPADORES"},
    {"id": "6.1.18.1", "und": "m2", "cant": 539.00, "vu": 41173.00, "vt": 22192247.00, "cat": "CONSTRUCCIÓN DE DISIPADORES"},
    {"id": "8.18", "und": "m3", "cant": 462.00, "vu": 1019967.00, "vt": 471224754.00, "cat": "CONSTRUCCIÓN DE DISIPADORES"},
    {"id": "10.1_3", "real_id": "10.1", "und": "kg", "cant": 2618.00, "vu": 9487.00, "vt": 24817982.00, "cat": "CONSTRUCCIÓN DE DISIPADORES"},
    
    # ESTABILIZACION CON MATERIAL GRANULAR
    {"id": "4.1.1", "und": "m3", "cant": 2625.00, "vu": 18728.00, "vt": 49161000.00, "cat": "ESTABILIZACION CON MATERIAL GRANULAR"},
    {"id": "5.1.2", "und": "m3", "cant": 2625.00, "vu": 162146.00, "vt": 425633250.00, "cat": "ESTABILIZACION CON MATERIAL GRANULAR"},
    {"id": "5.2.16", "und": "m3", "cant": 35000.00, "vu": 59266.00, "vt": 2074310000.00, "cat": "ESTABILIZACION CON MATERIAL GRANULAR"},
    {"id": "5.2.13", "und": "m3", "cant": 6500.00, "vu": 54742.00, "vt": 355823000.00, "cat": "ESTABILIZACION CON MATERIAL GRANULAR"},
    {"id": "4.1.95", "und": "m3", "cant": 4225.00, "vu": 27866.00, "vt": 117733850.00, "cat": "ESTABILIZACION CON MATERIAL GRANULAR"},
    {"id": "4.3.8", "und": "m3", "cant": 4225.00, "vu": 11049.00, "vt": 46682025.00, "cat": "ESTABILIZACION CON MATERIAL GRANULAR"},
    {"id": "5.1.15", "und": "m3", "cant": 16376.00, "vu": 115826.00, "vt": 1896766576.00, "cat": "ESTABILIZACION CON MATERIAL GRANULAR"},
    {"id": "7.1.1", "und": "m2", "cant": 125000.00, "vu": 5399.00, "vt": 674875000.00, "cat": "ESTABILIZACION CON MATERIAL GRANULAR"},
    {"id": "7.1.12.2", "und": "m2", "cant": 125000.00, "vu": 22788.00, "vt": 2848500000.00, "cat": "ESTABILIZACION CON MATERIAL GRANULAR"},
    {"id": "13.1_5", "real_id": "13.1", "und": "m3-Km", "cant": 4487700.00, "vu": 2033.00, "vt": 9123494100.00, "cat": "ESTABILIZACION CON MATERIAL GRANULAR"},
    {"id": "13.2", "und": "m3-Km", "cant": 259875.00, "vu": 2033.00, "vt": 528325875.00, "cat": "ESTABILIZACION CON MATERIAL GRANULAR"},
    
    # SEÑALIZACIÓN VIAL
    {"id": "12.1", "und": "m", "cant": 75000.00, "vu": 3444.00, "vt": 258300000.00, "cat": "SEÑALIZACIÓN VIAL"},
    {"id": "12.9", "und": "Und", "cant": 125.00, "vu": 870445.00, "vt": 108805625.00, "cat": "SEÑALIZACIÓN VIAL"}
]

# Copiamos la descripción del catálogo si ya existe (así compartimos las mismas actividades)
for a in frontino_acts:
    real_id = a.get('real_id', a['id']) # Some items share IDs like 4.1.8 in multiple categories. The original system used the same id. Wait! The original system didn't use real_id. It used just the code and depended on the category. But in our new system, `id_actividad` must be unique in the catalog. Let's make sure it's unique by appending category if needed, or if it's the exact same item, just use `real_id`.
    
    # Let's check if the base ID exists
    cat_item = next((c for c in catalogo if c['id_actividad'] == real_id), None)
    if cat_item:
        a['desc'] = cat_item['descripcion']
    else:
        # If it doesn't exist, we must add it. E.g. 6.2.50, 8.13.1
        a['desc'] = "VERIFICAR_DESCRIPCION"
        # We will manually correct these later or just leave a placeholder

for a in frontino_acts:
    real_id = a.get('real_id', a['id'])
    if not any(c['id_actividad'] == real_id for c in catalogo):
        # We need to pull from Miserenga script if they were there, but since we didn't add CUNETAS for Miserenga, they are missing.
        # I will manually add the descriptions for the new ones.
        desc = "Descripción no proporcionada en la página anterior"
        if real_id == "6.2.50": desc = "Concreto Clase D (28 MPa). Cunetas."
        elif real_id == "8.13.1": desc = "Suministro e instalación de dren francés de zanja de 0.4 m x 0.9 m, con Geotextil NT2500 y Grava de 3/4..."
        elif real_id == "8.1": desc = "Mantenimiento de obras de drenaje existentes..."
        elif real_id == "8.27": desc = "Suministro, transporte y colocación de Tubería PVC Alcantarillado pared interior lisa..."
        
        catalogo.append({
            "id_actividad": real_id,
            "categoria": a['cat'],
            "descripcion": desc,
            "unidad": a['und'],
            "valor_unitario": a['vu']
        })

for p in presupuestos:
    if p['id_circuito'] == 102: # Frontino - Nutibara
        for a in frontino_acts:
            real_id = a.get('real_id', a['id'])
            
            # Since an activity (e.g. 13.1) can appear multiple times in the SAME budget but under different categories, 
            # our JSON structure `actividades_programadas` only uses `id_actividad`.
            # If it appears multiple times, we need a unique ID or we sum them.
            # The original excel had them separate. Let's make the IDs unique per category to be safe, e.g. "13.1_CUNETA".
            
            unique_id = f"{real_id}_{a['cat'].replace(' ', '_')}"
            
            # Update catalog to use this unique ID if it doesn't exist
            if not any(c['id_actividad'] == unique_id for c in catalogo):
                cat_item = next((c for c in catalogo if c['id_actividad'] == real_id), None)
                catalogo.append({
                    "id_actividad": unique_id,
                    "categoria": a['cat'],
                    "descripcion": cat_item['descripcion'] if cat_item else "Descripción...",
                    "unidad": a['und'],
                    "valor_unitario": a['vu']
                })
            
            p['actividades_programadas'].append({
                "id_actividad": unique_id,
                "cantidad_total": a['cant'],
                "valor_total_esperado": a['vt']
            })
        
        p['meta_financiera_total'] = sum(a['valor_total_esperado'] for a in p['actividades_programadas'])

save_json('presupuestos_y_cronograma_base.json', presupuestos)
save_json('catalogo_actividades.json', catalogo)

print("Páginas 3 y 4 inyectadas con éxito para Frontino-Nutibara.")
