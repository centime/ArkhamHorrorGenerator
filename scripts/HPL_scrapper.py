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

def clean(txt) :
	""" removes single \n, change doubles into single"""
	# rewrites \n, put back doubles, removes singles
	# kaboom bug hotfix of the kill. '\n' indicated a new entry, and '\n ' the following of a long text. It's "fixed" now
	
	txt = txt.replace('\n','==').replace('====','\n').replace('==',' ').replace('\n','==').replace('====','\n').replace('==',' ')
	starts = [
		'[Winifred Virginia Jackson and H. P. Lovecraft]',
		'[C.L. Moore]',
		'By H. P. Lovecraft',
		'By R. H. Barlow and H. P. Lovecraft',
		'by H. P. Lovecraft',
		'By Percy Simple [H. P. Lovecraft]',
		'H.P. Lovecraft’s'
	]
	for start in starts :
		if start in txt :
			return txt.split(start)[1].split('\xa0\n  \xa0\n')[0]

def scrap_set(set_name, root_page, root_selector) :
	""" Scrap data for a given set, 
	where all wiki pages are indexed in the root wiki page root_page, 
	and can be idetified in this html using root_selector"""

	print('----------------------------------')
	print("\n[Start] scrapping for "+set_name+'\n')
	print("scrapping "+set_name+"... ")


	set_folder = mkdir_if_not_already(datasets_folder+set_name+'/')

	dl_if_not_already(raw_folder+set_name+".html", base_url+root_page)

	data = load( popen( "cat "+raw_folder+set_name+".html | pup '"+root_selector+" json{}'" ) )
	links = [ d['children'][0] for d in data['children']]

	for link in links :

		link_name = link['text'].replace(' ', '_').replace('\'','')
		link_raw_file = raw_folder+link_name+'.html'

		print("scrapping "+link['text']+'... ')
		try : # because Err 500 for one page (see at the end of the script)

			dl_if_not_already(link_raw_file, base_url+link['href'])		

			data = popen("cat "+link_raw_file+" | pup 'font text{}' ").read()
			
			print('writing to '+set_folder+link_name)
			open(set_folder+link_name, 'w').write( clean(data) )
		except URLError :
			print('[FAILED] download error')
			pass

	print('['+set_name+']'+' done.')

def merge(set_names):
	print('----------------------------------')
	print("\n[Start] Merge and Shuffle\n")
	sets = [ datasets_folder+set_name+'/* ' for set_name in set_names]

	open(full_folder+'input.txt','w').write( popen("cat "+" ".join(sets)+" | shuf").read() )
	
	print("full dataset written in "+full_folder+"input.txt ")

base_url = 'http://www.hplovecraft.com/writings/texts/'

if __name__ ==  "__main__" :

	datasets_folder = argv[1]+'/' if len(argv)>1 else '../datasets/hplovecraft-texts/'

	mkdir_if_not_already(datasets_folder)
	raw_folder = mkdir_if_not_already(datasets_folder+'raw/')
	full_folder = mkdir_if_not_already(datasets_folder+'full/')

	scrap_set('texts', '', 'font ul ul:nth-child(2)' )

	merge(['texts'])