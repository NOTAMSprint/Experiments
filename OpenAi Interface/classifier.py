import openai
import json
import requests

openai.api_key = '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'

taglist = [
    ["C1", "ATC status/hours"],
    ["C2", "ATC procedure"],
    ["C3", "ATC flow and delay"],
    ["C4", "Radio"],
    ["C5", "Radar & ADS"],
    ["C6", "Met"],
    ["P1", "Airport status/hours"],
    ["P2", "Airport restriction"],
    ["P3", "Fire & Rescue"],
    ["P4", "Fuel"],
    ["P5", "Apron & Parking"],
    ["P6", "Airport Facilities"],
    ["P7", "Airport Procedure"],
    ["P8", "WIP & Construction"],
    ["A1", "Approach not available"],
    ["A2", "Approach degraded"],
    ["A3", "Approach change"],
    ["R1", "Runway closed"],
    ["R2", "Runway length"],
    ["R3", "Runway strength"],
    ["R4", "Runway lights"],
    ["R5", "Runway condition"],
    ["R6", "Runway note"],
    ["T1", "Taxiway closed"],
    ["T2", "Taxiway restriction"],
    ["T3", "Taxiway lights"],
    ["T4", "Taxiway condition"],
    ["T5", "Taxiway note"],
    ["N1", "Navaid status"],
    ["N2", "Arrival"],
    ["N3", "Departure"],
    ["N4", "GPS"],
    ["S1", "Route closed"],
    ["S2", "Route restriction"],
    ["S3", "Route changed"],
    ["S4", "Special Use Airspace"],
    ["S5", "Special Routes"],
    ["S6", "Airspace structure"],
    ["H1", "Aircraft activity"],
    ["H2", "Explosives"],
    ["H3", "Missile, Gun or Rocket Firing"],
    ["H4", "Obstacle - New"],
    ["H5", "Obstacle - Light out"],
    ["H6", "Wildlife"],
    ["L1", "Trigger Notam"],
    ["L2", "Checklist NOTAM"],
    ["L3", "AIP Change"],
    ["L4", "AIP Chart Change"],
    ["L5", "Flight Planning"],
    ["L6", "State Rule"],
    ["L7", "Security warnings"]
]

def getnotambyid(notamid, location):
    # The API endpoint
    url = "http://api.anbdata.com/anb/states/notams/notams-realtime-list"
    # Adding a payload
    payload = {"type": "LOCATION", "locs": location}
    headers = {'Content-type': 'application/json'}
    # A get request to the API
    response = requests.post(url, data=json.dumps(payload), verify=False, headers=headers)
    r = response.json()

    # notamlist if burried in a structure under group and then notams. you can print(r) to see that
    notams = r["group"][0]["notams"][0]["list"]

    notam = None
    # Just searchign for the notam with the specified ID
    for n in notams:
        if n["id"] == notamid:
            notam = n["text"]

    return notam


def classifyone(message, tags):
    # this will call chatgpt with one message and the list of tags

    prompt = "Consider the following NOTAM message:\n\nNOTAM: " + message + "\nWhich of the following tags describes best the message:\n"
    for tag in tags:
        prompt = prompt + tag[0] + ": " + tag[1] + "\n"
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=prompt,
        max_tokens=1000,
        temperature=0.0,
        n=1,
        stop=None
    )
    predicted_tag = response.choices[0].text.strip()
    return predicted_tag


def summarize(message, maxwords):
    # this will call chatgpt with one message

    prompt = "Summarize the following NOTAM message in less than " + maxwords + " words:\n\nNOTAM: " + message

    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=prompt,
        max_tokens=1000,
        temperature=0.0,
        n=1,
        stop=None
    )
    predicted_tag = response.choices[0].text.strip()
    return predicted_tag


def tagging(notamid, location):
    # I get the message
    message = getnotambyid(notamid, location)
    # I ask for the summary
    summary = summarize(message, "10")
    # I ask for the classification
    c = classifyone(message, taglist)
    # I build the return string
    value = "NOTAM " + location + " " + notamid + ": Tag: " + c + ";Summary: " + summary
    return value


print(tagging("A0837/23", "EHAM"))