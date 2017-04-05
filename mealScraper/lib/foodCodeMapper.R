# Takes output from mealScraper and transforms to appropriate meal codes
# 

#script.dir <- dirname( sys.frame(1)$ofile)
library('optparse')

option_list <- list(
 		make_option(c("-o", "--outputfile"), type="character",
 			help="Output file name [REQUIRED]"),
        make_option(c("-d", "--directory"), type="character",
 			help="Full path to MealScraper folder [REQUIRED]")

 			)
 			
opts <- parse_args(OptionParser(option_list=option_list), 
 		args=commandArgs(trailing=TRUE))
 		

setwd(opts$directory)


foods <- read.table( paste( getwd(), "output", "mealSummaryOutput.txt",sep="/"), header=TRUE, sep="\t", quote="")
meals <- read.csv( paste( getwd(), "data", 'SuperTracker Foods Database 2017.csv', sep='/'))
output <- merge( foods, meals, by.x = "Food", by.y = "foodname", all.x=TRUE)

write.table(output, file=paste(getwd(), "output", opts$outputfile, sep="/"), sep="\t", eol="\n", quote=FALSE, row.names=F)
