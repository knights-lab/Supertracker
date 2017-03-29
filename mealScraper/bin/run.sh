#!/bin/bash

echo "Executing Meal Scraper script..."
#python mealScraper.py $1 $2 $3 $4
echo "Meal Scraper done!"
echo "Create Mapping..."
Rscript foodCodeMapper.r
echo "fin"