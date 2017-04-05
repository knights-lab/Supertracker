This script queries a range of dates from SuperTracker, retrieves all foods and portions eaten, then outputs a table containing all foods, food codes, portions, portion codes, for all dates within the specified range. Note that this is different from nutrientScraper in that it queries the foods eaten, not the nutrient components.

PREREQUISITES:
1. python 3 and selenium must be properly installed
2. place “SuperTracker Foods Database 2017.csv” file in /data
3. make sure phantomJS folder is in /Supertracker
4. make sure the optparse package is installed in your local version of R

example:
	./bin/scrape.foods.sh pvangay password123 01/01/17 01/31/17 pvangay_jan2017_foods.txt

parameters:
	user - super tracker username
	password - supertracker password
	first Date - start date of range to query (ex. "mm/dd/yy")
	second Date - end date of range to query (ex. "mm/dd/yy")
	outputfile - final outputfile containing all foods and food codes per date (written to /output)

ADDITIONAL NOTES
1. mealScraper.py scrapes the meal summaries for every date
2. foodCodeMapper.R merges the food descriptions with the super tracker CSV file in order to obtain food codes

