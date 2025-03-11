import os
import glob
import random as rn
from typing import List

import pandas as pd

import numpy as np
import scipy
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

def get_next_value(val: float, lower_bound: float, upper_bound: float) -> float:
    # See https://numpy.org/doc/stable/reference/random/generated/numpy.random.triangular.html
    next_val = rn.triangular(val - (val / 25), val + (val / 25), val)
    if next_val < lower_bound or next_val > upper_bound:
        return val
    return next_val

def add_medication(patient: pd.DataFrame, med: pd.DataFrame):
    nb_row = len(patient)
    # Totally arbitrary values
    med_start = rn.randint(2, int(nb_row / 5))
    med_end = rn.randint(med_start + int(nb_row / 5), med_start + int(nb_row / 1.5))

    # See https://numpy.org/doc/stable/reference/random/generated/numpy.random.triangular.html
    value_SBP = rn.triangular(med['LCL_SBP'].item(), med['UCL_SBP'].item(), med['SBP'].item())
    value_DBP = rn.triangular(med['LCL_DBP'].item(), med['UCL_DBP'].item(), med['DBP'].item())

    keep_ori_vals_SBP = patient['sys BP'].values.tolist()
    keep_ori_vals_DBP = patient['dia BP'].values.tolist()

    for i in range(med_start, med_end):
        patient['sys BP'][i] -= value_SBP
        patient['dia BP'][i] -= value_DBP

        value_SBP = get_next_value(value_SBP, med['LCL_SBP'].item(), med['UCL_SBP'].item())
        value_DBP = get_next_value(value_DBP, med['LCL_DBP'].item(), med['UCL_DBP'].item())

    sbp_threshold = [140 for x in range(len(keep_ori_vals_SBP))]
    dbp_threshold = [90 for x in range(len(keep_ori_vals_DBP))]

    plt.plot(patient['sys BP'], label='Mod SBP')
    plt.plot(patient['dia BP'], label="Mod DBP")
    plt.plot(keep_ori_vals_SBP, label="Ori SBP")
    plt.plot(keep_ori_vals_DBP, label="Ori DBP")
    plt.plot(sbp_threshold, linestyle='dashed', label="SBP Threshold", color='black')
    plt.plot(dbp_threshold, linestyle='dashed', label="DBP Threshold", color='black')
    ax = plt.gca()
    ax.set_ylim([0, 200])
    plt.legend()
    plt.show()


def main():
    med_list = import_medication("medication.csv")
    patient = import_patient("split_data/patient_2.csv")
    breakpoint()
    add_medication(patient, med_list.iloc[[0]])

if __name__ == '__main__':
    main()