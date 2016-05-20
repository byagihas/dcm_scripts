from xl import *
from gapi import *

import sys
import argparse

def main():
    parser = argparse.ArgumentParser(description = 'Upload Floodlights to DBM')
    parser.add_argument("file")
    args = parser.parse_args()
    path = str(args.file)

    xl_parsed = xl_parse(path)

    profileID = xl_parsed['profileID']
    advertiserID = xl_parsed['advertiserID']
    campaignID = xl_parsed['campaignID']
    redirects = buildRedirects(xl_parsed)
    
    google = gapi(profileID, advertiserID)
    configID = google.getConfigId()

    placements = google.getPlacements()
    placementArray = []
    

    
def buildRedirect(xl_parsed):
    redirect = {
        "type": "REDIRECT",
        "advertiserId": "690191",
        "size": {
            "width": 1,
            "height": 1
            },
        "redirectUrl": "https://www.google.com",
        "name": "REDIRECT_EXAMPLE"
    }
    
def installRedirects(api):
    #buildRedirect(x)

if __name__ == '__main__':
	main()
