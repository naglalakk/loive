import loive

import sys
import getopt
import pprint

def cmdLineHelp():
	help_list = {'-h'			 : 'List all commands',
				 '-q'		 : 'Exit shell',
				 'efx_local'     : 'Lists all local devices',
				 'efx_global' 	 : 'Lists all global devices / VST,AU plugins' ,
				 'pluginInfo'	 : 'Display all information about local/global plugin devices',
				 'version'	 : 'Display project version',
				 'print-summary' : 'Prints summary of ableton-project, tracks, plugins etc..' ,
				 'load'		 : 'Loads new als file',
				 'manufacturers' : 'Lists manufacturers of items that declare them' } 
	

	pprint.pprint(help_list)
	

def main(argv):
	
	command_args = { '-h'		  	 : 'cmdLineHelp()',
					 '-q'		  	 : 'exit()',
					 'efx_local'   	 : 'efx_local()',
					 'efx_global' 	 : 'efx_global()',
					 'pluginInfo'	 : 'getPluginInfo()',
					 'version'	  	 : 'print_live_version()',
					 'print-summary' : 'print_summary()',
					 'load'			 : 'load_new = raw_input("Path to new file: ")',
					 'manufacturers' : 'list_manufacturers()'} 

	if len(argv) < 2:
		sys.stderr.write("Usage: python loive.py [-File] \n")
		return 1

	filename = argv[1]
	command = None
	inputfile = ''

	lp = loive.Loive(filename)

	while True:

		if command in command_args:
			if command == '-h':
				exec(command_args[command])
			elif command == '-q':
				break
			else:
				if(command == 'load'):
					exec(command_args[command])
					print load_new
					loadcmnd = 'lp = loive.Loive("' + load_new  +'")'
					exec(loadcmnd)
			
				else:	
					cat_string = 'lp.' + command_args[command]
					exec(cat_string)
		
		command = raw_input('==> ')	
if __name__ == "__main__":
		main(sys.argv)	
