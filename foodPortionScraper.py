# Food Portion Scraper
# Scrapes Information from Supertracker's Food Details Report Page
# Due to Supertracker being slow, input is a txt file with specific dates. 

# Input File: 
# In order to simply enter a range of dates, add a dash between two dates
# 	Ex. 01/02/16-01/10/16
# 	For more information look at included file (sample.txt)
#
#	FYI: Input file will have to local, or have a relative path to this script file. 
#	Otherwise go to line 178 and just edit in the absolute path.
#
# Takes 3 Things as Input:
# 	1. Username
# 	2. Password
# 	3. Input Date File
#
# Sample call: python foodPortionScraper username password asdf.txt
#		


# ### SAMPLE PARAMETERS
user='chaustinkim'
password='asdfgh123'
inputf="sample.txt"
fileOutput="food_portion_output.txt"


from selenium import webdriver
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import unicodedata
import collections
import os.path as path
import sys
import datetime


def generateDate(datestr):
	global dateDict
	""" Will generate list of dates and input into global Datedict """
	if(len(datestr)>10):
		#dateList=[]
		res=datestr.split('\n')
		res=res[0].split('-')
		startDate=datetime.datetime.strptime(res[0], "%m/%d/%y")
		endDate=da=datetime.datetime.strptime(res[1], '%m/%d/%y')
		while(startDate!=endDate):
			print(startDate.strftime("%m/%d/%y"))
			dateDict[startDate.strftime("%m/%d/%y")]=""
			startDate+=datetime.timedelta(days=1)
		print(startDate.strftime("%m/%d/%y"))
		dateDict[startDate.strftime("%m/%d/%y")]=""
	else:
		print(datestr.split('\n')[0])
		dateDict[datestr.split('\n')[0]]=""


def getFoodPortions():
	global nutrientsList
	global dateDict
	try:
		checkboxesContain=WebDriverWait(driver, 30).until(bwaiter)
	finally:
		# Check all "Select All Buttons" for "Food Groups & Oils" 
		
		checkboxesContain[0].find_elements_by_tag_name('a')[0].click()
		foods="mast_level1_cph_mast_level2_cph_FoodGroupRepeater_lblItemText_"
		for i in range(20):
			nutrientsList.append(checkboxesContain[0].find_element_by_id(foods+str(i)).text)
		print("first section added")
		#
		#and "Limits"
		
		checkboxesContain[1].find_elements_by_tag_name('a')[0].click()
		limits="mast_level1_cph_mast_level2_cph_LimitsRepeater_lblItemText_"

		for limit in range(4):
			nutrientsList.append(checkboxesContain[1].find_element_by_id(limits+str(limit)).text)
		print("Second section added")

		#Start rolling in the dates and getting info
		for date in dateDict:
			driver.find_element_by_name("ctl00$ctl00$mast_level1_cph$mast_level2_cph$txtFrom").clear()
			driver.find_element_by_name("ctl00$ctl00$mast_level1_cph$mast_level2_cph$txtFrom").send_keys(date)
			try:
				driver.find_element_by_class_name("createbutton").find_element_by_tag_name('a').click()
				currDate="Date: "+date
				print(currDate)
				getDateData=WebDriverWait(driver, 30).until(EC.text_to_be_present_in_element((By.XPATH, "//div[@id='VisibleReportContentctl00_ctl00_mast_level1_cph_mast_level2_cph_FoodDetailsRptVwr_ctl09']/descendant::table/descendant::table/descendant::table//child::tr[4]//descendant::span[2]"), currDate))
			finally:
				try:
					getPors=WebDriverWait(driver, 120).until(waiter)
				finally:
					for td in getPors:
							v=0
							if(td.text=="No Data"):
								v=0
								dateDict[date]=dateDict[date]+'\t'+str(v)
							else:

								#Left this as split instead of find because not sure how to deal with units
								quantity=td.text.split(' ')[0]
								#print(quantity[:-1])
								try:
									char=quantity[-1]
									char.encode('ascii')
									v=int(quantity)
								except UnicodeEncodeError:
									char=unicodedata.numeric(char)
									if(len(quantity)>1):
										v=int(quantity[:-1])+char
									else:
										v=char
								# for char in quantity:
								# 	try:
								# 		char.encode('ascii')
								# 	except UnicodeEncodeError:
								# 		char=unicodedata.numeric(char)
								# 	v=v+float(char)

							dateDict[date]=dateDict[date]+'\t'+str(v)

def waiter(browser):

    elements = browser.find_elements_by_xpath("//div[@id='VisibleReportContentctl00_ctl00_mast_level1_cph_mast_level2_cph_FoodDetailsRptVwr_ctl09']/descendant::table/descendant::table/descendant::table//child::tr[last()-3]//child::td")
    if len(elements) != 0:
        return elements[2:]
    elif(len(browser.find_elements_by_id("mast_level1_cph_mast_level2_cph_lblRptEmpty"))!=0):
    	print("ERROR. Improper dates added. Please Redo. \n")
    	return True
    return False

def bwaiter(browser):
	elem=driver.find_element_by_id("selectareportdivcontainer").find_elements_by_class_name("box")
	if len(elem)!=0:
		print('yes')
		return elem 
	return False



def outputNutrients():
# Output result to food_portion_output.txt

	global fileOutput
	f=open(fileOutput, 'w')
	global nutrientsList
	global dateDict
	a=''

	# Will optimize using ''.join later if needed
	for i in nutrientsList:
		a=a+'\t'+i
	a=a+'\n'
	f.write(a)
	dateDictSorted=collections.OrderedDict(sorted(dateDict.items()))
	for key, value in dateDictSorted.items():
		f.write(key+value+'\n')

### PARAMETERS

# user=sys.argv[1]
# password=sys.argv[2]
# inputf=sys.argv[3]

nutrientsList=[]	
dateDict={}

# Create Browser
ROOT_DIR=path.dirname(path.abspath(__file__))
#driver=webdriver.PhantomJS(executable_path=path.join(ROOT_DIR, 'phantomjs-2.1.1-macosx/bin/phantomjs'))
driver=webdriver.Chrome(executable_path=path.join(ROOT_DIR, 'chromedriver'))

# Get Sample file and populate dateDict.
input_path=executable_path=path.join(ROOT_DIR, inputf)
dateFile=open(input_path,'r')
dateList=dateFile.readlines()
for i in dateList:
	generateDate(i)


### begin Selenium work
driver.get("https://www.supertracker.usda.gov/login.aspx")
driver.find_element_by_id("mast_level1_cph_mast_level2_cph_login_UserName").send_keys(user)
driver.find_element_by_id("mast_level1_cph_mast_level2_cph_login_Password").send_keys(password)
driver.find_element_by_id("mast_level1_cph_mast_level2_cph_login_LoginButton").click()
driver.get('https://www.supertracker.usda.gov/FoodDetailsReport.aspx')

# Retrieve
getFoodPortions()

# Print to file in outputNutrients
outputNutrients()