#! /usr/bin/python

import csv
import os
import sys

year='2014'
path='data/'+year 

fileNames = os.listdir(path)
# start from latest csv file
fileNames.reverse()			 

# Unique_ID = Model + Serial Number 
failed_ids = set()
success_ids = {}

# HD's that eventually failing
failed = open('failedHD', 'a')

# HD's that continued to work until the end
success = open('successHD', 'a')

# Iterate through all the csv files
for file in fileNames:
	with open(path+'/'+file, 'rb') as csvfile:
		reader = csv.reader(csvfile, delimiter=',')
		# skip first row
		try: 
			reader.next()
		except csv.Error:
			print "Failed at File: ",file 	
		count =0
		for row in reader:
			count = count +1
			# model + serial_number
			uid = row[2]+row[1] 
			# print uid 
			failedHD = uid in failed_ids
			successHD = uid in success_ids
			# format the entry: label <feature1: value1> <feature2: value2>
			new_entry =' name:'+ uid + ' capacity:'+ row[3] +'\n'
			if not failedHD and (int(row[4]) == 1):
				failed_ids.add(uid)
				failed.write('-1'+new_entry)
 			elif not failedHD and not successHD:
				success_ids[uid] = '+1'+new_entry
				#success.write('+1'+new_entry)
			elif failedHD and successHD:
				del success_ids[uid]
for key in success_ids:
	success.write(success_ids[key])

failed.close()
success.close()
print "Total rows: ", count
print "Total failed id's: ", len(failed_ids)

	
