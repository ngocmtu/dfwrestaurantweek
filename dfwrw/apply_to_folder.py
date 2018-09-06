#!/usr/bin/env python

import sys
from os import path, listdir

# get all files from folder
def get_files_without_csv(folder):
	files = listdir(folder)
	return [f for f in files if f[-3:len(f)]=='csv']

def get_all_files(folder):
	return [path.join(folder,f) for f in listdir(folder)]