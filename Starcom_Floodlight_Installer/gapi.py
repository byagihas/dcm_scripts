## gapi.py
## Adam Stein, Cahle Johnson
## 4-13-2016

from oauth2client import client
from oauth2client import file as authFile
from oauth2client import tools
from googleapiclient import discovery

import sys
import os
import argparse
import httplib2

#Google API Details
#API Scope
API_SCOPE = 'https://www.googleapis.com/auth/dfatrafficking'

#API_Version
API_VERSION = 'v2.4'

#API Name
API_NAME = 'dfareporting'

#Credential Storage
API_STORE = 'store.dat'

class gapi:
	def __init__( self, profile_id, advertiser_id, scope = API_SCOPE, version = API_VERSION, name = API_NAME, store = API_STORE):
		self.profileId = profile_id
		self.advertiserId = advertiser_id
		self.scope = scope
		self.version = version
		self.name = name
		self.store = store
		
	def getConfigId( self):
		service = api_con( self.scope, self.store, self.name, self.version)
		request = service.advertisers().get( profileId = self.profileId, id = self.advertiserId)
			
		try:
			response = request.execute()
			return response['floodlightConfigurationId']
				
		except client.AccessTokenRefreshError:
			print ('The credentials have been revoked or expired, please re-run the application to re-authorize')
			
	def getGroups( self):
		service = api_con( self.scope, self.store, self.name, self.version)
		request = service.floodlightActivityGroups().list(profileId = self.profileId, advertiserId = self.advertiserId)
		
		try:
			response = request.execute()
			return response['floodlightActivityGroups']
			
		except client.AccessTokenRefreshError:
			print ('The credentials have been revoked or expired, please re-run the application to re-authorize')
			
	def getActivities( self, mygroups = None):
		service = api_con( self.scope, self.store, self.name, self.version)
		
		if mygroups == None:
			request = service.floodlightActivities().list(profileId = self.profileId, advertiserId = self.advertiserId)
		else:
			request = service.floodlightActivities().list(profileId = self.profileId, advertiserId = self.advertiserId, floodlightActivityGroupIds = mygroups)
		
		try:
			response = request.execute()
			return response['floodlightActivities']
			
		except client.AccessTokenRefreshError:
			print ('The credentials have been revoked or expired, please re-run the application to re-authorize')
			
	def installFloodlightGroup( self, group):
		service = api_con( self.scope, self.store, self.name, self.version)
		
		request = service.floodlightActivityGroups().insert( profileId = self.profileId, body = group)
			
		try:
			response = request.execute()
			return response
				
		except client.AccessTokenRefreshError:
			print('The credentials have been revoked or expired, please re-run the application to re-authorize')
				
	def installFloodlightActivity( self, activity):
		service = api_con( self.scope, self.store, self.name, self.version)

		request = service.floodlightActivities().insert( profileId = self.profileId, body = activity)
			
		try:
			response = request.execute()
			return response
			
		except client.AccessTokenRefreshError:
			print('The credentials have been revoked or expired, please re-run the application to re-authorize')

	
	def generateFloodlightTag( self, floodlightResponse):
		service = api_con( self.scope, self.store, self.name, self.version)
		
		request = service.floodlightActivities().generatetag( profileId = self.profileId, floodlightActivityId = floodlightResponse['id'])
		
		try:
			response = request.execute()
			return response
		
		except client.AccessTokenRefreshError:
			print('The credentials have been revoked or expired, please re-run the application to re-authorize')
		

	
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
		
	