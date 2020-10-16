# Instructions for use

Run download, clean and merge scripts from [scripts folder](https://github.com/millalin/Train-predictor/tree/master/scripts). ML-model script and application should be run from the [root folder](https://github.com/millalin/Train-predictor). 

## Scripts

Many of the scripts are quite data intensive, and all the data is not included in Github because of the size limitations. To run scripts, you should have 'data' folder in the root of the project, and some additional folders in the data folder (these are specified later).

### Data download

To use [download_data.py](https://github.com/millalin/Train-predictor/blob/master/scripts/download_data.py), you should have 'data/raw' folder where you will get the train data jsons from years 2017 - 2019.

In the scripts folder run:

```
python download_data.py

```

### Data clean

To use [clean.py](https://github.com/millalin/Train-predictor/blob/master/scripts/clean.py) you should now have 'data/raw' folder full of nice train jsons. Next step is to collect all necessary data from these seperate files into the same file. For this you should have a folder 'data/clean'. Running the clean script for data made of three year timetables takes around 0.5-1 hours.

In the scripts folder run:

```
python clean.py

```

###  Data merge

To use [merge.py](https://github.com/millalin/Train-predictor/blob/master/scripts/merge.py), you should how have folder and file 'data/clean/trains.csv'. Now it is time to merge train data with weather data. For the end result you should have a folder 'data/merged'. Running the merge script should take 5-10 minutes.

In the scripts folder run:

```
python merge.py

```

###  Machine learning model creation

To use [model.py](https://github.com/millalin/Train-predictor/blob/master/application/model.py), you should now have folder and file 'data/merged/trains_and_weather.csv'. If your application does not yet have a ml-model or you want to make a new one, you can run this script. The created file will be situated in the already existing 'application' folder.

In the root folder run:

```
python model.py

```

Model will be created and model file saved, and in the terminal you can see accuracy score printed.

###  Run the application locally

To start the application locally, and use [run.py](https://github.com/millalin/Train-predictor/blob/master/run.py), you should now have ml-model file in 'application/model'.

In the root folder run:

```
python run.py

```

To see the application open browser in the address [http://localhost:5000/home](http://localhost:5000/home).
