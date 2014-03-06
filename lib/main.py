__author__ = 'Galkan'
__version__ = '1.0'
__date__ = '2014/01/12'

try:
        import sys
        import argparse
	import os
	from config import Config_Parser
	from exceptions import SeesExceptions
	from common import *
except ImportError,e:
        import sys
        sys.stdout.write("%s\n" %e)
        sys.exit(1)


def is_file_exists(file_list):

	for file in file_list:
        	if not os.path.exists(file):
			print >> sys.stderr, bcolors.OKBLUE + "Error : " + bcolors.ENDC + bcolors.FAIL + "The file \"%s\" doesn't Exists On The System !!!"% (file) + bcolors.ENDC
			sys.exit(2)  
		

class AddressAction(argparse.Action):

        def __call__(self, parser, args, values, option = None):
                args.options = values

                if args.attach:
			if not args.options:
                        	parser.error("Usage --attach <file1 file2 file3> ")
			else:
				is_file_exists(args.options)

class Main:

	def __init__(self):

		parser = argparse.ArgumentParser()
                group_parser = parser.add_mutually_exclusive_group(required = True)

                group_parser.add_argument('--attach', dest='attach', action='store_const', const='attach', help="Attach Email")
                group_parser.add_argument('--text', dest='text', action='store_const', const='text', help="Text Email")

                parser.add_argument('options', nargs='*', action = AddressAction)
                parser.add_argument('--config_file', '-c', action = 'store', dest = 'config_file', help = "Configuration Files", metavar="FILE", required = True)
                parser.add_argument('--mail_user', '-m', action = 'store', dest = 'mail_user_file', help = "Mail User File", metavar="FILE", required = True)
                parser.add_argument('--html_file', '-f', action = 'store', dest = 'html_file', help = "Content of Html File" ,metavar="FILE", required = True)
                parser.add_argument('--verbose', '-v', action = 'store_true', help = "Verbose For Eending Email", default = False)
		
                self.args = parser.parse_args()

		file_list = (self.args.config_file,self.args.mail_user_file,self.args.html_file)
		is_file_exists(file_list)
		
	
	def run(self):

		parser = Config_Parser(self.args.config_file)

		try:	
			if self.args.attach:
				parser.run(self.args.mail_user_file, self.args.attach, self.args.html_file, self.args.verbose,  self.args.options)
			else:
				parser.run(self.args.mail_user_file, self.args.text, self.args.html_file, self.args.verbose,  None)
		except SeesExceptions, mess:
			raise SeesExceptions("%s"% mess)
