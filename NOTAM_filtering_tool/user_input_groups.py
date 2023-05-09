def customize_user_input() ->dict:
    '''

    :return: "Inputs" dictionary with different groups as keys and search inputs as values.
    '''

    inputs = {}

    inputs['group_us'] = ["U/S", "NOT USABLE", "UNSERVICEABLE", "INOP", "INOPERATIVE", "SUSPENDED", "SUSP", "OUT OF SERVICE", "WITHDRAWN", "NOT AVBL"]

    inputs['group_clsd'] = ["CLSD", "CLOSED"]

    inputs['group_rwy'] = ["RWY", "RUNWAY"]

    inputs['group_navaids'] = ["ILS", "ILS/DME", "GP", "LOC", "VOR", "NDB"]

    return inputs
