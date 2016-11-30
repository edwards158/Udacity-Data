require(knitr)
require(markdown)
library(dplyr)
library(ggplot2)

setwd('/home/riched/udacity/nanodegree/P6')
airlines <- read.csv('airline_delay_causes_best.csv')
airlines = airlines[is.na(airlines$arr_flights) == 0,]
str(airlines)

airlines <-rename(airlines, weather_ct = X.weather_ct,arr_delay = X.arr_delay,
                  carrier_delay=X.carrier_delay, month=X.month)
str(airlines)
summary(airlines)

best5 = tail(sort(tapply(airlines$arr_flights, airlines$carrier_name, sum)),n=5)
best5.carrier_name = labels(best5)
best5.carrier_name = best5.carrier_name[[1]]
best5_airlines = airlines[airlines$carrier_name %in% best5.carrier_name  ,]
best5_airlines$X = NULL
best5_airlines$carrier_name = factor(best5_airlines$carrier_name)
levels(best5_airlines$carrier_name)


summary_data = aggregate(best5_airlines[,7:ncol(best5_airlines)],
                            by = list(best5_airlines$year,best5_airlines$carrier_name),
                            FUN=sum, na.rm=TRUE)

summary_data <-rename(summary_data, year = Group.1,carrier_name = Group.2)

summary_data$avg_arr_del15 = 100 * summary_data$arr_del15/summary_data$arr_flights
summary_data$avg_carrier_ct = 100 * summary_data$carrier_ct/summary_data$arr_flights
summary_data$avg_ontime = 100 - summary_data$avg_arr_del15
summary_data$num_flights = summary_data$arr_flights

library(ggplot2)

ggplot(data = summary_data,
       aes(x = year, y = avg_arr_del15)) +
  geom_line(aes(color = carrier_name))

ggplot(data = summary_data,
       aes(x = year, y = avg_ontime)) +
  geom_line(aes(color = carrier_name))

ggplot(data = summary_data,
       aes(x = year, y = num_flights)) +
  geom_line(aes(color = carrier_name))

write.csv(summary_data,"/home/riched/udacity/nanodegree/P6/airlines/summary_airlines.csv", row.names=FALSE)


