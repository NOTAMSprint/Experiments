import os
from pathlib import Path
import json


base_dir = os.path.abspath(os.path.dirname(__file__))
THIS_FOLDER = Path(__file__).parent.resolve()

matrix_dict = {
    'airport_status_hours': {'code': 'P1', 'departure': True, 'departure_alternate': True, 'enroute_alternate': True, 'edto_alternate': True, 'destination': True, 'destination_alternate': True},
    'airport_restriction': {'code': 'P2', 'departure': False, 'departure_alternate': True, 'enroute_alternate': True, 'edto_alternate': True, 'destination': True, 'destination_alternate': True},
    'atc_status_hours': {'code': 'C1', 'departure': True, 'departure_alternate': True, 'enroute_alternate': True, 'edto_alternate': True, 'destination': True, 'destination_alternate': True},
    'fire_and_rescue': {'code': 'P3', 'departure': False, 'departure_alternate': False, 'enroute_alternate': False, 'edto_alternate': True, 'destination': False, 'destination_alternate': False},
    'trigger_notam': {'code': 'L1', 'departure': True, 'departure_alternate': False, 'enroute_alternate': False, 'edto_alternate': False, 'destination': True, 'destination_alternate': False},
    'runway_closed': {'code': 'R1', 'departure': True, 'departure_alternate': True, 'enroute_alternate': True, 'edto_alternate': True, 'destination': True, 'destination_alternate': True},
    'runway_length': {'code': 'R2', 'departure': True, 'departure_alternate': True, 'enroute_alternate': True, 'edto_alternate': True, 'destination': True, 'destination_alternate': True},
    'runway_lights': {'code': 'R4', 'departure': True, 'departure_alternate': True, 'enroute_alternate': True, 'edto_alternate': True, 'destination': True, 'destination_alternate': True},
    'taxiway_closed': {'code': 'T1', 'departure': True, 'departure_alternate': False, 'enroute_alternate': False, 'edto_alternate': False, 'destination': True, 'destination_alternate': False},
    'taxiway_restriction': {'code': 'T2', 'departure': True, 'departure_alternate': False, 'enroute_alternate': False, 'edto_alternate': False, 'destination': True, 'destination_alternate': False},
    'taxiway_lights': {'code': 'T3', 'departure': True, 'departure_alternate': False, 'enroute_alternate': False, 'edto_alternate': False, 'destination': True, 'destination_alternate': False},
    'approach_not_available': {'code': 'A1', 'departure': True, 'departure_alternate': True, 'enroute_alternate': True, 'edto_alternate': True, 'destination': True, 'destination_alternate': True},
    'approach_degraded': {'code': 'A2', 'departure': True, 'departure_alternate': True, 'enroute_alternate': True, 'edto_alternate': True, 'destination': True, 'destination_alternate': True},
    'departure': {'code': 'N3', 'departure': True, 'departure_alternate': False, 'enroute_alternate': False, 'edto_alternate': False, 'destination': False, 'destination_alternate': False},
    'arrival': {'code': 'N2', 'departure': False, 'departure_alternate': False, 'enroute_alternate': False, 'edto_alternate': False, 'destination': True, 'destination_alternate': True},
    'atc_procedure': {'code': 'C2', 'departure': True, 'departure_alternate': False, 'enroute_alternate': False, 'edto_alternate': False, 'destination': True, 'destination_alternate': True},
    'atc_flow_and_delay': {'code': 'C3', 'departure': False, 'departure_alternate': False, 'enroute_alternate': False, 'edto_alternate': False, 'destination': True, 'destination_alternate': True},
    'radio': {'code': 'C4', 'departure': False, 'departure_alternate': False, 'enroute_alternate': False, 'edto_alternate': False, 'destination': False, 'destination_alternate': False},
    'radar_ads': {'code': 'C5', 'departure': True, 'departure_alternate': False, 'enroute_alternate': False, 'edto_alternate': False, 'destination': True, 'destination_alternate': True},
    'met': {'code': 'C6', 'departure': False, 'departure_alternate': False, 'enroute_alternate': True, 'edto_alternate': True, 'destination': True, 'destination_alternate': True},
    'fuel': {'code': 'P4', 'departure': False, 'departure_alternate': False, 'enroute_alternate': True, 'edto_alternate': True, 'destination': True, 'destination_alternate': True},
    'apron_parking': {'code': 'P5', 'departure': False, 'departure_alternate': False, 'enroute_alternate': False, 'edto_alternate': False, 'destination': True, 'destination_alternate': True},
    'airport_facilities': {'code': 'P6', 'departure': False, 'departure_alternate': False, 'enroute_alternate': False, 'edto_alternate': False, 'destination': False, 'destination_alternate': False},
    'airport_procedure': {'code': 'P7', 'departure': False, 'departure_alternate': False, 'enroute_alternate': False, 'edto_alternate': False, 'destination': False, 'destination_alternate': False},
    'wip_construction': {'code': 'P8', 'departure': False, 'departure_alternate': False, 'enroute_alternate': False, 'edto_alternate': False, 'destination': False, 'destination_alternate': False},
    'runway_strength': {'code': 'R3', 'departure': False, 'departure_alternate': True, 'enroute_alternate': True, 'edto_alternate': False, 'destination': True, 'destination_alternate': True},
    'runway_condition': {'code': 'R5', 'departure': True, 'departure_alternate': True, 'enroute_alternate': True, 'edto_alternate': False, 'destination': True, 'destination_alternate': True},
    'runway_note': {'code': 'R6', 'departure': False, 'departure_alternate': False, 'enroute_alternate': True, 'edto_alternate': False, 'destination': False, 'destination_alternate': False},
    'taxiway_condition': {'code': 'T4', 'departure': True, 'departure_alternate': False, 'enroute_alternate': False,
                          'edto_alternate': False, 'destination': True, 'destination_alternate': True},
    'taxiway_note': {'code': 'T5', 'departure': False, 'departure_alternate': False, 'enroute_alternate': False,
                     'edto_alternate': False, 'destination': False, 'destination_alternate': False},
    'approach_change': {'code': 'A3', 'departure': False, 'departure_alternate': False, 'enroute_alternate': False,
                        'edto_alternate': False, 'destination': False, 'destination_alternate': False},
    'navaid_status': {'code': 'N1', 'departure': True, 'departure_alternate': True, 'enroute_alternate': True,
                      'edto_alternate': True, 'destination': True, 'destination_alternate': True},
    'gps': {'code': 'N4', 'departure': False, 'departure_alternate': False, 'enroute_alternate': False,
            'edto_alternate': False, 'destination': False, 'destination_alternate': False},
    'aircraft_activity': {'code': 'H1', 'departure': False, 'departure_alternate': False, 'enroute_alternate': False,
                          'edto_alternate': False, 'destination': False, 'destination_alternate': False},
    'explosives': {'code': 'H2', 'departure': False, 'departure_alternate': False, 'enroute_alternate': False,
                   'edto_alternate': False, 'destination': False, 'destination_alternate': False},
    'missile_gun_or_rocket_firing': {'code': 'H3', 'departure': False, 'departure_alternate': False,
                                     'enroute_alternate': False, 'edto_alternate': False, 'destination': False,
                                     'destination_alternate': False},
    'obstacle_new': {'code': 'H4', 'departure': False, 'departure_alternate': False, 'enroute_alternate': False,
                     'edto_alternate': False, 'destination': False, 'destination_alternate': False},
    'obstacle_light_out': {'code': 'H5', 'departure': False, 'departure_alternate': False, 'enroute_alternate': False,
                           'edto_alternate': False, 'destination': False, 'destination_alternate': False},
    'wildlife': {'code': 'H6', 'departure': False, 'departure_alternate': False, 'enroute_alternate': False,
                 'edto_alternate': False, 'destination': False, 'destination_alternate': False},
    'aip_change': {'code': 'L3', 'departure': False, 'departure_alternate': False, 'enroute_alternate': False,
                   'edto_alternate': False, 'destination': False, 'destination_alternate': False},
    'aip_chart_change': {'code': 'L4', 'departure': False, 'departure_alternate': False, 'enroute_alternate': False,
                         'edto_alternate': False, 'destination': False, 'destination_alternate': False},
    'flight_planning': {'code': 'L5', 'departure': False, 'departure_alternate': False, 'enroute_alternate': False,
                        'edto_alternate': False, 'destination': False, 'destination_alternate': False},
    'state_rule': {'code': 'L6', 'departure': False, 'departure_alternate': False, 'enroute_alternate': False, 'edto_alternate': False, 'destination': False, 'destination_alternate': False},
    'security_warnings': {'code': 'L7', 'departure': False, 'departure_alternate': False, 'enroute_alternate': False, 'edto_alternate': False, 'destination': False, 'destination_alternate': False},
    'checklist_notam': {'code': 'L2', 'departure': False, 'departure_alternate': False, 'enroute_alternate': False, 'edto_alternate': False, 'destination': False, 'destination_alternate': False}
}

json_file_dir = THIS_FOLDER / 'Openai_interface' / 'json_files_for_airports'

# Load the json file from OpenaAi_interface
station = 'YBAS'
filepath = json_file_dir / f'{station}.json'
with open(filepath) as f:
    notams = json.load(f)

# Apply the matrix to sort into light and dark notams
# Add key 'relevant' with value True or False

for notam in notams:
    for key, value in matrix_dict.items():
        if notam['Tag'] == key:
            relevance_dict = {
                'departure': value['departure'],
                'departure_alternate': value['departure_alternate'],
                'enroute_alternate': value['enroute_alternate'],
                'edto_alternate': value['edto_alternate'],
                'destination': value['destination'],
                'destination_alternate': value['destination_alternate'],
                'FIR': True,
            }
            notam['relevant'] = relevance_dict

print(notams)


