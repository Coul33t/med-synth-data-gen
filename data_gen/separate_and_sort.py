import pandas as pd

def separate_data(filename: str):
    data = pd.read_csv(filename)
    return [x for _, x in data.groupby(data['pacient_id'])]
   
   
def sort_by_date(dfs):
    return [df.sort_values(by='Date_Time_measured') for df in dfs]

def main():
    dfs = separate_data('syn_data.csv')
    dfs = sort_by_date(dfs)

    for df in dfs:
        df.to_csv(f'split_syn_data/patient_{df.iloc[0]["pacient_id"]}_syn.csv', index=False)

if __name__ == '__main__':
    main()