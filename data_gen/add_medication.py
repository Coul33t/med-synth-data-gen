import csv

from dataclasses import dataclass

FIRST_INTERVAL = 68.3
SECOND_INTERVAL = 95.5
# In theory, this value should be 99.7
# In practice, this will not be used
THIRD_INTERVAL = 100
@dataclass
class Medication:
    def __init__(self, name, SBP, UCL_SBP, LCL_SBP, DBP, UCL_DBP, LCL_DBP):
        self.name = name
        self.SBP = SBP
        self.UCL_SBP = UCL_SBP
        self.LCL_SBP = LCL_SBP
        self.DBP = DBP
        self.UCL_DBP = UCL_DBP
        self.LCL_DBP = LCL_DBP

        self.is_combination = False

        if '_' in name:
            self.is_combination = True


@dataclass
class Patient:
    def __init__(self):
        pass


def import_medication():
    med_list = []

    with open("medication.csv", "r") as med_file:
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

def main():
    med_list = import_medication()
    breakpoint()

if __name__ == '__main__':
    main()