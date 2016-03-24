import sys
import csv
import argparse

import dfareporting_utils
from oauth2client import client

argparser = argparse.ArgumentParser(add_help=False)
argparser.add_argument(
    'profile_id', type=int,
    help='The ID of the profile')
argparser.add_argument(
    'floodlight_id', type=int,
    help='The ID of the Floodlight Activity')

def main(argv):
    flags = dfareporting_utils.get_arguments(argv, __doc__, parents=[argparser])

    # Authenticate and construct service.
    service = dfareporting_utils.setup(flags)

    profile_id = flags.profile_id
    floodlight_id = flags.floodlight_id
    
    try:
        #code here
        request = service.floodlightActivities().generatetag(profileId=profile_id, floodlightActivityId=floodlight_id).execute()
        print request['floodlightActivityTag']
    except client.AccessTokenRefreshError:
        print ('The credentials have been revoked or expired, please re-run the '
           'application to re-authorize')

if __name__ == '__main__':
  main(sys.argv)
