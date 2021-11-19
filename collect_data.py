#!/usr/bin/env python
# coding: utf-8

# In[ ]:


from bs4 import BeautifulSoup
import requests
import pandas as pd
import openpyxl
from openpyxl import Workbook


def get_html_table(url):
	html_content = requests.get(url).text
	soup = BeautifulSoup(html_content, "html.parser")
	table = soup.find_all("table", class_="table table-bordered table-hover cc_cursor")
	print('Returning html table')
	return table

def table_to_csv(table_data, headings,out_file):
	data = []
	for row in table_data:
		row_data = row.find_all('td')
		sub_data =[]
		for cell in row_data:
			entry = cell.text
			sub_data.append(entry)
		data.append(sub_data)

	df = pd.DataFrame(data, columns=headings)
	df.to_excel(out_file)


def get_river_flow_data():
	url="http://www.wapda.gov.pk/index.php/river-flow-data"
	table = get_html_table(url)
	table_data = table[0].find_all('tr')
	table_data = table_data[4:]
	Headings = ['Time', 'Indus_levels','Indus_Inflow','Indus_Outflow','Kabul_Inflow',
	'Jhelum_levels','Jhelum_Inflow','Jhelum_Outflow', 'Chenab_Inflow','System_Inflow_now',
	'System_Inflow_past','System_Inflow_avg']
	file = 'https://github.com/haris021/Indus-Tool/main/river_flow_data.xlsx'
	table_to_csv(table_data,headings = Headings, out_file = file)


def get_sindh_barage_data():
	url = "http://www.wapda.gov.pk/index.php/hydroreservior-in-pakistan?tmpl=component&id=43"
	table = get_html_table(url)
	caps = ['Time', 'Station', 'Today', 'Last Year', 'Avg 5 year', 'Avg 10 year']
	table_data = table[0].find_all('tr')
	time = table_data[1].text
	time_arr = time.split(" ")
	date = time_arr[1]
	print(date)
	sindh_data = table_data[25:28]
	out = 'Sindh_barage.xlsx'
	df = pd.read_excel(out)
	final_data = []
	for row in sindh_data:
		row_data = row.find_all('td')
		sub_data = [date]
		for cell in row_data:
			entry = cell.text
			sub_data.append(entry)
		print(sub_data)
		final_data.append(sub_data)
	print('df before append ........')
	print(df)
	df2 = pd.DataFrame(final_data, columns=caps)
	print(df2)
	df = df.append(df2, ignore_index=True)
	df['Time'] = pd.to_datetime(df['Time'])
	print(df)
	df = df.drop_duplicates()
	df.to_excel(out, index=False)
	


get_river_flow_data()
get_sindh_barage_data()
# final_data.to_excel('barage_data.xlsx')





# Make a GET request to fetch the raw HTML content
# html_content = requests.get(url).text

# Parse the html content
# soup = BeautifulSoup(html_content, "html.parser")
# wapda_table = soup.find_all("table", class_="table table-bordered table-hover cc_cursor")
#
# #3 elements in wapda table
# table_data = wapda_table[0]
# tr_data = table_data.find_all("tr")
#
# Headings = ['Time', 'Indus_levels','Indus_Inflow','Indus_Outflow','Kabul_Inflow','Jhelum_levels','Jhelum_Inflow','Jhelum_Outflow', 'Chenab_Inflow','System_Inflow_now','System_Inflow_past','System_Inflow_avg']
# river_flow_data =[]
#ignoring empty rows
#
# tr_data = tr_data[4:]
#
# for row in tr_data:
# 	flow_data = []
# 	row_data = row.find_all('td')
# 	for cell in row_data:
# 		entry = cell.text
# 		flow_data.append(entry)
#
# 	river_flow_data.append(flow_data)
#
# df = pd.DataFrame(river_flow_data, columns=Headings)
# df.to_excel("output.xlsx")

# processing three tables individually

