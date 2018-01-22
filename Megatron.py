import sys
import os
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

#======== DATASTRUCTURE ==============================
#1. LIST of lists (T1.A[], T2.X[], T2.Y[])
main_db_list = defaultdict (list) #MULTIMAP

#2. LIST of multimap,
# tablename.col name gives which hashTable, 
# then second key gives key for hash
# output is a list of values in list form
main_db_multimap = [defaultdict(list)]

#======== READING DB =================================
readD.read(table_names, main_db_list, main_db_multimap)


