
====PreReqs====
1. Install Selenium "pip install selenium" or "pip3 install selenium"
2. PhantomJS (included)


==Getting Started==
File can be run in terminal.
Parameters:
1. Username
2. Password
3. Start Date*
4. End Date*

*Date inputs are very sensitive and must be executed in the following format:
01/05/17

To Debug Graphics, download and run ChromeDriver instead of PhantomJS in script file not included)


-----------------------------------------------------------
SCRAPER INFO
-----------------------------------------------------------
Name: sel.py
====About====
This script will
1. Retrieve Nutrient information from all samples
2. Write results to file output.csv


===More Information===
	fn getFoodGroupInfo focuses on the 6 food groups provided (0-5)
	fn getNutrientInfo focuses on the 34 nutrient groups (0-33)
	If for any reason only one of the categories are needed, it can be found by calling the requisite function and the proper food number.
-------------------------------------------------------

-----------------------------------------------------------
SCRAPER INFO
-----------------------------------------------------------
Name: mealScraper
====About====
This script will
1. Retrieve meal information
2. Write results to /output/mealSummaryOutput.txt
3. Map meals to food codes
4. Final output to mealScraperOutput.txt