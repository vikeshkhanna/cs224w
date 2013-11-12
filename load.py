import sys
import os
from datetime import *
from subprocess import call
from parse import *

STREAM="-stream"
DB_FILE="-db"
DATE1="-date1"
DATE2="-date2"
DELIM=":"
FORMAT="%Y-%m-%d-%H"
BASE_URL="http://data.githubarchive.org"

online = True
data_root=""
db_file=""
date1 = None
date2 = None
 
def usage():
	return "Usage: ./program.py -date1:2012-10-11-1 -date2:2012-10-11-2 -stream:online/path -db:xyz.db"

def get_filename(date):
	filename = datetime.strftime(date, FORMAT)
	return "%s.json.gz"%filename

def fetch_file(filename):
	url = "%s/%s"%(BASE_URL, filename)
	call(["wget", url])

args = sys.argv[1:]
if len(args)<4:
	print(usage())
	sys.exit(1)

for arg in args:
	if arg.find(STREAM)==0:
		value = arg.split(DELIM)[1]
		
		if value=="online":
			online=True
		else:
			online=False
			data_root=value

	elif arg.find(DB_FILE)==0:
		db_file = arg.split(DELIM)[1]
	
	elif arg.find(DATE1)==0:
		value = arg.split(DELIM)[1]
		date1 = datetime.strptime(value, FORMAT)

	elif arg.find(DATE2)==0:
		value = arg.split(DELIM)[1]
		date2= datetime.strptime(value, FORMAT)
	
	else:
		print(usage())
		sys.exit(1)

print("Online: %s" % str(online))

while date1<date2:
	data_file = get_filename(date1)
	
	if online:
		#fetch file
		fetch_file(data_file)
		
		#parse
		try:
			parse(data_file, db_file)
			os.remove(data_file)
		except:
			print("Could not parse/remove the file: %s. Reason: %s" % (data_file, sys.exc_info()))

	else:
		data_path = os.path.join(data_root, data_file)
		del_after = False
	
		if not os.path.isfile(data_path):
			fetch_file(data_file)
			data_path = data_file
			del_after = True
	
		parse(data_path, db_file)
			
		if del_after:
			os.remove(data_path)	

	date1 = date1 + timedelta(hours=1)

#print date1, date2, online, data_root, db_file
