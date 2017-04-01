#!/bin/bash

echo "Executing Meal Scraper script..."
python3 mealScraper.py -u $1 -p $2 -f $3 -s $4 	-o $5
echo "Meal Scraper done!"
echo "Create Mapping..."
Rscript foodCodeMapper.r
echo "fin"