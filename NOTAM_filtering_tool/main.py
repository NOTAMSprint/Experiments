"""
Generate a flight briefing package with NOTAMs searched by the user via the CDI.
"""

import re
from typing import TextIO
from argparse import ArgumentParser, FileType
import lxml.etree as ET

from user_input_groups import customize_user_input

def generate_briefing(file: TextIO, user_input: str) -> dict:
    """
    Generate a dictionary with filtered NOTAMs.

    :param file: The .xml file containing the NOTAMs to be filtered.
    :param user_input: The query, a string.
    :return: A dictionary with NOTAMs searched for by the user.
    """

    ## parse the xml file and store the xml tree
    my_tree = ET.parse(file)
    my_root = my_tree.getroot()

    ## initialize empty briefing dictionary
    briefing = {}

    ## parse the xml
    for notam in my_root.iter("notam"):
        for subelem in notam:
            ## extract the NOTAM location
            if subelem.tag == "location":
                location = subelem.text
            ## extract the NOTAM number
            elif subelem.tag == "number":
                number = subelem.text
            ## extract the NOTAM effective date
            elif subelem.tag == "effective_date":
                effective_date = subelem.text
            ## extract the NOTAM expiry date
            elif subelem.tag == "expiry_date":
                expiry_date = subelem.text
            ## extract the NOTAM text
            elif subelem.tag == "notam_body":
                notam_body = subelem.text

                ## if user input to be found in the group "US" ("unserviceable")
                if user_input.lower() in (item.lower() for item in customize_user_input()['group_us']):
                    ## for each item of the group split the notam body on that item and only store it up to and including that item
                    for item in customize_user_input()['group_us']:
                        if re.search(item.lower(), notam_body.lower()):
                            notam_body_core = notam_body.split(item)[0].strip() + " " + item
                            ## store the location, number and notam body in the dictionary
                            briefing[(location, number, effective_date, expiry_date)] = notam_body_core.splitlines()

                ## if user input to be found in the group "CLSD" (closed)
                elif user_input.lower() in (item.lower() for item in customize_user_input()['group_clsd']):
                    ## for each item of the group split the notam body on that item and only store it up to and including that item
                    for item in customize_user_input()['group_clsd']:
                        if re.search(item.lower(), notam_body.lower()):
                            notam_body_core = notam_body.split(item)[0].strip() + " " + item
                            ## store the location, number and notam body in the dictionary
                            briefing[(location, number, effective_date, expiry_date)] = notam_body_core.splitlines()

                ## if user input to be found in the group "RWY" (runway)
                elif user_input.lower() in (item.lower() for item in customize_user_input()['group_rwy']):
                    ## for each item of the group split the notam body on that item and only store it starting from and including that item
                    for item in customize_user_input()['group_rwy']:
                        if re.search(item.lower(), notam_body.lower()):
                            notam_body_core = item + " " + notam_body.split(item)[1].strip()
                            ## store the location, number and notam body in the dictionary
                            briefing[(location, number, effective_date, expiry_date)] = notam_body_core.splitlines()

                ## if user input to be found in the group "navaids" (navigational aids)
                elif user_input.lower() in (item.lower() for item in customize_user_input()['group_navaids']):
                    ## for each item of the group split the notam body on that item and only store it starting from and including that item
                    for item in customize_user_input()['group_navaids']:
                        if re.search(item.lower(), notam_body.lower()):
                            notam_body_core = item + " " + notam_body.split(item)[1].strip()
                            ## store the location, number and notam body in the dictionary
                            briefing[(location, number, effective_date, expiry_date)] = notam_body_core.splitlines()

                ## if user input is not to be found in any of the groups
                else:
                    if re.search(user_input.lower(), notam_body.lower()):
                        ## store the whole notam body
                        notam_body_core = notam_body
                        ## store the location, number and notam body in the dictionary
                        briefing[(location, number, effective_date, expiry_date)] = notam_body_core.splitlines()

    return briefing


def write_briefing_to_file(user_input: str, briefing: dict):
    """
    Write the generated briefing into a .txt file.

    :param user_input: The query, a string.
    :param briefing: The dictionary with filtered NOTAMs.
    :return: Final file briefing_package.txt.
    """

    with open('briefing_package.txt', 'w') as file:
        file.write("Briefing package for search results: " + user_input.upper() + "\n" + "\n")
        for key in sorted(briefing.keys()):
            file.write("'%s':'%s', \n" % (key, briefing[key]))


def main():
    # Define console argument parser
    parser = ArgumentParser(description="Generate a briefing package matching a"
                                        "given string or regular expression.")
    parser.add_argument('filename', type=FileType('r', encoding='utf-8'),
                        help="The .xml file containing the NOTAMs to be analysed")
    parser.add_argument('user_input', type=str, help="The string or regular expression used as a query.")
    # Parse console arguments
    args = parser.parse_args()
    # Supply arguments to functions that do the actual work
    briefing = generate_briefing(args.filename, args.user_input)
    write_briefing_to_file(args.user_input, briefing)


if __name__ == '__main__':
    main()

