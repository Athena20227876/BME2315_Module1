from makayla_patient import *

Patient.instantiate_from_csv("C:/Users/makay/OneDrive - University of Virginia/BME 2315/Module 1/Metadata and Protein Data for Module 1.csv")

# import packages that will be used in the analysis of the data
import matplotlib.pyplot as plt # imports package for plotting data on a graph
from scipy import stats # imports package that statistically analyzes data
import numpy as np # imports package allowing mathematical operations with the data
import statistics # imports package that statistically analyzes data

with open("C:/Users/makay/OneDrive - University of Virginia/BME 2315/Module 1/Metadata and Protein Data for Module 1.csv", newline="") as f:
        reader = csv.reader(f)
        headers = next(reader) # Get the first row
        for h in headers:
            print(h)

Patient.all_patients.sort(key=Patient.get_Amyloid_Beta42_levels, reverse=False)

for patient in Patient.all_patients:
      print(patient)

filtered_patients = Patient.filter(
      Patient.get_all_patients(),
      sex = "Male",
      highest_education_level = "Trade School/ Tech School"
)

print("\nMale patients who have completed Trade or Tech School are:")

for patient in filtered_patients:
      print(patient)

Patient.all_patients.sort(key=Patient.get_age_at_death, reverse=False)

for patient in Patient.all_patients:
      print(patient)

Patient.all_patients.sort(key=Patient.get_Amyloid_Beta42_levels, reverse=False)

f_ABeta42 = []
m_ABeta42 = []

for patient in Patient.all_patients:
        if patient.sex == "Female":
            f_ABeta42.append(patient.Amyloid_Beta42_levels)
        elif patient.sex == "Male":
            m_ABeta42.append(patient.Amyloid_Beta42_levels)

f_mean = np.mean(f_ABeta42)
m_mean = np.mean(m_ABeta42)

f_standard_dev = np.std(f_ABeta42, ddof=1)
m_standard_dev = np.std(m_ABeta42, ddof=1)

sexes = ["Female", "Male"]
means = [f_mean, m_mean]
standard_devs = [f_standard_dev, m_standard_dev]

plt.bar(
      sexes,
      means,
      yerr=standard_devs,
      capsize=5
)

plt.xlabel("Sex")
plt.ylabel("Mean Amyloid-Beta42 (pg/ug)")
plt.title("Amyloid-Beta42 Levels by Sex")

plt.show()

patient.age_at_death
patient.Amyloid_Beta42_levels

age_at_death = []
ABeta42_values = []

for patient in Patient.all_patients:
      age_at_death.append(patient.age_at_death)
      ABeta42_values.append(patient.Amyloid_Beta42_levels)

plt.scatter(age_at_death, ABeta42_values)

plt.xlabel("Age at Death")
plt.ylabel("Amyloid-Beta42 (pg/ug)")
plt.title("Amyloid-Beta42 vs. Age at Death")

plt.show()