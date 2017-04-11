This script queries the dates listed in the provided datesfile from SuperTracker, retrieves all foods grouped by “food groups” (e.g. Whole Grains, Refined Grains, Dark Green Vegetables, etc.) and portions eaten, then outputs a table containing all food groups and portions for all dates. Note that this is different from nutrientScraper (queries nutrient components) and mealScraper (queries all foods and portions eaten).

PREREQUISITES:
1. python 3 and selenium must be properly installed
2. make sure phantomJS folder is in /Supertracker

example:
	python foodGroupScraper.py -u pvangay -p password123 -i dates.txt -o output.txt

parameters:
	user - super tracker username
	password - supertracker password
	dates file - file containing dates to get (ranges and/or single dates separated by newlines are acceptable, with date format MM/DD/YY)
	outputfile - final outputfile containing all foods and food codes per date (written to /output)


example dates file contents:
01/01/16-02/01/16
10/31/16
05/06/16