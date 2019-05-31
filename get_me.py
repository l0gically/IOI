#!/usr/bin/python3

import os
import sys
import urllib.request
import requests

# lookup extensions function
def lookupExt(url_z, url_p):
    r_zip = requests.head(url_z)
    r_pdf = requests.head(url_p)
    if(r_zip.status_code == 200 and r_zip.headers["Content-Type"] == "application/zip"):
        return "zip"
    elif (r_pdf.status_code == 200 and r_pdf.headers["Content-Type"] == "application/pdf"):
        return "pdf"
    else:
        return None

# get latest year 
def latest_year_lookup():
    # Get me the stats page in descending order
    r = requests.get("http://stats.ioinformatics.org/olympiads/?sort=year_desc")
    # First instance of "olympiads/2" is the latest year
    index = r.text.find("olympiads/2")
    year = ""
    for i in range (0,4):
        year = year + r.text[index+len("olympiads/")+i]
    return int(year)


argc = len(sys.argv)
first_IOI = 1989
latest_IOI = latest_year_lookup()

# Default setting
from_year = first_IOI
to_year = latest_IOI

#   ==== Check for any invalid inputs ====  #    
if argc == 2:
    save_path = sys.argv[1]
    if not os.path.exists(save_path):
        sys.exit("The specified path does not exist!")

elif not argc == 4:
    sys.exit("Usage: ./get_me.py [from_year] [to_year] [path_for_saving]")

elif argc == 4:
    try:
        from_year = int(sys.argv[1])
    except ValueError:
        sys.exit("Usage: ./get_me.py [from_year] [to_year] [path_for_saving]")
    try:
        # will download until specified in the 3 argument
        to_year = int(sys.argv[2])
    except ValueError:
        sys.exit("Usage: ./get_me.py [from_year] [to_year] [path_for_saving]")

    # Check for mixes of argv order
    if from_year < first_IOI:
        sys.exit("First year of IOI was 1989!")
    elif to_year > latest_IOI:
        sys.exit(f"The latest year of IOI is {latest_IOI}!")
    elif to_year < from_year:
        sys.exit("Usage: ./get_me.py [from_year] [to_year] [path_for_saving]")
    # path to save files in 
    save_path = sys.argv[3]
    if not os.path.exists(save_path):
        sys.exit("The specified path does not exist!")

# download url
url = "https://ioinformatics.org/files"
package_types = ["solutions", "tests", "practice", "problem", "source", "round"]
# adding 1 to "to_year" for the range to execute correctly
to_year = to_year + 1

for year in range (from_year, to_year):

    # Make a new directory for year at path
    if (not os.path.exists(f"{save_path}/{year}")):
        os.mkdir(f"{save_path}/{year}")

# download solutions, tests, practice problems,...
    for filler in package_types:
        num = 1
        # another loop for multiple files 
            # In the case of multiple files
        if filler == "problem" or filler == "round":
            while num:
                # check for the extension
                ext_num = lookupExt(f"{url}/ioi{year}{filler}{num}.zip",f"{url}/ioi{year}{filler}{num}.pdf")
                if ext_num:
                    # Create paths for to the files
                    path = f"{save_path}/{year}/{filler}"
                    if not os.path.exists(path):
                        os.mkdir(path)
                    
                    # create the new numbered filename with correct extension
                    filename = f"ioi{year}{filler}{num}.{ext_num}"
                    # download the files
                    print(f"Downloading {filler} number {num}...")
                #    urllib.request.urlretrieve(f"{url}/{filename}",f"{path}/{filename}")
                    # Make another iteration to check for an upcoming file
                    num = num + 1
                # reached the end of numbered files 
                else:
                    if num-1 == 0:
                        print(f"Didn't find {filler}s for {year}")
                    else:
                        print(f"Found {num-1} {filler}s for {year} :)")
                    num = False
        # In the case of a single file
        else:
            ext = lookupExt(f"{url}/ioi{year}{filler}.zip",f"{url}/ioi{year}{filler}.pdf")
            # Create paths for to the files
            if ext:
                path = f"{save_path}/{year}/{filler}"
                if not os.path.exists(path):
                    os.mkdir(path)
                filename = f"ioi{year}{filler}.{ext}"
                # download the file
                print(f"Downloading {filler}...")
            #    urllib.request.urlretrieve(f"{url}/{filename}",f"{path}/{filename}")
            else:
                print(f"Didn't find {filler} for {year}")



