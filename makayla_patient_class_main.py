from makayla_patient import * # import code from makayla_patient.py file

Patient.instantiate_from_csv("C:/Users/makay/OneDrive - University of Virginia/BME 2315/Module 1/Metadata and Protein Data for Module 1.csv") # instantiate Patient objects from the .csv file

# import packages that will be used in the analysis of the data
import matplotlib.pyplot as plt # imports package for plotting data on a graph
from scipy import stats # imports package that statistically analyzes data
import numpy as np # imports package allowing mathematical operations with the data
import statistics # imports package that statistically analyzes data

# open the .csv file and print the headers
with open("C:/Users/makay/OneDrive - University of Virginia/BME 2315/Module 1/Metadata and Protein Data for Module 1.csv", newline="") as f: # opens the .csv file
        reader = csv.reader(f)
        headers = next(reader) # Get the first row
        for h in headers: # function to print the headers
            print(h)

Patient.all_patients.sort(key=Patient.get_Amyloid_Beta42_levels, reverse=False) # sort patient data by Amyloid-Beta42 levels from lowest to highest

for patient in Patient.all_patients: # print the patient data in order of age onto terminal
      print(patient)

filtered_patients = Patient.filter( # filters the patient data by sex and education level
      Patient.get_all_patients(), # from all patients filter out only those that are male and went to Trade or Tech School
      sex = "Male",
      highest_education_level = "Trade School/ Tech School"
)

print("\nMale patients who have completed Trade or Tech School are:") # print out a message announcing what was just filtered and will be printed next

for patient in filtered_patients: # print the filtered patient data
      print(patient)

Patient.all_patients.sort(key=Patient.get_age_at_death, reverse=False) # order the patient data by age at death from youngest to oldest

for patient in Patient.all_patients: # print the patient data in order of age at death
      print(patient)

Patient.all_patients.sort(key=Patient.get_Amyloid_Beta42_levels, reverse=False)


# creating a box graph for data visualization of Amyloid-Beta42 levels by sex
f_ABeta42 = []
m_ABeta42 = []

for patient in Patient.all_patients: # function that will sort the Amyloid-Beta42 levels by sex and put them into separate lists
        if patient.sex == "Female": # clarifying that if the patient is female, their Amyloid-Beta42 levels will be added to the female list
            f_ABeta42.append(patient.Amyloid_Beta42_levels) 
        elif patient.sex == "Male": # clarifying that if the patient is male, their Amyloid-Beta42 levels will be added to the male list
            m_ABeta42.append(patient.Amyloid_Beta42_levels)

# taking the mean of both data sets
f_mean = np.mean(f_ABeta42)
m_mean = np.mean(m_ABeta42)

# finding the standard deviation of both data sets
f_standard_dev = np.std(f_ABeta42, ddof=1)
m_standard_dev = np.std(m_ABeta42, ddof=1)

# creating a bar graph for data visualization of Amyloid-Beta42 levels by sex
sexes = ["Female", "Male"]
means = [f_mean, m_mean]
standard_devs = [f_standard_dev, m_standard_dev]

# labeling the bar graph with the x-axis, y-axis, and title
plt.bar(
      sexes,
      means,
      yerr=standard_devs,
      capsize=5
)

plt.xlabel("Sex")
plt.ylabel("Mean Amyloid-Beta42 (pg/ug)")
plt.title("Amyloid-Beta42 Levels by Sex")

plt.show() # displays final graph

# creating a scatter plot for data visualization of Amyloid-Beta42 levels vs. age at death
patient.age_at_death
patient.Amyloid_Beta42_levels

# creating two lists to hold the data for the scatter plot
age_at_death = []
ABeta42_values = []

# populating the two lists with the data from the patient objects in the data set
for patient in Patient.all_patients:
      age_at_death.append(patient.age_at_death)
      ABeta42_values.append(patient.Amyloid_Beta42_levels)

plt.scatter(age_at_death, ABeta42_values) # clarifying the type of graph being used and which value is on the x or y axis

# labeling the scatter plot with the x-axis, y-axis, and title
plt.xlabel("Age at Death")
plt.ylabel("Amyloid-Beta42 (pg/ug)")
plt.title("Amyloid-Beta42 vs. Age at Death")

plt.show() # displays final scatterplot graph