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
	title_TOC = []
	Hasvolume = False
	title_nextline = False
	times = 0
	readHandle = codecs.open(file_book,'r','utf-8',errors='replace')
	readHandlelist = readHandle.readlines()
	while line < len(readHandlelist):
		#r'(?:(?:VOLUME|PART|Part|Volume)(?:\s\w*))|(?:CHAPTER|Chapter)\s(?:(?:\w*\.)|(?:(?:XC|X?L|L?X{1,3})?(?:IX|I?V|V?I{1,3}?))).*'
		match = re.findall(r'^(?:(VOLUME|PART|Volume)((?:\s\w*)|(?:(?:XC|X?L|L?X{1,3})?(?:IX|I?V|V?I{1,3}?))))|^(CHAPTER|Chapter)\s((?:\w*)|(?:(?:XC|X?L|L?X{1,3})*(?:IX|I?V|V?I{1,3})*))[\.\s]*(.*)', readHandlelist[line])
		# r'CHAPTER\s((?:\w*\.)|((?:XC|X?L|L?X{1,3})?(?:IX|I?V|V?I{1,3}?))).*'
		if match:
			if match not in listTOC:
				listTOC.append(match)
		if match and not match[0][0] and not match[0][4]:
			title_nextline = True
			line += 1
			while line < len(readHandlelist) and readHandlelist[line] == '\r\n':
				line += 1
			chaptercontentstr = ''.join(re.findall('.*', readHandlelist[line])).strip() + ' '
			while line < len(readHandlelist) - 1 and readHandlelist[line + 1] != '\r\n':
				line += 1
				chaptercontentstr += ''.join(re.findall('.*', readHandlelist[line])).strip() + ' '
			title_TOC.append(chaptercontentstr)
		line += 1
	for listtocnum in range(len(listTOC)):
		for five_tuple in listTOC[listtocnum]:
			if not title_nextline: ####新加的
				if five_tuple[0] != '':
					Hasvolume = True
					Volume_kept = five_tuple[0]
					number_volume_kept = five_tuple[1]
				if five_tuple[3] and five_tuple[4]:
					if Hasvolume:
						key = '(' + Volume_kept + number_volume_kept + ') ' + five_tuple[3]
						dictTOC[key] = five_tuple[4].strip()
					else:
						dictTOC[five_tuple[3]] = five_tuple[4].strip()
			else:
				if five_tuple[0] != '':
					Hasvolume = True
					Volume_kept = five_tuple[0]
					number_volume_kept = five_tuple[1]
					times += 1
				if five_tuple[3]:
					if Hasvolume:
						if listtocnum < len(title_TOC):
							key = '(' + Volume_kept + number_volume_kept + ') ' + five_tuple[3]
							dictTOC[key] = title_TOC[listtocnum-times].strip()
						else:
							break
					else:
						if listtocnum < len(title_TOC):
							dictTOC[five_tuple[3]] = title_TOC[listtocnum-times].strip()
						else:
							break

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
