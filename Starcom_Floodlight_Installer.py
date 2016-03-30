## Starcom_Floodlight_Installer
## Adam Stein, Patrick Nogacz, Cahle Johnson
## 3-18-2016

from xl import *
from oauth2client import client

import gapi
import argparse

#Google API scope
API_SCOPE = 'https://www.googleapis.com/auth/dfatrafficking'

#Google API name
API_NAME = 'dfareporting'

#API Version
API_VERSION = 'v2.4'

#API credential storage
API_STORE = 'store.dat'


def main():
	#Process Arguments
	parser = argparse.ArgumentParser(description = 'Upload Floodlights to DBM')
	parser.add_argument("file")
	args = parser.parse_args()
	path = str(args.file)
	
	#Process Excel sheet to floodlight list
	floodlights = xl_parse(path)
	
	configID = gapi.getConfigId( floodlights['profileID'], floodlights['advertiserID'])
	print(configID)
			
if __name__ == '__main__':
	main()