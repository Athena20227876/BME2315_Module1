# Name: Vincent LaGrua
# Resources: Claude Opus 5.0 - I used Claude to help debug the constructor and representer, to draft the 
# filter method, and to review my code for errors and consistency.

from patient_Vince import *
import matplotlib.pyplot as plt
import statistics


# Step 4: Creating patient objects from the CSV file (only load the file once)
Patient.instantiate_from_csv("C:\\Users\\vince\\OneDrive\\BME2315\\Module 1\\BME2315_Module1\\Metadata and Protein Data for Module 1.csv")

# Checking that all patients loaded
print(f"Number of patients = {len(Patient.all_patients)}")   # should be 84
print(Patient.all_patients[0])


# Step 5: Sorting and printing patients by MMSE score (lowest to highest)

# Using the getter to find a patient with a specific MMSE score
print(Patient.get_patient(20))

# Only patients with an MMSE score can be sorted, since None can't be compared
tested_patients = []
for patient in Patient.all_patients:
    if patient.mmse is not None:
        tested_patients.append(patient)

tested_patients.sort(key=Patient.get_mmse, reverse=False)

for patient in tested_patients:
    print(patient)

print(f"Patients without an MMSE score = {len(Patient.all_patients) - len(tested_patients)}")


# Step 6: Filtering patients with high tau pathology (Braak V or VI) and at least 16 years of education
high_braak_educated = Patient.filter_by_braak_and_education(5, 16)

for patient in high_braak_educated:
    print(patient)

print(f"Patients with Braak >= 5 and >= 16 years of education = {len(high_braak_educated)}")


# Step 7: Making a bar graph that compares the mean and standard deviation of pTAU levels in male vs. female patients with dementia
ptau_male_dementia = []
ptau_female_dementia = []

for patient in Patient.filter(Patient.all_patients, cognitive_status="Dementia", sex="Male"):
    ptau_male_dementia.append(patient.ptau)
for patient in Patient.filter(Patient.all_patients, cognitive_status="Dementia", sex="Female"):
    ptau_female_dementia.append(patient.ptau)

# Means are the bar heights
x_male_dementia_bar = statistics.mean(ptau_male_dementia)
x_female_dementia_bar = statistics.mean(ptau_female_dementia)

# Standard deviations are the error bars
ptau_male_dementia_stdev = statistics.stdev(ptau_male_dementia)
ptau_female_dementia_stdev = statistics.stdev(ptau_female_dementia)

print(f"x_male_dementia_bar = {x_male_dementia_bar}, ptau_male_dementia_stdev = {ptau_male_dementia_stdev}")
print(f"x_female_dementia_bar = {x_female_dementia_bar}, ptau_female_dementia_stdev = {ptau_female_dementia_stdev}")

# Group sizes go in the labels so readers can see how small the samples are
dementia_groups = [f"Male (n={len(ptau_male_dementia)})", f"Female (n={len(ptau_female_dementia)})"]
mean_ptau = [x_male_dementia_bar, x_female_dementia_bar]
stdev_ptau = [ptau_male_dementia_stdev, ptau_female_dementia_stdev]

plt.bar(dementia_groups, mean_ptau, yerr=stdev_ptau, capsize=10, color=["blue", "pink"])
plt.title("Average pTAU Levels in Male vs. Female Patients with Dementia")
plt.xlabel("Patient Group")
plt.ylabel("Average pTAU (pg/ug)")
plt.show()


# Step 8: Making a scatter plot that compares pTAU levels to MMSE score
ptau_levels = []
mmse_scores = []

for patient in Patient.all_patients:
    # Skip patients with no MMSE, and the one impossible score above 30 (donor H20.33.002)
    if patient.mmse is not None and patient.mmse <= 30:
        ptau_levels.append(patient.ptau)
        mmse_scores.append(patient.mmse)

x = ptau_levels   # Independent variable
y = mmse_scores   # Dependent variable

plt.scatter(x, y, color="purple")
plt.title("pTAU Levels vs. MMSE Score")
plt.xlabel("pTAU (pg/ug)")
plt.ylabel("MMSE Score")
plt.show()
