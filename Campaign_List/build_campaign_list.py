# Brandon Yagihashi - 4/1/2016
# Campaign List Builder
# This script takes a profile ID and Advertiser ID and writes all relevant campaign names and dates to an HTML file - "campaign_list.html"
# Also prints how many days until start date if it has not already launched. Need to convert to business days.

from gapi import *

import sys
import csv
import argparse

import datetime
from time import strptime
from datetime import datetime, timedelta

#import pandas as pd
#from pandas.tseries.offsets import BDay Possible business day workaround - Python Data Analysis Lib

def main(argv):
    parser = argparse.ArgumentParser(description = 'List Campaigns and Placements')
    parser.add_argument('profile_id')
    parser.add_argument('advertiser_id')
    parser.add_argument('--campaign_id')
    args = parser.parse_args()

    profileID = args.profile_id
    advertiserID = args.advertiser_id
    campaignID = args.campaign_id

    google = gapi(profileID, advertiserID)
    campaign_list = google.getCampaigns()
    placement_list = google.getPlacements(campaignID)

    encoded_campaign_list = campaign_list['campaigns']
    encoded_placement_list = placement_list
    
    #Pending business day implementation
    #today = pd.datetime.today()
    #BDexample = today - BDay(4)

    #Campaign level view
    if(campaignID):
        htmlfile = open('campaign_list.html', "w")#Open HTML file for writing
        htmlfile.write('<link rel="stylesheet" href="campaign_list.css">')
        htmlfile.write('<table class="test">') #Start writing
        
        for campaigns in encoded_campaign_list: #List campaigns
            htmlfile.write("<tr>" + "<td>" + campaigns + "</td>"  + "</tr>")

        htmlfile.write('</table>')
    #Advertiser level view        
    else:
        htmlfile = open('campaign_list.html', "w")#Open HTML file for writing
        htmlfile.write('<link rel="stylesheet" href="campaign_list.css">')
        htmlfile.write('<table class="test">') #Start writing
        htmlfile.write(("<tr>" + "<td>" + "Campaign Name" + "</td>"+ "<td>" + "Campaign ID" + "</td>" + "<td>" + "Start Date" +  "End Date").encode('utf-8'))

        for campaigns in encoded_campaign_list:
            startDate = strptime(campaigns['startDate'], "%Y-%m-%d")
            if(datetime(startDate[0],startDate[1],startDate[2]) > datetime.now()):
                htmlfile.write(("<tr>" + "<td>" + campaigns['name'] + "</td>"+ "<td>" + campaigns['id'] + "</td>" + "<td>" + str(startDate[1]) +  "-" + str(startDate[2]) + "-" + str(startDate[0]) + "</td>").encode('utf-8'))
                htmlfile.write(("<td>" + str(campaigns['lastModifiedInfo']).encode('utf-8') + "</td>"))
                htmlfile.write(("<td>" + str(datetime(startDate[0],startDate[1],startDate[2]) - datetime.now()).encode('utf-8') + "</td>" + "</tr>"))#Days from start
            else:
                htmlfile.write("</tr>")
        
        
        htmlfile.write('</table>')
if __name__ == '__main__':
  main(sys.argv)
