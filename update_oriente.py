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
        if 'Pe' in name and 'Pe' in c['corredor_vial'] and 'San Vicente' in c['corredor_vial']:
            return c
        if 'Alejandr' in name and 'Alejandr' in c['corredor_vial']:
            return c
    return None

def update_corte(corredor_name, acts, obs, insumos=[]):
    c = find_circuit(corredor_name)
    if not c:
        print(f"No se encontró circuito {corredor_name}")
        return

    # Buscar corte semana 1 o crear
    corte = next((co for co in c['cortes_semanales'] if co['semana'] == 1), None)
    if not corte:
        corte = {
            "semana": 1,
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

    # Actualizar fecha y datos
    corte["fecha_corte"] = "2026-07-24"

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


# Datos San Vicente - El Peñol
sv_acts = [
    {"nombre": "Topografía", "unidad": "km", "total": 12.5, "completado": 4.0},
    {"nombre": "Exploración Geotécnica", "unidad": "km", "total": 12.5, "completado": 12.5},
    {"nombre": "Limpieza de Obras Transversales", "unidad": "und", "total": 91, "completado": 5},
    {"nombre": "Construcción de filtros", "unidad": "km", "total": 12.5, "completado": 0},
    {"nombre": "Construcción de Cuneta", "unidad": "km", "total": 12.5, "completado": 0},
    {"nombre": "Conformación y adecuación", "unidad": "km", "total": 12.5, "completado": 0}
]

sv_insumos = [
    {"nombre": "Perfil Topográfico del tramo (K15+138 - K18+150)", "responsable": "CONTRATISTA", "fecha_presentacion": "jueves, julio 23, 2026", "estado_observacion": ""},
    {"nombre": "Estudios de tránsito", "responsable": "SIF", "fecha_presentacion": "junio 16 de 2026 Entrega final ajustada de los Certificados de TPD y Ejes Equivalentes definitivos", "estado_observacion": ""},
    {"nombre": "Presentación diseño estructura (K15+138 - K18+150)", "responsable": "CONTRATISTA", "fecha_presentacion": "Contructor prepara entrga a Interventoría de resultados de laboratorio y diseño inicial para julio 24 de 2026", "estado_observacion": ""}
]

sv_obs = "El desarrollo de las actividades dentro del corredor se ejecutarán en sentido El Peñol hacia San Vicente, dado que el tramo inicial a estabilizar (K15+138 - K18+150) está en jurisdicción de El Peñol. Aún no se ha iniciado la rocería del tramo que se va a estabilizar inicialmente. Quedó definido que esta actividad será ejecutada por RENTAN y está por iniciar. El levantamiento topográfico avanzó de abscisa final a menores hasta la abscisa K15+138, dado que se evidencia la ampliación y corte de taludes desde el K5+700 hasta el K15+000 aproximadamente. A la fecha estas labores continúan en ejecución con permanencia de material depositado en márgenes de la vía. Situación reportada por el Contructor quien está atento a que se le haga entrega del tramo para avanzar con actividades de topografía, inventario, limpieza y mantenimiento de obras transversales. El tramo vial para estabilizar tiene una longitud aproximada de 12,5 km, dado que se tienen 5,4 km en pavimento flexible dentro de este corredor."

update_corte("San Vicente - El", sv_acts, sv_obs, sv_insumos)

# Datos Guarne - Yolombal
gy_acts = [
    {"nombre": "Topografía", "unidad": "km", "total": 5.0, "completado": 0},
    {"nombre": "Exploración Geotécnica", "unidad": "km", "total": 5.0, "completado": 1.0},
    {"nombre": "Limpieza de Obras Transversales", "unidad": "und", "total": 42, "completado": 0},
    {"nombre": "Construcción de filtros", "unidad": "km", "total": 5.0, "completado": 0},
    {"nombre": "Construcción de Cuneta", "unidad": "km", "total": 5.0, "completado": 0},
    {"nombre": "Conformación y adecuación", "unidad": "km", "total": 5.0, "completado": 0}
]
update_corte("Guarne - Yolombal", gy_acts, None, [])

# Datos San Rafael - San Roque...
sr_acts = [
    {"nombre": "Topografía", "unidad": "km", "total": 2.26, "completado": 0},
    {"nombre": "Exploración Geotécnica", "unidad": "km", "total": 2.26, "completado": 0},
    {"nombre": "Limpieza de Obras Transversales", "unidad": "und", "total": 11, "completado": 0},
    {"nombre": "Construcción de filtros", "unidad": "km", "total": 2.26, "completado": 0},
    {"nombre": "Construcción de Cuneta", "unidad": "km", "total": 2.26, "completado": 0},
    {"nombre": "Conformación y adecuación", "unidad": "km", "total": 2.26, "completado": 0}
]
update_corte("San Rafael - San Roque", sr_acts, None, [])

with open(db_path, 'w', encoding='utf-8') as f:
    json.dump(db, f, indent=2, ensure_ascii=False)

print("Datos de ORIENTE actualizados exitosamente.")
