from selenium import webdriver
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import unicodedata
import collections
import os.path as path
import string


#USE supertracker.csv to match supertracker food des cwith code
def waiter(browser):
	elements = browser.find_elements_by_xpath("//*[text()='Date']/parent::*/parent::*/following-sibling::tr")
	if len(elements) != 0:
		print(len(elements))
		return elements
	print('fuck')
	return False

def getFoodInfo():
	global foodstr
	global dateDict
	
	try:
		driver.find_element_by_id("mast_level1_cph_mast_level2_cph_btnreport").click()
		#element=WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.LINK_TEXT, "Your plan is based on a 2400 Calorie allowance.")))
		#element=WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "ctl00_ctl00_mast_level1_cph_mast_level2_cph_MealSummaryRptVwr")))
		element=WebDriverWait(driver, 120).until(waiter)

	finally:
		newDate=""
		print("0:"+element[0].text)
		print("1:"+element[1].text)
		print("2:"+ element[2].text)
		print("3:"+element[3].text)
		print("4:"+element[4].text)
		#print("5:"+element[5].text)
		#print("6:"+element[6].text)
		for i in element:				#FOR EACH ROW in TABLE
			#newDate=""
			elements = i.find_elements_by_xpath("child::td")		#find all td in row
			print("1:"+elements[1].text)
			print("2:"+ elements[2].text)
			print("3:"+elements[3].text)
			print("4:"+elements[4].text)
			print("5:"+elements[5].text)
			print("6:"+elements[6].text)
			if(elements[2].text!=" " and elements[2].text!=""):
				newDate=elements[2].text
				print("new date is"+newDate)

				for td in range(3, len(elements)):
					tempXpath=elements[td].find_elements_by_xpath("descendant::span")
					if(len(tempXpath)!=0):
						print(tempXpath[0].text)
						if("empty" in tempXpath[0].text.lower() or tempXpath[0].text==u'\xa0'):
							print('empty')
							pass
						else:
							try:
								food=tempXpath[0].text
								separate=getFoodIndex(food)
								portion=food[:separate].split(" ")
								print("portion")
								print(portion)
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
							meal=(newDate, ' '.join(portion[1:-1]), str(v), food[separate:])
							mealData='\t'.join(str(d) for d in meal)+'\n'
							print(mealData)
							foodstr=foodstr+mealData

			else:
				print('date not found?')
				for td in range(4, len(elements)):
					tempXpath=elements[td].find_elements_by_xpath("descendant::span")
					if(len(tempXpath)!=0):
						print(tempXpath[0].text)
						if("empty"in tempXpath[0].text.lower() or tempXpath[0].text==u'\xa0'):
							print('pass')
							pass
						else:
							try:
								food=tempXpath[0].text
								separate=getFoodIndex(food)
								portion=food[:separate].split(" ")

								portionAmt=portion[0]
								print("PORTION IS")
								print(portionAmt)
								char=portionAmt[-1]
								char.encode('ascii')
								v=int(portionAmt)
							except UnicodeEncodeError:
								char=unicodedata.numeric(char)
								if(len(quantity[0])>1):
									v=int(portionAmt[:-1])+char
								else:
									v=char
							meal=(newDate, ' '.join(portion[1:-1]), str(v), food[separate:])
							mealData='\t'.join(str(d) for d in meal)+'\n'
							print(mealData)
							foodstr=foodstr+mealData
							

#Return index of first uppercase
def getFoodIndex(strung):
	uppercaseNotFound=True
	i=0
	while(uppercaseNotFound and i<len(strung)):
		if(strung[i] in string.ascii_uppercase):
			uppercaseNotFound=False
			return i
		else:
			i=i+1
	return -1

ROOT_DIR=path.dirname(path.abspath(__file__))
#driver=webdriver.PhantomJS(executable_path=path.join(ROOT_DIR, 'phantomjs-2.1.1-macosx/bin/phantomjs'))
driver=webdriver.Chrome(executable_path=path.join(ROOT_DIR, 'chromedriver'))

###PARAMETERS
user='chaustinkim'
password='asdfgh123'
firstDate="01/07/17"
secondDate="01/8/17"
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
foodstr=""
formatStr="Date"+'\t'+"Portion"+'\t'+"PortionAmt"+'\t'+"Food"+'\t'+'Original'+'\n'
print(formatStr)
getFoodInfo()
print(foodstr)
