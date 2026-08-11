import json
import copy

new_data = {
    "CONSTRUCCIÓN DE ALCANTARILLAS": {
        "entregable": "10 un",
        "actividades": {
            "2.8": 24.0,
            "2.14.1": 30.0,
            "4.1.8": 340.0,
            "4.2.2": 110.0,
            "5.1.7": 40.0,
            "6.2.4": 10.0,
            "6.2.24": 88.0,
            "8.1": 48.0,
            "8.27": 60.0,
            "10.1": 4840.0,
            "13.1": 2160.0
        }
    },
    "CONSTRUCCIÓN DE CUNETA": {
        "entregable": "1,000 m",
        "actividades": {
            "4.1.8": 174.0,
            "5.1.7": 80.0,
            "6.2.50": 100.0,
            "10.1": 2802.0,
            "13.1": 4320.0
        }
    },
    "CONSTRUCCIÓN DE FILTRO PARA CUNETAS": {
        "entregable": "1,000 m",
        "actividades": {
            "8.13.1": 1000.0,
            "13.9": 19440.0
        }
    },
    "CONSTRUCCIÓN DE BORDILLOS": {
        "entregable": "200 m",
        "actividades": {
            "4.1.2": 16.0,
            "5.1.7": 4.0,
            "14.3": 200.0
        }
    },
    "CONSTRUCCIÓN DE DISIPADORES": {
        "entregable": "8 Un",
        "actividades": {
            "4.1.9": 180.0,
            "6.1.18.1": 56.0,
            "8.18": 48.0,
            "10.1": 272.0
        }
    },
    "ESTABILIZACION CON MATERIAL GRANULAR": {
        "entregable": "1 Km",
        "actividades": {
            "4.1.1": 105.0,
            "5.1.2": 105.0,
            "5.2.16": 1400.0,
            "5.2.13": 260.0,
            "4.1.96": 208.0,
            "4.3.8": 208.0,
            "5.1.15": 640.0,
            "7.1.1": 5000.0,
            "7.1.12.2": 5000.0,
            "13.1": 86548.50,
            "13.2": 1575.0
        }
    },
    "SEÑALIZACIÓN VIAL": {
        "entregable": "1 Km",
        "actividades": {
            "12.1": 3000.0,
            "12.9": 5.0
        }
    }
}

with open('actividades.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Clone the first circuit to create Miserenga
new_circuit = copy.deepcopy(data['circuitos'][0])
new_circuit['nombre'] = "VIA MISERENGA - EBEJICO"

for cat in new_circuit.get('categorias', []):
    cat_name = cat['nombre']
    if cat_name in new_data:
        cat['entregable'] = new_data[cat_name]['entregable']
        
        # Update actividades
        for act in cat.get('actividades', []):
            act['cantidad_ejecutada'] = 0.0 # reset executed to 0 for this new circuit
            item = act['item']
            if item in new_data[cat_name]['actividades']:
                act['cantidad_inicial'] = new_data[cat_name]['actividades'][item]

data['circuitos'].append(new_circuit)

with open('actividades.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print("Added MISERENGA - EBEJICO successfully.")
