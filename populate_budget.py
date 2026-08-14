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

circuitos = load_json('circuitos_maestros.json')
presupuestos = load_json('presupuestos_y_cronograma_base.json')
catalogo = load_json('catalogo_actividades.json')

# 1. Definir los 5 circuitos del Lote 2 - Occidente
nuevos_circuitos = [
    {"id_circuito": 101, "corredor_vial": "Miserenga - Ebejico"},
    {"id_circuito": 102, "corredor_vial": "Frontino - Nutibara"},
    {"id_circuito": 103, "corredor_vial": "Ebejico - Heliconia - Medellin"},
    {"id_circuito": 104, "corredor_vial": "Titiribi - Armenia"},
    {"id_circuito": 105, "corredor_vial": "Sopetran - Belmira - Horizontes"}
]

# Filtrar circuitos existentes de Occidente para reemplazarlos con la verdad del contrato
circuitos = [c for c in circuitos if c.get('id_subregion') != 'OCC']

for nc in nuevos_circuitos:
    circuitos.append({
        "id_circuito": nc['id_circuito'],
        "id_subregion": "OCC",
        "corredor_vial": nc['corredor_vial'],
        "municipio": "VARIOS",
        "contrato": {
            "contratista": "CONSORCIO LOTE 2 OCCIDENTE",
            "numero_contrato": "POR DEFINIR",
            "valor_total": 104855613958, # El global aplica para todo el lote
            "fecha_inicio": "",
            "fecha_fin": ""
        }
    })

# 2. Configurar presupuestos base
macro_data = {
    101: {"PMA": 33016917, "PMT": 61822034, "CARAC": 1055961},
    102: {"PMA": 232478312, "PMT": 236983041, "CARAC": 26399025},
    103: {"PMA": 243833071, "PMT": 209492241, "CARAC": 30369438},
    104: {"PMA": 110835670, "PMT": 132518461, "CARAC": 5279805},
    105: {"PMA": 304537083, "PMT": 291964641, "CARAC": 37159268}
}

macro_ids = {
    "PMA": {"id": "MACRO-PMA", "desc": "PLAN DE MANEJO AMBIENTAL, SOCIAL Y SST"},
    "PMT": {"id": "MACRO-PMT", "desc": "PLAN DE MANEJO DE TRANSITO (PMT)"},
    "CARAC": {"id": "MACRO-CARAC", "desc": "CARACTERIZACION VIAL"}
}

for m_key, m_val in macro_ids.items():
    if not any(c['id_actividad'] == m_val['id'] for c in catalogo):
        catalogo.append({
            "id_actividad": m_val['id'],
            "categoria": "GENERAL",
            "descripcion": m_val['desc'],
            "unidad": "Estimado" if m_key != "CARAC" else "Km",
            "valor_unitario": 0 
        })

for circ_id, m_vals in macro_data.items():
    presupuestos = [p for p in presupuestos if p['id_circuito'] != circ_id]
    
    act_prog = [
        {"id_actividad": macro_ids['PMA']['id'], "cantidad_total": 1, "valor_total_esperado": m_vals['PMA']},
        {"id_actividad": macro_ids['PMT']['id'], "cantidad_total": 1, "valor_total_esperado": m_vals['PMT']},
        {"id_actividad": macro_ids['CARAC']['id'], "cantidad_total": 1 if circ_id==101 else (25 if circ_id==102 else (28.76 if circ_id==103 else (5 if circ_id==104 else 35.19))), "valor_total_esperado": m_vals['CARAC']}
    ]
    
    if circ_id == 101:
        acts_miserenga = [
            {"id": "2.8", "desc": "Demolición de estructuras (Concreto reforzado)", "und": "m3", "cant": 24.0, "vu": 230711.0, "vt": 5537064.0, "cat": "CONSTRUCCIÓN DE ALCANTARILLAS"},
            {"id": "2.14.1", "desc": "Retiro de tubería existente de 36, sin excavación", "und": "m", "cant": 30.0, "vu": 60377.0, "vt": 1811310.0, "cat": "CONSTRUCCIÓN DE ALCANTARILLAS"},
            {"id": "4.1.8", "desc": "Excavación para estructuras varias en material común en seco", "und": "m3", "cant": 204.0, "vu": 54161.0, "vt": 11048844.0, "cat": "CONSTRUCCIÓN DE ALCANTARILLAS"},
            {"id": "4.2.2", "desc": "Lleno manual compactado con material proveniente de la excavación", "und": "m3", "cant": 66.0, "vu": 32553.0, "vt": 2148498.0, "cat": "CONSTRUCCIÓN DE ALCANTARILLAS"},
            {"id": "5.1.7", "desc": "Suministro, colocación y compactación de subbase granular", "und": "m3", "cant": 24.0, "vu": 108602.0, "vt": 2606448.0, "cat": "CONSTRUCCIÓN DE ALCANTARILLAS"},
            {"id": "6.2.4", "desc": "Concreto Clase E (17.5 MPa). Elementos varios.", "und": "m3", "cant": 6.0, "vu": 841878.0, "vt": 5051268.0, "cat": "CONSTRUCCIÓN DE ALCANTARILLAS"},
            {"id": "6.2.24", "desc": "Suministro, transporte y colocación de Concreto Clase C (28 MPa)", "und": "m3", "cant": 53.0, "vu": 1239676.0, "vt": 65702828.0, "cat": "CONSTRUCCIÓN DE ALCANTARILLAS"}
        ]
        
        for a in acts_miserenga:
            if not any(c['id_actividad'] == a['id'] for c in catalogo):
                catalogo.append({
                    "id_actividad": a['id'],
                    "categoria": a['cat'],
                    "descripcion": a['desc'],
                    "unidad": a['und'],
                    "valor_unitario": a['vu']
                })
            act_prog.append({
                "id_actividad": a['id'],
                "cantidad_total": a['cant'],
                "valor_total_esperado": a['vt']
            })

    presupuestos.append({
        "id_circuito": circ_id,
        "meta_financiera_total": sum(a['valor_total_esperado'] for a in act_prog),
        "actividades_programadas": act_prog
    })

save_json('circuitos_maestros.json', circuitos)
save_json('presupuestos_y_cronograma_base.json', presupuestos)
save_json('catalogo_actividades.json', catalogo)

print("Datos macro y POC Miserenga-Ebejico importados con éxito.")
