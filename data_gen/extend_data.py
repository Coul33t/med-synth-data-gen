import pandas as pd

def separate_data():
    data = pd.read_csv('data_1.csv')
    return [x for _, x in data.groupby(data['pacient_id'])]
   
   
def sort_by_date(dfs):
    return [df.sort_values(by='Date_Time_measured') for df in dfs]

def add_HT_data(dfs):
    extended_dfs = []
    
    for df in dfs:
        new_df = df
        new_df.loc[((new_df['sys BP'] >= 140) | (new_df['dia BP'] >= 90)), 'has BP'] = 1
        new_df.fillna(0)
        extended_dfs.append(new_df)

    return extended_dfs


def main():
    dfs = separate_data()
    dfs = sort_by_date(dfs)

    extended_dfs = add_HT_data(dfs)

    for df in extended_dfs:
        df.to_csv(f'extended_data/patient_{df.iloc[0]["pacient_id"]}_extended.csv', index=False)

if __name__ == '__main__':
    main()