__author__ = 'Galkan'
__version__ = '1.0'
__date__ = '2014/01/12'


try:
	import sys
	import re
	import socket
	import time
	import random
        from ConfigParser import SafeConfigParser
	from exceptions import SeesExceptions
	from smtp import Smtp
	from common import *
	from version import *
except ImportError,e:
        import sys
        sys.stdout.write("%s\n" %e)
        sys.exit(1)


class Config_Parser:
	"""
		Configuration Parser ...
	"""

	def __init__(self, config_file):

		self.comment_reg = re.compile("^[#|;].*")
                self.exit_reg = re.compile("^exit$")

		self.config_file = config_file
		self.cmd_parser = SafeConfigParser()
		self.cmd_parser.read(self.config_file)

	
	def random_time(self, interval):
		"""
			Create random time
		"""	

		return random.randrange(int(interval[0]),int(interval[1]))

		
	def run(self, mail_user_file, attach_or_not, html_file, verbose, attach_list = None):
                """
                        Configuration File Parser
                """

                for section_name in self.cmd_parser.sections():
                        if section_name == "mail":
                                for name, value in self.cmd_parser.items(section_name):
                                        if name == "domain":
                                                domain = value
                        elif section_name == "smtp":
                                for name,value in self.cmd_parser.items(section_name):
                                        if name == "server":
                                                server = value
                                        elif name == "time":
                                                wait_time = value
                        else:
				print >> sys.stderr, bcolors.OKBLUE + "Error : " + bcolors.ENDC + bcolors.FAIL + "Wrong Parametre Usage In The Config File: %s"% (self.config_file) + bcolors.ENDC
				sys.exit(2)

                try:
                        sock = socket.socket()
                        sock.connect((server,25))
                except:
			raise SeesExceptions("Please check your smtp server, netstat -nlput | grep 25")


		try:
                	read_file = open(mail_user_file, "r").read().splitlines()
		except Exception, mess:
			raise SeesExceptions("Error: %s"%  mess)


                for  line in read_file:
                        if re.search (self.exit_reg, line):
                                print >> sys.stdout, bcolors.FAIL + "%s"% (message) + bcolors.ENDC
                                sys.exit (3)

                        elif re.search(self.comment_reg, line):
                                continue

                        else:
				if not len(line.split(":")) == 4:
					print >> sys.stderr, bcolors.OKBLUE + "Warning : " + bcolors.ENDC + bcolors.FAIL + "Line must be \"X:X:X:X\" format," + bcolors.OKBLUE +  "But line is " + bcolors.ENDC + bcolors.FAIL+ "%s"% (line) + bcolors.ENDC
				else:
                                	from_mail_header = line.split(":")[0]
                                	from_mail_gecos = line.split(":")[1]
                                	subject = line.split(":")[2]
                                	mail_to = line.split(":")[3]

					time_interval = wait_time.split(",")
					if len(time_interval) == 2:
						wait = self.random_time(time_interval)
					else:
						wait = int(wait_time.split(",")[0])

					smtp = Smtp()
                			if attach_or_not == "attach":	
                        			smtp.main(attach_or_not, from_mail_header, from_mail_gecos, mail_to, subject, server, domain, html_file, verbose, attach_list)
                			else:
                        			smtp.main(attach_or_not, from_mail_header, from_mail_gecos, mail_to, subject, server, domain, html_file, verbose, attach_list)

                                	time.sleep(float(wait))
