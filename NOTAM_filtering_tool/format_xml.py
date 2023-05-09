"""
Clean up the xml file (return only part E) with the main contents of the NOTAM).
"""

import lxml.etree as ET
import sys


## get the filename to be searched
file = sys.argv[1]
## open file for reading
my_infile = open(file, 'r')

my_tree = ET.parse(file)
my_root = my_tree.getroot()
for notam in my_root.iter("notam"):
    for notam_body in notam:
        body = notam_body.text
        if 'E) ' in body:
            new_body = body.split('E) ')[1].strip()
            notam_body.text = new_body

## write the result to a new .xml file
my_tree.write("clean_notams.xml", encoding='utf-8')