# Takes output from mealScraper and transforms to appropriate meal codes
# 

#script.dir <- dirname( sys.frame(1)$ofile)
setwd("~/Documents/mealScraper")
foods <- read.table( paste( getwd(), "output", "mealSummaryOutput.txt",sep="/"), header=TRUE, sep="\t", quote="")
meals <- read.csv( paste( getwd(), "output", 'SuperTracker Foods Database 2017.csv', sep='/'))
output <- merge( foods, meals, by.x = "Food", by.y = "foodname", all.x=TRUE)

write.table( output, file=paste(getwd(), "output", "mealScraperOutput.txt", sep="/"), sep="\t", eol="\n", quote=FALSE)
