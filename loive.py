#Loive - Interactive command line API for ableton live

import xml.etree.ElementTree as ET
import pprint
import shutil
import os.path, time
import gzip

from subprocess import call

from colorama import init
from colorama import Fore,Back,Style

#We introduce class Loive, were everything
#always goes smoothe...
class Loive:

	def __init__(self, cmands, fpath=False):
		#Temporary, this means all string must match
		#find a handler for this later,
		self.args = cmands
		
		#Store full path:
		self.hasfp = fpath

		if fpath:
			self.full_path = cmands
		else:
			self.full_path = os.getcwd()

		#zipped

		self.zipped = self.full_path + '/' + cmands

		self.strip_string = cmands.split('.', 1)[0]
	
		conversionString = self.strip_string + '.gz'

		#XML-Conversion
		if fpath:
			shutil.copyfile(self.full_path, conversionString)
			gzip_path = conversionString
		else:
			shutil.copyfile(self.full_path + '/' + cmands, conversionString)
			gzip_path = self.full_path + '/' + self.strip_string + '.gz'
	
	
		call(["gunzip", gzip_path])
		
		self.tree = ET.parse(self.strip_string)
		self.root = self.tree.getroot()

		#Perform queries at initialization
		self.run_query()
		#Fetch local-plugin data
		self.efx_local()
		#Fetch external plugin data (VST, AU etc..)
		self.efx_global()

		#Initialize colors
		init(autoreset=True)
	
	def run_query(self):		
		#Track listing

		self.track_query = self.root.findall(".//LiveSet//Tracks/")
		self.track_count = len(self.track_query)
	

		#Local plugin query
		#Fetches all local Devices, Ableton effects, non vst-plugins
		self.local_xml_query = ".//LiveSet//Tracks//DeviceChain//Devices[1]/*"
		self.local_elems  = self.root.findall(self.local_xml_query) 

		#Global plugin query

		self.vst_xml_query = ".//LiveSet//Tracks//DeviceChain//Devices//PluginDevice//PluginDesc//VstPluginInfo//PlugName"
		self.vst_elem = self.root.findall(self.vst_xml_query)

		#We need special query for Au plugins
		self.AU_query = ".//LiveSet//Tracks//DeviceChain//Devices//AuPluginDevice//PluginDesc//AuPluginInfo/Name"
		self.AuPlugs = self.root.findall(self.AU_query)
	

	def efx_local(self):
		
		self.list_values 	  = []
		self.clean_local_list = []
		
		#Extract values
		for e in self.local_elems:
			self.list_values.append(e.tag)
	
		#Remove duplicates
		self.clean_local_list = list(set(self.list_values))
		
		return self.clean_local_list

	def efx_global(self):
		
		#Follow Au or Ableton devices and are useless
		default_a = 'AuPluginDevice'
		default_b = 'PluginDevice'

		#Setup containers
		self.vst_list 		 = []
		self.Au_list  	 	 = []
		self.global_ext_list = []

		#Extract values
		for v in self.vst_elem:
			self.vst_list.append(v.attrib['Value'])

		for au in self.AuPlugs:
			self.Au_list.append(au.attrib['Value'])

		#Remove duplicates
		self.clean_vst_list = list(set(self.vst_list))
		self.clean_au_list  = list(set(self.Au_list))

		#construct one final list
		self.global_ext_list = self.clean_vst_list + self.clean_au_list

		return self.global_ext_list

	def getPluginInfo(self):
		#Very simple, fetches local/global plugin info
		#Prints it out

		print(Fore.RED + 'Ableton Effects: \n')
		pl = pprint.PrettyPrinter(indent=4)
		pl.pprint(self.clean_local_list)

		print '\n'
		
		print(Fore.RED + 'Global Effects/VST: \n')
		pe = pprint.PrettyPrinter(indent=4)
		pe.pprint(self.global_ext_list)

		print '\n'

	def live_version(self):
		#returns verison number in string format

		minorVersion = '[Ableton live minor version: ' + self.root.attrib['MinorVersion'] + ']'

		if len(self.root.attrib) == 2:
			return minorVersion

		else:
			creator_str = self.root.attrib['Creator']
			return creator_str
		

	def print_summary(self):
	
		print '\n'
	
		if self.hasfp:
			nameis = os.path.basename(self.args)
	
			print 'Name : ' + nameis
			print 'Full path : ' + self.args

		else:
			print 'Name : ' + self.args
			print 'Full path : ' + self.full_path
		
		print 'Version : ' + self.live_version()

		print '\n'

		print( 'Number of tracks : ' + str(self.track_count))

		print '\n'

		self.getPluginInfo()
		
		print '\n'			

		if self.hasfp:
			print "last modified: %s" % time.ctime(os.path.getmtime(self.full_path))
			print "created: %s" % time.ctime(os.path.getctime(self.full_path))
		else:
			print "last modified: %s" % time.ctime(os.path.getmtime(self.zipped))
			print "created: %s" % time.ctime(os.path.getctime(self.zipped))
		

		
		
		
		
