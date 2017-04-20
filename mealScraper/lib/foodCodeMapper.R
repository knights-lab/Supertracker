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


foods <- read.table( paste( getwd(), "output", "mealSummaryOutput.txt",sep="/"), header=TRUE, sep="\t", quote="", as.is=T, strip.white=T)
meals <- read.csv( paste( getwd(), "data", 'SuperTracker Foods Database 2017.csv', sep='/'), as.is=T, strip.white=T)
output0 <- merge( foods, meals, by.x = "Food", by.y = "foodname", all.x=TRUE, all.y=FALSE)

portions <- read.table( paste( getwd(), "data", "SuperTracker Foods Database 2017 - Portion Data Tab.txt", sep="/"), header=TRUE, sep="\t", as.is=T, strip.white=T, quote="")

# for any foods not defined, take them out and add them back in later
new.foods <- output0[is.na(output0$foodcode),]
output0 <- output0[!is.na(output0$foodcode),]

output <- merge( output0, subset(portions, select = c(foodname, foodcode, modcode, portion_code, portiondesc, default.portion, portionwgt)), by.x=c("foodcode", "modcode", "Portion" ), by.y=c("foodcode", "modcode", "portiondesc" ), all.x=TRUE)
output$grams <- (output$PortionAmt/as.numeric(output$default.portion))*output$portionwgt
output <-subset(output, select=c(DATE, Food, foodcode, modcode, portion_code, Portion, PortionAmt, default.portion, portionwgt, grams))

NAS <- rep(NA, nrow(new.foods))
finaloutput <- rbind(output, cbind(DATE=new.foods$DATE, Food=new.foods$Food, foodcode=NAS, modcode=NAS, portion_code=NAS, Portion=new.foods$Portion, PortionAmt=new.foods$PortionAmt, default.portion=NAS, portionwgt=NAS, grams=NAS))
# add new.foods back in

write.table(finaloutput, file=paste(getwd(), "output", opts$outputfile, sep="/"), sep="\t", eol="\n", quote=FALSE, row.names=F)
