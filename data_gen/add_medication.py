import csv
import random as rn

from dataclasses import dataclass
from datetime import datetime

FIRST_INTERVAL = 68.3
SECOND_INTERVAL = 95.5
# In theory, this value should be 99.7
# In practice, this will not be used
THIRD_INTERVAL = 100

def strToFloat(val: str) -> float:
    if not val:
        return

    if ',' in val:
        return float(val.replace(',', '.'))
    
    return float(val)
@dataclass
class Medication:
    def __init__(self, name, SBP, UCL_SBP, LCL_SBP, DBP, UCL_DBP, LCL_DBP):
        self.name = name
        self.SBP = strToFloat(SBP)
        self.UCL_SBP = strToFloat(UCL_SBP)
        self.LCL_SBP = strToFloat(LCL_SBP)
        self.DBP = strToFloat(DBP)
        self.UCL_DBP = strToFloat(UCL_DBP)
        self.LCL_DBP = strToFloat(LCL_DBP)

        self.is_combination = False

        if '_' in name:
            self.is_combination = True

    def __str__(self):
        return f"{self.name}:\nSBP = {self.SBP} ({self.LCL_SBP} - {self.UCL_SBP})\nDBP = {self.DBP} ({self.LCL_DBP} - {self.UCL_DBP})"

@dataclass
class PatientData:
    def __init__(self, date, id, SBP, DBP, pulse, arrythmia, weight, SpO2):
        self.date = datetime.strptime(' '.join(date.split(' ')[:-1]), '%Y-%m-%d %H:%M:%S')
        self.id = int(id)
        self.SBP = strToFloat(SBP)
        self.DBP = strToFloat(DBP)
        self.pulse = int(pulse)
        self.arrythmia = bool(arrythmia)
        self.weight = strToFloat(weight)
        self.SpO2 = strToFloat(SpO2)

@dataclass
class BPInfo:
    def __init__(self):
        pass

class Patient:
    def __init__(self):
        self.data = []

    def add_data(self, row) -> None:
        self.data.append(PatientData(*row))

    def create_medication_data(self, medication: Medication):
        # ALGO:
        # 1) choose a random timeframe to apply the medication on
        # 2) from this timeframe, count at least 2 weeks
        # 3) from here, decrease the BP by random values in the medication's interval
        # 4) when it's over, increase back right now or wait 2-4 weeks? 
        pass


def import_medication(filename):
    med_list = []

    with open(filename, "r") as med_file:
        reader = csv.reader(med_file, delimiter=',')
        headers = []
        for i, row in enumerate(reader):
            formatted_row = [x for x in row if x]
            if not formatted_row:
                continue

            if i == 0:
                headers = formatted_row

            elif len(formatted_row) == 7:
                med_list.append(Medication(*formatted_row))

    return med_list

def import_patient(filename):
    patient = Patient()

    with open(filename, "r") as patient_file:
        reader = csv.reader(patient_file, delimiter=',')
        next(reader) # skip the first line
        for row in reader:
            patient.add_data(row)

    return patient
        


def main():
    med_list = import_medication("medication.csv")
    patient = import_patient("split_data/patient_2.csv")
    breakpoint()

if __name__ == '__main__':
    main()