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

page_2_acts = [
    # CONSTRUCCIÓN DE BORDILLOS
    {"id": "4.1.2", "desc": "Excavación manual en material común. Incluye cargue, transporte y disposición final del material sobrante.", "und": "m3", "cant": 16.00, "vu": 52282.00, "vt": 836512.00, "cat": "CONSTRUCCIÓN DE BORDILLOS"},
    {"id": "5.1.7_2", "desc": "Suministro, colocación y compactación de subbase granular para cimentación de tubería y lleno de zanjas, no incluye transporte. Compactación hasta obtener una densidad mínima del 95%, de la obtenida en el ensayo del Proctor modificado.", "und": "m3", "cant": 4.00, "vu": 108602.00, "vt": 434408.00, "cat": "CONSTRUCCIÓN DE BORDILLOS"},
    {"id": "14.3", "desc": "Suministro, transporte e instalación de Bordillo barrera recto 15x35x80 prefabricado para pompeyanos, rebajes, entre otros", "und": "m", "cant": 200.00, "vu": 115109.00, "vt": 23021800.00, "cat": "CONSTRUCCIÓN DE BORDILLOS"},
    
    # CONSTRUCCIÓN DE DISIPADORES
    {"id": "4.1.9", "desc": "Excavación para estructuras varias en material común en seco sin entibado. Incluye transporte y disposición final de los materiales.", "und": "m3", "cant": 180.00, "vu": 33663.00, "vt": 6019540.00, "cat": "CONSTRUCCIÓN DE DISIPADORES"},
    {"id": "6.1.18.1", "desc": "Concreto Clase F (14 MPa). Solados de E=0.05 m", "und": "m2", "cant": 35.00, "vu": 41173.00, "vt": 1441055.00, "cat": "CONSTRUCCIÓN DE DISIPADORES"},
    {"id": "8.18", "desc": "Disipadores de energía y sedimentador en Concreto Clase H (Ciclópeo con concreto clase D - 21 MPa)", "und": "m3", "cant": 30.00, "vu": 1019967.00, "vt": 30599010.00, "cat": "CONSTRUCCIÓN DE DISIPADORES"},
    {"id": "10.1", "desc": "Suministro, transporte y colocación de Acero de refuerzo fy=420 Mpa (Grado 60)", "und": "kg", "cant": 170.00, "vu": 9487.00, "vt": 1612790.00, "cat": "CONSTRUCCIÓN DE DISIPADORES"},
    
    # ESTABILIZACION CON MATERIAL GRANULAR
    {"id": "4.1.1", "desc": "Excavación en material común de la explanación, canales y préstamos. Incluye cargue y disposición final del material sobrante. No incluye transporte.", "und": "m3", "cant": 105.00, "vu": 18728.00, "vt": 1966440.00, "cat": "ESTABILIZACION CON MATERIAL GRANULAR"},
    {"id": "5.1.2", "desc": "Suministro, colocación, conformación y compactación de afirmado para Bacheo, no incluye transporte. Compactación hasta obtener una densidad mínima del 95%, de la obtenida en el ensayo del Proctor modificado.", "und": "m3", "cant": 105.00, "vu": 162146.00, "vt": 17025330.00, "cat": "ESTABILIZACION CON MATERIAL GRANULAR"},
    {"id": "5.2.16", "desc": "Proceso de estabilización con material granular y cemento. Incluye colocación y compactación de la mezcla con cemento y todo lo necesario para su correcta instalación. No incluye suministro del cemento.", "und": "m3", "cant": 1400.00, "vu": 59266.00, "vt": 82972400.00, "cat": "ESTABILIZACION CON MATERIAL GRANULAR"},
    {"id": "5.2.13", "desc": "Proceso de estabilización de material granular y cal. Incluye suministro, colocación y compactación de material granular. No incluye el suministro de la cal.", "und": "m3", "cant": 260.00, "vu": 54742.00, "vt": 14232920.00, "cat": "ESTABILIZACION CON MATERIAL GRANULAR"},
    {"id": "4.1.95", "desc": "Excavación en material común de la explanación con motoniveladora. Incluye cargue y transporte del material al sitio de acopio especificado.", "und": "m3", "cant": 208.00, "vu": 27866.00, "vt": 5796128.00, "cat": "ESTABILIZACION CON MATERIAL GRANULAR"},
    {"id": "4.3.8", "desc": "Disposición de material para conformación de la calzada, incluye transporte descargue y regado del material. No incluye compactación ni material para la conformación.", "und": "m3", "cant": 208.00, "vu": 11049.00, "vt": 2298192.00, "cat": "ESTABILIZACION CON MATERIAL GRANULAR"},
    {"id": "5.1.15", "desc": "Suministro de sub base granular, medido suelto. No incluye nivelación, compactación, limpieza ni transporte del material, los cuales serán pagados en su respectivo ítem.", "und": "m3", "cant": 640.00, "vu": 115826.00, "vt": 74128640.00, "cat": "ESTABILIZACION CON MATERIAL GRANULAR"},
    {"id": "7.1.1", "desc": "Suministro, transporte y aplicación de emulsión asfáltica catiónica de rompimiento lento C.R.L. para imprimación de superficie a pavimentar según normas para la construcción de pavimentos del INVIAS 420-22. Incluye todo lo necesario para su correcta construcción y funcionamiento. Incluye recuperación de superficie y riego inicial con carrotanque.", "und": "m2", "cant": 5000.00, "vu": 5399.00, "vt": 26995000.00, "cat": "ESTABILIZACION CON MATERIAL GRANULAR"},
    {"id": "7.1.12.2", "desc": "Tratamiento superficial doble con emulsión CRR-2M. No incluye transporte.", "und": "m2", "cant": 5000.00, "vu": 22788.00, "vt": 113940000.00, "cat": "ESTABILIZACION CON MATERIAL GRANULAR"},
    {"id": "13.1_2", "desc": "Transporte de materiales de afirmado, sub-base, base y mezcla asfáltica para distancias superiores a 1000 m medidos a partir de 100 m. Material compacto (Incluye 30% de expansión).", "und": "m3-Km", "cant": 86549.50, "vu": 2033.00, "vt": 175953101.00, "cat": "ESTABILIZACION CON MATERIAL GRANULAR"},
    {"id": "13.2", "desc": "Transporte de sobrantes provenientes de la excavación, canales, préstamos para distancias superiores a 1000 m medidos a partir de 100 m. Material compacto (Incluye 30% de expansión).", "und": "m3-Km", "cant": 1575.00, "vu": 2033.00, "vt": 3201975.00, "cat": "ESTABILIZACION CON MATERIAL GRANULAR"},
    
    # SEÑALIZACIÓN VIAL
    {"id": "12.1", "desc": "Suministro, transporte y aplicación con pintura acrílica en frío reflectorizada con microesferas de vidrio para línea de demarcación en pavimento.", "und": "m", "cant": 3000.00, "vu": 3444.00, "vt": 10332000.00, "cat": "SEÑALIZACIÓN VIAL"},
    {"id": "12.9", "desc": "Suministro, transporte e instalación de señal vertical de 75cmx75cm doble (SP/SR/SI), en lámina galvanizada calibre 16, reflectivo tipo IX, estructura metálica tipo pedestal compuesto por un paral en ángulo de 2\"x2\"x1/4\" y brazos en ángulo 2\"x2\"x1/8\"", "und": "Und", "cant": 5.00, "vu": 870445.00, "vt": 4352225.00, "cat": "SEÑALIZACIÓN VIAL"}
]

for a in page_2_acts:
    if not any(c['id_actividad'] == a['id'] for c in catalogo):
        catalogo.append({
            "id_actividad": a['id'],
            "categoria": a['cat'],
            "descripcion": a['desc'],
            "unidad": a['und'],
            "valor_unitario": a['vu']
        })

for p in presupuestos:
    if p['id_circuito'] == 101: # Miserenga - Ebejico
        for a in page_2_acts:
            # check if exists
            if not any(act['id_actividad'] == a['id'] for act in p['actividades_programadas']):
                p['actividades_programadas'].append({
                    "id_actividad": a['id'],
                    "cantidad_total": a['cant'],
                    "valor_total_esperado": a['vt']
                })
        
        # update total
        p['meta_financiera_total'] = sum(a['valor_total_esperado'] for a in p['actividades_programadas'])

save_json('presupuestos_y_cronograma_base.json', presupuestos)
save_json('catalogo_actividades.json', catalogo)

print("Página 2 inyectada con éxito para Miserenga-Ebejico.")
