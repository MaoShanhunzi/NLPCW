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

def exec_regex_questions( file_chapter = None ) :

	# CHANGE BELOW CODE TO USE REGEX TO LIST ALL QUESTIONS IN THE CHAPTER OF TEXT (task 2)

	# Input >> www.gutenberg.org sourced plain text file for a chapter of a book
	# Output >> questions.txt = plain text set of extracted questions. one line per question.

	# hardcoded output to show exactly what is expected to be serialized

	# readHandle = codecs.open(file_chapter,'r','utf-8',errors='replace')
	# readHandlelist = readHandle.readlines()
	listTOC = []
	with codecs.open(file_chapter, 'r', 'utf-8') as readHandle:
		readHandleStr = readHandle.read()
	matchs = re.findall(r'[\s]*[\u2019A-Za-z\d\s\"\,\-\'\;\_\—\è]*\?', readHandleStr,flags=re.MULTILINE)

	# 	if matchs:
		# print('111')
		# print(matchs)
		# str_match = ''.join(match).strip()
		# if str_match not in listTOC:
		# 	listTOC.append(str_match)
	# print('111')
	# print(matchs)
	for match in matchs:
		#方法1
		# match_P1 = match.strip(u'\u2019')
		# match_P2 = match_P1.replace('\n','')
		# match_P3 = match_P2.replace('\r',' ')
		# match_P4 = match_P3.strip()
		# match_P5 = match_P4.strip(u'\u2018')
		# match_P6 = match_P5.strip('\'')
		#方法2
		ch = match[0]
		while not str.isalpha(ch):
			match = ''.join(match.split(ch,1))
			if match:
				ch = match[0]
			else:
				break
			#-----------
		match_deletehuanhang = match.replace('\n','')
		match_deletehuiche = match_deletehuanhang.replace('\r',' ')
		listTOC.append(match_deletehuiche)
	# print('222')
	# print(listTOC)
	setQuestions = set(listTOC)
	# setQuestions = set([
	# 	"Traddles?",
	# 	"And another shilling or so in biscuits, and another in fruit, eh?",
	# 	"Perhaps you’d like to spend a couple of shillings or so, in a bottle of currant wine by and by, up in the bedroom?",
	# 	"Has that fellow’--to the man with the wooden leg--‘been here again?"
	# 	])

	# DO NOT CHANGE THE BELOW CODE WHICH WILL SERIALIZE THE ANSWERS FOR THE AUTOMATED TEST HARNESS TO LOAD AND MARK

	writeHandle = codecs.open( 'questions.txt', 'w', 'utf-8', errors = 'replace' )
	for strQuestion in setQuestions :
		writeHandle.write( strQuestion + '\n' )
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

	exec_regex_questions( chapter_file )

