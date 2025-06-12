import sys

import pandas as pd

from sdv.metadata import Metadata

from sdv.sequential import PARSynthesizer

def import_data(filename: str) -> pd.DataFrame:
    # data = load_csvs(folder_name='split_data')
    return  pd.read_csv(filename)

def import_or_create_metadata(data, filename: str):

    metadata = Metadata.detect_from_dataframe(data)

    metadata.update_column(column_name='pacient_id', sdtype='id')
    metadata.update_column(column_name='SpO2', sdtype='numerical')
    metadata.set_sequence_key('pacient_id')

    return metadata


def fit_synthetizer(data, metadata, filename, save: bool = True):
    synthetizer = PARSynthesizer(metadata)
    synthetizer.fit(data)

    synthetizer.save(filepath=f'model/{filename}_synthesizer.pkl')

    return synthetizer

def synthetize(synthetizer, filename: str):
    synthetic_data = synthetizer.sample(num_sequences=100)
    synthetic_data.to_csv(f'syn_data/{filename}_syn_data.csv', index=False)

def main(args):
    filename = 'data_data_1_cleaned'
    metadata_name = 'data_1_metadata'
    
    if len(args) > 1:
        filename = args[1]

    if len(args) > 2:
        metadata_name = args[2]

    print('Importing data')
    data = import_data(f'{filename}.csv')

    print('Creating metadata')
    metadata = import_or_create_metadata(data, f'{metadata_name}.json')

    print('Fitting synthetizer')
    synthetizer = fit_synthetizer(data, metadata, filename)

    print('Synthetizing data')
    synthetize(synthetizer, filename)

if __name__ == '__main__':
    main(sys.argv)
