def customize_user_input() ->dict:

    inputs = {}

    inputs['group_us'] = ["U/S", "NOT USABLE", "UNSERVICEABLE", "INOP", "INOPERATIVE", "SUSPENDED", "SUSP", "OUT OF SERVICE", "WITHDRAWN", "NOT AVBL"]

    inputs['group_clsd'] = ["CLSD", "CLOSED"]

    inputs['group_rwy'] = ["RWY", "RUNWAY"]

    inputs['group_navaids'] = ["ILS", "ILS/DME", "GP", "LOC", "VOR", "NDB"]

    return inputs

def test_customize_user_input():
    assert "U/S" in customize_user_input()['group_us']
    assert "CLSD" in customize_user_input()['group_clsd']
    assert "RUNWAY" in customize_user_input()['group_rwy']
    assert "NDB" in customize_user_input()['group_navaids']
