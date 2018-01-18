import sys
import os
from collections import defaultdict #for multimap
import ReadMetadata as readM

table_names = defaultdict(list)  #MULTIMAP
readM.read_metadata(table_names)


#=========PARSING CMD================================
cmd_raw = sys.argv[1:]
print ("cmd", end = " : ");
cmd_split = (cmd_raw[0].lower()).split()
print(cmd_split)

#=====================================================

