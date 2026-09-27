# Name: Vincent LaGrua
# Final Project: Patient class for the pTAU, MMSE, and APOE e4 analysis

'''
OVERVIEW
1. Define a helper function that turns CSV text into numbers (blank cells become None)
2. Define the Patient class
   a. Constructor: store each patient's attributes and add the patient to all_patients
   b. Representer: choose what is shown when a patient is printed
   c. Class method: read the CSV file and build one Patient object per row
   d. Getters: return a single attribute (used for sorting)
   e. Instance method: check whether one patient carries an APOE e4 allele
   f. Class methods: build the groups of patients used in the graphs
'''

import csv


# ===== Helper Function: Converting CSV text to numbers =====
# IF the cell is blank -> return None
# ELSE try to convert the text to a float
# IF the text is not a number (e.g., "Unavailable") -> return None
def to_float(value: str):
    """Convert a CSV string to a float; return None if blank or not a number."""
    value = value.strip()
    if value == "":
        return None              # accounts for blank cells in the CSV
    try:
        return float(value)
    except ValueError:
        return None              # text like "Unavailable" in Fresh Brain Weight


# ===== Patient Class =====
class Patient:
    # Class variable: every Patient object is added here by the constructor
    all_patients = []

    # The highest possible MMSE score; anything above this is a data entry error
    MAX_MMSE = 30

    # Converts text labels in the CSV to ordered integers
    THAL_MAP = {"Thal 0": 0, "Thal 1": 1, "Thal 2": 2,
                "Thal 3": 3, "Thal 4": 4, "Thal 5": 5}
    BRAAK_MAP = {"Braak 0": 0, "Braak I": 1, "Braak II": 2, "Braak III": 3,
                 "Braak IV": 4, "Braak V": 5, "Braak VI": 6}

    # ===== Constructor: the attributes each patient has =====
    # SET each attribute from the values passed in
    # COUNT the e4 alleles in the APOE genotype
    # ADD the new patient to all_patients
    def __init__(self, donor_id: str, sex: str, age_at_death: int,
                 cognitive_status: str, apoe_genotype: str = "n/a",
                 years_education: int | None = None,
                 mmse: float | None = None, mmse_interval: float | None = None,
                 thal: int | None = None, braak: int | None = None,
                 abeta42: float | None = None, ptau: float | None = None):
        # Identifier and demographics
        self.donor_id = donor_id
        self.sex = sex                            # "Female" or "Male"
        self.age_at_death = age_at_death
        self.years_education = years_education

        # Clinical data
        self.cognitive_status = cognitive_status  # "Dementia" or "No dementia"
        self.mmse = mmse                          # 0 to 30; None if not tested
        self.mmse_interval = mmse_interval        # months between last MMSE and death

        # Genetics: file uses underscores (e.g., "3_4")
        self.apoe_genotype = apoe_genotype
        # Count the "4"s to get the number of e4 alleles (0, 1, or 2)
        if apoe_genotype != "n/a":
            self.apoe4_count = apoe_genotype.count("4")
        else:
            self.apoe4_count = None

        # Pathology (converted to integers before being passed in)
        self.thal = thal      # 0 to 5
        self.braak = braak    # 0 to 6

        # Luminex protein data, pg/ug
        self.abeta42 = abeta42
        self.ptau = ptau

        # Add this patient to the class-wide list
        Patient.all_patients.append(self)

    # ===== Representer: what is shown when a patient is printed =====
    def __repr__(self):
        # :.2f rounds the protein values to 2 decimal places
        return (f"{self.donor_id}: ({self.sex} | age {self.age_at_death} | "
                f"{self.cognitive_status} | MMSE {self.mmse} | "
                f"APOE {self.apoe_genotype} | Braak {self.braak} | "
                f"pTau {self.ptau:.2f})")

    # ===== Creating patient objects from the CSV file =====
    # OPEN the CSV and store each row as a dictionary
    # FOR each row:
    #     convert each value to the right type
    #     build a Patient object (the constructor adds it to all_patients)
    @classmethod
    def instantiate_from_csv(cls, filename: str):
        # Open the file and store each row as a dictionary
        with open(filename, encoding="utf8") as f:
            reader = csv.DictReader(f)
            rows_of_patients = list(reader)

        # Create one patient object for each row
        for row in rows_of_patients:
            Patient(
                donor_id=row["Donor ID"],
                sex=row["Sex"],
                age_at_death=int(row["Age at Death"]),
                cognitive_status=row["Cognitive Status"],
                apoe_genotype=row["APOE Genotype"],
                years_education=(
                    int(row["Years of education"])
                    if row["Years of education"]
                    else None
                ),
                mmse=to_float(row["Last MMSE Score"]),
                mmse_interval=to_float(row["Interval from last MMSE in months"]),
                thal=Patient.THAL_MAP.get(row["Thal"]),
                braak=Patient.BRAAK_MAP.get(row["Braak"]),
                abeta42=to_float(row["ABeta42 pg/ug"]),
                ptau=to_float(row["pTAU pg/ug"])
            )

    # ===== Getters: return one attribute of a patient =====

    # Getting the MMSE score of a patient (used as a sort key)
    def get_mmse(self):
        return self.mmse

    # Getting the pTAU level of a patient (used as a sort key)
    def get_ptau(self):
        return self.ptau

    # ===== Checking one patient's APOE e4 status =====
    # IF the patient has 1 or 2 e4 alleles -> carrier (True)
    # ELSE -> non-carrier (False)
    def is_apoe4_carrier(self):
        return self.apoe4_count is not None and self.apoe4_count >= 1

    # ===== Filter for the bar graph: APOE e4 carriers or non-carriers =====
    # START with an empty list
    # FOR each patient:
    #     IF their carrier status matches the one asked for -> add them to the list
    # RETURN the list
    @classmethod
    def filter_by_apoe4(cls, carrier: bool):
        matches = []

        for patient in Patient.all_patients:
            # Skip patients with no APOE genotype on file
            if patient.apoe4_count is None:
                continue
            if patient.is_apoe4_carrier() == carrier:
                matches.append(patient)

        return matches

    # ===== Filter for the scatter plot: patients with a usable MMSE score =====
    # START with an empty list
    # FOR each patient:
    #     IF the MMSE score exists AND is between 0 and 30 -> add them to the list
    # RETURN the list
    @classmethod
    def get_valid_mmse_patients(cls):
        matches = []

        for patient in Patient.all_patients:
            # Skips the 4 untested patients and the impossible score of 33 (donor H20.33.002)
            if patient.mmse is not None and 0 <= patient.mmse <= Patient.MAX_MMSE:
                matches.append(patient)

        return matches