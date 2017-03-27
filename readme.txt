#supertracker.py



====About====
This script will
1. Use Selenium(python module) to automate javascript loading. To skip having an actual browser open, I used PhantomJS(JS Browser), an invisible browser which can skip graphics rendering.
2. Use Selenium to find necessary HTML text
3. Retrieve Nutrient information from all samples
4. Write results to file output.csv

To Debug Graphics, download and run ChromeDriver instead of PhantomJS in script file not included)


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

===More Information===
	fn getFoodGroupInfo focuses on the 6 food groups provided (0-5)
	fn getNutrientInfo focuses on the 34 nutrient groups (0-33)
	If for any reason only one of the categories are needed, it can be found by calling the requisite function and the proper food number.