## gapi.py
## Adam Stein, Patrick Nogacz, Cahle Johnson
## 3-18-2016

import sys
import os
import argparse
import httplib2

from oauth2client import client
from oauth2client import file as authFile
from oauth2client import tools
from googleapiclient import discovery

def api_con( scope, store, name, version):
	#Identify client secret file
	client_secrets = os.path.join( os.path.dirname(sys.argv[0]), 'client_secret.json')
	
	#Establish flow for API connection
	flow = client.flow_from_clientsecrets( client_secrets, scope, message=tools.message_if_missing(client_secrets))
	
	#Establishes storage file
	storage = authFile.Storage(store)
	
	#Checks for credentials and builds new credentials if none are found
	credentials = storage.get()
	if credentials is None or credentials.invalid:
		flags = tools.argparser.parse_args(args=[])
		credentials = tools.run_flow( flow, storage, flags)
	
	http = credentials.authorize(http = httplib2.Http())
	
	#Generates and runs a service object
	return discovery.build( name, version, http=http)
	
def getConfigId( profile_id, advertiser_id):
	service = gapi.api_con( API_SCOPE, API_STORE, API_NAME, API_VERSION)
	request = service.advertisers().get( profileId = profile_id, id = advertiser_id)
		
	try:
		response = request.execute()
		return response['floodlightConfigurationId']
			
	except client.AccessTokenRefreshError:
		print ('The credentials have been revoked or expired, please re-run the application to re-authorize')
		
def getGroupList():
	print('Hello')