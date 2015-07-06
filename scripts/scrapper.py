from os import popen, makedirs
from os.path import isfile, exists
from json import load
from urllib.request import urlopen
from urllib.error import URLError
from sys import argv
import re

def mkdir_if_not_already(path) :
	if not exists(path): makedirs(path)
	return path

def dl_if_not_already(file_path, url) :
	if not isfile( file_path ) :
		print('downloading...')
		with urlopen(url) as response:
			open(file_path,'w').write( response.read().decode(response.headers.get_content_charset()) )

def clean_events(data) :
	""" removes single \n, change doubles into single"""
	# rewrites \n, put back doubles, removes singles
	# kaboom bug hotfix of the kill. '\n' indicated a new entry, and '\n ' the following of a long text. It's "fixed" now
	return data.replace('\n','==').replace('====','\n').replace('==','').replace('\n ','=').replace('\n',' ').replace('=','\n')


def scrap_set(set_name, root_page, root_selector) :
	""" Scrap data for a given set, 
	where all wiki pages are indexed in the root wiki page root_page, 
	and can be idetified in this html using root_selector"""

	print('----------------------------------')
	print("\n[Start] scrapping for "+set_name+'\n')
	print("scrapping "+set_name+"... ")


	set_folder = mkdir_if_not_already(datasets_folder+set_name+'/')

	dl_if_not_already(raw_folder+root_page+".html", "http://www.arkhamhorrorwiki.com/"+root_page)

	locations = load( popen( "cat "+raw_folder+root_page+".html | pup '"+root_selector+" json{}'" ) )

	for location in locations :

		location_name = location['text'].replace(' ', '_').replace('\'','')
		location_raw_file = raw_folder+location_name+'.html'

		print("scrapping "+location['text']+'... ')
		try : # because Err 500 for one page (see at the end of the script)

			dl_if_not_already(location_raw_file, base_url+location['href'])		

			data = popen("cat "+location_raw_file+" | pup 'tbody td:first-child text{}' ").read()
			
			print('writing to '+set_folder+location_name)
			open(set_folder+location_name, 'w').write( clean_events(data) )
		except URLError :
			print('[FAILED] download error')
			pass

	print('['+set_name+']'+' done.')

def clean(stream) :
	ops = [
		['  ',' '],
		['Mkae', 'Make'],
		['\[\d\] ', ''],
		['\[\[Clue', 'Clue'],
		['\[\[William Bain', 'William Bain'],
		['\[\[Madness\]', 'Madness'],
		['\[\[Stamina', 'Stamina'],
		['\[\[Spell\]', 'Spell'],
		['\[\[toughness\]', 'toughness'],
		['[dD]raw a Madness Card', 'Lose 2 Sanity'],
		['Rail Pass card', 'Common Item'],
		['gain 1 Corruption card', 'Lose 2 Sanity'],
		['\\.M','. M'],
		[' Make +Sneak', ' Make a Sneak'],
		['\\.Gain', '. Gain'],
		['!Discard', '! Discard'],
		['\n \$\d\).*\n',''],
		['If you Sanity', 'If your Sanity'],
		['passing eon','passing one'],
	]

	for op in ops :
		stream = re.sub(op[0], op[1], stream)

	return stream

def merge_and_shuffle(set_names):
	print('----------------------------------')
	print("\n[Start] Merge and Shuffle\n")
	sets = [ datasets_folder+set_name+'/* ' for set_name in set_names]

	full_shuf_clean = clean(popen("cat "+" ".join(sets)+" | shuf").read())

	open(full_folder+'input.txt','w').write(full_shuf_clean)
	
	print("full dataset written in "+full_folder+"input.txt ")


base_url = 'http://www.arkhamhorrorwiki.com'

if __name__ ==  "__main__" :

	datasets_folder = argv[1]+'/' if len(argv)>1 else '../datasets/'

	mkdir_if_not_already(datasets_folder)
	raw_folder = mkdir_if_not_already(datasets_folder+'raw/')
	full_folder = mkdir_if_not_already(datasets_folder+'full/')

	scrap_set('locations', 'Location', 'tbody td:first-child a' )
	scrap_set('other_worlds', 'Other_World', 'ul li a[href][title*="(encounters)"]' )

	merge_and_shuffle(['locations', 'other_worlds'])

# writing to ../Wireless_Station
# scrapping Wizard's Hill... 
# downloading...
# Traceback (most recent call last):
#   File "scrapper.py", line 35, in <module>
#     with urlopen(base_url+location['href']) as response:
#   File "/usr/lib/python3.4/urllib/request.py", line 161, in urlopen
#     return opener.open(url, data, timeout)
#   File "/usr/lib/python3.4/urllib/request.py", line 469, in open
#     response = meth(req, response)
#   File "/usr/lib/python3.4/urllib/request.py", line 579, in http_response
#     'http', request, response, code, msg, hdrs)
#   File "/usr/lib/python3.4/urllib/request.py", line 507, in error
#     return self._call_chain(*args)
#   File "/usr/lib/python3.4/urllib/request.py", line 441, in _call_chain
#     result = func(*args)
#   File "/usr/lib/python3.4/urllib/request.py", line 587, in http_error_default
#     raise HTTPError(req.full_url, code, msg, hdrs, fp)
# urllib.error.HTTPError: HTTP Error 500: Internal Server Error

