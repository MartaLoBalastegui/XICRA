#usr/bin/env python

## useful imports
import time
import io
import os
import re
import subprocess
import sys
from datetime import datetime
import concurrent.futures
from termcolor import colored
import pandas as pd

########################################################################
######## 					TIME								######## 					
########################################################################

###############   
def print_time ():
	"""Prints time stamp in human readable format: month/day/year, hour:minute:seconds."""
	now = datetime.now()
	date_time = now.strftime("%m/%d/%Y, %H:%M:%S")
	print ('\t' + date_time + '\n')

###############   
def gettime (start_time):
	"""Obtains time stamp in human readable format: hour:minute:seconds from a time.time() format timestamp."""
	total_sec = time.time() - start_time
	m, s = divmod(int(total_sec), 60)
	h, m = divmod(m, 60)
	return h, m, s

###############	
def timestamp (start_time_partial):
	"""Prints a stamp of the time spent for a process in human readable format: hour:minute:seconds.
	Returns time in format time.time().
	"""
	h,m,s = gettime(start_time_partial)
	print_sepLine("-", 25, False)
	print ('(Time spent: %i h %i min %i s)' %(int(h), int(m), int(s)))
	print_sepLine("-", 25, False)
	return time.time()

###############	
def print_time_stamp (out):
	"""Prints out timestamp in a file provided. Format: time.time()"""
	timefile = open(out, 'w')    
	string2write = str(time.time())
	timefile.write(string2write)
	return()

###############	
def read_time_stamp (out):
	"""Reads timestamp from a file provided. Format: time.time()"""
	st_hd = open(out, 'r')
	st = st_hd.read()
	st_hd.close()
	stamp = datetime.fromtimestamp(float(st)).strftime('%Y-%m-%d %H:%M:%S')
	return(stamp)

###############	
def get_diff_time(stamp):
	"""Obtains the time spent for a process in days given a stamp in time.time() format.
	Returns days passed since.
	"""

	time_today = time.time()
	elapsed = time_today - float(time_today)
	days_passed = int((elapsed/3600)/24)
	return(days_passed)

###############    
def create_human_timestamp():
	"""Generates human timestamp for the date of day in format (yearmonthday): e.g. 20191011"""
	now = datetime.now()
	timeprint = now.strftime("%Y%m%d")
	return timeprint


###############
def create_subfolder (name, path):
	"""Create a subfolder named 'name' in directory 'path'. Returns path created."""
	## create subfolder  ##	
	subfolder_path = path + "/" + name
	access_rights = 0o755

	# define the access rights
	try:
		os.mkdir(subfolder_path, access_rights)
	except OSError:  
	   	#print ("\tDirectory %s already exists" % subfolder_path)
		return subfolder_path
	else:  
		print (colored("Successfully created the directory %s " % subfolder_path, 'yellow'))

	return subfolder_path

    
###############  
def create_folder (path):
	"""Create a folder directory 'path'. Returns path created."""

	## create subfolder  ##	
	access_rights = 0o755

	# define the access rights
	try:
		os.mkdir(path, access_rights)
	except OSError:  
		#print ("\tDirectory %s already exists" %path)
		return path
	else:  
		print (colored("Successfully created the directory %s " %path, 'yellow'))

	return path


############### 
def get_symbolic_link (sample_list, path_to_samples, directory):
	for samplex in sample_list:
		sample_path = path_to_samples + '/' + samplex
		cmd = 'ln -s %s %s' %(sample_path, directory)
		system_call(cmd)

	files2return = os.listdir(directory)
	return files2return

###############
def system_call(cmd):	
	## call system
	## send command	
	try:
		subprocess.check_output(cmd, shell = True)
		return ('OK')
	except subprocess.CalledProcessError as err:
		print (err.output)
		return ('FAIL')

###############	
def extract(fileGiven):
	print ("")
	#xtract(fileGiven, all=True)
	
###############
def sender(list_cmd, num_threads):	
	# We can use a with statement to ensure threads are cleaned up promptly
	with concurrent.futures.ThreadPoolExecutor(max_workers=num_threads) as executor:
		# Start the load operations and mark each future with its URL
		commandsSent = { executor.submit(command_sender, commands): commands for commands in list_cmd }	
		for cmd2 in concurrent.futures.as_completed(commandsSent):
			details = commandsSent[cmd2]
			try:
				data = cmd2.result()
			except Exception as exc:
				print ('***ERROR:')
				print (string2send)
				print('%r generated an exception: %s' % (details, exc))
###############

###############
def command_sender(string2send):
	#print (string2send)
	try:
		subprocess.check_output(string2send, shell = True)
	except subprocess.CalledProcessError as err:
		print ('')
###############

def retrieve_matching_files(folder, string):
	"""Lists folder path provided and given a string to search, returns all files ending with the given string"""
	my_all_list = get_fullpath_list(folder)
	matching = [s for s in my_all_list if s.endswith(string)]
	return (matching)

############### 
def get_symbolic_link_file (file2link, newfile):
	"""Creates symbolic link for a file into a new name file"""
	cmd = 'ln -s %s %s' %(file2link, newfile)
	system_call(cmd, returned=False)

#################
def get_fullpath_list(dir_given):
	"""Retrieve full absolute path for the files within a directory specified.

	:param dir_given: Directory to retrieve files
	:type dir_given: string

	:returns: List of absolute path files.
	"""
	return_path = []
	for root, dirs, files in os.walk(dir_given):
		for f in files:
			return_path.append(os.path.join(root,f))
	return return_path


############################################################################
######## 					AESTHETICS								######## 					
############################################################################
def pipeline_header():
	"""
	Prints a common header for the pipeline including name, author, copyright and year.	    
	"""
	print ("\n")
	print_sepLine("#", 70, False)
	print('#', '{: ^66}'.format("XICRA pipeline"), '#')
	print('#', '{: ^66}'.format("Jose F. Sanchez & Lauro Sumoy"), '#')
	print('#', '{: ^66}'.format("Copyright (C) 2019-2020 Lauro Sumoy Lab, IGTP, Spain"), '#')
	print_sepLine("#", 70, False)

###############
def print_sepLine(char, num, color):
	string = char * num
	if (color):
		print (colored(string, color))
	else:
		print (string)

###############
def boxymcboxface(message):
	## this function is from ARIBA (https://github.com/sanger-pathogens/ariba)
	## give credit to them appropiately
   	#print('-' * 79)
	print ('\n')
	print('|', '=' * 50, '|', sep='')
	print('|', '{: ^48}'.format(message), '|')
	print('|', '=' * 50, '|', sep='')
	print ('\n')
    #print('-' * 79)

###############
def outdir_project(outdir, project_mode, pd_samples, mode):
	"""
	"""
	# Group dataframe by sample name
	sample_frame = pd_samples.groupby(["new_name"])

	dict_outdir = {}	
	for name, cluster in sample_frame:
		print (name)
		if (project_mode):
			#print ("Create subdir for every sample: ", mode)
			sample_dir = create_subfolder('data', outdir)		

			## create sample
			sample_name_dir = create_subfolder(name, sample_dir)		

			## create subdir sub sample
			mode_name_dir = create_subfolder(mode, sample_name_dir)		
			dict_outdir[name] = mode_name_dir

		else:
			#print ("All samples share same folder")
			sample_name_dir = create_subfolder(name, outdir)		
			dict_outdir[name] = sample_name_dir

	return (dict_outdir)

###############
def print_all_pandaDF(pd_df):
	pd.set_option('display.max_colwidth', None)
	pd.set_option('display.max_columns', None)
	print (pd_df)
	
#################
def optimize_threads(total, samples):
	cpu = int(int(total)/int(samples))
	
	if (cpu==0): ## 5 availabe cpus for 10 samples == 0 cpu
		cpu = 1
	
	return(cpu)

###############
def system_call(cmd, returned=False, message=True):
	"""Generates system call using subprocess.check_output"""
	## call system
	## send command
	if (message):
		print (colored("[** System: %s **]" % cmd, 'magenta'))

	try:
		out = subprocess.check_output(cmd, shell = True)
		if (returned):
			return (out)
		return ('OK')
	except subprocess.CalledProcessError as err:
		if (returned):
			return (err.output)
		if (message):
			print (colored("** ERROR **", 'red'))
			print (colored(err.output, 'red'))
			print (colored("** ERROR **", 'red'))
		
		return ('FAIL')

def is_non_zero_file(fpath):  
	# https://stackoverflow.com/a/15924160
	"""Returns TRUE/FALSE if file exists and non zero"""
	return os.path.isfile(fpath) and os.path.getsize(fpath) > 0
