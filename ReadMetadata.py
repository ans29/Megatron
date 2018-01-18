#read metadata=====================================
def read_metadata(table_names):
	try:
		meta_file = open ("metadata.txt", "r")
	except IOError:
		print ("\n\t ERROR : metadata file not found\n\t EXITING..")
		exit()

	current_table = ''
	flag = 0
	for line in meta_file:
		line = line[:-1]
		if (flag == 0 and line == "<begin_table>"):
			flag = 1;
		elif (flag == 1):
			current_table = line
			flag = 2
		elif (line == "<end_table>" or line == "<end_table"):
			flag = 0;
		elif (flag == 2):
			table_names [current_table].append(line)

	print ("=====TABLES : =====");
	for d in table_names:
		print (d + ": " + str(table_names[d]))
	print ("===================\n");
