import sys
import os
from collections import defaultdict #for multimap
import ReadMetadata as readM
import ParserFile as parser

table_names = defaultdict(list)  #MULTIMAP
readM.read_metadata(table_names)


#=========PARSING CMD================================
cmd_raw = sys.argv[1:]
select_list = []
from_list = []
condition_list = []
parser.parse (cmd_raw, select_list, from_list, condition_list)