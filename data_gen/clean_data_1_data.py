import sys

import pandas as pd

def separate_data(filename: str, col_to_group_by: str='pacient_id'):
    data = pd.read_csv(filename)
    return [x for _, x in data.groupby(data['pacient_id'])]
   
   
def sort_by_date(dfs, col_to_sort_by: str='Date_Time_measured'):
    return [df.sort_values(by=col_to_sort_by) for df in dfs]

def main(args):
    filename = 'data_renew'
    if len(args) > 1:
       filename = args[1]

    if filename[-4:] != '.csv':
        filename += '.csv'

    breakpoint()

    col_to_group_by = 'pacient_id'
    if len(args) > 2:
        col_to_group_by = args[2]

    col_to_sort_by = None
    if len(args) > 2:
        col_to_sort_by = args[2]

    dfs = separate_data(filename, col_to_group_by)
    dfs = sort_by_date(dfs, col_to_sort_by)
    final_df = pd.concat(dfs)
    final_df.to_csv(f'cleaned_data/{filename}_cleaned.csv', index=False)

    has_HT = []
    not_HT = []

    for df in dfs:
        if len(df[((df['sys BP'] >= 140) | (df['dia BP'] >= 90))]) >= len(df) / 2:
            has_HT.append(df)
        else:
            not_HT.append(df)
    
    final_has_HT = pd.concat(has_HT)
    final_not_HT = pd.concat(not_HT)

    final_has_HT.to_csv(f'cleaned_data/{filename}_cleaned_has_HT.csv', index=False)
    final_not_HT.to_csv(f'cleaned_data/{filename}_cleaned_not_HT.csv', index=False)



if __name__ == '__main__':
    main(sys.argv)