#!/usr/bin/python
#
# Copyright 2015 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""This example displays all active ads your DFA user profile can see.

Only name and ID are returned.
"""

import argparse
import sys

import dfareporting_utils
from oauth2client import client

# Declare command-line flags.
argparser = argparse.ArgumentParser(add_help=False)
argparser.add_argument(
    'profile_id', type=int,
    help='The ID of the profile to look up ads for')
argparser.add_argument(
    'campaign_id', type=int,
    help='The ID of the campaign to look up ads for')


def main(argv):
  # Retrieve command line arguments.
  flags = dfareporting_utils.get_arguments(argv, __doc__, parents=[argparser])

  # Authenticate and construct service.
  service = dfareporting_utils.setup(flags)

  profile_id = flags.profile_id
  campaign_id = flags.campaign_id

  try:
    # Construct the request.
    ad = {
      "active": "true"
    }
    request = service.ads().list(profileId=profile_id, campaignIds=campaign_id)
    while True:
      # Execute request and print response.
      response = request.execute()

      for ad in response['ads']:
        print ('Found ad with ID %s and name "%s" and is active? "%s".' % (ad['id'], ad['name'], ad['active']))
        if ad['active']:
          ad_res = {
            "campaignId": ad['campaignId'],
            "startTime": ad['startTime'],
            "endTime": ad['endTime'],
            "deliverySchedule": {
              "priority": "AD_PRIORITY_15",
              "impressionRatio": "1"
            },
            "name" : ad['name'],
            "id" : ad['id'],
            "active": "false"
          }
          update_request = service.ads().update(profileId=profile_id, body = ad_res)
          update_response = update_request.execute()

      if response['ads'] and response['nextPageToken']:
        request = service.ads().list_next(request, response)
      else:
        break

  except client.AccessTokenRefreshError:
    print ('The credentials have been revoked or expired, please re-run the '
           'application to re-authorize')


if __name__ == '__main__':
  main(sys.argv)
