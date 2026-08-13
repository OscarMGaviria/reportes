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
    for c in oriente['circuitos']:
        if name.lower() in c['corredor_vial'].lower():
            return c
    return None

def update_corte(corredor_name, acts, obs, insumos=[]):
    c = find_circuit(corredor_name)
    if not c:
        print(f"No se encontró circuito {corredor_name}")
        return

    # Buscar corte con fecha más reciente o crear uno para 8/6/2026
    corte = next((co for co in c['cortes_semanales'] if co['fecha_corte'] == "2026-08-06"), None)
    if not corte:
        # Get max semana
        max_semana = max([co['semana'] for co in c['cortes_semanales']] + [0])
        corte = {
            "semana": max_semana + 1,
            "fecha_corte": "2026-08-06",
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


# Datos ABEJORRAL - SANTA BARBARA
ab_sb_acts = [
    {"nombre": "Topografía", "unidad": "km", "total": 23.77, "completado": 10.00},
    {"nombre": "Exploración Geotécnica", "unidad": "und", "total": 98, "completado": 96},
    {"nombre": "Mantenimiento de Obras Transversales", "unidad": "und", "total": 115, "completado": 80},
    {"nombre": "Construcción de filtros", "unidad": "km", "total": 23.77, "completado": 0},
    {"nombre": "Construcción de Cuneta", "unidad": "km", "total": 23.77, "completado": 0},
    {"nombre": "Conformación y adecuación", "unidad": "km", "total": 23.77, "completado": 0}
]

ab_sb_insumos = [
    {"nombre": "Perfil Topográfico (Longitudinal y Transversal)", "responsable": "CONTRATISTA", "fecha_presentacion": "julio 28 de 2026 tramo inicial de 5 km", "estado_observacion": ""},
    {"nombre": "Estudios de tránsito", "responsable": "EN TRAMITE", "fecha_presentacion": "junio 16 de 2026 Entrega final ajustada de los Certificados de TPD y Ejes Equivalentes definitivos", "estado_observacion": ""},
    {"nombre": "Presentación diseño estructura", "responsable": "EN TRAMITE", "fecha_presentacion": "julio 28 de 2026 tramo inicial de 5 km", "estado_observacion": ""},
    {"nombre": "Aprobación diseño de estructura", "responsable": "EN TRAMITE", "fecha_presentacion": "EN PROCESO", "estado_observacion": ""},
    {"nombre": "Complemento Aprobación diseño de estructura", "responsable": "N.A", "fecha_presentacion": "N.A", "estado_observacion": ""}
]

ab_sb_obs = "Se cuenta con diseño de estructura en proceso de aprobación y diseño de perfil de via de los primeros 3 kilometros desde el K0+00 hasta el k3+00. De la reunión general (comité de seguiminento del 28 de julio de 2026 que contó con la participación de Gobernación, Rentan, Contractor e Interventor y sus correspondientes asesores) la Gobernación solicitó expresamente que los asesores de las tres partes revisaran los diseños con el ánimo de establecer unidad en conclusiones sobre metodología, analisis de resultados y espesores de los tramos presentados por diseñador del constructor.\nA la fecha el contratista ha adelantado actividades en topografia y limpieza de obras transversales. Está listo apra el inicio de ejecución de actividades constructivas, lascuales dependen del PMT, PMA, definición de rasante y diseño"

update_corte("Abejorral - Santa Barbara", ab_sb_acts, ab_sb_obs, ab_sb_insumos)

# Datos LA FRONTERA - ABEJORRAL
lf_ab_acts = [
    {"nombre": "Topografía", "unidad": "km", "total": 25.49, "completado": 10.00},
    {"nombre": "Exploración Geotécnica", "unidad": "und", "total": 98, "completado": 96},
    {"nombre": "Limpieza de Obras Transversales", "unidad": "und", "total": 21, "completado": 18},
    {"nombre": "Construcción de filtros", "unidad": "km", "total": 25.49, "completado": 0},
    {"nombre": "Construcción de Cuneta", "unidad": "km", "total": 25.49, "completado": 0},
    {"nombre": "Conformación y adecuación", "unidad": "km", "total": 25.49, "completado": 0}
]

lf_ab_obs = "A la fecha el contratista no ha presentado diseño topografico de via existente del tramo LA FRONTERA -ABEJORRAL.\nNOTA: después de la entrega de los resultados de ensayos de los 10 km iniciales, el cosntructor prepara la entrega del diseño de la estructura de soporte, a la fecha este no se ha presentado."

update_corte("Abejorral - La Frontera", lf_ab_acts, lf_ab_obs, [])

with open(db_path, 'w', encoding='utf-8') as f:
    json.dump(db, f, indent=2, ensure_ascii=False)

print("Datos de ORIENTE GRUPO 2 actualizados exitosamente.")
