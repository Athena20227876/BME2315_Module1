# Name: Vincent LaGrua
# Resources: Claude Opus 5.0 - I used Claude to help debug the constructor and representer, 
# to draft the filter method, and to review my code for errors and consistency.

from patient_Vince import *
import matplotlib.pyplot as plt
import statistics
from scipy import stats
from sklearn.linear_model import LinearRegression


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

# Collect pTAU values separately for the two dementia groups.
for patient in Patient.filter(Patient.all_patients, cognitive_status="Dementia", sex="Male"):
    ptau_male_dementia.append(patient.ptau)
for patient in Patient.filter(Patient.all_patients, cognitive_status="Dementia", sex="Female"):
    ptau_female_dementia.append(patient.ptau)

# The mean is the average pTAU value and determines each bar's height.
x_male_dementia_bar = statistics.mean(ptau_male_dementia)
x_female_dementia_bar = statistics.mean(ptau_female_dementia)

# Standard deviation shows how spread out the pTAU values are in each group.
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


# Step 8: Compare pTAU levels with MMSE scores using a scatterplot.
ptau_levels = []
mmse_scores = []

for patient in Patient.all_patients:
    # Keep only usable MMSE scores; the expected maximum score is 30.
    if patient.mmse is not None and patient.mmse <= 30:
        ptau_levels.append(patient.ptau)
        mmse_scores.append(patient.mmse)

x = ptau_levels   # Independent variable: pTAU
y = mmse_scores   # Dependent variable: MMSE score
# scikit-learn expects input features in a two-dimensional list.
X = [[value] for value in x]

# Fit a line that predicts MMSE score from pTAU.
model = LinearRegression()
model.fit(X, y)
# The coefficient is the slope and the intercept is where the line crosses the y-axis.
slope = model.coef_[0]
intercept = model.intercept_
# R-squared describes how much of the variation in MMSE is explained by pTAU.
regression_r_squared = model.score(X, y)
# Use the smallest and largest pTAU values as the endpoints of the plotted line.
regression_x = [min(x), max(x)]
regression_y = model.predict([[value] for value in regression_x])

plt.scatter(x, y, color="purple")
plt.plot(regression_x, regression_y, color="black", linewidth=2,
         label="Linear regression")
plt.legend()
plt.title("pTAU Levels vs. MMSE Score")
plt.xlabel("pTAU (pg/ug)")
plt.ylabel("MMSE Score")
plt.show()

# Compare the two dementia groups with Welch's t-test.
# This version does not assume that the groups have equal variance.
t_stat, p_value = stats.ttest_ind(ptau_male_dementia, ptau_female_dementia, equal_var=False)
print(f"t-statistic = {t_stat:.2f}, p-value = {p_value:.3f}")

plt.bar(dementia_groups, mean_ptau, yerr=stdev_ptau, capsize=10, color=["blue", "pink"])

# One-way ANOVA tests whether the two group means are significantly different.
f_statistic, anova_p_value = stats.f_oneway(ptau_male_dementia, ptau_female_dementia)
print(f"One-way ANOVA: F-statistic = {f_statistic:.2f}, p-value = {anova_p_value:.3f}")

# Placing the ANOVA result just above the taller error bar
top_of_bars = max(x_male_dementia_bar + ptau_male_dementia_stdev,
                  x_female_dementia_bar + ptau_female_dementia_stdev)
plt.text(0.5, top_of_bars * 1.05,
         f"ANOVA: F = {f_statistic:.2f}, p = {anova_p_value:.3f}", ha="center")
plt.ylim(0, top_of_bars * 1.15)   # extra room so the text isn't cut off

plt.title("Average pTAU Levels in Male vs. Female Patients with Dementia")
plt.xlabel("Patient Group")
plt.ylabel("Average pTAU (pg/ug)")
plt.show()

''' We are unable to reject the null hypothesis that the two groups have 
the same mean pTAU levels, since p > 0.05.'''

# Report the fitted regression model and its R-squared value.
print(f"Linear Regression: slope = {slope:.4f}, intercept = {intercept:.2f}, "
    f"R-squared = {regression_r_squared:.3f}")
