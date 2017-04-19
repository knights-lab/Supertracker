#!/bin/bash

echo "Executing Meal Scraper script..."
python3 ./lib/mealScraper.py -u $1 -p $2 -f $3 -s $4
echo "Meal Scraper done!"
echo "Create Mapping..."
echo "Rscript ./lib/foodCodeMapper.r -o $5 -d $PWD"
Rscript ./lib/foodCodeMapper.r -o $5 -d $PWD
echo "fin"