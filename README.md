# CGM-dashboard
A Dashboard application built using flask and plotly-dash.

## Configuring the data path:
Use the `.env` to add an absolute path to the directory of files or you may export the path an environment variable `DATA_PATH` The app expects a directory and not a file. The directory must contain excel files only. either ending with `.xlsx` or `.xls`.
The `get_data_path()` function in `dataprocessor.py` is responsible for returning the folder path to each endpoint.
It returns the value of environment variable `DATA_PATH`.

## Format for the data:
The app also expects the excel file to follow a certain format. The details of which have been mentioned below. Any deviation from this standard will cause a `runtimeError`
- The summary data must be in the first 2 columns.
- second column name must contain count (case insensitive)
- File name should be id_CGM_month_year.xlsx
- Oncomine, parental should be in order
- count must include month name

## Authentication for uploading files.
The app can connect to any local or remote database given that you specify the URI as an environment variable.
The `DATABASE_URI` must be specified using the standard convention 
```
[DB_TYPE]+[DB_CONNECTOR]://[USERNAME]:[PASSWORD]@[HOST]:[PORT]/[DB_NAME]
```
