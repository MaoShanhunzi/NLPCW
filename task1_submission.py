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
	listTOC = []
	dictTOC = {}
	readHandle = codecs.open(file_book,'r','utf-8',errors='replace')
	readHandlelist = readHandle.readlines()
	line = 0
	Chapterindexdot = True
	while line < len(readHandlelist):
		# dictTOC += re.findall('CHAPTER\s*\w*\.*\s\w*',line)
		# listTOC += [i.strip() for i in re.findall('CHAPTER.*',line)]
		# dictTOC += [re.sub(r'^(\s+)|(\s+)&','',i) for i in re.findall('CHAPTER[\s\w]*\.*[\s\w\.]*', line)]
		# dictTOC += [i.strip() for i in re.findall('CHAPTER[\s\w]*\.*[\s\w\.]*', line)]
		#如果这一行只有章节序号，标题在其他行
		if re.findall('CHAPTER.*', readHandlelist[line]) != []:
			if re.findall('(?<=CHAPTER[\s\w])[\sa-zA-Z\u2018\u2019\.\,]*',readHandlelist[line]) == ['']:
				Chapterindexdot = False
				chapterindexstr = ''.join(re.findall('CHAPTER.*', readHandlelist[line]))
				line += 1
				while line < len(readHandlelist) and readHandlelist[line] == '\r\n':
					line += 1
				chaptercontentstr = ''.join(re.findall('.*',readHandlelist[line])).strip()+' '
				while line < len(readHandlelist)-1 and readHandlelist[line+1] != '\r\n':
					line += 1
					chaptercontentstr += ''.join(re.findall('.*',readHandlelist[line])).strip()+' '
				listTOC += [chapterindexstr + chaptercontentstr]
			else: #章节标题就一行
				listTOC += re.findall('CHAPTER.*', readHandlelist[line])
		line += 1
	readHandle.close()
	if Chapterindexdot:
		for listTOC_line in listTOC:
			key = ''.join(re.findall('\d+', listTOC_line))
			value = ''.join(re.findall('(?<=\.)[\sa-zA-Z\u2018\u2019\.\,]*', listTOC_line))
			dictTOC[key] = value.strip()  # book does not have parts and volumes or made up multibooks
	else:
		for listTOC_line in listTOC:
			key = ''.join(re.findall('\d+', listTOC_line))
			value = ''.join(re.findall('(?<=[\d|\.])[\sa-zA-Z\u2018\u2019\.\,]*', listTOC_line))
			dictTOC[key] = value.strip()  # book does not have parts and volumes or made up multibooks
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
