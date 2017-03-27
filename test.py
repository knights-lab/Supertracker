import datetime
import os.path as path
import sys
import string



def generateDate(datestr):

	"""Will generate list of dates and input into global Datedict"""
	if(len(datestr)>10):
		dateList=[]
		res=datestr.split('\n')
		res=res[0].split('-')
		startDate=datetime.datetime.strptime(res[0], "%m/%d/%y")
		endDate=da=datetime.datetime.strptime(res[1], '%m/%d/%y')
		while(startDate!=endDate):
			startDate+=datetime.timedelta(days=1)
			print(startDate.strftime("%m/%d/%y"))
	else:
		print(datestr.split('\n')[0])
def getFoodIndex(strung):
	uppercaseNotFound=True
	i=0
	while(uppercaseNotFound and i<len(strung)):
		if(strung[i] in string.ascii_uppercase):
			uppercaseNotFound=False
			return i
		else:
			i=i+1
	print("No FOOD FOUnd")
	return -1


formatStr="Date"+'\t'+"Portion"+'\t'+"PortionAmt"'+\t'+"Food"+'\t'+'Original'+'\n'
print(formatStr)
newDate="01/07/17"
strung="1 mug (8 fl oz) Coffee, brewed, regular"
q="&nbsp;"
try:
	food=strung
	separate=getFoodIndex(food)
	portion=food[:separate].split(" ")
	print("PORTIONLIST")
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
print(meal)
mealData='\t'.join(str(d) for d in meal)+'\n'
print(mealData)
print('q')
print(q)
