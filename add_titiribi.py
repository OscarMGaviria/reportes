import json
import copy

new_data_titiribi = {
    "CONSTRUCCIÓN DE ALCANTARILLAS": {
        "entregable": "35 un",
        "actividades": {
            "2.8": 24.0,
            "2.14.1": 30.0,
            "4.1.8": 1190.0,
            "4.2.2": 385.0,
            "5.1.7": 140.0,
            "6.2.4": 35.0,
            "6.2.24": 308.0,
            "8.1": 120.0,
            "8.27": 210.0,
            "10.1": 16940.0,
            "13.1": 8078.0
        }
    },
    "CONSTRUCCIÓN DE CUNETA": {
        "entregable": "5,000 m",
        "actividades": {
            "4.1.8": 869.0,
            "5.1.7": 400.0,
            "6.2.50": 500.0,
            "10.1": 14002.0,
            "13.1": 23080.0
        }
    },
    "CONSTRUCCIÓN DE FILTRO PARA CUNETAS": {
        "entregable": "5000 m",
        "actividades": {
            "8.13.1": 5000.0,
            "13.9": 103860.0
        }
    },
    "CONSTRUCCIÓN DE BORDILLOS": {
        "entregable": "1,000 m",
        "actividades": {
            "4.1.2": 80.0,
            "5.1.7": 20.0,
            "14.3": 1000.0
        }
    },
    "CONSTRUCCIÓN DE DISIPADORES": {
        "entregable": "26 un",
        "actividades": {
            "4.1.9": 137.0,
            "6.1.18.1": 182.0,
            "8.18": 156.0,
            "10.1": 170.0
        }
    },
    "ESTABILIZACION CON MATERIAL GRANULAR": {
        "entregable": "5 Km",
        "actividades": {
            "4.1.1": 525.0,
            "5.1.2": 525.0,
            "5.2.16": 7000.0,
            "5.2.13": 1300.0,
            "4.1.96": 1040.0,
            "4.3.8": 1040.0,
            "5.1.15": 3200.0,
            "7.1.1": 25000.0,
            "7.1.12.2": 25000.0,
            "13.1": 243133.38,
            "13.2": 7875.0
        }
    },
    "SEÑALIZACIÓN VIAL": {
        "entregable": "5 Km",
        "actividades": {
            "12.1": 15000.0,
            "12.9": 25.0
        }
    }
}

with open('actividades.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Clone the first circuit to create Titiribi
new_circuit = copy.deepcopy(data['circuitos'][0])
new_circuit['nombre'] = "VIA TITIRIBI - ARMENIA"

for cat in new_circuit.get('categorias', []):
    cat_name = cat['nombre']
    if cat_name in new_data_titiribi:
        cat['entregable'] = new_data_titiribi[cat_name]['entregable']
        
        # Update actividades
        for act in cat.get('actividades', []):
            act['cantidad_ejecutada'] = 0.0 # reset executed to 0 for this new circuit
            item = act['item']
            if item in new_data_titiribi[cat_name]['actividades']:
                act['cantidad_inicial'] = new_data_titiribi[cat_name]['actividades'][item]

data['circuitos'].append(new_circuit)

with open('actividades.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print("Added TITIRIBI - ARMENIA successfully.")
