import openai
import json
import requests


taglist=[
["C1","ATC status/hours"],
["C2","ATC procedure"],
["C3","ATC flow and delay"],
["C4","Radio"],
["C5","Radar & ADS"],
["C6","Met"],
["P1","Airport status/hours"],
["P2","Airport restriction"],
["P3","Fire & Rescue"],
["P4","Fuel"],
["P5","Apron & Parking"],
["P6","Airport Facilities"],
["P7","Airport Procedure"],
["P8","WIP & Construction"],
["A1","Approach not available"],
["A2","Approach degraded"],
["A3","Approach change"],
["R1","Runway closed"],
["R2","Runway length"],
["R3","Runway strength"],
["R4","Runway lights"],
["R5","Runway condition"],
["R6","Runway note"],
["T1","Taxiway closed"],
["T2","Taxiway restriction"],
["T3","Taxiway lights"],
["T4","Taxiway condition"],
["T5","Taxiway note"],
["N1","Navaid status"],
["N2","Arrival"],
["N3","Departure"],
["N4","GPS"],
["S1","Route closed"],
["S2","Route restriction"],
["S3","Route changed"],
["S4","Special Use Airspace"],
["S5","Special Routes"],
["S6","Airspace structure"],
["H1","Aircraft activity"],
["H2","Explosives"],
["H3","Missile, Gun or Rocket Firing"],
["H4","Obstacle - New"],
["H5","Obstacle - Light out"],
["H6","Wildlife"],
["L1","Trigger Notam"],
["L2","Checklist NOTAM"],
["L3","AIP Change"],
["L4","AIP Chart Change"],
["L5","Flight Planning"],
["L6","State Rule"],
["L7","Security warnings"]
]


def respond(err, res=None):
    return {
        'statusCode': '400' if err else '200',
        'body': err.message if err else json.dumps(res),
        'headers': {
            'Content-Type': 'application/json',
        },
    }


def getnotambyid(notamid,location):
    # The API endpoint
    url="https://www.daip.jcs.mil/daip/mobile/query"
    
    # Adding a payload
    payload = {"type":"LOCATION","locs":location}
    headers={'Content-type': 'application/json'}
    # A get request to the API
    response = requests.post(url, data=json.dumps(payload),verify=False,headers=headers)
    r=response.json()

    # notamlist if burried in a structure under group and then notams. you can print(r) to see that
    notams=r["group"][0]["notams"][0]["list"]
    
    notam=None
    #Just searchign for the notam with the specified ID
    for n in notams:
        if n["id"]==notamid:
            notam=n["text"]
    
    return  notam



def classifyone(message,tags):
    #this will call chatgpt with one message and the list of tags

    prompt = "Consider the following NOTAM message:\n\nNOTAM: "+message+"\nWhich of the following tags describes best the message:\n"
    for tag in tags:
        prompt=prompt+tag[0]+": "+tag[1]+"\n"
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

def summarize(message,maxwords):
    #this will call chatgpt with one message

    prompt = "Summarize the following NOTAM message in less than "+maxwords+" words:\n\nNOTAM: "+message

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

def tagging(notamid,location):
    #I get the message
    try:
        message=getnotambyid(notamid,location)
        if message==None:
            value="No active NOTAM found with this ID at "+location
        else:
            message=message[0:200]
            try:
                #I ask for the summary
                summary=summarize(message,"10")
                #I ask for the classification
                c=classifyone(message,taglist)
                #I build the return string
                value="NOTAM "+location+" "+notamid+": Tag: "+c+";Summary: "+summary
            except:
                value="There was a problem treating this NOTAM with Open AI"
    except:
        value="There was a problem retrieving the NOTAM "+notamid+" from "+location
    return {"value":value}
    

def lambda_handler(event, context):
    '''An API will call this function by passing location,notamid and openaikey as parameters
    '''
    #print("Received event: " + json.dumps(event, indent=2))

    
    if "location" in event['queryStringParameters'] and "notamid" in event['queryStringParameters'] and "openaikey" in event['queryStringParameters']:
        openai.api_key = event['queryStringParameters']["openaikey"]
        return respond(None, tagging(event['queryStringParameters']["notamid"], event['queryStringParameters']["location"]))
    else:
        return respond(None,{"message":'Unsupported call. you need to submit location, notamid and openaikey query string parameters'})
'''
#this is some test code

print(lambda_handler({"queryStringParameters":{
    "openaikey":"PUTKEYHERE",
    "location":"WSJC",
    "notamid":"A0493/23"
}},None))
'''
