import openai
import json
import requests


taglist=[
["P1","Airport status/hours","Airport Closed, Airport operating hours, AD AP not available"],
["P2","Airport restriction","Not available as alternate, airport slots, PPR required, max aircraft weight, etc."],
["P3","Fire & Rescue","RFF Category change, Rescue equipment"],
["P4","Fuel","All fuel related NOTAMs, JET, JETA1, Avgas, Hydrants, Tankering"],
["P5","Apron & Parking","Apron, Stands, Gates, Followme, Apron lighting, docking, guidance, limited parking"],
["P6","Airport Facilities","Equipment (GSE, Rwy/Twy equip, WDI etc.), Facilities Pax processing, airport strikes"],
["P7","Airport Procedure","Manoeuvring, Handling, Deboarding, APU usage etc. NABT and noise curfew"],
["P8","WIP & Construction","Work in Progress, WIP, Construction, Building works, digging, men and equipment"],
["A1","Approach not available","Instrument approach not available, suspended eg. ILS, VOR/DME approach, RNP approach, LPV."],
["A2","Approach degraded","Some part of ILS not working, no cirlcing, minima not available"],
["A3","Approach change","Chart change, Missed approach, RVR minina"],
["R1","Runway closed","Runway Closed/Hours"],
["R2","Runway length","TODA, TORA, ASDA, LDA changed, Displaced THR, CWY, Width change."],
["R3","Runway strength","Runway PCN change, weight restriction."],
["R4","Runway lights","Including ALS/Approach lights, Stopbars, PAPI, VASI"],
["R5","Runway condition","Poor suface, potholes, ungrooved, FOD, contamination (sand, ash), RWYCC"],
["R6","Runway note","Eg. Runway for Arrivals/Departures only, any other minor changes, runway reopened. Runway markings go here too, signs changed, missing, obscured. Building turbulence (Windshear)"],
["T1","Taxiway closed","TWY closed, All taxiway closures."],
["T2","Taxiway restriction","Taxiway limited to specific aircraft weight/MTOW, entry points, one-way taxiways"],
["T3","Taxiway lights","TWY taxiway Lights"],
["T4","Taxiway condition","Poor surface, potholes"],
["T5","Taxiway note","Taxiway Signs, markings, New named, new taxiway, re-opened."],
["C1","ATC status/hours","ATC operating hours, ATC Strike, ATC failure (ATC Zero). Including FIS/AFIS"],
["C2","ATC procedure","TWR/APP/ACC change of procedure, lost comms procedure, contingency, emergency, DCL departure clearance"],
["C3","ATC flow and delay","Flow control, enroute delays, expect holding"],
["C4","Radio","HF, VHF, CPDLC, Satcom, ATIS - u/s, freq changes etc. KHZ, MHZ."],
["C5","Radar & ADS","Radar (PSR, MSSR, SMR, PAR, TAR), ADS (ADS-B, ADS-C) & MLAT"],
["C6","Met","Met service hours, VOLMET, Met Equipment, Met Strikes"],
["N1","Navaid status","Navaids like VOR, NDB, TACAN. U/S, downgraded."],
["N2","Arrival","STAR (Standard Instrument Arrival), any changes to arrival"],
["N3","Departure","SID, SID not avbl. change, any changes to departures"],
["N4","GPS","GPS outages, GPS jamming, RAIM, GNSS, EGNOS, WAAS"],
["S1","Route closed","Airway, ATS Route closed"],
["S2","Route restriction","Airway, ATS Route Open but some restriction"],
["S3","Route changed","Change to ATS Route, Airway definition"],
["S4","Special Use Airspace","SUA's - Danger, Prohibited, Restricted, TRA"],
["S5","Special Routes","Conditional routes. CDR open/closed. CDR1, CDR2, CDR3. Track Systems: Prefered routing, flight level allocation scheme (FLAS), User Prefered Routings (UPR), AUSOTS, Pacific OTS, NAR, NAT Tracks"],
["S6","Airspace structure","Change to specific area, eg. CTR, TMA, FIR, coordinates"],
["H1","Aircraft activity","Air Display, Aerobatics, Balloon or Kite, Exercises, Air Refuelling, Glider, Paraglider, Hang Glider, Banner towing, Mass Movement of aircraft, Parachuting (PJE), Unmanned aircraft, Formation flight, Aerial Survey, Model Flying"],
["H2","Explosives","Fireworks, Blasting, Demolition of explosives, Burning gas"],
["H3","Missile, Gun or Rocket Firing","Military exercises involving any firing activity"],
["H4","Obstacle - New","OBST Newly erected Obstacle, Crane, Wind Farm, Turbines, LIT OBST"],
["H5","Obstacle - Light out","OBST Lights not working u/s Obstacle, Crane, Wind Farm, Turbines"],
["H6","Wildlife","Birds, animals"],
["L1","Trigger Notam","Trigger Notam pointing to AIRAC change, AIC Sup, etc."],
["L2","Checklist NOTAM","Q-KKKK/Checklist of valid NOTAMs"],
["L3","AIP Change","Change to AIP. Use also for AIC related NOTAM"],
["L4","AIP Chart Change","Small chart change ie not AIP, including enroute charts."],
["L5","Flight Planning","Flight planning requirements, Field 18 of FPL"],
["L6","State Rule","National notices, Covid rules, Turkey-Greece notams"],
["L7","Security warnings","Risk warnings, Conflict Zones, Security related NOTAM"]

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

    staglist="List of NOTAM Tags, in three columns\nTag Code\tTag Name\tTag Descriptioncode\n"
    for tag in tags:
        staglist=staglist+tag[0]+"\t*"+tag[1]+"*\t"+tag[2]+"\n"
    staglist=staglist+"Read and wait, no action yet"
    prompt1="You are a NOTAM Librarian.\
    I will give you a NOTAM message. Create a JSON object with the following 2 fields: \n\
    Explanation: In very simple English only, explain the NOTAM in 7 words or less. Do not use abbreviations. Use sentence case.\n\
    Tag: Choose the most logical Tag for this NOTAM from the list of Tags. Format as Tag Code - Tag Name.\n\
    Now wait for the NOTAM."
    prompt2="Here is the NOTAM: "+message
    #print(staglist)
    #print(prompt1)
    #print(prompt2)
    
    #prompt="You are a NOTAM Librarian. First, I will give you a list of NOTAM Tags in three columns: Tag Code, Tag Name, Tag Description. Here they are: \n\n" + staglist + ". Next, I will give you a NOTAM. Choose the most logical Tag for this NOTAM from the list of Tags. Format as Tag Code - Tag Name. Here is the NOTAM:\n\n " + message
    #print(prompt)
    response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
        {"role": "user", "content": staglist},
        {"role": "assistant", "content" : "Thank you, I got the NOTAM tags"},
        {"role": "user", "content": prompt1},
        {"role": "assistant", "content" : "Ok, reday for the NOTAM"},
        {"role": "user", "content": prompt2}
        ]
    )
    predicted_tag = response.choices[0].message.content.strip()
    #print(response)
    
    return predicted_tag


def summarize(message,maxwords):
    #this will call chatgpt with one message

    prompt = "In very simple English only, explain the NOTAM in "+maxwords+" words or less. Do not use abbreviations. Use sentence case.\n\nNOTAM: "+message
    #print(prompt)
    response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
              messages=[
        {"role": "system", "content": "You are a helpful NOTAM librarian."},
        {"role": "user", "content": prompt}
        ]
            
    )
    #print(response)
    predicted_tag = response.choices[0].message.content.strip()
    return predicted_tag

def tagging(notamid,location):
    #I get the message
    try:
        message=getnotambyid(notamid,location)
        if message==None:
            value="No active NOTAM found with this ID at "+location
        else:
            message=message[0:400]
            try:
                #I ask for the summary
                #summary=summarize(message,"7")
                #I ask for the classification
                res=json.loads(classifyone(message,taglist).replace("\n",""))
                print(res)
                newres={}
                for k in res.keys():
                    newres[k.upper()]=res[k]
                #I build the return string
                value="NOTAM "+location+" "+notamid+": Tag: "+newres["TAG"]+";Summary: "+newres["EXPLANATION"]
            except:
                value="There was a problem treating this NOTAM with Open AI"
    except:
        value="There was a problem retrieving the NOTAM "+notamid+" from "+location
    return {"value":value}
    
def tagging_debug(notamid,location):
    #I get the message
    message=getnotambyid(notamid,location)
    if message==None:
        value="No active NOTAM found with this ID at "+location
    else:
        message=message[0:400]
        #I ask for the summary
        summary=summarize(message,"7")
        #I ask for the classification
        c=classifyone(message,taglist)
        #I build the return string
        value="NOTAM "+location+" "+notamid+": Tag: "+c+";Summary: "+summary
    return {"value":value}

def lambda_handler(event, context):
    '''An API will call this function by passing location,notamid and openaikey as parameters
    '''
    #print("Received event: " + json.dumps(event, indent=2))

    
    if "location" in event['queryStringParameters'] and "openaikey" in event['queryStringParameters']:
        openai.api_key = event['queryStringParameters']["openaikey"]
        return respond(None, tagging(event['queryStringParameters']['notamid'], event['queryStringParameters']["location"]))
    else:
        return respond(None,{"message":'Unsupported call. you need to submit location, notamid and openaikey query string parameters'})

#this is some test code
'''
print(lambda_handler({"queryStringParameters":{
    "openaikey":"YOURAPIKEYHERE",
    "location":"EINN",
    "notamid":"B1142/15"
}},None))
'''
