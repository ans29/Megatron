
def parse (cmd_raw, select_list, from_list, condition_list):

	print ("cmd", end = " : ");
	cmd_split = ((cmd_raw[0].lower()).replace(",", " ")).split()

	if (cmd_split[-1][-1] != ';'):
		print ("\tSYNTAX ERR : missing ';'")
		exit()

	print(cmd_split)

	flag = 0
	for wrd in cmd_split:
		if (wrd == "select"):
			flag = 1
		elif (wrd == "from"):
			flag = 2
		elif (wrd == "where"):
			flag = 3
		elif (flag == 1):
			select_list.append (wrd)
		elif (flag == 2):
			from_list.append (wrd)
		elif (flag == 3):
			condition_list.append (wrd)

	print ("\nSELECT" , end = " : ")
	for wrd in select_list:
		print (wrd, end = " ")
	print ("\nFROM", end = " : ")
	for wrd in from_list:
		print (wrd, end = " ")
	print ("\nWHERE" , end = " : ")
	for wrd in condition_list:
		print (wrd, end = " ")


#=====================================================
'''
	select  
			(*, A, A,B,C,) (sum(A), avg(A)) + distinct|all ) 
	from
			tableName
	where
			asdasd
'''
