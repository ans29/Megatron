import csv 			# to read csv files

def read (table_names, main_db_list, main_db_multimap):
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
