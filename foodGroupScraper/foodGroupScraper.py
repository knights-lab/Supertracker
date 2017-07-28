# Food Portion Scraper
# Scrapes Information from Supertracker's Food Details Report Page
# Due to Supertracker being slow, input is a txt file with specific dates. 

# Input File: 
# In order to simply enter a range of dates, add a dash between two dates
#   Ex. 01/02/16-01/10/16
#   For more information look at included file (sample.txt)
#
#   FYI: Input file will have to local, or have a relative path to this script file. 
#   Otherwise go to line 178 and just edit in the absolute path.
#
# Takes 3 Things as Input:
#   1. Username
#   2. Password
#   3. Input Date File
#
# Sample call: python foodPortionScraper username password asdf.txt
#       


# ### SAMPLE PARAMETERS
# user='chaustinkim'
# password='asdfgh123'
# inputf="sample.txt"
# fileOutput="food_portion_output.txt"


from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import unicodedata
import collections
import os.path as path
import sys
import datetime
import argparse



def make_arg_parser():
    parser = argparse.ArgumentParser(description='Scrapes portion and meal data')
    parser.add_argument('-o', '--outputdir', help='Output directory', required=True)    
    parser.add_argument('-u', '--user', help='Supertracker user', required=True)
    parser.add_argument('-p', '--password', help='password', required=True)
    parser.add_argument('-i', '--inputDates', help='Get dates', required=False)
    return parser

def generateDate(datestr):
    global dateList
    global dateDict
    if(len(datestr)>10):
        res = datestr.split('\n')
        res = res[0].split('-')
        startDate = res[0]
        endDate = res[1]
        generateDates(startDate, endDate)
    else:
        datestr=datestr.split('\n')[0]
        print(datestr)
        dateList.append(datestr)
        dateDict[datestr]=""

def generateDates(start, end):
    global dateList
    global dateDict
    """ Will generate list of dates and input into global list """
    #if(len(datestr)>10):
        #dateList=[]
        
    startDate=datetime.datetime.strptime(start, "%m/%d/%y")
    endDate=da=datetime.datetime.strptime(end, '%m/%d/%y')
    while(startDate!=endDate):
        print(startDate.strftime("%m/%d/%y"))
        dateList.append(startDate.strftime("%m/%d/%y"))
        dateDict[startDate.strftime("%m/%d/%y")]=""
        startDate+=datetime.timedelta(days=1)
    print(startDate.strftime("%m/%d/%y"))
    dateList.append(startDate.strftime("%m/%d/%y"))
    #return dateList
    dateDict[startDate.strftime("%m/%d/%y")]=""

def getFoodPortions():
    global driver
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
        #Xpaths were reallly weird for nutrients, so just decided to do this instead
        seafood=nutrientsList[len(nutrientsList)-4]
        nutrientsList[len(nutrientsList)-4]=nutrientsList[len(nutrientsList)-3]
        nutrientsList[len(nutrientsList)-3]=nutrientsList[len(nutrientsList)-2]
        nutrientsList[len(nutrientsList)-2]=seafood
        print("first section added")
        
        # and "Limits"
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
                currDate="Date: "+ date
                print(currDate)
                getDateData=WebDriverWait(driver, 120).until(EC.text_to_be_present_in_element((By.XPATH, "//div[@id='VisibleReportContentctl00_ctl00_mast_level1_cph_mast_level2_cph_FoodDetailsRptVwr_ctl09']/descendant::table/descendant::table/descendant::table//child::tr[4]//descendant::span[2]"), currDate))
            # except TimeoutException:
            #     print("After inputting date, food group table is not rendering! Increase wait time for getDateData")
            finally:
                try:
                    getPors=WebDriverWait(driver, 120).until(waiter)
                except TimeoutError:
                    print('increase getPors wait time')
                finally:
                    for td in getPors:
                            v=0
                            if(td.text=="No Data"):
                                v=0
                                dateDict[date]=dateDict[date]+'\t'+str(v)
                            else:
                                try:
                                    food=td.text
                                    portion=food.split(" ")
                                    
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
                                if(' '.join(portion[1:])==""):
                                    meal=("Calories", str(v))
                                else:
                                    meal=(''.join(portion[1]), str(v))
                                #print(meal)
                                mealData='\t'.join(str(d) for d in meal)+'\n'
                                #print(mealData)
                                dateDict[date]=dateDict[date]+mealData

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

# def foodWaiter(browser):
#     #initialize foods properly
#     elements=driver.find_elements_by_id("//div[@id='VisibleReportContentctl00_ctl00_mast_level1_cph_mast_level2_cph_FoodDetailsRptVwr_ctl09']/descendant::table/descendant::table/descendant::table//child::tr[7]//child::td[1]")
#     if len(elements) !=0:
#         print('foods found')
#         return elements
#     print('attaching')
#     return False

def outputNutrients():
    # Output result to food_portion_output.txt
    global fileOutput
    global nutrientsList
    global dateList
    global dateDict
    global ROOT_DIR
    a=''
    f=open(fileOutput, 'w')
    formatStr="Date"+'\t'+"PortionUnit"+'\t'+"Amount"+'\t'+"FoodType"+'\n'
    f.write(formatStr)
    for i in dateList:
        print(i)
        print(formatStr)
        oneMealList=dateDict[i].split('\n')
        for it in range(len(oneMealList)-1):
            print(oneMealList[it]+ " " +nutrientsList[it])
            f.write('{}\t{}\t{}\n'.format(i, oneMealList[it], nutrientsList[it]))
    f.close()



def main():
    global nutrientsList
    global driver
    global dateDict
    global dateList
    global ROOT_DIR
    global fileOutput
    global dateList
    try:
        #Get params
        parser = make_arg_parser()
        args = parser.parse_args()
        user=args.user
        password = args.password
        fileOutput = args.outputdir
        nutrientsList=[]    
        dateDict = {}
        dateList = []
        # Create Browser
        ROOT_DIR=path.dirname(path.abspath(__file__))
        driver=webdriver.PhantomJS(executable_path='../phantomjs-2.1.1-macosx/bin/phantomjs')
        #driver=webdriver.Chrome(executable_path='../chromedriver')

        # Get Sample file and populate dateDict.
        input_path=path.join(ROOT_DIR, args.inputDates)
        dateFile=open(input_path,'r')
        dateA=dateFile.readlines()
        for i in dateA:
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
        driver.close()
    except BaseException as e:
        print('There seems to be an error. There\'s a good chance that it involves the variable referenced below:')
        print(str(e))

if __name__ == '__main__':
    # Python syntax to run main when script is called
    main()