import json

new_data_frontino = {
    "CONSTRUCCIÓN DE ALCANTARILLAS": {
        "entregable": "102 un",
        "actividades": {
            "2.8": 9.0,
            "2.14.1": 12.0,
            "4.1.8": 3468.0,
            "4.2.2": 1122.0,
            "5.1.7": 408.0,
            "6.2.4": 102.0,
            "6.2.24": 899.0,
            "8.1": 876.0,
            "8.27": 612.0,
            "10.1": 49368.0,
            "13.1": 45696.0
        }
    },
    "CONSTRUCCIÓN DE CUNETA": {
        "entregable": "25,000 m",
        "actividades": {
            "4.1.8": 4345.0,
            "5.1.7": 2000.0,
            "6.2.50": 2500.0,
            "10.1": 70002.0,
            "13.1": 224000.0
        }
    },
    "CONSTRUCCIÓN DE FILTRO PARA CUNETAS": {
        "entregable": "25,000 m",
        "actividades": {
            "8.13.1": 25000.0,
            "13.9": 1008000.0
        }
    },
    "CONSTRUCCIÓN DE BORDILLOS": {
        "entregable": "5,000 m",
        "actividades": {
            "4.1.2": 400.0,
            "5.1.7": 100.0,
            "14.3": 5000.0
        }
    },
    "CONSTRUCCIÓN DE DISIPADORES": {
        "entregable": "77 Un",
        "actividades": {
            "4.1.9": 180.0,
            "6.1.18.1": 539.0,
            "8.18": 462.0,
            "10.1": 2616.0
        }
    },
    "ESTABILIZACION CON MATERIAL GRANULAR": {
        "entregable": "25 Km",
        "actividades": {
            "4.1.1": 2625.0,
            "5.1.2": 2625.0,
            "5.2.16": 35000.0,
            "5.2.13": 6500.0,
            "4.1.96": 4225.0,
            "4.3.8": 4225.0,
            "5.1.15": 16376.0,
            "7.1.1": 125000.0,
            "7.1.12.2": 125000.0,
            "13.1": 4487700.0,
            "13.2": 259875.0
        }
    },
    "SEÑALIZACIÓN VIAL": {
        "entregable": "25 Km",
        "actividades": {
            "12.1": 75000.0,
            "12.9": 125.0
        }
    }
}

with open('actividades.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

for circuito in data.get('circuitos', []):
    if circuito['nombre'] == "VIA FRONTINO - NUTIBARA":
        for cat in circuito.get('categorias', []):
            cat_name = cat['nombre']
            if cat_name in new_data_frontino:
                cat['entregable'] = new_data_frontino[cat_name]['entregable']
                
                # Update actividades
                for act in cat.get('actividades', []):
                    item = act['item']
                    if item in new_data_frontino[cat_name]['actividades']:
                        act['cantidad_inicial'] = new_data_frontino[cat_name]['actividades'][item]

with open('actividades.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print("Updated FRONTINO - NUTIBARA successfully.")
