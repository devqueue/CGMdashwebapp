import collections.abc as abc
import pandas as pd
import pathlib
import os
import json


def get_data_path():
    JSON_FILE = pathlib.Path(__file__).parent.parent.parent / 'appconfig.json'

    with open(JSON_FILE, "r") as stream:
        try:
            jsonfile = json.load(stream)
            PATH = jsonfile["DATA_PATH"]
            return PATH
        except json.decoder.JSONDecodeError as exec:
            print(exec)
            return False



def rearranage_files(location):

    filenames = os.listdir(location)

    def rearrange(seq, order, keyfunc):
        if not isinstance(order, abc.Mapping):
            order = {v: i for i, v in enumerate(order)}
        return sorted(seq, key=lambda x: order[keyfunc(x)])

    months = ['January', 'February', 'March', 'April', 'May', 'June', 'July',
              'August', 'September', 'October', 'November', 'December']

    def get_month_name(filename):
        return filename.split('_')[2]

    rearranged_list = rearrange(filenames, months, get_month_name)

    return rearranged_list


def rearranage_columns(columns):

    def rearrange(seq, order, keyfunc):
        if not isinstance(order, abc.Mapping):
            order = {v: i for i, v in enumerate(order)}
        return sorted(seq, key=lambda x: order[keyfunc(x)])

    months = ['January', 'February', 'March', 'April', 'May', 'June', 'July',
              'August', 'September', 'October', 'November', 'December']

    def get_month_name(column_name):
        return column_name.split(' ')[0]

    rearranged_list = rearrange(columns, months, get_month_name)

    return rearranged_list


def clean_data(excelfile):
    df = pd.read_excel(excelfile)
    df = df.iloc[:, 0:2]
    df.dropna(inplace=True)
    df.columns = ["1st", "2nd"]
    df = df.reset_index()
    df = df.drop("index", axis=1)

    header_rows = []
    dfs = {}
    for row in df.iterrows():
        for i in row[1].to_list():
            if "Count" in str(i) or "count" in str(i):
                header_rows.append(row[0])
    header_rows.append(None)
    
    for (i, x, y) in zip(range(len(header_rows)), header_rows, header_rows[1:]):
        dfs[i] = df[x:y]  # condition

    for i in dfs:
        new_header = dfs[i].iloc[0]  # grab the first row for the header
        dfs[i] = dfs[i][1:]  # take the data less the header row
        dfs[i].columns = new_header

    return dfs


def find_2nd(string, substring):
   return string.find(substring, string.find(substring) + 1)


def create_df(location):
    months = {}
    for i in rearranage_files(location):
        file, _ = i.split(".")
        second_ = find_2nd(file, '_')
        month = file[second_+1:]
        file_loc = os.path.join(location, i)
        months[month] = clean_data(file_loc)

    megadf = pd.DataFrame(months)

    # remove all null values
    for i in megadf:
        for j in megadf[i]:
            if type(j) == float:
                pass
            else:
                j.drop(j.loc[j.iloc[:, 1] == 0].index, inplace=True)

    return megadf


def get_index(megadf):
    duplicate = megadf.copy()
    duplicate.dropna(axis=1, inplace=True)
    index_list = []
    for i in duplicate.index:
        try:
            name = " ".join(duplicate.iloc[i, 0].columns[0].split()[:2])
            index_list.append(name)
        except AttributeError:
            pass
    return index_list


def combine_all(dff):
    list_of_dfs = []
    for row in dff.index:
        df_first = None
        counter = 0
        for df_month in dff.loc[row]:
            if type(df_month) == float:
                pass
            else:
                if counter == 0:
                    df_first = df_month
                else:
                    df_first = df_first.combine_first(df_month)
                counter += 1

        list_of_dfs.append(df_first)
    dff["All Months"] = list_of_dfs

    for ddf in dff['All Months']:
        ddf['Total'] = ddf.sum(axis=1, skipna=True)
        first_column = ddf.pop('Total')
        ddf.insert(0, 'Total', first_column)

    return dff


def combine_between(df_filtered):
    counter = 0
    for idf in df_filtered:
        if type(idf) == float:
            continue
        else:
            if counter == 0:
                df_first = idf
            else:
                df_first = df_first.combine_first(idf)
            counter += 1
    
    df_first['Total'] = df_first.sum(axis=1, skipna=True)
    first_column = df_first.pop('Total')
    df_first.insert(0, 'Total', first_column)

    return df_first


def clean_df(location):
    megadf = create_df(location)
    index_list = get_index(megadf)
    megadf.index = index_list

    for i in megadf:
        for j in megadf[i]:
            if type(j) == float:
                pass
            else:
                j.index = j.iloc[:, 0]
                j.drop(j.iloc[:, 0].name, axis=1, inplace=True)

    megadf = combine_all(megadf)

    for metric in megadf.index:
        for dfi in megadf.loc[metric]:
            if type(dfi) != float:
                dfi.columns = [colname.replace("Count", "") for colname in list(dfi.columns)]

    return megadf



