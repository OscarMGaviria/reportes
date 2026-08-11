import json
import copy

# Load original json template
with open('actividades.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

template_circuit = data['circuitos'][0]

executed_data = {
    "VIA FRONTINO - NUTIBARA": {
        "2.8": 580.63,
        "4.1.8": 1483.10,
        "5.1.7": 921.05,
        "6.2.4": 0.00,
        "6.2.24": 0.00,
        "8.1": 2022.27,
        "8.27": 510.68,
        "10.1": 0.00,
        "13.1": 116981.17 + 297300.41,
        "4.1.1": 27.00,
        "5.1.2": 177.00,
        "5.1.15": 3717.95,
        "13.2": 255.42
    },
    "VIA EBEJICO - HELICONIA": {
        "2.8": 61.67,
        "4.1.8": 1515.63,
        "5.1.7": 463.35,
        "8.1": 2814.69,
        "8.27": 211.20,
        "5.1.15": 260.30,
        "13.1": 29098.14 + 15765.00
    },
    "VIA SOPETRAN - BELMIRA HORIZONTES": {
        "2.8": 48.16,
        "4.1.8": 442.77,
        "5.1.7": 95.28,
        "8.1": 4411.51,
        "8.27": 58.60,
        "13.1": 4025.87 + 305882.64,
        "5.1.15": 3044.64,
        "13.9": 9903.69,
        "8.13.1": 1169.64,
        "6.1.18.1": 49.44  # This matches "Concreto clase F"
    }
}

new_circuitos = []

for circuit_name, quantities in executed_data.items():
    circuit_copy = copy.deepcopy(template_circuit)
    circuit_copy['nombre'] = circuit_name
    
    # Keep track of items already updated so we don't duplicate the quantity
    # We will assign the full quantity to the first match we find
    applied_items = set()
    
    for categoria in circuit_copy['categorias']:
        for actividad in categoria['actividades']:
            item_code = actividad['item']
            if item_code in quantities and item_code not in applied_items:
                actividad['cantidad_ejecutada'] = quantities[item_code]
                applied_items.add(item_code)
                
    new_circuitos.append(circuit_copy)

# Save back to json
data['circuitos'] = new_circuitos
with open('actividades.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print("actividades.json updated successfully.")
