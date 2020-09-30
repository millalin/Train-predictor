# Train-predictor
In a busy world like ours, it is important for people to be able to plan their timetables accurately. In Finland the trains are often late, making planning hard. Having a model that predicts if a train is late would help in this. The predictions could be checked for a certain date, time and a station. The results would also help HSL and VR to recognize if there are some patterns that cause trains to be late.


Data is collected from [Digitraffic API](https://www.digitraffic.fi/rautatieliikenne/) and from [Ilmatieteenlaitos](https://www.ilmatieteenlaitos.fi/avoin-data). Data used in project is between 2017-2019, containing over 50 million rows of train travels. Weather data is collected from 8 different weather stations. Some weather stations are missing wind speed so it is collected from nearby stations and merged to data. After cleaning and merging trains data to weather data used travel amounts and rows are about 10,5 million. 

Weather predictions are also queried from [Ilmatieteenlaitos](https://www.ilmatieteenlaitos.fi/avoin-data), these can be used when making predictions about train lateness.
