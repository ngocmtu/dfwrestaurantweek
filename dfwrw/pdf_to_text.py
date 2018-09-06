#!/usr/bin/env python

import sys
import PyPDF2
import string
from os import path
from nltk import FreqDist
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from apply_to_folder import get_all_files

reload(sys)
sys.setdefaultencoding('utf8')
stop_words=set(stopwords.words('english'))
text = []
raw_text_menu = ''

file_or_folder = sys.argv[1]
filename = sys.argv[2]

def extract_and_count(fileObj):
	try:
		global raw_text_menu
		pdfFileObj = open(fileObj, 'rb')
		pdfReader = PyPDF2.PdfFileReader(pdfFileObj)

		num_pages = pdfReader.numPages
		count = 0

		while count < num_pages:
		    pageObj = pdfReader.getPage(count)
		    count +=1
		    extracted_text = pageObj.extractText()
		    raw_text_menu = extracted_text
		    extracted_text = [word.lower() for word in word_tokenize(extracted_text) if word not in stop_words and word not in string.punctuation]
		    text.extend(extracted_text)

	except Exception as e:
		print(str(e))

def write_to_text(filename):
	global raw_text_menu
	newfilename = filename[:-4] + '.txt'
	newfilename = path.join('/home/ngocmtu/dfwrestaurantweek/dfwrw/txt_menus',newfilename)
	with open(newfilename,'a+') as f:
		f.write(raw_text_menu.encode('utf-8'))
		fdist = FreqDist(text)
		for word,freq in fdist.most_common(200):
			f.write(str(word.encode('utf-8'))+','+str(freq)+'\n')
		f.write(str(text))

if file_or_folder == 'folder':
	files = get_all_files('/home/ngocmtu/dfwrestaurantweek/dfwrw/pdf_menus')
	for f in files:
		extract_and_count(f)
elif file_or_folder == 'text_folder':
	files = get_all_files('/home/ngocmtu/dfwrestaurantweek/dfwrw/txt_menus')
	for f in files:
		fileObj = open(f,'rb')
		extracted_text = fileObj.read().replace('\n', ' ').encode('utf-8')
		extracted_text = [word.lower() for word in word_tokenize(extracted_text) if word not in stop_words and word not in string.punctuation]
		text.extend(extracted_text)
		fileObj.close()
	with open('txt_menus_info.txt','a+') as f:
		fdist = FreqDist(text)
		for word,freq in fdist.most_common(200):
			f.write(str(word.encode('utf-8'))+','+str(freq)+'\n')
else:
	extract_and_count(filename)
	write_to_text(filename)
