#
# Example python script to generate a BOM from a KiCad generic netlist
#
# Example: Sorted and Grouped CSV BOM
#

"""
    @package
    Generate a comma delimited list (csv file type).
    Components are sorted by ref and grouped by value with same footprint
    Fields are (if exist)
    'Ref', 'Qnty', 'Value', 'Footprint', 'Ref', 'Vendor Ref'

    Command line:
    python "pathToFile/bom_csv_grouped_by_value_with_fp.py" "%I"
"""

# Import the KiCad python helper module and the csv formatter
import kicad_netlist_reader
import csv
import sys
import os
from datetime import datetime as dt

# Generate an instance of a generic netlist, and load the netlist tree from
# the command line option. If the file doesn't exist, execution will stop
net = kicad_netlist_reader.netlist(sys.argv[1])

# Open a file to write to, if the file cannot be opened output to stdout
# instead
outname = os.path.splitext(sys.argv[1])[0] + ".csv"
try:
    f = open(outname, 'w')
except IOError:
    e = "Can't open output file for writing: " + outname
    print(__file__, ":", e, sys.stderr)
    f = sys.stdout

# Create a new csv writer object to use as the output formatter
out = csv.writer(f, lineterminator='\n', delimiter=',', quotechar='\"', quoting=csv.QUOTE_ALL)

# Output a set of rows for a header providing general information
today = dt.now()
date = "{:d}/{:d}/{:d}".format(today.day, today.month, today.year)
out.writerow(['Source:', net.getSource()])
out.writerow(['Date:', date])
out.writerow(['Component Count:', len(net.components)])
out.writerow(['Ref', 'Qnty', 'Value', 'Footprint', 'Ref', 'Vendor Ref'])

vendors = ["RS","Farnell","Mouser"]
exclude = ["Fiducial", "MountingHole"]
# Get all of the components in groups of matching parts + values
# (see ky_generic_netlist_reader.py)
grouped = net.groupComponents()

# Output all of the component information
for group in grouped:
    refs = ""

    # Add the reference of every component in the group and keep a reference
    # to the component so that the other data can be filled in once per group
    for component in group:
        refs += component.getRef() + ", "
        c = component

    # Get vendor name used for this group
    fieldnames = c.getFieldNames()
    vendor = ""
    for vdr in vendors:
        if vdr in fieldnames:
            vendor = c.getField(vdr)
            break

    # Exclude virtual components
    if c.getValue() in exclude:
        continue

    # Fill in the component groups common data
    out.writerow([refs, len(group), c.getValue(), c.getFootprint(),
                  c.getField("Ref"), vendor])


