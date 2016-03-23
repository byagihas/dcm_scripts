import sys
import csv
import argparse
import datetime
from time import strptime

import dfareporting_utils
from oauth2client import client

argparser = argparse.ArgumentParser(add_help=False)
argparser.add_argument(
    'profile_id', type=int,
    help='The ID of the profile')
argparser.add_argument(
    'advertiser_id', type=int,
    help='The ID of the Advertiser')

def main(argv):
    flags = dfareporting_utils.get_arguments(argv, __doc__, parents=[argparser])

    # Authenticate and construct service.
    service = dfareporting_utils.setup(flags)

    profile_id = flags.profile_id
    advertiser_id = flags.advertiser_id
    current_date=datetime.datetime.now()
    
    try:
        htmlfile = open('Campaign_list.html', "w")
        htmlfile.write('<table>')
        request = service.campaigns().list(profileId=profile_id, advertiserIds=advertiser_id).execute()
        for campaigns in request['campaigns']:
            startDate = strptime(campaigns['startDate'], "%Y-%m-%d")
            htmlfile.write(("<tr>" + "<td>" + campaigns['name'] + "</td>" + "<td>" + str(campaigns['lastModifiedInfo']) + "</td>" + "<td>" + str(startDate[0]) +  str(startDate[1]) +  str(startDate[2]) + "</td>" + "</tr>").encode('utf-8'))
        htmlfile.write('</table>')
            
    except client.AccessTokenRefreshError:
        print ('The credentials have been revoked or expired, please re-run the '
           'application to re-authorize')

if __name__ == '__main__':
  main(sys.argv)
