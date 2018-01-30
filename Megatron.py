import sys
from collections import defaultdict #for multimap
import ReadMetadata as readM
import ReadData as readD
import ParserFile as parser
import End 
import numpy
import itertools


End.happy_start()
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
	for tab in table_names: #from_list
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
for (i,requested_col) in enumerate(condition_list):
	for tab in table_names:
		if ((requested_col in map(str.lower, table_names[tab]))):
			condition_list[i] = tab + "." + requested_col
			break;

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


#============= QUERY HANDLING ======================
print ("===== QUERY HANDLING ======")
print ("select_list[0] = " + select_list[0])

#============ 2.Trivial AGGREGATES ================	
if "max" in select_list[0]:
	tablename = str(from_list[0]) + "." +str(select_list[0][4:-1])
	print ("Max (" + tablename + ") ")
	print (max (main_db_list [tablename]))
	print()
	exit()
	
if "min" in select_list[0]:
	tablename = str(from_list[0]) + "." +str(select_list[0][4:-1])
	print ("Min (" + tablename + ") ")
	print (min (main_db_list [tablename]))
	print()
	exit()
	
if "avg" in select_list[0]:
	tablename = str(from_list[0]) + "." +str(select_list[0][4:-1])
	print ("Avg (" + tablename + ") ")
	print (float (sum(main_db_list [tablename]))/ float(len(main_db_list [tablename])))
	print()
	exit()
	
if "sum" in select_list[0]:
	tablename = str(from_list[0]) + "." +str(select_list[0][4:-1])
	print ("Sum (" + tablename + ") ")
	print (sum (main_db_list [tablename]))
	print ("")
	exit()
	



#========== 4.DISTINCT ============================
if "distinct" in select_list[0]: #using set
	prev_size = 0
	new_size = 0
	ans_set = set()
	index_set = set()
	
	for (i,val) in enumerate (main_db_list [select_list[1]] ):
		prev_size = len(ans_set)
		ans_set.add(val)
		new_size = len(ans_set)
		
		if (prev_size != new_size):
			index_set.add(i)

	for tab in select_list[1:]:
		print (tab, end = ",")
	print ("")
	
	for i in index_set:
		for tab in select_list[1:]:
			print (main_db_list [tab][i], end = ",")
		print ("")
	print ("\n")
	exit()
	#End.happy_exit()

#========= 1.ALL ============

if "*" in select_list[0]: #may need where comditions
	print (from_list)
	replacing_list = []
	for tab in from_list: 
		for col in table_names[tab]:
			replacing_list.append(tab+"."+col.lower())
	select_list = replacing_list[:]
	print (select_list)
	print ("\n")
	

#========= 3.MULTI COL FROM MULTI TAB ============
select_list.sort()
print (select_list)
ans_meta = defaultdict (list)


tab_col = []
for val in select_list:
	tab_col = [val.split(".")]
	ans_meta[tab_col[0][0]].append(tab_col[0][1])

for d in ans_meta:
	print (d+ ": "+ str(ans_meta[d]))

print (" ==--==")
ans_data = []
#creating first table
first_table = ""
for tabNm in ans_meta:
	first_table = tabNm
	for (i,colnm) in enumerate(ans_meta[tabNm]):
		idf = (tabNm + "." + colnm)
		ans_data.append(list(main_db_list[idf]))
	break
#repeating values xN times 
size_of_before_table = 0
for tab in ans_meta:
	if tab != first_table:
		size_of_before_table = len(ans_data[0])
		idf = (tab+ "." + ans_meta[tab][0])
		for (i,ans_col) in enumerate (ans_data):
			ans_data[i] = (numpy.repeat (ans_col,len(main_db_list[idf])) )
#appending new cols
		for col in ans_meta[tab]:
			idf = (tab + "." + col)
			ans_data.append(main_db_list[idf]*size_of_before_table)

for col in select_list:
	print (col, end = ",")
print ("")

for i in range(len(ans_data[0])):
	for (j,col) in enumerate(select_list):
		print (ans_data[j][i], end = ",")
	print("")
print ("\n")