#!/usr/bin/env python

import json

def inquire_menu_info(prompt):
	done_course = 'n'
	to_be_inserted = []

	while done_course == 'n':
		course = raw_input(prompt)
		course.replace('\n','')
		course.replace('\r\n','')
		course = course.split('|')
		to_be_inserted.append({
			"main":course[0],
			"description":course[1],
			"wine_pairing":course[2],
			"wine_price":course[3]
		})
		done_course = raw_input('Done?(y/n)')
	return to_be_inserted

with open('test_restaurant.json','r') as f:
	data = json.load(f)
	restaurants = data['restaurants']
	done = True

	name = raw_input('Enter restaurant name: ')
	insert_type = raw_input('Insert type (menu,new,lunch): ')

	if insert_type == 'new':
		print('Key to be inserted')
		key = raw_input('>')
		print('Value to be inserted')
		val = raw_input('>')

	elif insert_type == 'menu':
		one_price_wine_pairing = raw_input('One price wine pairing?(price/n) ')
		insert_first_course = inquire_menu_info('First course (need 3, separated by |): ')
		insert_second_course = inquire_menu_info('Second course (need 3, separated by |): ')
		insert_third_course = inquire_menu_info('Third course (need 3, separated by |): ')
		insert_fourth_course = inquire_menu_info('Fourth course (need 3, separated by |): ')
		
		idx = 0
		while data['restaurants'][idx]['name'] != name:
			idx += 1

		if one_price_wine_pairing == 'n':
			data['restaurants'][idx]['one_price_wine_pairing'] = False
		else:
			data['restaurants'][idx]['one_price_wine_pairing'] = int(one_price_wine_pairing)
		data['restaurants'][idx]['menu'] = {
	    	"first_course": insert_first_course, 
	        "second_course": insert_second_course,
			"third_course":insert_third_course,
			"fourth_course":insert_fourth_course
	    }

	elif insert_type == 'lunch':
		one_price_wine_pairing = raw_input('One price wine pairing?(price/n) ')
		insert_first_course = inquire_menu_info('First lunch course (need 3, separated by |): ')
		insert_second_course = inquire_menu_info('Second lunch course (need 3, separated by |): ')

		idx = 0
		while data['restaurants'][idx]['name'] != name:
			idx += 1

		if one_price_wine_pairing == 'n':
			data['restaurants'][idx]['one_price_wine_pairing'] = False
		else:
			data['restaurants'][idx]['one_price_wine_pairing'] = int(one_price_wine_pairing)
		data['restaurants'][idx]['lunch_menu'] = {
	    	"first_course": insert_first_course, 
	        "second_course": insert_second_course
	    }

with open('test_restaurant.json','w') as f:
	json.dump(data,f,indent=4)