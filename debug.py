import json
import sys
from parser.yajl_helper import *
from parser.events import *

# Returns the deserialized JSON objects of interests

def main(args):
	event = args[1]
	cnt = 1

	if len(args)>2:
		cnt = int(args[2])			

	# Create an instance of the appropriate processor
	processor = DebugProcessor(event, cnt)
	parser = YajlParser(ContentHandler(processor.process))
	parser.allow_multiple_values = True
	parser.parse()
	return 0

if __name__ == "__main__":
	main(sys.argv)

