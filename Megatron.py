import sys
from collections import defaultdict #for multimap
import ReadMetadata as readM
import ReadData as readD
import ParserFile as parser


#======== METADATA ===================================
table_names = defaultdict(list)  #MULTIMAP
readM.read_metadata(table_names)

#======== PARSING CMD ================================
cmd_raw = sys.argv[1:]
select_list = []
from_list = []
condition_list = []
parser.parse (cmd_raw, select_list, from_list, condition_list)

#======== CONFLICTING COLOUMN ERR ===================
print ("\n\n==== col err ====")
for requested_col in select_list:
	print (requested_col)
	count = 0
	for tab in table_names:
		#if re.match('hello[0-9]+', 'hello1'): #REGEX
		if ((requested_col in map(str.lower, table_names[tab]))):# or (re.match(requested_col in map(str.lower, table_names[tab]))): ERR HANDLING REAAINS
			count += 1
	print (count)

	if count > 1:
		print (" ERROR : CONFLICTING COLOUMNS ")
		exit()
	
	if count == 0 and ('.' in requested_col ==0):
		print (" ERROR : COLOUMN NOT FOUND ")
		exit()

#======== Col->Table.col=============================
print("\n== col-> tab.col ===")
for (i,requested_col) in enumerate(select_list):
	for tab in table_names:
		if ((requested_col in map(str.lower, table_names[tab]))):
			select_list[i] = tab + "." + requested_col
			break;

print ("SELECT" , end = " : ")
for wrd in select_list:
	print (wrd, end = " ")
print ("\nFROM", end = " : ")
for wrd in from_list:
	print (wrd, end = " ")
print ("\nWHERE" , end = " : ")
for wrd in condition_list:
	print (wrd, end = " ")
print (" ")
#======== DATASTRUCTURE ==============================
#1. LIST of lists (T1.A[], T2.X[], T2.Y[])
#2. LIST of multimap,
# tablename.col name gives which hashTable, 
# then second key gives key for hash
# output is a list of values in list form
main_db_list = defaultdict (list) #MULTIMAP
main_db_multimap = [defaultdict(list)]

#======== READING DB =================================
readD.read(table_names, main_db_list, main_db_multimap)

#======== WHERE ======================================
if len(condition_list) == 0:
	from_list[-1] = from_list[-1].rstrip(';')
	condition_list.append("1=1;")

condition_list[-1] = condition_list[-1].rstrip(';')
print ("=====WHERE : ======")
or_list = []
or_part = []
flag = 0
for conds in condition_list:
	if conds == "or":
		new_list = or_part[:]
		or_list.append(new_list)
		or_part.clear()
	else:
		or_part.append(conds)

or_list.append(or_part)
print ("  OR LIST: ")
for or_pt in or_list:
	print (or_pt)