"""
To send the notam to openai GPT-4 endpoint and get tags
"""

import requests
import json
import os
import backoff
import openai

from dotenv import load_dotenv


OPENAI_KEY = os.environ.get("OPENAI_KEY")
load_dotenv()


tags_dict = {
    "ATC": {
        "ATC status/hours": None,
        "ATC procedure": None,
        "ATC flow and delay": None,
        "Radio": None,
        "Radar & ADS": None,
        "Met": None,
    },
    "Airport": {
        "Airport status/hours": None,
        "Airport restriction": None,
        "Fire & Rescue": None,
        "Fuel": None,
        "Apron & Parking": None,
        "Airport Facilities": None,
        "Airport Procedure": None,
        "WIP & Construction": None,
    },
    "Approach": {
        "Approach not available": None,
        "Approach degraded": None,
        "Approach change": None,
    },
    "Runway": {
        "Runway closed": None,
        "Runway length": None,
        "Runway strength": None,
        "Runway lights": None,
        "Runway condition": None,
        "Runway note": None,
    },
    "Taxiway": {
        "Taxiway closed": None,
        "Taxiway restriction": None,
        "Taxiway lights": None,
        "Taxiway condition": None,
        "Taxiway note": None,
    },
    "Navigation": {
        "Navaid status": None,
        "Arrival": None,
        "Departure": None,
        "GPS": None,
    },
    "Airspace": {
        "Route closed": None,
        "Route restriction": None,
        "Route changed": None,
        "Special Use Airspace": None,
        "Special Routes": None,
        "Airspace structure": None,
    },
    "Hazards": {
        "Aircraft activity": None,
        "Explosives": None,
        "Missile, Gun or Rocket Firing": None,
        "Obstacle - New": None,
        "Obstacle - Light out": None,
        "Wildlife": None,
    },
    "Library": {
        "Trigger Notam": None,
        "Checklist NOTAM": None,
        "AIP Change": None,
        "AIP Chart Change": None,
        "Flight Planning": None,
        "State Rule": None,
        "Security warnings": None,
    },
    "Operator Specific": {
        "Below 36M wingspan": None,
        "36M to 65M wingspan": None,
        "Above 65M wingspan": None,
        "IFR": None,
        "VFR": None
    },
    "Weather Dependant": {
        "Low visibility": None,
        "Marginal Conditions": None
    }
}

def create_message(tags_dict: dict, notam: str):
    """Creates a message to send to OpenAI API"""

    # Make call to openai to summarise the notam
    content_string = f"""
    You are a tagging system that tags NOTAMs with the following tags:
    {tags_dict}
    Return json with the following keys: NOTAM_ID, Tags, 7_word_summary
    """
    user_string = f"""
    NOTAM ID: {notam_id}, Body: {body}
    """
    messages = [
        {"role": "system",
         "content": content_string},
        {"role": "user",
         "content": user_string}
    ]


@backoff.on_exception(backoff.expo, Exception, max_tries=20)
def ask_openai(messages, model="gpt-3.5-turbo", temperature=0.0):
    """ Sends call to OpenAI API to summarise and translate into plain English the notam."""


    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=temperature,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
    )


    return response['choices'][0]['message']['content']



