#weekly_sum_sediment_April_14_2014.R
#gfiske April 2014
#for BPE sediment flux cartogram
#creates weekly sum sediment values
#it does this by first summing the "kg/s mean sed value" by day (i.e. i.e. 60*60*24*sedvalue) then by week 

#this will be used for the cartogram that shows fluctuation through the year

#load packages
library(gsubfn)

#set working directory
setwd("\\\\ripple\\Data\\Global\\CarbonRivers\\bernhard_global_sediment\\sediment\\test_folder\\")
rm(list = ls())

#read a sediment files from Albert
myfiles = list.files("\\\\ripple\\Data\\Global\\CarbonRivers\\bernhard_global_sediment\\sediment\\", pattern = "*.txt", full.names=T)

#create a data frame with the years
years <- as.data.frame(c(1960:2011))

#create an empty vector to hold output
outvec <- c()

#for each file create a new file that has the sum of each daily sediment value
for (f in myfiles) {
  #read the csv file
  watershed <- read.csv(f, header=F)
  #name the column headings 1:ncol
  names(watershed) <- c(1:ncol(watershed))
    
  #for each daily kg/s mean sed value, calc total sediment load, effectively convert the table to Mt
  day.sums <- (((watershed[,2:ncol(watershed)] * 60)*60)*24)*0.000000001
  #remove years 1987 and 2011 from the Mt table as the readme.pdf says
  day.sums <- day.sums[-28,] #1987
  day.sums <- day.sums[-51,] #2011
  #remove 1987 and 2011 from the years df too 
  watershed.years <- watershed[,1]
  #remove 1987 and 2011 from that too
  watershed.years <- as.data.frame(watershed.years[-c(28,52)])
  
  #now take the mean value of each column in the Mt table 
  col.means <- apply(day.sums[,1:ncol(day.sums)], 2, mean, na.rm=T)
  col.means <- t(col.means)
  
    
  #for each week in each row sum the total Mt of sediment
  #create vector for week numbers
  weeks <- c(1:53)
  #create an empty vector to dump the week sums to
  myweeksum <- c()
  week.number = 1
  j = 1
  while (j < 370) {
    if(week.number < 52){
      week.sums <- sum(col.means[,j:(j+6)]) #may need to address no data values with na.rm=T
    }else{week.sums <- sum(col.means[,j:(j+1)])}    
    #append the incremental week sum values to the empty vector
    myweeksum <- union(myweeksum, c(week.sums))
    j=j+7
    week.number = week.number + 1
  }
  

  #get just the shedID from the csv file
  shedID <- strapply(f, "\\d+", as.numeric, simplify = TRUE)
  
  #row bind week numbers with week sum values
  weeks <- rbind(weeks, myweeksum)
  #bind the shedID and out data
  outvec <- cbind(shedID, weeks)
  #strip the first row and transpose (back to rows)
  outvec <- t(outvec[-1,])
  #prep the outfile name  
  outfile <- paste("\\\\ripple\\Data\\Global\\CarbonRivers\\bernhard_global_sediment\\sediment\\test_folder\\output\\", shedID, "_SedimentFlux_weeklysum_yearlymean.csv", sep="")
  #write output to csv
  write.table(outvec outfile, sep=",", row.names=FALSE, col.names=FALSE)
  
}

