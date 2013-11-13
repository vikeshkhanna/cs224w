import json
import sys
import gzip
from parser.yajl_helper import *
from parser.events import *

def parse_inner(data_file, processor):
	f = None

	if data_file.index("gz")==len(data_file)-2:
		f = gzip.open(data_file, 'rb')
	else:
		f = open(data_file, 'r')
		
	# Create an instance of the appropriate processor
	parser = YajlParser(ContentHandler(processor))
	parser.allow_multiple_values = True
	parser.parse(f=f)
	
	f.close()

def parse(data_file, db_file):
	processor = BaseProcessor(db_file)
	
	try:
		parse_inner(data_file, processor)
	except:
		pass

	# Parse the entire file and then commit db and close connection
	processor.action()
	
def main(args):	
	if len(args)<3:
		print("Usage: python program.py <gz_file> <db_file>")
		sys.exit(1)
	
	data_file = args[1]
	db_file = args[2]
	
	parse(data_file, db_file)	
	return 0

if __name__ == "__main__":
	main(sys.argv)

