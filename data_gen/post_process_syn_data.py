import pandas as pd

def separate_data(filename: str):
    data = pd.read_csv(filename)
    return [x for _, x in data.groupby(data['pacient_id'])]
   
   
def sort_by_date(dfs):
    return [df.sort_values(by='Date_Time_measured') for df in dfs]

def average_weigth(dfs):
    new_dfs = []

    for df in dfs:
        # Arbitrary value of 15
        new_weight = df['weight'].rolling(window=15, center=True, min_periods=1).mean()
        new_weight = new_weight.round(1)
        new_df = df
        new_df['weight'] = new_weight
        new_dfs.append(new_df)

    return new_dfs

def main():
    dfs = separate_data('syn_data.csv')
    dfs = sort_by_date(dfs)
    dfs = average_weigth(dfs)
    final_df = pd.concat(dfs)
    final_df.to_csv(f'data_syn_cleaned.csv', index=False)

if __name__ == '__main__':
    main()