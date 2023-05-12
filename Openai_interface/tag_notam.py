"""
To send the notam to openai GPT-4 endpoint and get tags
"""

import requests
import json
import os
import backoff
import openai
import re
from pprint import pprint

from dotenv import load_dotenv
load_dotenv()

OPENAI_KEY = os.environ.get("OPENAI_KEY")
ICAO_KEY = os.environ.get("ICAO_KEY")

openai.api_key = OPENAI_KEY




tags_li = ['atc_status_hours', 'atc_procedure', 'atc_flow_and_delay', 'radio', 'radar_and_ads', 'met', 'airport_status_hours', 'airport_restriction', 'fire_and_rescue', 'fuel', 'apron_and_parking', 'airport_facilities', 'airport_procedure', 'wip_and_construction', 'approach_not_available', 'approach_degraded', 'approach_change', 'runway_closed', 'runway_length', 'runway_strength', 'runway_lights', 'runway_condition', 'runway_note', 'taxiway_closed', 'taxiway_restriction', 'taxiway_lights', 'taxiway_condition', 'taxiway_note', 'navaid_status', 'arrival', 'departure', 'gps', 'route_closed', 'route_restriction', 'route_changed', 'special_use_airspace', 'special_routes', 'airspace_structure', 'aircraft_activity', 'explosives', 'missile_gun_or_rocket_firing', 'obstacle_new', 'obstacle_light_out', 'wildlife', 'trigger_notam', 'checklist_notam', 'aip_change', 'aip_chart_change', 'flight_planning', 'state_rule', 'security_warnings']


def get_notam_from_icao(station):

    key = ICAO_KEY
    url = f'http://api.anbdata.com/anb/states/notams/notams-realtime-list?'

    parameters = {
        'api_key': key,
        'format': 'json',
        'locations': station,
    }

    response = requests.get(url, params=parameters)
    # pprint(response.json())
    return response.json()


def parse_american_notams(notam_raw_text):
    """Extracts the body of the notam from the raw text of the notam
    The body of american notams aren't separated out in the ICAO API endpoint"""

    match = re.search(r'(?<=\s)[A-Z\s\(\)0-9./]+(?=\s\d{10}-\d{10})', notam_raw_text)
    if match:
        body = match.group()
        return body
    else:
        return None


def parse_response(response_json):
    """Parses the json response from AVWX API and returns a list of notams.
    1. Initialises an empty list of notams
    2. initialises i which is used to make a temporary notam ID when there is no ID for the notam
    3. Loops through the json response and extracts the airport code, notam ID and body
    4. Appends the notam data (one python dict for each notam) to the notams list"""

    notams_li = []
    for notam in response_json:
        airport_code = notam['location']
        notam_id = notam['id']
        # Check to see if the 'message' key is there
        if 'message' in notam:
            body = notam['message']
        else:
            body = parse_american_notams(notam['all'])

        raw_text = notam['all']


        notam_data = {
            'airport_code' : airport_code,
            'notam_id': notam_id,
            'body': body,
            'raw_text': raw_text
        }
        notams_li.append(notam_data)

    return notams_li



def create_message(tags_li: list, notam: dict):
    """Creates a message to send to OpenAI API"""

    # Make call to openai to summarise the notam
    content_string = f"""
    You are a tagging system that applies tags to NOTAMs. You only choose from the following tags: {tags_li}. Only choose one tag. Return a json string with the following keys: NOTAM_ID, Tag, seven_word_summary
    """
    station = notam['airport_code']
    notam_id = notam['notam_id']
    body = notam['body']

    user_string = f"""
    Station Code: {station}, NOTAM ID: {notam_id}, Body: {body}
    """
    messages = [
        {"role": "system",
         "content": content_string},
        {"role": "user",
         "content": user_string}
    ]

    return messages


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

def save_station(station, tagged_notams_li):
    """Saves the tagged notams for one station to a json file in a sub directory of the parent directory called 'json_files_for_airports'"""


    # Save the json file
    with open(f'json_files_for_airports/{station}.json', 'w') as f:
        json.dump(tagged_notams_li, f, indent=4)


def process_one_station(station, tags_li):
    """
    Tags all the notams for a station
    :param station:
    :return: A list of dictionaries with the notam ID, tags and summary of each notam from one station
    """


    response_json = get_notam_from_icao(station)
    notams_li = parse_response(response_json)
    # pprint(notams_li)
    tagged_notams_li = []
    num_notams = len(notams_li)
    print(f'Procesing {station}. Number of notams: {num_notams}')
    print('Tagging notams...')
    i = 1
    for notam in notams_li:
        print(f'\nTagging notam {i} of {num_notams}')
        messages = create_message(tags_li=tags_li, notam=notam)
        tagged_notam = ask_openai(messages, model="gpt-3.5-turbo", temperature=0.0)
        tagged_notam = json.loads(tagged_notam)

        raw_text = notam['raw_text']
        # Add a new key to the response from openai
        tagged_notam['raw_text'] = raw_text
        tagged_notam['station'] = station

        tagged_notams_li.append(tagged_notam)
        i += 1

    print(f'Tagging complete for {station}')
    save_station(station, tagged_notams_li)

if __name__== '__main__':
    process_one_station('YBAS', tags_li=tags_li)

