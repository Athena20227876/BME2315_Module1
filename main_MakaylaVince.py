# Name: Vincent LaGrua
# Final Project: pTAU, cognition (MMSE), and APOE e4 in Alzheimer's disease donors
# Resources: Claude - I used Claude to help build the final project graphs and
# statistical analysis, and to review my code for errors and consistency.

'''
OVERVIEW
1. Load all patients from the CSV file and check that 84 were created
2. Bar graph: pTAU in APOE e4 carriers vs. non-carriers
   a. Split patients into carriers and non-carriers
   b. Calculate the mean and standard deviation of pTAU for each group
   c. Test whether the means differ (Welch's t-test and one-way ANOVA)
   d. Plot the bars with error bars and print the test results on the graph
3. Scatter plot: pTAU vs. MMSE score
   a. Collect pTAU and MMSE for every patient with a usable MMSE score
   b. Fit a linear regression line (slope, intercept, R-squared)
   c. Test whether the correlation is significant (Pearson r and p-value)
   d. Plot the points and regression line and print the results on the graph
'''

from patient_MakaylaVince import *
import matplotlib.pyplot as plt
import statistics
from scipy import stats
from sklearn.linear_model import LinearRegression


# ===== Section 1: Loading the patient data =====
# CREATE one Patient object per row of the CSV (only load the file once)
Patient.instantiate_from_csv("C:\\Users\\vince\\OneDrive\\BME2315\\Module 1\\BME2315_Module1\\Metadata and Protein Data for Module 1.csv")

# CHECK that all patients loaded
print(f"Number of patients = {len(Patient.all_patients)}")   # should be 84
print(Patient.all_patients[0])


# ===== Section 2: Bar graph of pTAU in APOE e4 carriers vs. non-carriers =====
# Question: Do patients with the APOE e4 risk allele have more pTAU in their brains?

# --- 2a: Splitting patients into the two groups ---
# FOR each carrier -> add their pTAU to the carrier list
# FOR each non-carrier -> add their pTAU to the non-carrier list
ptau_e4_carriers = []
ptau_non_carriers = []

for patient in Patient.filter_by_apoe4(carrier=True):
    ptau_e4_carriers.append(patient.ptau)
for patient in Patient.filter_by_apoe4(carrier=False):
    ptau_non_carriers.append(patient.ptau)

# --- 2b: Calculating the mean and standard deviation of each group ---
# The mean is the average pTAU value and determines each bar's height
x_e4_carrier_bar = statistics.mean(ptau_e4_carriers)
x_non_carrier_bar = statistics.mean(ptau_non_carriers)

# Standard deviation shows how spread out the pTAU values are in each group
ptau_e4_carrier_stdev = statistics.stdev(ptau_e4_carriers)
ptau_non_carrier_stdev = statistics.stdev(ptau_non_carriers)

print(f"x_e4_carrier_bar = {x_e4_carrier_bar}, ptau_e4_carrier_stdev = {ptau_e4_carrier_stdev}")
print(f"x_non_carrier_bar = {x_non_carrier_bar}, ptau_non_carrier_stdev = {ptau_non_carrier_stdev}")

# --- 2c: Testing whether the two group means are different ---
# Welch's t-test does not assume the groups have equal variance (the groups are 25 vs. 59 patients)
t_stat, p_value = stats.ttest_ind(ptau_e4_carriers, ptau_non_carriers, equal_var=False)
print(f"Welch's t-test: t-statistic = {t_stat:.2f}, p-value = {p_value:.3f}")

# One-way ANOVA tests whether the group means are significantly different
f_statistic, anova_p_value = stats.f_oneway(ptau_e4_carriers, ptau_non_carriers)
print(f"One-way ANOVA: F-statistic = {f_statistic:.2f}, p-value = {anova_p_value:.3f}")

# --- 2d: Plotting the bar graph ---
# Group sizes go in the labels so readers can see how large each sample is
apoe_groups = [f"APOE e4 Carriers (n={len(ptau_e4_carriers)})", f"Non-Carriers (n={len(ptau_non_carriers)})"]
mean_ptau = [x_e4_carrier_bar, x_non_carrier_bar]
stdev_ptau = [ptau_e4_carrier_stdev, ptau_non_carrier_stdev]

plt.figure()   # start a new, blank graph
plt.bar(apoe_groups, mean_ptau, yerr=stdev_ptau, capsize=10, color=["purple", "gray"])

# Placing the test results just above the taller error bar
top_of_bars = max(x_e4_carrier_bar + ptau_e4_carrier_stdev,
                  x_non_carrier_bar + ptau_non_carrier_stdev)
plt.text(0.5, top_of_bars * 1.05,
         f"Welch's t-test: t = {t_stat:.2f}, p = {p_value:.3f}\n"
         f"ANOVA: F = {f_statistic:.2f}, p = {anova_p_value:.3f}", ha="center")
plt.ylim(0, top_of_bars * 1.25)   # extra room so the text isn't cut off

plt.title("Average pTAU Levels in APOE e4 Carriers vs. Non-Carriers")
plt.xlabel("APOE Group")
plt.ylabel("Average pTAU (pg/ug)")
plt.savefig("apoe_ptau_bar_graph.png", dpi=300, bbox_inches="tight")
plt.show()

''' Since p < 0.05 for both tests, we reject the null hypothesis that APOE e4
carriers and non-carriers have the same mean pTAU level. Carriers had higher
pTAU on average, which fits APOE e4 being the strongest genetic risk factor
for Alzheimer's disease.'''


# ===== Section 3: Scatter plot of pTAU vs. MMSE score =====
# Question: Do patients with more pTAU in their brains score lower on the MMSE?

# --- 3a: Collecting paired pTAU and MMSE values ---
# FOR each patient with a usable MMSE score:
#     add their pTAU AND their MMSE in the same step so the pairs stay lined up
ptau_levels = []
mmse_scores = []

for patient in Patient.get_valid_mmse_patients():
    ptau_levels.append(patient.ptau)
    mmse_scores.append(patient.mmse)

x = ptau_levels   # Independent variable: pTAU
y = mmse_scores   # Dependent variable: MMSE score

# --- 3b: Fitting a linear regression line ---
# scikit-learn expects input features in a two-dimensional list
X = [[value] for value in x]

# Fit a line that predicts MMSE score from pTAU
model = LinearRegression()
model.fit(X, y)
# The coefficient is the slope and the intercept is where the line crosses the y-axis
slope = model.coef_[0]
intercept = model.intercept_
# R-squared describes how much of the variation in MMSE is explained by pTAU
regression_r_squared = model.score(X, y)
# Use the smallest and largest pTAU values as the endpoints of the plotted line
regression_x = [min(x), max(x)]
regression_y = model.predict([[value] for value in regression_x])

print(f"Linear Regression: slope = {slope:.4f}, intercept = {intercept:.2f}, "
      f"R-squared = {regression_r_squared:.3f}")

# --- 3c: Testing whether the correlation is significant ---
# Pearson r measures the strength and direction of the linear relationship (-1 to 1)
# The p-value tests whether r is different from 0 (scikit-learn does not give a p-value)
r_value, r_p_value = stats.pearsonr(x, y)
print(f"Pearson correlation: r = {r_value:.2f}, p-value = {r_p_value:.3f}, n = {len(x)}")

# --- 3d: Plotting the scatter plot ---
plt.figure()   # start a new, blank graph
plt.scatter(x, y, color="purple")
plt.plot(regression_x, regression_y, color="black", linewidth=2,
         label="Linear regression")
plt.legend(loc="lower right")

# Printing the results in the top right corner of the graph
plt.text(0.97, 0.97,
         f"r = {r_value:.2f}, p = {r_p_value:.3f}\n"
         f"R-squared = {regression_r_squared:.3f}\n"
         f"n = {len(x)}",
         transform=plt.gca().transAxes, ha="right", va="top")

plt.title("pTAU Levels vs. MMSE Score")
plt.xlabel("pTAU (pg/ug)")
plt.ylabel("MMSE Score")
plt.savefig("ptau_vs_mmse_scatter.png", dpi=300, bbox_inches="tight")
plt.show()

''' Since p < 0.05, we reject the null hypothesis that there is no linear
relationship between pTAU and MMSE score. Patients with more pTAU tended to
score lower on the MMSE. However, R-squared is small, so pTAU explains only
a small part of the variation in MMSE scores; other factors (co-pathologies,
cognitive reserve, and the time between the last MMSE and death) also matter.'''