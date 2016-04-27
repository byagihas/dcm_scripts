## Starcom_Floodlight_Installer
## Adam Stein, Patrick Nogacz, Cahle Johnson
## 4-13-2016

from xl import *
from gapi import *

import sys
import argparse

def main():
	#Process Arguments
	parser = argparse.ArgumentParser(description = 'Upload Floodlights to DBM')
	parser.add_argument("file")
	args = parser.parse_args()
	path = str(args.file)
	
	#Process Excel sheet to floodlight list
	xl_parsed = xl_parse(path)
	#print(xl_parsed)
		
	profileID = xl_parsed['profileID']
	advertiserID = xl_parsed['advertiserID']
	floodlights = buildActivities(xl_parsed)
	#print(floodlights)
	
	google = gapi(profileID, advertiserID)
	
	#Fetch config ID to complete activity objects
	configID = google.getConfigId()
	
	#Fetch existing groups
	allGroups = google.getGroups()
	existingGroups = findGroups(floodlights['groups'], allGroups)
	#print(existingGroups)
	
	#Fetch existing Activities
	groupIdArray = []
	for key in existingGroups:
		groupIdArray.append(existingGroups[key])
	allActivities = google.getActivities(groupIdArray)
	
	#Build Installer
	install = buildInstaller( floodlights, existingGroups, allActivities)
	#print(install)
	
	#Output items to install
	if (len(install['groups']) == 0) and (len(install['activities']) == 0 ):
		print('\n No new Groups or Activities to create.')
		print('\n Program closing')
		sys.exit()
	else:
		print(	'\n' + str(len(install['groups'])) + ' new Groups and '+ str(len(install['activities'])) +' new Activities being created' + '\n')
				
		print(	'New Groups:')
		for group in install['groups']:
			print(	'\n' + '\t' + group)
		
		print ( '\n' + 'New Activities:')
		for activity in install['activities']:
			print(	'\n' + '\t' + activity['floodlightActivityGroupName']+ ' - ' + activity['name'])
			activity['floodlightConfigurationId'] = configID
		
		print('\n')
		
	response = input('Install? <Y/N>:')
	response = response.upper().strip()
	
	#Process input and install
	if response == 'Y':
		#print('\n\t' + 'Im working I swear...')
		result = installFloodlights(install, existingGroups, google, configID)
	elif response == 'N':
		print('\t' + 'Installation cancelled.')
		sys.exit()
	else:
		print('\t' + 'Response not valid, program quitting.')
		sys.exit()
	
	#Confirm completion
	try:
		result
		print('Installation successful! \n')
		print('Program closing.')
	except NameError:
		print('Installation failed. \n')
		print('Program closing.')

def buildActivities(xl_parsed):
	floodlights = {
					'groups': [],
					'activities': []
						}
						
	for line in xl_parsed['lines']:
		floodlight = line 
		
		if (line['unique'] == 'YES') and (line['standard'] == 'YES'):
			buildStandard( line, floodlight, floodlights)
			#print(floodlight)
			#print(floodlights)
			buildUnique( line, floodlight, floodlights)
			#print(floodlight)
			#print(floodlights)			
		elif line['unique'] == 'YES':
			buildUnique( line, floodlight, floodlights)
			#print(floodlights)
		elif line['standard'] == 'YES':
			buildStandard( line, floodlight, floodlights)
			#print(floodlights)
		else:
			print('No countingMethod selected.  Program quitting.')
			sys.exit()
	
	return floodlights

def buildStandard( line, floodlight, floodlights):
	try:
		del floodlight['standard']
		del floodlight['unique']
	except KeyError:
		pass
	floodlight['countingMethod'] = 'STANDARD_COUNTING'
	floodlights['activities'].append(floodlight)
			
	try:
		floodlights['groups'].index(line['floodlightActivityGroupName'])
	except ValueError:
		floodlights['groups'].append(line['floodlightActivityGroupName'])

def buildUnique( line, floodlight, floodlights):
	try:
		del floodlight['standard']
		del floodlight['unique']
	except KeyError:
		pass
		
	floodlight2 = {
					'floodlightActivityGroupType': floodlight['floodlightActivityGroupType'],
					'name': floodlight['name'] + ' Unique',
					'floodlightActivityGroupName': floodlight['floodlightActivityGroupName'] + ' Unique',
					'countingMethod': 'UNIQUE_COUNTING',
					'expectedUrl': floodlight['expectedUrl']}
	floodlights['activities'].append(floodlight2)
			
	try:
		floodlights['groups'].index(line['floodlightActivityGroupName'] + ' Unique')
	except ValueError:
		floodlights['groups'].append(line['floodlightActivityGroupName'] + ' Unique')
			
def findGroups( inputGroups, allGroups):
	existingGroups = {}

	for inputGroup in inputGroups:
		for group in allGroups:
			if inputGroup == group['name']:
				existingGroups[group['name']] = group['id']
				break
	return existingGroups
	
def buildInstaller( floodlights, existingGroups, allActivities):
	installer = {	'groups': [],
					'activities': []
	}
	
	newgroups = floodlights['groups']
	installerGroups = []
	
	for floodlight in floodlights['activities']:
		index = 0
		
		if len(allActivities) == 0:
			installer['activities'].append(floodlight)
		
		for activity in allActivities:
			if (activity['name'] == floodlight['name']) and (activity['floodlightActivityGroupName'] == floodlight['floodlightActivityGroupName']):
				break
			
			if index == len(allActivities) - 1:
				installer['activities'].append(floodlight)
	
			index += 1
	
	for i in range(len(newgroups)):
		try:
			existingGroups[newgroups[i]]
		except KeyError:
			installerGroups.append(newgroups[i])
			
	print(newgroups)
	installer['groups'] = installerGroups
	
	return installer

def installFloodlights( floodlights, groups, api, configID):
	uniqueIDs = {}
	stdQueue = []

	for group in floodlights['groups']:
		newgroup = api.installFloodlightGroup({
			'name': group,
			'floodlightConfigurationId': configID,
			'type': 'COUNTER'
		})
		groups[newgroup['name']] = newgroup['id']
	
	for activity in floodlights['activities']:
		if activity['countingMethod'] == 'STANDARD_COUNTING':
			stdQueue.append(activity)
		else:
			activity['floodlightActivityGroupId'] = groups[activity['floodlightActivityGroupName']]
			newactivity = api.installFloodlightActivity(activity)
			uniqueIDs[newactivity['name']] = api.generateFloodlightTag(newactivity)['floodlightActivityTag']
	for stdActivity in stdQueue:
		try:
			stdActivity['defaultTags'] = [{
											'name': 'Unique',
											'tag': uniqueIDs[stdActivity['name'] + ' Unique']}]
			stdActivity['floodlightActivityGroupId'] = groups[stdActivity['floodlightActivityGroupName']]
			api.installFloodlightActivity(stdActivity)
		except KeyError:
			stdActivity['floodlightActivityGroupId'] = groups[stdActivity['floodlightActivityGroupName']]
			api.installFloodlightActivity(stdActivity)
	
if __name__ == '__main__':
	main()