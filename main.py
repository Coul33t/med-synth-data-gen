import pandas as pd
import numpy as np

import datetime as dt
import math
import statistics
import os

import matplotlib.pyplot as plt
import matplotlib.dates as mdates

class Dataset:
    def __init__(self, name='none', path='None', id_col_name='None', date_format='%Y-%m-%d %H:%M:%S', date_time_col='NOT SET'):
        self.name = name
        self.path = path
        self.id_col_name = id_col_name
        self.df = None
        self.splitted_dfs = None
        self.infos = {}
        self.date_format = date_format
        self.date_time_col = date_time_col

    def load(self):
        self.df = pd.read_excel(self.path)
        breakpoint()

    def split(self):
        self.splitted_dfs = [d for _, d in self.df.groupby([self.id_col_name])]

    def transform_str_date_into_datetime(self, x):
        date_obj = dt.datetime.strptime(x.replace(' UTC', ''), self.date_format)
        return date_obj

    def format_str_to_datetime(self):
        for df in self.splitted_dfs:
            df[self.date_time_col] = df[self.date_time_col].apply(self.transform_str_date_into_datetime)

    def order(self):
        for i, df in enumerate(self.splitted_dfs):
            self.splitted_dfs[i] = df.sort_values(by=self.date_time_col)

    def get_stats(self):
        self.infos['nb_patients'] = len(self.splitted_dfs)
        self.infos['data_per_patients'] = [len(x) for x in self.splitted_dfs]
        self.infos['mean_data_per_patients'] = statistics.mean(self.infos['data_per_patients'])
        self.infos['std_data_per_patients'] = statistics.stdev(self.infos['data_per_patients'])

    def compute_timestep_info(self):
        for df in self.splitted_dfs:
            df['time_diff'] = df[self.date_time_col].diff()

    def init(self):
        print(f'Loading dataset {self.name} (path: {self.path})...')
        self.load()
        print(f'Dataset {self.name} loaded.')
        self.split()
        self.format_str_to_datetime()
        self.order()
        self.get_stats()
        self.compute_timestep_info()


    def __repr__(self):
        return f'<Dataset name:\"{self.name}\" path:\"{self.path}\" id_col_name:\"{self.id_col_name}\">'

    def __str__(self):
        ret_str  = f'Dataset {self.name}\n'
        ret_str += f'{self.infos["nb_patients"]} patients\n'
        ret_str += f'{self.infos["mean_data_per_patients"]} average data per patients (std = {self.infos["std_data_per_patients"]})\n'
        return  ret_str


class Patient():
    def __init__(self, infos):
        for key in infos:
            #setattr(self, key.strip('_') if type(key) == str else key, infos[key])
            if key == '_id':
                setattr(self, 'user_id', infos[key])
            else:
                setattr(self, key, infos[key])

    def add_attrs(self, attrs, prefix=''):
        for key in attrs:
                setattr(self, prefix + key, attrs[key])



class MultifilesDataset():
    def __init__(self, name='None', path='None'):
        self.name = name
        self.path = path
        self.raw_dfs = []
        self.dfs = []
        self.patients = []

    def load(self):
        files = [f for f in os.listdir(self.path) if os.path.isfile(os.path.join(self.path, f))]
        for file in files:
            if file.endswith('.csv'):
                self.raw_dfs.append(pd.read_csv(self.path + file))
                self.raw_dfs[-1].name = file[:-4]

    def create_patients(self):
        tmp = [x for x in self.raw_dfs if x.name == 'users'][0]
        self.patients = [Patient(x) for x in tmp.to_dict(orient='records')]

    def associate_data(self):
        for df in self.raw_dfs:
            # User has already been processed and activity_data and brushingResponses need special processing
            if df.name == 'users' or df.name == 'activity_data' or df.name == 'brushingResponses':
                continue

            print(f'DF name = {df.name}')

            rows = [x for x in df.to_dict(orient='records')]

            for row in rows:
                patient = next((x for x in self.patients if x.user_id == row['user_id']), None)
                if patient is not None:
                    patient.add_attrs(row, df.name + '_')

        
        activity_df = next(x for x in self.raw_dfs if x.name == 'activity_data')
        rows = [x for x in activity_df.to_dict(orient='records')] 

        for row in rows:
            patient = next((x for x in self.patients if (hasattr(x, 'mi_bands_mac') and x.mi_bands_mac == row['value_info.device_id'])), None)
            if patient is not None:
                patient.add_attrs(row, 'activity_data_')

        brushing_df = next(x for x in self.raw_dfs if x.name == 'brushingResponses')
        rows = [x for x in brushing_df.to_dict(orient='records')] 

        for row in rows:
            patient = next((x for x in self.patients if x.username == row['user']), None)
            if patient is not None:
                patient.add_attrs(row, 'brushing_responses_')






def box_plot_df(*dfs):
    data = {}
    for df in dfs:
        data[df.name] = df.infos['data_per_patients']

    returned_box_data = plt.boxplot(data.values())
    fliers = [len(x.get_data()[0]) for x in returned_box_data['fliers']]
    plt.close()
    fig, ax = plt.subplots()
    ax.boxplot(data.values(), showfliers=False)
    ax.set_xticklabels(data.keys())
    ax.set_title("Data per patient")
    print(f'Outliers: {fliers}')
    plt.show()

def plot_time_diff(dfs):
    fig, ax = plt.subplots()
    for df in dfs:
        x = [x for x in range(df.shape[0] - 1)]
        ax.plot(x, df['time_diff'][1:])
    plt.show()

def all_datasets():
    oana_dataset = Dataset('Oana', 'datasets/data1/data_renew.xls', 'pacient_id', date_format='%Y-%m-%d %H:%M:%S', date_time_col='Date_Time_measured')
    oana_dataset.init()
    plot_time_diff(oana_dataset.splitted_dfs)
    
    incare_dataset = Dataset('Incare', 'datasets/INCARE/INCARE_data.xlsx', 'User', date_format='%d/%m/%Y_%H:%M:%S', date_time_col='Concat_date_time')
    incare_dataset.init()
    plot_time_diff(incare_dataset.splitted_dfs)

    perheart_dataset = Dataset('Perheart', 'datasets/PERHEART/PERHEART_data.xlsx', 'ID_Patient', date_format='', date_time_col='Date_reformated')
    perheart_dataset.init()

    print(oana_dataset)
    print(incare_dataset)
    print(perheart_dataset)

    box_plot_df(oana_dataset, incare_dataset, perheart_dataset)


def complex_dataset():
    aceso_dataset = MultifilesDataset('ACESO', 'datasets/ACESO/')
    aceso_dataset.load()
    aceso_dataset.create_patients()
    aceso_dataset.associate_data()

def main():
    all_datasets()
    #complex_dataset()

if __name__ == '__main__':
    main()


"""

def transform_str_date_into_datetime(x):
    date_format: str = '%Y-%m-%d %H:%M:%S'
    date_obj = dt.datetime.strptime(x.replace(' UTC', ''), date_format)
    return date_obj

def date_to_timestamp(x):
    return dt.datetime.timestamp(x)

def date_str_to_timestamp(x):
    x2 = transform_str_date_into_datetime(x)
    return dt.datetime.timestamp(x2)

def timestamp_to_int(x):
    return int(x)

def date_to_seconds(x):
    if pd.isnull(x):
        return 0

    days_to_seconds = x.days * 24 * 60 * 60
    seconds = x.seconds
    return days_to_seconds + seconds

def timestamp_to_times(x):
    if not math.isnan(x):
        days = int(x / 24)
        hours = int((x - (days * 24 * 60 * 60)) / (60 * 60))
        minutes = int((x - (days * 24 * 60 * 60) - (hours * 60 * 60)) / 60)
        seconds = int(x - (days * 24 * 60 * 60) - (hours * 60 * 60) - (minutes * 60))
        date = dt.datetime(year=0, month=0, day=days, hour=hours, minute=minutes, second=seconds)
        breakpoint()
        return date

    return x

def split_dataset_by_patient_id(df):
    df_list = [d for _, d in df.groupby(['pacient_id'])]
    return df_list

def sort_dfs_by_date(dfs):
    for df in dfs:
        df['Date_Time_measured'] = df['Date_Time_measured'].apply(transform_str_date_into_datetime)
        df = df.sort_values(by='Date_Time_measured')
    
    return dfs

def diff_dfs(dfs):
    return [df.diff() for df in dfs]

def dfs_to_timestamp(dfs):
    breakpoint()

def main():
    #sorted_patients_dfs = sort_dfs_by_date(patients_dfs)
    #sorted_patient_timestamp_dfs = dfs_to_timestamp(sorted_patients_dfs)
     #print(diff_df)
    #diff_df['Date_Time_measured'] = diff_df['Date_Time_measured'].apply(date_to_seconds)
    #breakpoint()
    #print(diff_df)
    #diff_df['Date_Time_measured'] = diff_df['Date_Time_measured'].astype(int) / max(diff_df['Date_Time_measured'].astype(int))
    #print(diff_df)
    #diff_df['Date_Time_measured'] = df['Date_Time_measured'].div(df['Date_Time_measured'].max())
    
    #plot_df(sorted_patient_timestamp_dfs)
"""