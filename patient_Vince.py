import csv


# Function to convert CSV string values to floats, handling missing data and unexpected text
def to_float(value: str):
    """Convert a CSV string to a float; return None if blank or not a number."""
    value = value.strip()
    if value == "":
        return None              # accounts for blank cells in the CSV
    try:
        return float(value)
    except ValueError:
        return None              # text like "Unavailable" in Fresh Brain Weight


# Step 1: Defining the Patient class to represent each patient in the dataset
class Patient:
    # Class variable: every Patient object is added here by the constructor
    all_patients = []

    # Converts text labels in the CSV to ordered integers 
    THAL_MAP = {"Thal 0": 0, "Thal 1": 1, "Thal 2": 2,
                "Thal 3": 3, "Thal 4": 4, "Thal 5": 5}
    BRAAK_MAP = {"Braak 0": 0, "Braak I": 1, "Braak II": 2, "Braak III": 3,
                 "Braak IV": 4, "Braak V": 5, "Braak VI": 6}

    # Step 2: Making a constructor that lists the attributes each patient has
    def __init__(self, donor_id: str, sex: str, age_at_death: int,
                 cognitive_status: str, apoe_genotype: str = "n/a",
                 years_education: int | None = None,
                 mmse: float | None = None, mmse_interval: float | None = None,
                 thal: int | None = None, braak: int | None = None,
                 abeta42: float | None = None, ptau: float | None = None):
        # Identifier and demographics
        self.donor_id = donor_id
        self.sex = sex                            
        self.age_at_death = age_at_death         
        self.years_education = years_education

        # Clinical Data 
        self.cognitive_status = cognitive_status  # "Dementia" or "No dementia"
        self.mmse = mmse                          # 0 to 30; None if not tested
        self.mmse_interval = mmse_interval        # months between last MMSE and death

        # Genetics: file uses underscores
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

    # Step 3: Making a representer to display key attributes when a patient is printed
    def __repr__(self):
        # :.2f rounds the protein values to 2 decimal places
        return (f"{self.donor_id}: ({self.sex} | age {self.age_at_death} | "
                f"{self.years_education} yrs edu | {self.cognitive_status} | "
                f"MMSE {self.mmse} | APOE {self.apoe_genotype} | "
                f"Thal {self.thal} | Braak {self.braak} | "
                f"AB42 {self.abeta42:.2f} | pTau {self.ptau:.2f})")

    # Step 4: Creating patient objects from the CSV data
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

    # Step 5: Getters used for sorting and finding patients

    # Getting the MMSE score of a patient (used as the sort key)
    def get_mmse(self):
        return self.mmse

    # Getting the first patient with a specific MMSE score
    @classmethod
    def get_patient(cls, mmse):
        for patient in Patient.all_patients:
            if mmse == patient.mmse:
                return patient

    # Step 6: Filtering patients based on two attributes (Braak stage and years of education)
    @classmethod
    def filter_by_braak_and_education(cls, min_braak: int, min_education: int):
        # Empty list to collect the patients who match
        matches = []

        for patient in Patient.all_patients:
            # Keep the patient only if BOTH conditions are true:
            # tau pathology at or above min_braak, AND education at or above min_education
            if (patient.braak is not None
                    and patient.years_education is not None
                    and patient.braak >= min_braak
                    and patient.years_education >= min_education):
                matches.append(patient)

        return matches

    # Step 7: General filter that keeps patients matching every attribute given (used in step 7)
    @classmethod
    def filter(cls, patients, **criteria):
        matches = []

        for patient in patients:
            keep = True
            # Check each attribute; if any one doesn't match, drop the patient
            for name, value in criteria.items():
                if getattr(patient, name, None) != value:
                    keep = False
            if keep:
                matches.append(patient)

        return matches