import sys
from collections import defaultdict #for multimap
import ReadMetadata as readM
import ReadData as readD
import ParserFile as parser
import End 

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
if "*" in select_list[0]: #may need where comditions
	print ("\n")
	exit()

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
		print (tab, end = "|")
	print ("")
	for tab in select_list[1:]:
		print ("========", end = "|")
	print("")
	

	for i in index_set:
		for tab in select_list[1:]:
			print (main_db_list [tab][i], end = " \t|")
		print ("")
	print ("\n")
	exit()
	#End.happy_exit()
#========= 3.MULTI COL FROM MULTI TAB ============
