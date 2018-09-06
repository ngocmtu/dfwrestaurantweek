#!/usr/bin/env python

import sys
import PyPDF2
import string

pdfFileObj = open('/home/ngocmtu/dfwrestaurantweek/dfwrw/pdf_menus/lonesome_dove.pdf', 'rb')
pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
		
num_pages = pdfReader.numPages
count = 0

while count < num_pages:
    pageObj = pdfReader.getPage(count)
    count +=1
    extracted_text = pageObj.extractText()
    print(extracted_text)