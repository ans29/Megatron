import time;
import sys;

start_t = 0
end_t = 0

def happy_start():
	start_t = time.time()

def happy_exit():
	end_t = time.time()
	print ("\n\n\t TIME TAKEN ", end= ": ")
	print (end_t - start_t , end = " micro-seconds\n")
	exit()