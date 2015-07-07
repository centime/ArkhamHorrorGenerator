from os import popen, path
from sys import argv
import json


if __name__ == "__main__" :
	
	logs_path = argv[1]
	logs_file = open(logs_path, 'r')
	logs = json.loads(logs_file.read())
	logs_file.close()

	reverse = True if len(argv)>2 and argv[2] == 'reverse' else False

	i = 0
	logs = sorted(logs, key= lambda x:x['rating'], reverse = reverse)
	for log in logs :
		print()
		print('['+str(i)+'] '+str(log['rating'])+' : '+log['text'])
		i += 1

	print()
	print('------------------------')
	print('Edit rating with the following syntax: id1:rating1 id2:rating2 ...')
	edits = input() # id1:rating1 id2:rating2 ...
	edits = [ e.split(':') for e in edits.split(' ')]

	for edit in edits :
		logs[int(edit[0])]['rating'] = int(edit[1])

	open(logs_path,'w').write(json.dumps(logs))
