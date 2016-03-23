import os
import sys
import argparse

import dfareporting_utils
from oauth2client import client

argparser = argparse.ArgumentParser(add_help=False)
argparser.add_argument(
    'profile_id', type=int,
    help='The ID of the profile to add a placement for')
argparser.add_argument(
    'campaign_id', type=int,
    help='The ID of the campaign to associate the placement with')
argparser.add_argument(
    'site_id', type=int,
    help='The ID of the site to associate the placement with')

def main(argv):
    flags = dfareporting_utils.get_arguments(argv, __doc__, parents=[argparser])

    # Authenticate and construct service.
    service = dfareporting_utils.setup(flags)
    profile_id = flags.profile_id
    campaign_id = flags.campaign_id
    site_id = flags.site_id
    try:
        # Look up the campaign
        campaign = service.campaigns().get(
            profileId=profile_id, id=campaign_id).execute()

        logDir = 'file_name_here' #File that is being read
        with open(logDir, "r") as fl:
            next(fl)
            next(fl)
            for line in fl:
                arr = line.split(',')
                if(len(arr[0]) != 9):
                    next(fl)
                    
                # Construct and save placement.
              
                placement = {
                    'name': arr[1],
                    'campaignId': campaign_id,
                    'compatibility': 'DISPLAY',
                    'siteId': site_id,
                    'size': {
                        'height': '1',
                        'width': '1'
                    },
                    'paymentSource': 'PLACEMENT_AGENCY_PAID',
                    'tagFormats': ['PLACEMENT_TAG_STANDARD']
                }

                # Set the pricing schedule for the placement.
                placement['pricingSchedule'] = {
                    'startDate': campaign['startDate'],
                    'endDate': campaign['endDate'],
                    'pricingType': 'PRICING_TYPE_CPM'
                }

                ad = {
                 "campaignId": "9481389",
                 "startTime": "2016-3-06T10:30:00-0800",
                 "endTime": "2016-12-06T10:30:00-0800",
                 "deliverySchedule": {
                  "priority": "AD_PRIORITY_15",
                  "impressionRatio": "1"
                 },
                 "name": arr[2],
                 "placementAssignments": [
                  {
                   "placementId": arr[0]
                  }
                 ]
                }

                request = service.ads().update(profileId=profile_id, body=ad)

                # Execute request and print response.
                response = request.execute()

                print ('Created placement with ID %s and name "%s".'
                       % (long(response['id']), response['name']))

    except client.AccessTokenRefreshError:
        print ('The credentials have been revoked or expired, please re-run the '
           'application to re-authorize')


if __name__ == '__main__':
  main(sys.argv)
