import json
import sys
from parser.yajl_helper import *
from parser.events import *

# Returns the deserialized JSON objects of interests

def main(args):	
	if len(args)<2:
		print("Usage: python program.py <db_file>")
		sys.exit(1)
	
	db_file = args[1]

	# Create an instance of the appropriate processor
	processor = BaseProcessor(db_file)
	parser = YajlParser(ContentHandler(processor.process))
	parser.allow_multiple_values = True
	parser.parse()
	return 0

if __name__ == "__main__":
	main(sys.argv)

