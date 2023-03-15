# !/usr/bin/env python
# -*- coding: utf-8 -*-

######################################################################
#
# (c) Copyright University of Southampton, 2021
#
# Copyright in this software belongs to University of Southampton,
# Highfield, University Road, Southampton SO17 1BJ
#
# Created By : Stuart E. Middleton
# Created Date : 2021/01/29
# Project : Teaching
#
######################################################################

from __future__ import absolute_import, division, print_function, unicode_literals

import sys, codecs, json, math, time, warnings, re, logging
warnings.simplefilter( action='ignore', category=FutureWarning )

# import nltk, numpy, scipy, sklearn, sklearn_crfsuite, sklearn_crfsuite.metrics

LOG_FORMAT = ('%(levelname) -s %(asctime)s %(message)s')
logger = logging.getLogger( __name__ )
logging.basicConfig( level=logging.INFO, format=LOG_FORMAT )
logger.info('logging started')

def exec_regex_toc( file_book = None ) :

	# CHANGE BELOW CODE TO USE REGEX TO BUILD A TABLE OF CONTENTS FOR A BOOK (task 1)

	# Input >> www.gutenberg.org sourced plain text file for a whole book
	# Output >> toc.json = { <chapter_number_text> : <chapter_title_text> }

	# hardcoded output to show exactly what is expected to be serialized
	line = 0
	listTOC = []
	dictTOC = {}
	Hasvolume = False
	title_nextline = False
	readHandle = codecs.open(file_book,'r','utf-8',errors='replace')
	readHandlelist = readHandle.readlines()
	while line < len(readHandlelist):
		#r'(?:(?:VOLUME|PART|Part|Volume)(?:\s\w*))|(?:CHAPTER|Chapter)\s(?:(?:\w*\.)|(?:(?:XC|X?L|L?X{1,3})?(?:IX|I?V|V?I{1,3}?))).*'
		match = re.findall(r'^(?:(VOLUME|PART|Part|Volume)((?:\s\w*)|(?:(?:XC|X?L|L?X{1,3})?(?:IX|I?V|V?I{1,3}?))))|^(CHAPTER|Chapter)\s((?:\w*)|(?:(?:XC|X?L|L?X{1,3})*(?:IX|I?V|V?I{1,3})*))[\.\s]*(.*)', readHandlelist[line])
		# r'CHAPTER\s((?:\w*\.)|((?:XC|X?L|L?X{1,3})?(?:IX|I?V|V?I{1,3}?))).*'
		if not match[0][4]:
			if match not in listTOC:
				listTOC.append(match)
		else:
			title_nextline = True
		line += 1
	print(listTOC)
	for listtoc in listTOC:
		for Volume , number_volume , _ , number_chapter , chapter_title in listtoc:
			if Volume != '':
				Hasvolume = True
				Volume_kept = Volume
				number_volume_kept = number_volume
			if number_chapter and chapter_title:
				if Hasvolume:
					key = '(' + Volume_kept + number_volume_kept + ') ' + number_chapter
					dictTOC[key] = chapter_title.strip()
				else:
					dictTOC[number_chapter] = chapter_title.strip()

	# dictTOC = {
	# 		"1": "I AM BORN",
	# 		"2": "I OBSERVE",
	# 		"3": "I HAVE A CHANGE"
	# 	}

	# DO NOT CHANGE THE BELOW CODE WHICH WILL SERIALIZE THE ANSWERS FOR THE AUTOMATED TEST HARNESS TO LOAD AND MARK

	writeHandle = codecs.open( 'toc.json', 'w', 'utf-8', errors = 'replace' )
	strJSON = json.dumps( dictTOC, indent=2 )
	writeHandle.write( strJSON + '\n' )
	writeHandle.close()

if __name__ == '__main__':
	if len(sys.argv) < 4 :
		raise Exception( 'missing command line args : ' + repr(sys.argv) )
	ontonotes_file = sys.argv[1]
	book_file = sys.argv[2]
	chapter_file = sys.argv[3]

	logger.info( 'ontonotes = ' + repr(ontonotes_file) )
	logger.info( 'book = ' + repr(book_file) )
	logger.info( 'chapter = ' + repr(chapter_file) )

	# DO NOT CHANGE THE CODE IN THIS FUNCTION

	exec_regex_toc( book_file )
