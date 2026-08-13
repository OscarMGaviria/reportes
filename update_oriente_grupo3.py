import json
import os

db_path = os.path.join('src', 'data', 'db.json')
with open(db_path, 'r', encoding='utf-8') as f:
    db = json.load(f)

# Find Oriente
oriente = next((s for s in db['subregiones'] if s['nombre'] == 'ORIENTE'), None)
if not oriente:
    print("No se encontró ORIENTE")
    exit(1)

def find_circuit(name):
    # Try to find by exact or partial match due to encoding
    name = name.lower().replace('á', 'a').replace('é', 'e').replace('í', 'i').replace('ó', 'o').replace('ú', 'u')
    for c in oriente['circuitos']:
        c_name = c['corredor_vial'].lower().replace('á', 'a').replace('é', 'e').replace('í', 'i').replace('ó', 'o').replace('ú', 'u')
        if name in c_name:
            return c
    return None

def update_corte(corredor_name, acts, obs, insumos=[]):
    c = find_circuit(corredor_name)
    if not c:
        print(f"No se encontró circuito {corredor_name}")
        return

    # Buscar corte para 7/24/2026 (2026-07-24)
    corte = next((co for co in c['cortes_semanales'] if co['fecha_corte'] == "2026-07-24"), None)
    if not corte:
        max_semana = max([co['semana'] for co in c['cortes_semanales']] + [0])
        corte = {
            "semana": max_semana + 1,
            "fecha_corte": "2026-07-24",
            "financiero": {
                "anticipo": {"valor": 0, "porcentaje": 0},
                "programado": {"valor": 0, "porcentaje": 0},
                "ejecutado": {"valor": 0, "porcentaje": 0},
                "avance": {"valor": 0, "porcentaje": 0},
                "estado": "En ejecución"
            },
            "fisico": {
                "programado": 0,
                "ejecutado": 0,
                "avance": 0,
                "estado": "En ejecución"
            },
            "actividades_ejecutadas": [],
            "insumos": [],
            "imagenes": [],
            "observaciones_tecnicas": []
        }
        c['cortes_semanales'].append(corte)

    # Actualizar actividades
    for a in acts:
        # buscar si ya existe
        act_exist = next((ac for ac in corte['actividades_ejecutadas'] if ac['nombre'] == a['nombre']), None)
        if act_exist:
            act_exist['completado'] = a['completado']
            act_exist['total'] = a['total']
            act_exist['unidad'] = a['unidad']
        else:
            corte['actividades_ejecutadas'].append(a)

    # Actualizar insumos
    for ins in insumos:
        ins_exist = next((i for i in corte['insumos'] if i['nombre'] == ins['nombre']), None)
        if ins_exist:
            ins_exist['fecha_presentacion'] = ins['fecha_presentacion']
            ins_exist['responsable'] = ins['responsable']
        else:
            corte['insumos'].append(ins)

    # Actualizar observaciones
    if obs and obs not in corte['observaciones_tecnicas']:
        corte['observaciones_tecnicas'].append(obs)


# Datos SONSÓN - AGUADAS
sa_acts = [
    {"nombre": "Topografía", "unidad": "km", "total": 19.22, "completado": 3.3},
    {"nombre": "Exploración Geotécnica", "unidad": "und", "total": 77, "completado": 41},
    {"nombre": "Limpieza de Obras Transversales", "unidad": "und", "total": 150, "completado": 54},
    {"nombre": "Construcción de filtros", "unidad": "km", "total": 19.22, "completado": 0},
    {"nombre": "Construcción de Cuneta", "unidad": "km", "total": 19.22, "completado": 0},
    {"nombre": "Conformación y adecuación", "unidad": "km", "total": 19.22, "completado": 0}
]

sa_insumos = [
    {"nombre": "Perfil Topográfico (Longitudinal y Transversal) del Tramo Sonsón - Aguadas (19.22 Km)", "responsable": "CONTRATISTA", "fecha_presentacion": "julio 28 de 2026 tramo inicial de 2 km", "estado_observacion": ""},
    {"nombre": "Estudios de tránsito", "responsable": "SIF", "fecha_presentacion": "junio 16 de 2026 Entrega final ajustada de los Certificados de TPD y Ejes Equivalentes definitivos", "estado_observacion": ""},
    {"nombre": "Presentación diseño estructura (Hasta K1+850)", "responsable": "CONTRATISTA", "fecha_presentacion": "", "estado_observacion": ""},
    {"nombre": "Aprobación diseño de estructura (Hasta k1+850)", "responsable": "SIF", "fecha_presentacion": "", "estado_observacion": ""},
    {"nombre": "Complemento Aprobación diseño de estructura (Hasta k1+850)", "responsable": "SIF", "fecha_presentacion": "", "estado_observacion": ""}
]

sa_obs = "Hasta el momento no se cuenta con diseños entregados por parte del Contratista. Se requiere que el contratista presente información de apiques y topografía y con ello avanzar en el diseño y fórmula de trabajo."

update_corte("sonson - aguadas", sa_acts, sa_obs, sa_insumos)

# Datos LA QUIEBRA - SANTA ANA
lq_sa_acts = [
    {"nombre": "Topografía", "unidad": "km", "total": 5.33, "completado": 0},
    {"nombre": "Exploración Geotécnica", "unidad": "und", "total": 22, "completado": 0},
    {"nombre": "Limpieza de Obras Transversales", "unidad": "und", "total": 204, "completado": 0},
    {"nombre": "Construcción de filtros", "unidad": "km", "total": 5.33, "completado": 0},
    {"nombre": "Construcción de Cuneta", "unidad": "km", "total": 5.33, "completado": 0},
    {"nombre": "Conformación y adecuación", "unidad": "km", "total": 5.33, "completado": 0}
]

lq_sa_obs = "NOTA: el Constructor anunció que la próxima semana iniciara con topografía y apiques en esta vía"

update_corte("la quiebra - santa ana", lq_sa_acts, lq_sa_obs, [])

with open(db_path, 'w', encoding='utf-8') as f:
    json.dump(db, f, indent=2, ensure_ascii=False)

print("Datos de ORIENTE GRUPO 3 actualizados exitosamente.")
