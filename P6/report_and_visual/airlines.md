### Data Visualization Project: U.S Domestic Airline Carriers 2003 - 2016

#### Summary

To investigate and produce a data visualization of the flight
performance of US airline carriers over the years 2003 to 2016. The data
documented the carriers performance in terms of metrics such as number
of flights, arrivals per airport, delays and flights cancelled. This
information was downloaded from RITA at:
<http://www.transtats.bts.gov/OT_Delay/OT_DelayCause1.asp>

#### Design

**Exploratory Data Analysis**

I downloaded the dataset as a csv file for exploratory data analysis
(EDA) in R studio. I thought originally it would be more interesting to
focus on airports such as asking the question "which airport has the
most flight arrivals?" but after looking at the data the information was
not so interesting as the busiest airports were at obvious geographical
hubs such as Hartsfield-Jackson Atlanta and Chicago O'Hara.

I therefore started to look at the actual carriers and ask question such
as "Which carrier has the most flights?" and "Which carrier has the
least delays?". After looking at the dataset there were many carriers in
operation (27 in total). I realized that to display this information
graphically would be difficult so I decided to cut down the number of
carriers to five. The five biggest carriers were defined by the summing
the number of flights per carrier and taking the five carriers with
greatest totals:

    ## [1] "American Airlines Inc."   "Delta Air Lines Inc."    
    ## [3] "ExpressJet Airlines Inc." "SkyWest Airlines Inc."   
    ## [5] "Southwest Airlines Co."

The dataset was processed to produce another csv file
**summary\_airline.csv** . After EDA I decided to use the data
visualization to answer the question "Amongst the bigger carriers is
there a relationship between carrier size and flight delay times?".
Because of the flexibility of R compared to processing the data using
dimple, I decided to generate plots first in R to get a feel of how they
would look using **dimple.js**. The R code is included in the file
**airlines.r**.

The first plot shows the actual number of flights per year per carrier
over the time period. Clearly Southwest Airlines has the most flights
over this period:

    ggplot(data = summary_data,
           aes(x = year, y = num_flights)) +
      geom_line(aes(color = carrier_name))

![](airlines_files/figure-markdown_strict/code3-1.png)

The second plot shows the percentage of on-time flights per carrier, we
can see that Delta airlines significantly improved its number of on-time
flights. This number is defined as arriving within 15 mins of due
arrival time:

    ggplot(data = summary_data,
           aes(x = year, y = avg_ontime)) +
      geom_line(aes(color = carrier_name))

![](airlines_files/figure-markdown_strict/code4-1.png)

The final plot shows the actual percentage of late flights caused by the
actual carrier as opposed to other delay causes such as weather and
security issues. We can see that SkyWest Airlines at the beginning of
the chart was the worst carrier but improved significantly.

    ggplot(data = summary_data,
           aes(x = year, y = avg_carrier_ct)) +
      geom_line(aes(color = carrier_name))

![](airlines_files/figure-markdown_strict/code5-1.png)

**Data Visualisation**

I implemented the visualization using **dimple.js**. Time was of the
essence to me, so I only used a small amount of **d3.js** code. I
decided to employ three charts similar to the ones I completed in R
studio.

I decided to employ a line chart as I wanted to show the change over
time for each of the carriers. I added a scatter plot overlay to the
line chart, so the specific information for each year could be
displayed.

After the initial visualization I made some changes to the
visualization:

-   I overlayed a scatter plot to the series lines
-   I added a title for each of the plots

After making these changes to the visualization, I asked three people
for feedback:

-   'the figures should be placed with the number of flights per carrier
    at the top on its own line'
-   'the colors for the plots are too bright make them more subtle'
-   'the placement of the figures dos not look right'

After reviewing the feedback, I placed the Nnumber of flights per
carrier plot at the top of the page in the center. I then placed the
remaining two plots in the center directly under the first plot. I
researched colors and found some colors that i felt to be less bright
and more easy on the eye.

As I wanted to emphasise Southwest Airlines, I made the line for
Southwest Airlines darker than the rest and also made the other lines
slighly less opaque, so they could be clearly differentiated.

The final visualization is available as **index.html**. From the
visualization it is clear that Southwest Airlines has the most flights
but this does not translate into delay times. In the percentage of on
time flights Delta Airlines performs best and in the percentage of late
flights caused by the actual carrier performance amongst the carriers is
very similar. Southwest Airlines does not provide better time
performance for its flights, there must be other reasons it has many
more flights than the other carriers.

#### References

-   <http://www.color-hex.com/color-names.html>
-   <http://dimplejs.org/>
-   <http://stackoverflow.com/>
-   <https://github.com/d3/d3-3.x-api-reference/blob/master/API-Reference.md>
