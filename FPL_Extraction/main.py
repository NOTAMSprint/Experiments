import re


# Regular expressions used to extract the data
findFplMessage = r'\(FPL[A-Za-z0-9\-\s\/]*\)'
findFplFields = r'\-[A-Za-z0-9\/\s]*'
findIcaoCode = r'[A-Za-z]{4}'


# Isolate and broadly validate the input FPL message
def validate_fpl(path):
    with open(path, 'r') as file:
        fpl = file.read()
        fpl = re.search(findFplMessage, fpl)
        if fpl:
            message = fpl.group()
        else:
            exit('Invalid FPL message')

        # remove all `\n` characters
        message = message.replace('\n', '')

        return message


# Extract the fields from the FPL message
def extract_fpl_fields(fpl):
    fpl_fields = re.findall(findFplFields, fpl)

    # Create the flightplan object
    flightplan = {}

    # capture the departure airport from field 13
    flightplan['adep'] = re.search(findIcaoCode, fpl_fields[4]).group()

    # extract field 16
    field_16 = fpl_fields[6]
    # extract the destination airport from field 16
    flightplan['ades'] = re.search(r'([A-Za-z]{4})[0-9]{4}', field_16).group(1)
    # extract all alternate airports from field 16
    flightplan['dalts'] = re.findall(findIcaoCode, field_16)[1:]

    # extract field 18
    field_18 = fpl_fields[7]

    # find the EET section in field 18
    eet = re.search(r'EET\/([A-Za-z0-9\s]*)\s{1}[A-Za-z]+\/', field_18).group(1)
    # extract all FIR codes
    firs = re.findall(r'\b([A-Za-z]{4})[0-9]{4}', eet)
    # remove duplicates and assign to flightplan
    flightplan['firs'] = list(dict.fromkeys(firs))

    # find the RALT section in field 18
    ralt = re.search(r'RALT\/([A-Za-z0-9\s]*)\s{1}[A-Za-z]+\/', field_18)
    if ralt:
        ralt = ralt.group(1)
        # extract all enroute alternates
        flightplan['ralts'] = re.findall(findIcaoCode, ralt)
    else:
        flightplan['ralts'] = []

    #find the TALT section in field 18
    talt = re.search(r'TALT\/([A-Za-z0-9\s]*)\s{1}[A-Za-z]+\/', field_18)
    if talt:
        talt = talt.group(1)
        # extract the takeoff alternate
        flightplan['talt'] = re.search(findIcaoCode, talt).group()
    else:
        flightplan['talt'] = ''

    return flightplan


# if the script is running from the main directory, execute the extract function
if __name__ == "__main__":
    fpl = validate_fpl('Sample_Data/5.txt')
    print(extract_fpl_fields(fpl))
