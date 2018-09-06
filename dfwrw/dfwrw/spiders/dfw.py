import scrapy
import json
import re
from dfwrw.items import DfwrwItem

class RestaurantSpider(scrapy.Spider):
	name = 'dfw'
	start_urls = ['http://www.dfwrestaurantweek.com/search_alpha']
	file_urls = []

	def parse(self,response):
		for href in response.css('span.field-content a::attr(href)').extract():
			yield response.follow(href,callback=self.parse_menu)

	def get_text(self,element):
		return element.css('::text').extract_first().replace('\\u00a0','')

	def parse_menu(self,response):
		tags = response.css('div.tags a::text').extract()
		price = '$49' if '$49' in tags else '$39'
		lunch = True if 'Lunch Experience' in tags else False
		_4th = True if '4th Course' in tags else False
		week = ''
		if '3 Weeks' in tags:
			week = '3 Weeks'
		elif '2 Weeks' in tags:
			week = '2 Weeks'
		else:
			week = '1 Week'

		menu_link = response.css('div.field-items p a::attr(href)').extract()
		restaurant_info = response.css('div.field-items p')
		name = self.get_text(restaurant_info[0])

		if len(restaurant_info) > 7:

			second_address = self.get_text(restaurant_info[2])


			# features = re.split('[:|]', self.get_text(restaurant_info[7]).replace(' ',''))[1:]
			# features = [feature.replace('\xc2\xa0','') for feature in features]
			# features = [feature.replace('\xa0','') for feature in features]
			# price = '$49' if '49' in feature else '$39'
			# lunch = True if 'Lunch' in feature else False
			
			data = {
				'name':name,
				'first_address':self.get_text(restaurant_info[1]),
				'second_address':{
					'full':second_address,
					'city':second_address.split(',')[0]
				},
				'phone':self.get_text(restaurant_info[4]).replace(' ','').split(':')[1],
				'cuisine':re.split('[:,]',self.get_text(restaurant_info[5]).replace(' ',''))[1:], 
				# separate cuisine by : and , after that only saves the list of cuisines
				# example 'Cusine: European, French' -> 'Cusine:European,French' -> [Cuisine,European,French] -> [European,French]
				'participating_week':week,
				'price':price,
				'lunch':lunch,
				'_4th_course':_4th,
				'menu':{
					'first_course':[
						{
			    			'main':'',
			    			'description':'',
			    			'wine_pairing':''
			    		}
					],
					'second_course':[
						{
			    			'main':'',
			    			'description':'',
			    			'wine_pairing':''
			    		}
					],
					'third_course':[
						{
			    			'main':'',
			    			'description':'',
			    			'wine_pairing':''
			    		}
					],
					'fourth_course':[
						{
			    			'main':'',
			    			'description':'',
			    			'wine_pairing':''
			    		}
					]
				},
				"lunch_menu":{
			    	"first_course": [
			    		{
			    			'main':'',
			    			'description':'',
			    			'wine_pairing':''
			    		}
			    	], 
			        "second_course": [
			        	{
			    			'main':'',
			    			'description':'',
			    			'wine_pairing':''
			    		}
			        ]
			    }
			}
			with open('test_dfw.json','a') as f:
				f.write(json.dumps(data,indent=4))
		else:
			print('Restaurant does not follow format')

		if len(menu_link) >= 3:
			menu_link = menu_link[2]
			if menu_link[-3:] != 'pdf':
				with open('nopdf','a+') as nopdf:
					nopdf.write(menu_link+'\r\n')
					print('No pdf found: ')
			else:
				yield DfwrwItem(file_urls=[menu_link])
		else:
			print('---------------------------------------------------------')
			print('No View Menu link')
			with open('noviewmenu','a+') as noviewmenu:
				noviewmenu.write(name)
				for link in menu_link:
					noviewmenu.write(link+'\r\n')
			print('---------------------------------------------------------')