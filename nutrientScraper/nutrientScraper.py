"""
	To Install Selenium: pip install selenium
	This script will scrape nutritional data from Supertracker
"""

from selenium import webdriver
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import unicodedata
import collections
import os.path as path
import sys
import argparse

def make_arg_parser():
	parser = argparse.ArgumentParser(description='Scrapes portion and meal data')
	parser.add_argument('-o', '--outputdir', help='Output directory', required=True)
	parser.add_argument('-u', '--user', help='Supertracker user', required=True)
	parser.add_argument('-p', '--password', help='password', required=True)
	parser.add_argument('-f', '--firstDate', help='ex. 01/01/16', required=True, type=dateChecker)
	parser.add_argument('-s', '--secondDate', help='ex. 01/02/16', required=True, type=dateChecker)
	return parser

def dateChecker(date):
	try:
		datetime.datetime.strptime(date, "%m/%d/%y")
	except ValueError:
		e = "%s is not a proper date. Do in this format: 01/15/17" %date
		raise argparse.ArgumentTypeError(e)
	return date

def getCalories():
	global nutrientsList
	global dateDict
	number="mast_level1_cph_mast_level2_cph_lnkCalories"
	try:
		element=WebDriverWait(driver, 50).until(EC.presence_of_element_located((By.ID, "mast_level1_cph_mast_level2_cph_lbDataDetails")))
	finally:
		webe=driver.find_element_by_id(number)
		print(webe.text.encode('ascii', errors='ignore').decode('utf-8'))
		webe.click()
		try:
			chartElem=WebDriverWait(driver, 50).until(EC.presence_of_element_located((By.ID, "mast_level1_cph_mast_level2_cph_profiletextChart")))
			driver.find_element_by_id("mast_level1_cph_mast_level2_cph_lbDataDetails").click()
		finally:
			try:		
				nextElem=WebDriverWait(driver, 50).until(EC.presence_of_element_located((By.TAG_NAME, "th")))
			finally:
				if(len(dateDict)==0):
					dateElems=driver.find_elements_by_class_name("dateColumn")
					for i in dateElems:
						dateDict[i.text]=""
				lista=driver.find_elements_by_id("divdataTableContainer")[0].find_elements_by_tag_name("div")
				if(len(lista)==1):
					
					listrows=lista[0].find_elements_by_class_name("dateColumn")
					listvalues=lista[0].find_elements_by_class_name("valueColumn")
					listheader=lista[0].find_element_by_class_name("valueField").text.encode('ascii', errors='ignore').decode('utf-8')
					print(listheader)
					listind=0
					for i in range(len(listrows)):
						dateDict[listrows[i].text]=dateDict[listrows[i].text]+'\t'+listvalues[i].text
		
					nutrientsList.append(listheader)

def getFoodGroupInfo(num):
	"""Retrieve All Major Food Groups"""
	global nutrientsList
	global dateDict
	number="mast_level1_cph_mast_level2_cph_gvFoodGroups_btnSelect_"+str(num)
	try:
		element=WebDriverWait(driver, 50).until(EC.presence_of_element_located((By.ID, "mast_level1_cph_mast_level2_cph_lbDataDetails")))
	finally:
		webe=driver.find_element_by_id(number)
		print(webe.text.encode('ascii', errors='ignore').decode('utf-8'))
		webe.click()
		try:
			chartElem=WebDriverWait(driver, 50).until(EC.presence_of_element_located((By.ID, "mast_level1_cph_mast_level2_cph_profiletextChart")))
			driver.find_element_by_id("mast_level1_cph_mast_level2_cph_lbDataDetails").click()
		finally:
			try:		
				nextElem=WebDriverWait(driver, 50).until(EC.presence_of_element_located((By.TAG_NAME, "th")))
			finally:
				if(len(dateDict)==0):
					dateElems=driver.find_elements_by_class_name("dateColumn")
					for i in dateElems:
						dateDict[i.text]=""
				lista=driver.find_elements_by_id("divdataTableContainer")[0].find_elements_by_tag_name("div")
				if(len(lista)==1):
					listrows=lista[0].find_elements_by_class_name("dateColumn")
					listvalues=lista[0].find_elements_by_class_name("valueColumn")
					listheader=lista[0].find_element_by_class_name("valueField").text.encode('ascii', errors='ignore').decode('utf-8')
					print(listheader)
					for i in range(len(listrows)):
						v=0
						if(listvalues[i].text=="No Data"):
							v=0
							#dateDict[listrows[i].text]=dateDict[listrows[i].text]+'{:25}'.format("0")
						else:
							
							try:
								quantity=listvalues[i].text
								char=quantity[-1]
								char.encode('ascii')
								v=int(quantity)
							except UnicodeEncodeError:
								char=unicodedata.numeric(char)
								if(len(quantity)>1):
									v=int(quantity[:-1])+char
								else:
									v=char
						dateDict[listrows[i].text]=dateDict[listrows[i].text]+'\t'+str(v)
		
					nutrientsList.append(listheader)
					
				else:
					for div in lista:
						listrows=div.find_elements_by_class_name("dateColumn")
						listvalues=div.find_elements_by_class_name("valueColumn")
						listheader=div.find_element_by_class_name("valueField").text.encode('ascii', errors='ignore').decode('utf-8')
						print(listheader)
						for i in range(len(listrows)):
							v=0
							if(listvalues[i].text=="No Data"):
								v=0
							else:
								try:
									quantity=listvalues[i].text
									char=quantity[-1]
									char.encode('ascii')
									v=int(quantity)
								except UnicodeEncodeError:
									char=unicodedata.numeric(char)
									if(len(quantity)>1):
										v=int(quantity[:-1])+char
									else:
										v=char
							dateDict[listrows[i].text]=dateDict[listrows[i].text]+'\t'+str(v)
		
						
def getNutrientInfo(num):

	global nutrientsList
	global dateDict
	number="mast_level1_cph_mast_level2_cph_gvNutrients_btnSelect_"+str(num)
	try:
		element=WebDriverWait(driver, 50).until(EC.presence_of_element_located((By.ID, "mast_level1_cph_mast_level2_cph_lbDataDetails")))
	finally:
		webe=driver.find_element_by_id(number)
		print(webe.text.encode('ascii', errors='ignore').decode('utf-8'))
		webe.click()
		try:
			chartElem=WebDriverWait(driver, 50).until(EC.presence_of_element_located((By.ID, "mast_level1_cph_mast_level2_cph_profiletextChart")))
			driver.find_element_by_id("mast_level1_cph_mast_level2_cph_lbDataDetails").click()
		finally:
			try:		
				nextElem=WebDriverWait(driver, 50).until(EC.presence_of_element_located((By.TAG_NAME, "th")))
			finally:
				if(len(dateDict)==0):
					dateElems=driver.find_elements_by_class_name("dateColumn")
					for i in dateElems:
						dateDict[i.text]=""
				lista=driver.find_elements_by_id("divdataTableContainer")[0].find_elements_by_tag_name("div")
				if(len(lista)==1):
					
					listrows=lista[0].find_elements_by_class_name("dateColumn")
					listvalues=lista[0].find_elements_by_class_name("valueColumn")
					listheader=lista[0].find_element_by_class_name("valueField").text.encode('ascii', errors='ignore').decode('utf-8')
					print(listheader)
					listind=0
					for i in range(len(listrows)):
						dateDict[listrows[i].text]=dateDict[listrows[i].text]+'\t'+listvalues[i].text
		
					nutrientsList.append(listheader)
					
				else:
					for div in lista:
						listrows=div.find_elements_by_class_name("dateColumn")
						listvalues=div.find_elements_by_class_name("valueColumn")
						listheader=div.find_element_by_class_name("valueField").text.encode('ascii', errors='ignore').decode('utf-8')	
						print(listheader)
						for i in range(len(listrows)):
							dateDict[listrows[i].text]=dateDict[listrows[i].text]+'\t'+listvalues[i].text
		
						nutrientsList.append(listheader)	

def addAllNut():
	getCalories()
	for i in range(6):
		getFoodGroupInfo(i)

	for ii in range(35):
		getNutrientInfo(ii)
	
def outputNutrients():
	global fileOutput
	f=open(fileOutput, 'w')
	global nutrientsList
	global dateDict
	a=''
	for i in nutrientsList:
		a=a+'\t'+i
	a=a+'\n'
	f.write(a)
	dateDictSorted=collections.OrderedDict(sorted(dateDict.items()))
	for key, value in dateDictSorted.items():
		#print(key)
		f.write(key+value+'\n')



###
###This part will just "Initialize" the browser: logging in and navigating to the necessary pages
###Uncomment Chromedriver and comment PhantomJS for JS debugging issues


ROOT_DIR=path.dirname(path.abspath(__file__))
driver=webdriver.PhantomJS(executable_path=path.join(ROOT_DIR, 'phantomjs-2.1.1-macosx/bin/phantomjs'))
#driver=webdriver.Chrome(executable_path=path.join(ROOT_DIR, 'chromedriver'))

parser = make_arg_parser()
args = parser.parse_args()
# ###PARAMETERS
user = args.user
password = args.password
firstDate = args.firstDate
secondDate = args.secondDate
fileOutput = args.outputdir

###begin Selenium work
driver.get("https://www.supertracker.usda.gov/login.aspx")
driver.find_element_by_id("mast_level1_cph_mast_level2_cph_login_UserName").send_keys(user)
driver.find_element_by_id("mast_level1_cph_mast_level2_cph_login_Password").send_keys(password)
driver.find_element_by_id("mast_level1_cph_mast_level2_cph_login_LoginButton").click()
driver.get("https://www.supertracker.usda.gov/HistoryCharts.aspx")
driver.find_element_by_name("ctl00$ctl00$mast_level1_cph$mast_level2_cph$txtFrom").clear()
driver.find_element_by_name("ctl00$ctl00$mast_level1_cph$mast_level2_cph$txtFrom").send_keys(firstDate)
driver.find_element_by_name("ctl00$ctl00$mast_level1_cph$mast_level2_cph$txtThru").clear()
driver.find_element_by_name("ctl00$ctl00$mast_level1_cph$mast_level2_cph$txtThru").send_keys(secondDate)
driver.find_element_by_id("mast_level1_cph_mast_level2_cph_btnCreateReport").click()

###
nutrientsList=[]	
dateDict={}


### Add all nutrient informations
addAllNut()


### Print to file in outputNutrients
#getFoodGroupInfo(1)
outputNutrients()

driver.close()
