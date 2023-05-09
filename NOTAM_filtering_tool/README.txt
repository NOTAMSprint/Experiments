NOTAM FILTERING TOOL by Anna Mogiłło-Dettwiler

Generate a flight briefing package with NOTAMs including keywords searched by the user via the CDI.

1. Introduction

Before each flight, pilots and flight dispatchers need to process a lot of information coded in NOTAMs. NOTAMs (Notice To Airmen) are filed with an aviation authority to alert aircraft pilots of potential hazards along a flight route or at a location that could affect the flight. This could be anything from a runway closure to numerous COVID19-related issues. Pilots and flight dispatchers need to read all NOTAMs issued for a given route in order to legally plan a flight. Many times, however, only a few NOTAMs are really critical for the  given flight. Mainly, those concerning runway closures or unserviceability of navigational aids.

The NOTAM FILTERING TOOL aims at facilitating the process of flight preparation. It lets its users search for keywords and generate a tailor-made briefing including only those NOTAMs that are of interest to the user.

2. Usage

Example user input: python main.py notam_small_pack.xml Closed

The output is generated into a separate .txt file: briefing_package.txt.

The user needs to enter a keyword into the CDI. Based on that, from an unfiltered NOTAM package, a customised briefing package for the given flight will be generated. The user can either enter a string, such as "closed" or a string containing wildcards, such as "clos.?d". The search with wildcards could be useful for dealing with spelling mistakes in NOTAMs. The search is automatically made case-insensitive by lowering the user input and the NOTAMs. However, the output is capitalised, as this is the writing convention of NOTAMs.

If the user input is included in the "inputs" dictionary from the user_input_groups.py, a search for other words with similar meaning will automatically be triggered. For example, if the user input is "unserviceable", the program will search for "u/s", "not usable", "unserviceable", "inop", "inoperative", "suspended", "susp", "out of service" etc., as these are the words frequently used in NOTAMs. In the case of "unserviceable", the NOTAM will be split on the input and only returned up to and including the input, for instance "RWY28 ILS UNSERVICEABLE". If the input belongs to another group, such as "rwy", only the part from and including the input will be returned: "RWY 09 MINIMUM RAISED TO 2200FT AMSL".

If the user input is not included in the "inputs" dictionary, or if it contains a wildcard, the whole NOTAM will be returned and no splitting will be performed.

The briefing dictionary, which is written into a briefing_package.txt, contains following information in its keys: a four-letter ICAO-location code of the airport concerned, the NOTAM serial number, effective date and expiry date. The value contains the actual NOTAM text.

3. Data

The data has been generated using the Federal Aviation Administration NOTAM search tool available at https://notams.aim.faa.gov/notamSearch/nsapp.html#/

The tool pre-filters the NOTAMs for locations or routes. It offers possibilities to export the NOTAMs into a .pdf or .xslx format.

The .xslx file can be transformed into an .xml using an in-built Excel functionality, which was the case in the course of this project. The generated xml file (notams_faa.xml) has been cleaned up using the format_xml.py script. The end product's name is clean_notams.xml.

4. Background

The author of the project, as a pilot and a flight dispatcher herself, aims at facilitating the process of flight preparation with the use of NLP tools. Having to read through numerous NOTAMs every day made her think of a tool that could be implemented in the flight preparation process.

5. References

International Civil Aviation Organization (ICAO) Annex 15 - Aeronautical Information Services
https://ops.group/blog/
https://www.icao.int/airnavigation/information-management/Pages/GlobalNOTAMcampaign.aspx
https://notams.aim.faa.gov/notamSearch/nsapp.html#/
