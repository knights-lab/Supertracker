from selenium import webdriver
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import unicodedata
import collections
import os.path as path


def waiter(browser):
	global firstDate
	elements = browser.find_elements_by_xpath("//*[text()='Date']/parent::*/parent::*/following-sibling::tr")
	if len(elements) != 0:
		print(len(elements))
		print(elements[0])
		print(elements[0].text)
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
		date=WebDriverWait(driver, 30).until(preWaiter)
		driver.implicitly_wait(5)
		element=WebDriverWait(driver, 120).until(waiter)
		print("element1: "+element[0].text)
		#print("element1: "+element[0].getAttribute("value"))
		print("element2: "+date[0].text)
		#print("element2: "+date[0].getAttribute("value"))
		# if(element[0].text!=element2[0].text):
		# 	element=element2
		# else:
		print('nothing wrong')
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
						if("empty" in tempXpath[0].text.lower()):
							pass
						else:
							dateDict[newDate]=dateDict[newDate]+"\t "+tempXpath[0].text

			else:
				for td in range(4, len(elements)):
					tempXpath=elements[td].find_elements_by_xpath("descendant::span")
					if(len(tempXpath)!=0):
						if("empty"in tempXpath[0].text.lower()):
							pass
						else:
							dateDict[newDate]=dateDict[newDate]+" \t "+tempXpath[0].text

	print(dateDict)


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
getFoodInfo()
