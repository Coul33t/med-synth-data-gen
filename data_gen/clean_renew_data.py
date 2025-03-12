import pandas as pd

def separate_data(filename: str):
    data = pd.read_csv(filename)
    return [x for _, x in data.groupby(data['pacient_id'])]
   
   
def sort_by_date(dfs):
    return [df.sort_values(by='Date_Time_measured') for df in dfs]

def main():
    dfs = separate_data('data_renew.csv')
    dfs = sort_by_date(dfs)
    final_df = pd.concat(dfs)
    final_df.to_csv(f'data_renew_cleaned.csv', index=False)

if __name__ == '__main__':
    main()