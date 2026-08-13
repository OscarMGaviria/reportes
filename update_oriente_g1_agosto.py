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
    name = name.lower().replace('á', 'a').replace('é', 'e').replace('í', 'i').replace('ó', 'o').replace('ú', 'u')
    for c in oriente['circuitos']:
        c_name = c['corredor_vial'].lower().replace('á', 'a').replace('é', 'e').replace('í', 'i').replace('ó', 'o').replace('ú', 'u')
        if name in c_name:
            return c
        # fallback for el peñol mapping
        if 'vicente' in name and 'vicente' in c_name:
            return c
    return None

def update_corte(corredor_name, acts, obs, insumos=[]):
    c = find_circuit(corredor_name)
    if not c:
        print(f"No se encontró circuito {corredor_name}")
        return

    # Buscar corte para 8/6/2026
    corte = next((co for co in c['cortes_semanales'] if co['fecha_corte'] == "2026-08-06"), None)
    if not corte:
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


# Datos SAN VICENTE - EL PEÑOL
sv_acts = [
    {"nombre": "Topografía", "unidad": "km", "total": 18.15, "completado": 3.50},
    {"nombre": "Exploración Geotécnica", "unidad": "km", "total": 12.70, "completado": 12.70},
    {"nombre": "Mantenimiento de Obras Transversales", "unidad": "und", "total": 91, "completado": 7},
    {"nombre": "Construcción de filtros", "unidad": "km", "total": 12.70, "completado": 0},
    {"nombre": "Construcción de Cuneta", "unidad": "km", "total": 12.70, "completado": 0},
    {"nombre": "Conformación y adecuación", "unidad": "km", "total": 12.70, "completado": 0}
]

sv_insumos = [
    {"nombre": "Perfil Topográfico del tramo (K15+138 - K18+150)", "responsable": "CONTRATISTA", "fecha_presentacion": "jueves, julio 23, 2026", "estado_observacion": ""},
    {"nombre": "Estudios de tránsito", "responsable": "SIF", "fecha_presentacion": "jueves, junio 11, 2026", "estado_observacion": ""},
    {"nombre": "Presentación diseño estructura (K15+138 - K18+150)", "responsable": "CONTRATISTA", "fecha_presentacion": "", "estado_observacion": ""},
    {"nombre": "Aprobación diseño de estructura (K15+138 - K18+150)", "responsable": "SIF", "fecha_presentacion": "", "estado_observacion": ""},
    {"nombre": "Complemento Aprobación diseño de estructura (K15+138 - K18+150)", "responsable": "SIF", "fecha_presentacion": "", "estado_observacion": ""}
]

sv_obs = "Se ha iniciado la rocería del tramo que se estabilizará inicialmente. Esta actividad es ejecutada por RENTAN. Se inició por el K0+000 en jurisdicción del municipio de SanVicente por lo que se les solicitó arrancar desde el Peñol. El levantamiento topográfico de la vía quedó suspendido hasta la abscisa K15+138, dado que la Alcaldía Municipal de San Vicente se encuentra realizando ampliación y corte de taludes desde el K5+700 hasta el K15+000 aproximadamente. El tramo vial para estabilizar tiene una longitud aproximada de 12,7 km, dado que se tienen 5.4 km en pavimento flexible dentro de este corredor.\nNOTA: El Contratista entregó a Interventoría resultado de ensayos y diseño de los primeros tres kilómetros (K18+150 - K15+138). Se estima que la proxima semana se realice reunión entre diseñadores."

update_corte("san vicente", sv_acts, sv_obs, sv_insumos)


# Datos Guarne - Yolombal
gy_acts = [
    {"nombre": "Topografía", "unidad": "km", "total": 5.0, "completado": 2.5},
    {"nombre": "Exploración Geotécnica", "unidad": "km", "total": 5.0, "completado": 5.0},
    {"nombre": "Mantenimiento de Obras Transversales", "unidad": "und", "total": 42, "completado": 0},
    {"nombre": "Construcción de filtros", "unidad": "km", "total": 5.0, "completado": 0},
    {"nombre": "Construcción de Cuneta", "unidad": "km", "total": 5.0, "completado": 0},
    {"nombre": "Conformación y adecuación", "unidad": "km", "total": 5.0, "completado": 0}
]

gy_obs = "NOTA: Finalizaron los apiques, toma de muestras y ensayos PDC en este corredor. Se esta pendiente de resultados de laboratorio por parte de EVALTEC."

update_corte("guarne", gy_acts, gy_obs, [])


# Datos San Rafael - San Roque...
sr_acts = [
    {"nombre": "Topografía", "unidad": "km", "total": 2.26, "completado": 0},
    {"nombre": "Exploración Geotécnica", "unidad": "km", "total": 2.26, "completado": 2.26},
    {"nombre": "Mantenimiento de Obras Transversales", "unidad": "und", "total": 11, "completado": 0},
    {"nombre": "Construcción de filtros", "unidad": "km", "total": 2.26, "completado": 0},
    {"nombre": "Construcción de Cuneta", "unidad": "km", "total": 2.26, "completado": 0},
    {"nombre": "Conformación y adecuación", "unidad": "km", "total": 2.26, "completado": 0}
]

sr_obs = "NOTA: Finalizaron los apiques, toma de muestras y ensayos PDC en este corredor. Se esta pendiente de resultados de laboratorio por parte de EVALTEC."

update_corte("san rafael", sr_acts, sr_obs, [])


with open(db_path, 'w', encoding='utf-8') as f:
    json.dump(db, f, indent=2, ensure_ascii=False)

print("Datos de ORIENTE GRUPO 1 AGOSTO actualizados exitosamente.")
