#Loive - Interactive command line API for ableton live

import xml.etree.ElementTree as ET
import pprint

from colorama import init
from colorama import Fore,Back,Style

#We introduce class Loive, were everything
#always goes smoothe...
class Loive:

	def __init__(self, cmands):
		#Temporary, this means all string must match
		#find a handler for this later,
		self.args = cmands
		self.tree = ET.parse(self.args)
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
		pp = pprint.PrettyPrinter(indent=4)
		pp.pprint(self.clean_local_list)

		print '\n'
		
		print(Fore.RED + 'Global Effects/VST: \n')
		pp.pprint(self.global_ext_list)


	def live_version(self):
		#returns verison number in string format

		minorVersion = '[Ableton live minor version: '

		if len(self.root.attrib) == 2:
			print(Style.BRIGHT + Fore.MAGENTA + minorVersion + self.root.attrib['MinorVersion'] + ']')

		else:
			print(Style.BRIGHT + Fore.MAGENTA + '[' + self.root.attrib['Creator'] + ']')
		
		
		
