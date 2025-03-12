import sys
import pathlib

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

def main(args):
    filename = 'syn_data'
    path_to_output = 'syn_data/gen_data/'

    if len(args) > 1:
        filename = args[1]

    if len(args) > 2:
        separate = True
        path_to_output = args[2]
        if path_to_output[-1] == '/':
            path_to_output = path_to_output[:-1]

        
    dfs = separate_data(f'{filename}.csv')
    dfs = sort_by_date(dfs)
    dfs = average_weigth(dfs)
    final_df = pd.concat(dfs)
    final_df.to_csv(f'{filename}_cleaned.csv', index=False)

    if separate:
        pathlib.Path(path_to_output).mkdir(parents=True, exist_ok=True) 
        for df in dfs:
            df.to_csv(f'{path_to_output}/patient_{df.iloc[0]["pacient_id"]}_syn.csv', index=False)

if __name__ == '__main__':
    main(sys.argv)