# Brandon Yagihashi - 4/1/2016
# Campaign List Builder
# This script takes a profile ID and Advertiser ID and writes all relevant campaign names and dates to an HTML file - "campaign_list.html"
# Also prints how many days until start date if it has not already launched. Need to convert to business days.

import sys
import csv
import argparse
import datetime
from time import strptime
from datetime import datetime, timedelta
#import pandas as pd
#from pandas.tseries.offsets import BDay Possible business day workaround - Python Data Analysis Lib

import dfareporting_utils
from oauth2client import client

argparser = argparse.ArgumentParser(add_help=False)
argparser.add_argument('profile_id', type=int, help='The ID of the Profile')
argparser.add_argument('advertiser_id', type=int,help='The ID of the Advertiser')
argparser.add_argument('--campaign_id', type=int,help='The ID of the Campaign')


def main(argv):
    flags = dfareporting_utils.get_arguments(argv, __doc__, parents=[argparser])

    # Authenticate and construct service.
    service = dfareporting_utils.setup(flags)

    profile_id = flags.profile_id
    advertiser_id = flags.advertiser_id
    campaign_id = flags.campaign_id


    #Pending business day implementation
    #today = pd.datetime.today()
    #BDexample = today - BDay(4) 

    #Campaign level view
    if(flags.campaign_id):
        try:
            htmlfile = open('campaign_list.html', "w")#Open HTML file for writing
            htmlfile.write('<link rel="stylesheet" href="campaign_list.css">')
            htmlfile.write('<table class="test">') #Start writing
            request = service.placements().list(profileId=profile_id,advertiserIds=advertiser_id,campaignIds=campaign_id).execute()
            
            for placements in request['placements']: #List campaigns
                htmlfile.write(("<tr>" + "<td>" + placements['name'] + "</td>" + int(placements['size']) + "</tr>").encode('utf-8'))
            htmlfile.write('</table>')

        except client.AccessTokenRefreshError:
            print ('The credentials have been revoked or expired, please re-run the application to re-authorize')
    #Advertiser level view        
    else:
        try:
            htmlfile = open('campaign_list.html', "w")#Open HTML file for writing
            htmlfile.write('<link rel="stylesheet" href="campaign_list.css">')
            htmlfile.write('<table class="test">') #Start writing

            request = service.campaigns().list(profileId=profile_id, advertiserIds=advertiser_id).execute()

            for campaigns in request['campaigns']: #List campaigns
                startDate = strptime(campaigns['startDate'], "%Y-%m-%d")
                htmlfile.write(("<tr>" + "<td>" + campaigns['name'] + "</td>" + "<td>" + str(startDate[1]) +  "-" + str(startDate[2]) + "-" + str(startDate[0]) + "</td>").encode('utf-8'))
                htmlfile.write(("<td>" + str(campaigns['lastModifiedInfo']) + "</td>").encode('utf-8'))
                if(datetime(startDate[0],startDate[1],startDate[2]) > datetime.now()):
                    htmlfile.write(("<td>" + str(datetime(startDate[0],startDate[1],startDate[2]) - datetime.now()) + "</td>" + "</tr>"))#Days from start
                else:
                    htmlfile.write("</tr>")
                
            
            htmlfile.write('</table>')

        except client.AccessTokenRefreshError:
            print ('The credentials have been revoked or expired, please re-run the '
               'application to re-authorize')

if __name__ == '__main__':
  main(sys.argv)
