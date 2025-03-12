import pandas as pd

from sdv.metadata import Metadata

from sdv.sequential import PARSynthesizer

def import_data(filename: str) -> pd.DataFrame:
    # data = load_csvs(folder_name='split_data')
    return  pd.read_csv(filename)

def import_or_create_metadata(data, filename: str):
    # load metadata if it exists
    try:
        metadata = Metadata()
        metadata.load_from_json(filename)
        return metadata

    except Exception as ex:
        metadata = Metadata.detect_from_dataframe(data)

        metadata.update_column(column_name='pacient_id', sdtype='id')
        metadata.update_column(column_name='SpO2', sdtype='numerical')
        metadata.set_sequence_key('pacient_id')

        metadata.save_to_json(filepath=filename)
        return metadata


def fit_synthetizer(data, metadata, save: bool = True):
    synthetizer = PARSynthesizer(metadata)
    synthetizer.fit(data)

    synthetizer.save(filepath='my_synthesizer.pkl')

    return synthetizer

def synthetize(synthetizer):
    synthetic_data = synthetizer.sample(num_sequences=100)
    synthetic_data.to_csv('syn_data.csv', index=False)

def main():
    print('Importing data')
    data = import_data('data_renew_cleaned.csv')
    print('Creating metadata')
    metadata = import_or_create_metadata(data, 'renew_metadata.json')
    print('Fitting synthetizer')
    synthetizer = fit_synthetizer(data, metadata)
    print('Synthetizing data')
    synthetize(synthetizer)

if __name__ == '__main__':
    main()
