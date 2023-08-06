#!python

"""
Script to get a staff member's favourite object.
"""

import argparse

from lancstro.members import staff


parser = argparse.ArgumentParser(description="Get a staff member's favourite object")

parser.add_argument("name", nargs=2, help="The staff member's full name")

args = parser.parse_args()

# get full name from command line arguments
name = " ".join(args.name)

if name not in staff:
    print(f"The staff member '{name}' does not exist")
    
fav = staff[name].favourite_object

if fav is None:
    print(f"{name} does not have a favourite object")
else:
    favname = fav["MAIN_ID"].data.item()
    print(f"{name}'s favourite object is {favname}")

