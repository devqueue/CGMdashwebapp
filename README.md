# CGM-dashboard
A Dashboard application built using flask and plotly-dash.

## Configuring the data path:
Use the `appconfig.json` to add an absolute path to the directory of files. The app expects a directory and not a file. The directory must contain excel files only. either ending with `.xlsx` or `.xls`.
The `get_data_path()` function in `dataprocessor.py` is responsible for returning the folder path to each endpoint.
You may edit this function if required, but make sure it returns an absolute path to a folder containing excel files.

## Format for the data:
The app also expects the excel file to follow a certain format. The details of which have been mentioned below. Any deviation from this norm will cause a `runtimeError`
- The summary data must be in the first 2 columns.
- second column name must contain count (case insensitive)
- File name should be id_CGM_month_year.xlsx
- Oncomine, parental should be in order
- count must include month name

## Authentication for uploading files.
The app uses an `sqlite` database which contains a table with the following schema
```
CREATE TABLE users(id integer primary key ,username text unique, hash text);
```
By default the repository does not contain a database file, it creates the database at runtime and adds users as they are registered from the `/register` route. but you may create one named `users.db` with the above schema and add users to it. but remember anyone can add a new user from the register route. You may choose to secure it by added `@login_required` decorator to the function, or you may disable it all together by removing the function entirely.