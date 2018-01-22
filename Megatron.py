import sys
import os
from collections import defaultdict #for multimap
import ReadMetadata as readM
import ParserFile as parser
import csv 			# to read csv files


#======== METADATA ===================================
table_names = defaultdict(list)  #MULTIMAP
readM.read_metadata(table_names)

#======== PARSING CMD ================================
cmd_raw = sys.argv[1:]
select_list = []
from_list = []
condition_list = []
parser.parse (cmd_raw, select_list, from_list, condition_list)

#======== DATASTRUCTURE ==============================
#1. LIST of lists (T1.A[], T2.X[], T2.Y[])
main_db_list = defaultdict (list) #MULTIMAP

#2. LIST of multimap,
# tablename.col name gives which hashTable, 
# then second key gives key for hash
# output is a list of values in list form
main_db_multimap = [defaultdict(list)]

#======== READING DB =================================
print ("\n")

for table in table_names:
	table_name = table + ".csv"
	with open(table_name, 'r') as f:	#Reading full CSV
		reader = csv.reader (f)
		listx = list (reader)			
	
	count = -1
	for sublist in listx:
		count += 1
		for item, col in zip(sublist, table_names[table]):
			key = table+"."+col
		#INSERT IN LIST
			main_db_list [key].append(item)
		#INSERT IN MAP
		#	main_db_multimap [key][item] = count


for d in main_db_list:
	print (d+ ": "+ str(main_db_list[d]))


