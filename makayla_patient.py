import csv

class Patient:
    all_patients = []

    @classmethod
    def filter(cls, list, age_at_death:int = "any", sex:str = "any", highest_education_level:str = "any", known_head_injury:str = "any",Amyloid_Beta42_levels:int= "any",Tau_levels:int = "any" ):
            all_patients = list
            remove_list = []
            attr_list = (
                        age_at_death,
                        sex,
                        highest_education_level,
                        known_head_injury,
                        Amyloid_Beta42_levels,
                        Tau_levels
                        )
            attr_name = (
                        "age_at_death",
                        "sex",
                        "highest_education_level",
                        "known_head_injury",
                        "Amyloid_Beta42_levels",
                        "Tau_levels"
                        )
            for attr in range(len(attr_list)):
                if attr_list[attr] != "any":
                    for patient in all_patients:
                        if getattr(patient, attr_name[attr]) != attr_list[attr]:
                            remove_list.append(patient)
                    all_patients = [patient for patient in all_patients if patient not in remove_list]
                    remove_list.clear()

            return all_patients
    @classmethod
    def instantiate_from_csv(cls, filename: str):

         with open(filename, encoding="utf8") as f:
            reader = csv.DictReader(f)
            rows_of_patients = list(reader)

            for row in rows_of_patients:
                    Patient(
                    age_at_death = float(row['Age at Death']),
                    sex = row['Sex'],
                    highest_education_level = row['Highest level of education'],
                    known_head_injury = row['Known head injury'],
                    Amyloid_Beta42_levels = float(row['ABeta42 pg/ug']),
                    Tau_levels = float(row['pTAU pg/ug'])
                )
    @classmethod
    def get_all_patients(cls):
        return cls.all_patients
    def __init__(self, age_at_death, sex, highest_education_level, known_head_injury, Amyloid_Beta42_levels, Tau_levels):
        self.age_at_death = age_at_death
        self.sex = sex
        self.highest_education_level = highest_education_level
        self.known_head_injury = known_head_injury
        self.Amyloid_Beta42_levels = Amyloid_Beta42_levels
        self.Tau_levels = Tau_levels
        Patient.all_patients.append(self)

    def __repr__(self):
        return f"Patient(age_at_death={self.age_at_death}, sex={self.sex}, highest_education_level={self.highest_education_level}, known_head_injury={self.known_head_injury}, Amyloid_Beta42_levels={self.Amyloid_Beta42_levels}, Tau_levels={self.Tau_levels})"

    def get_age_at_death(self):
        return self.age_at_death

    def get_Amyloid_Beta42_levels(self):
        return self.Amyloid_Beta42_levels