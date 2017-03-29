from selenium import webdriver
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import unicodedata
import collections
import os.path as path
import string
import sys
import datetime


def generateDates(start, end):
	print("Generating Dates")
	global dateList
	""" Will generate list of dates and input into global list """
	#if(len(datestr)>10):
		#dateList=[]
		
	startDate=datetime.datetime.strptime(start, "%m/%d/%y")
	endDate=da=datetime.datetime.strptime(end, '%m/%d/%y')
	while(startDate!=endDate):
		print(startDate.strftime("%m/%d/%y"))
		dateList.append(startDate.strftime("%m/%d/%y"))
		#dateDict[startDate.strftime("%m/%d/%y")]=""
		startDate+=datetime.timedelta(days=1)
	print(startDate.strftime("%m/%d/%y"))
	dateList.append(startDate.strftime("%m/%d/%y"))
	#return dateList
		#dateDict[startDate.strftime("%m/%d/%y")]=""

def getFoodIndex(strung):
	#Find index where portion desc ends and food begins, first capital letter
	i=0
	while(i<len(strung)):
		if(strung[i] in string.ascii_uppercase):
			return i
		else:
			i = i + 1
	print("No FOOD FOUND")
	return -1

def waiter(browser):
	global firstDate
	elements = browser.find_elements_by_xpath("//*[text()='Date']/parent::*/parent::*/following-sibling::tr")
	if len(elements) != 0:
		return elements
	return False

def preWaiter(browser):
	global firstDate
	global secondDate
	elements = browser.find_elements_by_xpath("//*[text()='Date']/parent::*/parent::*/following-sibling::tr/child::td/child::div[text()='"+secondDate+"']")
	if len(elements) != 0:
		print("elements found: "+elements[0].text + "aaa")
		if(secondDate not in elements[0].text):
			return False
		print(len(elements))
		print(elements[0])
		print("ELEMENT IS"+elements[0].text)
		return elements
	print("fuck")
	return False

def getFoodInfo():
	global dateDict
	
	try:
		driver.find_element_by_id("mast_level1_cph_mast_level2_cph_btnreport").click()

		#Wait for DOM to attach
		date=WebDriverWait(driver, 30).until(preWaiter)
		driver.implicitly_wait(5)
		element=WebDriverWait(driver, 120).until(waiter)
		print("element1: "+element[0].text)
		print("element2: "+date[0].text)

	finally:
		newDate=""
		for i in element:				#FOR EACH ROW in TABLE
			print("beginning iteration")
			elements = i.find_elements_by_xpath("child::td")		#find all td in row
			if(elements[2].text!=" "):
				newDate=elements[2].text
				print(newDate)
				dateDict[newDate]=""
				for td in range(3, len(elements)):
					tempXpath=elements[td].find_elements_by_xpath("descendant::span")
					if(len(tempXpath)!=0):
						utfString=tempXpath[0].text

					#Check for empty conditions
						if("empty" in utfString.lower() or utfString=='\s' or "\xa0" in utfString or utfString[0]==" "):
							pass
						else:
							try:
								food=utfString
								separate=getFoodIndex(food)
								portion=food[:separate].split(" ")
								#print("PORTIONLIST")
								#print(portion)
								portionAmt=portion[0]
								char=portionAmt[-1]
								char.encode('ascii')
								v=int(portionAmt)
							except UnicodeEncodeError:
								char=unicodedata.numeric(char)
								if(len(portionAmt)>1):
									v=int(portionAmt[:-1])+char
								else:
									v=char
	#Date, Portion, Food
							meal=(' '.join(portion[1:-1]), str(v), food[separate:])
							#print(meal)
							mealData='\t'.join(str(d) for d in meal)+'\n'
							#print(mealData)
							dateDict[newDate]=dateDict[newDate]+mealData

			else:
				for td in range(3, len(elements)):
					tempXpath=elements[td].find_elements_by_xpath("descendant::span")
					if(len(tempXpath)!=0):
						utfString=tempXpath[0].text
						if("empty" in utfString.lower() or utfString=='\s' or "\xa0" in utfString or utfString[0]==" "):
							pass
						else:
							try:
								food=utfString
								separate=getFoodIndex(food)
								portion=food[:separate].split(" ")
								print("PORTIONLIST")
								#print(portion)
								portionAmt=portion[0]
								char=portionAmt[-1]
								char.encode('ascii')
								v=int(portionAmt)
							except UnicodeEncodeError:
								char=unicodedata.numeric(char)
								if(len(portionAmt)>1):
									v=int(portionAmt[:-1])+char
								else:
									v=char
							meal=(' '.join(portion[1:-1]), str(v), food[separate:])
							#print(meal)
							mealData='\t'.join(str(d) for d in meal)+'\n'
							#print(mealData)
							dateDict[newDate]=dateDict[newDate]+mealData

	for i in dateDict:
		print(dateDict[i])
	#print(dateDict)

def writeOutput():
	global fileOutput
	global dateList
	global dateDict
	f=open(fileOutput, 'w')
	formatStr="Date"+'\t'+"Portion"+'\t'+"PortionAmt"+'\t'+"Food"+'\n'
	f.write(formatStr)
	for i in dateList:
		oneMealList=dateDict[i].split('\n')
		for it in range(len(oneMealList)-1):
			f.write('{}\t{}\n'.format(i, oneMealList[it]))

ROOT_DIR=path.dirname(path.abspath(__file__))
#driver=webdriver.PhantomJS(executable_path=path.join(ROOT_DIR, 'phantomjs-2.1.1-macosx/bin/phantomjs'))
driver=webdriver.Chrome(executable_path=path.join(ROOT_DIR, 'chromedriver'))

###PARAMETERS
user='chaustinkim'
password='asdfgh123'
firstDate="01/05/17"
secondDate="01/09/17"
fileOutput="foodOutput.txt"

driver.get("https://www.supertracker.usda.gov/login.aspx")
driver.find_element_by_id("mast_level1_cph_mast_level2_cph_login_UserName").send_keys(user)
driver.find_element_by_id("mast_level1_cph_mast_level2_cph_login_Password").send_keys(password)
driver.find_element_by_id("mast_level1_cph_mast_level2_cph_login_LoginButton").click()

driver.get("https://www.supertracker.usda.gov/MealSummaryReport.aspx")
driver.find_element_by_name("ctl00$ctl00$mast_level1_cph$mast_level2_cph$txtFrom").clear()
driver.find_element_by_name("ctl00$ctl00$mast_level1_cph$mast_level2_cph$txtFrom").send_keys(firstDate)
driver.find_element_by_name("ctl00$ctl00$mast_level1_cph$mast_level2_cph$txtThru").clear()
driver.find_element_by_name("ctl00$ctl00$mast_level1_cph$mast_level2_cph$txtThru").send_keys(secondDate)
driver.find_element_by_id("mast_level1_cph_mast_level2_cph_MealCheckBoxAll").click()



dateDict={}
dateList=[]
generateDates(firstDate, secondDate)
getFoodInfo()
writeOutput()
driver.close()
