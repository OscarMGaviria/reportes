import json
import os
import re

DATA_DIR = os.path.join('src', 'data')

def load_json(name):
    path = os.path.join(DATA_DIR, name)
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

def save_json(name, data):
    path = os.path.join(DATA_DIR, name)
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

circuit_mapping = {
    "MISERENGA-EBEJICO": 101,
    "FRONTINO-NUTIBARA": 102,
    "EBÉJICO -HELICONIA-MEDELLÍN": 103,
    "TITIRIBÍ-ARMENIA": 104,
    "SOPETRAN-BELMIRA-HORIZONTES": 105,
    "EL GUAYABO-EL SALTO-PARTIDAS A GUADALUPE": 21,
    "CAROLINA DEL PRINCIPE-ANGOSTURA": 5,
    "ALTO DEL CARDAL-TOLEDO": 34,
    "SANTA ROSA-CAROLINA DEL PRINCIPE": 36,
    "ENTRERRIOS-LABORES-SAN JOSE DE LA MONTAÑA": 15,
    "SOPETRAN-HORIZONTES-BELMIRA": 12,
    "Cáceres-El Tigre-Alto de Tamaná- La Chilona": 25,
    "VÍA CARAMANTA - CRISTALES - SAN ROQUE": 22,
    "VÍA SAN RAFAEL-SAN ROQUE-SANTO DOMINGO-ALEJANDRÍA": 28,
    "VÍA AMALFI-PORTACHUELOS-SANTA ISABEL": 32,
    "Circuito Remedios - La Y De La Virgen - Puerto Berrío": 33,
    "Vía La Ye - Yondo": 31,
    "Vía San Pedro - El Tres - Turbo": 40,
    "Vía San Pedro de Urabá - Arboletes": 39,
    "Vía San Pedro de Urabá - Necoclí": 26,
    "Corredor Mutatá - Pavarando": 38
}

act_to_id = {
    "Estabilización con material granular": "4.1.1",
    "Construcción de alcantarillas": "2.8",
    "Construcción de filtro para cunetas": "8.13.1",
    "Construcción de cuneta": "6.2.50",
    "Construcción de cunetas": "6.2.50",
    "Construcción de disipadores": "4.1.9",
    "Construcción de bordillos": "4.1.2",
    "Señalización vial": "12.1",
    "PMA": "MACRO-PMA",
    "PMT": "MACRO-PMT",
    "Caracterización vial": "MACRO-CARAC",
    "Topografia": "MACRO-CARAC-TOPO", # Will map visually later
    "Exploracion de campo": "MACRO-CARAC-EXPL"
}

with open('budgets_dump.txt', 'r', encoding='utf-8') as f:
    lines = f.readlines()

circuits = {}
current_circuit = None

for line in lines:
    line = line.strip()
    if not line: continue
    
    # Check if it's a circuit name
    matched_name = None
    for cname in circuit_mapping.keys():
        if line.startswith(cname) or cname in line:
            matched_name = cname
            break
            
    if matched_name:
        current_circuit = circuit_mapping[matched_name]
        if current_circuit not in circuits:
            circuits[current_circuit] = []
        continue
        
    if current_circuit is None: continue
    
    if line.startswith("No.") or line.startswith("TOTAL") or line.startswith("VALOR TOTAL"):
        continue
        
    # Parse line
    parts = line.split('\t')
    if len(parts) >= 3:
        act_name = parts[1].strip()
        val_str = parts[2].replace('$', '').replace('.', '').replace(',', '').strip()
        if not val_str: val_str = '0'
        try:
            val = float(val_str)
        except:
            continue
            
        cant = 1.0
        unidad = 'Glb'
        
        if len(parts) >= 4 and parts[3].strip():
            c_str = parts[3].replace(',', '').strip()
            try:
                cant = float(c_str)
            except:
                pass
        
        if len(parts) >= 5 and parts[4].strip():
            unidad = parts[4].strip().upper()
            if unidad == 'M ': unidad = 'm'
            if unidad == 'M': unidad = 'm'
            if unidad == 'UN' or unidad == 'UN ': unidad = 'und'
            if unidad == 'KM': unidad = 'Km'
            
        # Specific overrides based on user's manual fix for Frontino
        if act_name == "Señalización vial" and matched_name == "FRONTINO-NUTIBARA":
            val = 367105625 # there was a typo in user's prompt 367.105.625.
            
        if act_name in act_to_id:
            circuits[current_circuit].append({
                "act": act_name,
                "id": act_to_id[act_name],
                "val": val,
                "cant": cant,
                "und": unidad
            })

presupuestos = load_json('presupuestos_y_cronograma_base.json')
metas_fisicas = {}

for c_id, acts in circuits.items():
    # Meta fisicas
    c_metas = {}
    
    for a in acts:
        # Standardize name for metas dict keys in Vue
        name = a['act']
        if name == "Construcción de cuneta": name = "Construcción de cunetas"
        if name == "Estabilización con material granular": name = "Estabilización con material granular"
        if name.upper() == "PMA" or name.upper() == "PMT" or name.upper() == "CARACTERIZACIÓN VIAL": continue
        
        c_metas[name] = {"total": a['cant'], "unidad": a['und']}
        
        if name.lower() == "construcción de alcantarillas" and c_id != 101: # 101 was already hardcoded
            # Auto split into Limpieza, Remplazar, Nuevas
            split_val = a['cant'] / 3
            c_metas[name]["subItems"] = [
                { "nombre": "Limpieza", "completado": 0, "total": split_val },
                { "nombre": "Remplazar", "completado": 0, "total": split_val },
                { "nombre": "Nuevas", "completado": 0, "total": split_val }
            ]
    
    metas_fisicas[str(c_id)] = c_metas
    
    # Presupuestos
    p_idx = next((i for i, p in enumerate(presupuestos) if p['id_circuito'] == c_id), None)
    
    new_acts = []
    for a in acts:
        new_acts.append({
            "id_actividad": a['id'],
            "cantidad_total": a['cant'],
            "valor_total_esperado": a['val']
        })
        
    if p_idx is not None:
        presupuestos[p_idx]['actividades_programadas'] = new_acts
    else:
        presupuestos.append({
            "id_circuito": c_id,
            "meta_financiera_total": sum(a['val'] for a in acts),
            "actividades_programadas": new_acts
        })

save_json('metas_fisicas.json', metas_fisicas)
save_json('presupuestos_y_cronograma_base.json', presupuestos)
print("Finished processing all budgets.")
