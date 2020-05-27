# dash-garmin-dashboard
This is a work in progress project that makes use of Garmin Connect and Dash to display a Garmin user's exercise activities and the trends in their exercise.

### Installing
All required packages can be installed using the requirements.txt file.

### Environment
Before running the app make sure to activate the Python environment titled 'env'.

#### (alternative) Conda env
You may also create a conda environment using the `.yml` file provided

```{bash}
conda env create --file environment.yml
conda activate garmin
```

### Running the Dash App
Assuming you have already signed up for a [Garmin Connect](https://connect.garmin.com/modern/) account - fill in your email and password in the `config.py` file

Then, the dash app can be run from the command line using the following command:

```{bash}
python index.py
```

### Built With

* [Dash](https://dash.plotly.com/) - The web framework used
* [Garmin Connect](https://pypi.org/project/garminconnect/)

### Authors
Devon Stone & James Leslie
