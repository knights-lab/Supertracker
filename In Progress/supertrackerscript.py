"""
Supertracking Script
Scroll to bottom to see function calls
"""

from selenium import webdriver
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from os import path
import unicodedata
import collections
import sys
def getCalories():
	global nutrientsList
	global dateDict
	number="mast_level1_cph_mast_level2_cph_lnkCalories"
	try:
		element=WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.ID, "mast_level1_cph_mast_level2_cph_lbDataDetails")))
	finally:
		webe=driver.find_element_by_id(number)
		print(webe.text.encode('ascii', errors='ignore').decode('utf-8'))
		webe.click()
		try:
			chartElem=WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.ID, "mast_level1_cph_mast_level2_cph_profiletextChart")))
			driver.find_element_by_id("mast_level1_cph_mast_level2_cph_lbDataDetails").click()
		finally:
			try:		
				nextElem=WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.TAG_NAME, "th")))
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
		#print(str(webe.text.encode('ascii', errors='ignore')))
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
					#listheader=str(lista[0].find_element_by_class_name("valueField").text.encode('ascii', errors='ignore'), 'utf-8')
					listheader=lista[0].find_element_by_class_name("valueField").text.encode('ascii', errors='ignore').decode('utf-8')
					print(listheader)
					for i in range(len(listrows)):
						v=0.0
						if(listvalues[i].text=="No Data"):
							v=0.0
							#dateDict[listrows[i].text]=dateDict[listrows[i].text]+'{:25}'.format("0")
						else:
							for char in listvalues[i].text:
								try:
									char.encode('ascii')
								except UnicodeEncodeError:
									char=unicodedata.numeric(char)
								v=v+float(char)
						dateDict[listrows[i].text]=dateDict[listrows[i].text]+'\t'+str(v)
						
					nutrientsList.append(listheader)
					
				else:
					for div in lista:
						listrows=div.find_elements_by_class_name("dateColumn")
						listvalues=div.find_elements_by_class_name("valueColumn")
						#listheader=str(div.find_element_by_class_name("valueField").text.encode('ascii', errors='ignore'), 'utf-8')
						listheader=div.find_element_by_class_name("valueField").text.encode('ascii', errors='ignore').decode('utf-8')
						print(listheader)
						for i in range(len(listrows)):
							v=0.0
							if(listvalues[i].text=="No Data"):
								v=0
							else:
								for char in listvalues[i].text:
									try:
										char.encode('ascii')
									except UnicodeEncodeError:
										char=unicodedata.numeric(char)
									v=v+float(char)
							#dateDict[listrows[i].text]=dateDict[listrows[i].text]+'{:<35}'.format(v)
							dateDict[listrows[i].text]=dateDict[listrows[i].text]+'\t'+str(v)
		
						nutrientsList.append(listheader)
						
def getNutrientInfo(num):

	global nutrientsList
	global dateDict
	number="mast_level1_cph_mast_level2_cph_gvNutrients_btnSelect_"+str(num)
	try:
		element=WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.ID, "mast_level1_cph_mast_level2_cph_lbDataDetails")))
	finally:
		webe=driver.find_element_by_id(number)
		print(webe.text.encode('ascii', errors='ignore').decode('utf-8'))
		webe.click()
		try:
			chartElem=WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.ID, "mast_level1_cph_mast_level2_cph_profiletextChart")))
			driver.find_element_by_id("mast_level1_cph_mast_level2_cph_lbDataDetails").click()
		finally:
			try:		
				nextElem=WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.TAG_NAME, "th")))
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
	#print(a)
	f.write(a)
	#dateDictSorted=collections.OrderedDict(sorted(dateDict.items()))
	for key in sorted(dateDict):
		f.write(key+dateDict[key]+'\n')
		#print(key+'\t'+dateDict[key])



###
###This part will just "Initialize" the browser: logging in and navigating to the necessary pages
###Uncomment Chromedriver and comment PhantomJS for JS debugging issues
###

#ROOT_DIR=path.dirname(path.abspath(__file__))
#driver=webdriver.PhantomJS(executable_path=path.join(ROOT_DIR, 'phantomjs-2.1.1-macosx/bin/phantomjs'))
driver=webdriver.PhantomJS(executable_path='phantomjs')
print(path.join(ROOT_DIR, 'phantomjs-2.1.1-macosx/bin/phantomjs'))

###PARAMETERS
user=sys.argv[1]
password=sys.argv[2]
firstDate=sys.argv[3]
secondDate=sys.argv[4]
fileOutput="output.txt"

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
###Add all nutrient informations
addAllNut()
###Print to file in outputNutrients
outputNutrients()

driver.close()