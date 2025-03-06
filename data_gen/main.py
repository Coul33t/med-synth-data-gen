import pandas as pd

def separate_data():
    data = pd.read_csv('data_renew.csv')
    return [x for _, x in data.groupby(data['pacient_id'])]
   
   
def sort_by_date(dfs):
    return [df.sort_values(by='Date_Time_measured') for df in dfs]

def main():
    dfs = separate_data()
    dfs = sort_by_date(dfs)

    for df in dfs:
        df.to_csv(f'split_data/patient_{df.iloc[0]["pacient_id"]}.csv')

if __name__ == '__main__':
    main()