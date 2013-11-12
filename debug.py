import json
import sys
from parser.yajl_helper import *
from parser.events import *
from parse import parse_inner

# Returns the deserialized JSON objects of interests

def main(args):
	data_file = args[1]
	event = args[2]
	cnt = 1

	if len(args)>3:
		cnt = int(args[3])

	# Create an instance of the appropriate processor
	processor = DebugProcessor(event, cnt)
	parse_inner(data_file, processor)
	return 0

if __name__ == "__main__":
	main(sys.argv)

