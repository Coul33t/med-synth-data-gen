import sys
import random as rn
from datetime import datetime
from typing import List

import pandas as pd
import numpy as np

from scipy.interpolate import make_interp_spline, BSpline
from matplotlib import pyplot as plt

FIRST_INTERVAL = 68.3
SECOND_INTERVAL = 95.5
# In theory, this value should be 99.7
# In practice, this will not be used
THIRD_INTERVAL = 100


def import_medication(filename: str) -> pd.DataFrame:
    med = pd.read_csv(filename)
    med.dropna(how='all', axis=1, inplace=True)
    med.dropna(how='all', axis=0, inplace=True)

    med.replace(',', '.', regex=True, inplace=True)

    name_col = 'medication'
    other_cols = med.columns.difference([name_col])
    med[other_cols] = med[other_cols].astype(float)

    return med

def import_patient(filename: str) -> List:
    return pd.read_csv(filename)

def get_next_value(val: float, lower_bound: float, upper_bound: float, rounded: int = -1) -> float:
    # See https://numpy.org/doc/stable/reference/random/generated/numpy.random.triangular.html
    next_val = rn.triangular(val - (val / 25), val + (val / 25), val)
    
    if rounded > 0:
        next_val = round(next_val, rounded)

    if next_val < lower_bound or next_val > upper_bound:
        return val

    return next_val

def get_smooth_plot(data):
    x_vals = np.linspace(0, len(data) - 1, len(data))
    new_x = np.linspace(0, len(data) - 1, (len(data) - 1) * 10)
    spl = make_interp_spline(x_vals, data, k=3)
    return new_x, spl(new_x)


def add_medication(patient: pd.DataFrame, med_list: pd.DataFrame, med_name: str):
    # TODO: kick in time (2 to 4 weeks)
    # TODO: add medication column
    nb_row = len(patient)

    # Totally arbitrary values
    med_start = rn.randint(2, int(nb_row / 5))
    med_end = rn.randint(med_start + int(nb_row / 5), med_start + int(nb_row / 1.5))

    taking_med_col = pd.Series([1 if (i > med_start and i < med_end) else 0 for i in range(len(patient))])
    patient[med_name] = taking_med_col

    med = med_list.loc[med_list['medication'] == med_name]

    # Take a random value in the interval [LCL;UCL], skewed towards the center
    # TODO: proper skewed Gaussian distribution
    # See https://numpy.org/doc/stable/reference/random/generated/numpy.random.triangular.html
    value_SBP = round(rn.triangular(med['LCL_SBP'].item(), med['UCL_SBP'].item(), med['SBP'].item()), 1)
    value_DBP = round(rn.triangular(med['LCL_DBP'].item(), med['UCL_DBP'].item(), med['DBP'].item()), 1)

    keep_ori_vals_SBP = patient['sys BP'].values.tolist()
    keep_ori_vals_DBP = patient['dia BP'].values.tolist()

    # [:-1] because there's a whitespace at the end of the date str
    current_date = datetime.fromisoformat(patient.loc[med_start]['Date_Time_measured'][:-1])
    next_date = datetime.fromisoformat(patient.loc[med_start + 1]['Date_Time_measured'][:-1])
    delta = next_date - current_date

    kick_in_date = rn.randint(14, 28)
    kick_in_idx = med_start

    print(f'Initial i: {med_start}')

    while (delta.days < kick_in_date):
        kick_in_idx += 1
        current_date = next_date
        next_date = datetime.fromisoformat(patient.loc[kick_in_idx + 1]['Date_Time_measured'][:-1])
        delta += next_date - current_date

    print(f'Final i: {kick_in_idx}')



    for i in range(kick_in_idx, med_end):
        patient['sys BP'][i] -= value_SBP
        patient['dia BP'][i] -= value_DBP

        value_SBP = get_next_value(value_SBP, med['LCL_SBP'].item(), med['UCL_SBP'].item(), 1)
        value_DBP = get_next_value(value_DBP, med['LCL_DBP'].item(), med['UCL_DBP'].item(), 1)

    sbp_threshold = [140 for x in range(len(keep_ori_vals_SBP))]
    dbp_threshold = [90 for x in range(len(keep_ori_vals_DBP))]

    #plt.plot(patient['sys BP'], label='Mod SBP')
    #plt.plot(patient['dia BP'], label="Mod DBP")
    #plt.plot(keep_ori_vals_SBP, label="Ori SBP")
    #plt.plot(keep_ori_vals_DBP, label="Ori DBP")
    plt.plot(*get_smooth_plot(patient['sys BP']), label='Mod SBP')
    plt.plot(*get_smooth_plot(patient['dia BP']), label='Mod DBP')
    plt.plot(*get_smooth_plot(keep_ori_vals_SBP), label='Ori SBP')
    plt.plot(*get_smooth_plot(keep_ori_vals_DBP), label='Ori SBP')
    
    plt.plot(sbp_threshold, linestyle='dashed', label="HT (SBP) thres", color='black')
    plt.plot(dbp_threshold, linestyle='dashed', label="HT (DBP) Thres", color='black')

    plt.axvline(x=med_start, color='blue', linestyle='dashed', label='Med start')
    plt.axvline(x=med_end, color='red', linestyle='dashed', label='Med end')

    ax = plt.gca()
    ax.set_ylim([0, 200])

    plt.legend()
    plt.show()

    return patient


def main(args):
    med_list_path = 'medication'
    patient_path = 'syn_data/has_HT/patient_555319_syn'
    medication_name = 'DIU'
    output_name = patient_path.split('/')[-1]

    if len(args) > 2:
        med_list_path = args[1]
        patient_path = args[2]

    if len(args) > 3:
        medication_name = args[3]

        
    med_list = import_medication(f'{med_list_path}.csv')
    patient = import_patient(f'{patient_path}.csv')

    patient_with_med = add_medication(patient, med_list, medication_name)
    patient_with_med.to_csv(f'syn_data/HT_with_med/{output_name}_with_med.csv', index=False)

if __name__ == '__main__':
    main(sys.argv)