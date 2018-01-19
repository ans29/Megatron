import sys
import os
from collections import defaultdict #for multimap
import re  							#for spliting over multiple delimeters
import ReadMetadata as readM

table_names = defaultdict(list)  #MULTIMAP
readM.read_metadata(table_names)


#=========PARSING CMD================================
cmd_raw = sys.argv[1:]
print ("cmd", end = " : ");
#re.split('; |, |\*|\n',a)
cmd_split = re.split( '; |,| |\n' , (cmd_raw[0].lower()))
print(cmd_split)
cmd_split = ((cmd_raw[0].lower()).replace(",", " ")).split()
print(cmd_split)
print (cmd_split[-1])
print (cmd_split[-1][-1])
#=====================================================
'''
	select  
			(*, A, A,B,C,) (sum(A), avg(A)) + distinct|all ) 
	from
			tableName
	where
			asdasd
'''

