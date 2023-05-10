import re


# Regular expressions used to extract the data
findFplMessage = '\(FPL[A-Za-z0-9\-\s\/]*\)'
findFplFields = '\-[A-Za-z0-9\/\s]*'


# Isolate and broadly validate the input FPL message
def validate_fpl(path):
    with open(path, 'r') as file:
        fpl = file.read()
        fpl = re.search(findFplMessage, fpl)
        if fpl:
            message = fpl.group()
        else:
            return 'Invalid FPL message'

        # remove all `\n` characters
        message = message.replace('\n', '')

        return message


# Extract the fields from the FPL message
def extract_fpl_fields(fpl):
    fpl_fields = re.findall(findFplFields, fpl)
    return fpl_fields


# if the script is running from the main directory, execute the extract function
if __name__ == "__main__":
    fpl = validate_fpl('Sample_Data/5.txt')
    print(fpl)
    print(extract_fpl_fields(fpl))
