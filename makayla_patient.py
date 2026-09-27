import csv # importing the csv module to read the .csv file

class Patient: # defining the patient class
    all_patients = [] # creating a list to hold all the patient objects that will be created from the .csv file

    @classmethod # defining a class method that will filter the patient objects based on the attributes provided in the data set
    def filter(cls, list, age_at_death:int = "any", sex:str = "any", highest_education_level:str = "any", known_head_injury:str = "any",Amyloid_Beta42_levels:int= "any",Tau_levels:int = "any" ): # inputting the attributes that will be used to filter the patient objects, with default values of "any" if no value is provided
            all_patients = list # the patients will be filtered from the list of all patients
            remove_list = [] # creating a list to hold the patient objects that will be removed from the list of all patients
            attr_list = ( # creating a tuple to hold the attributes that will be used to filter the patient objects
                        age_at_death,
                        sex,
                        highest_education_level,
                        known_head_injury,
                        Amyloid_Beta42_levels,
                        Tau_levels
                        )
            attr_name = ( # creating a tuple to hold the names of the attributes that will be used to filter the patient objects
                        "age_at_death",
                        "sex",
                        "highest_education_level",
                        "known_head_injury",
                        "Amyloid_Beta42_levels",
                        "Tau_levels"
                        )
            for attr in range(len(attr_list)): # looping through the attributes in the attr_list tuple to filter the patient objects based on the values provided in the data set
                if attr_list[attr] != "any": # clarifying that if the value of the attribute is not "any", the patient objects will be filtered based on the value provided in the data set
                    for patient in all_patients: # looping through the patient objects in the all_patients list to filter the patient objects based on the values provided in the data set
                        if getattr(patient, attr_name[attr]) != attr_list[attr]: # clarifying that if the value of the attribute is not equal to the value provided in the data set, the patient object will be added to the remove_list
                            remove_list.append(patient) 
                    all_patients = [patient for patient in all_patients if patient not in remove_list] # clarifying that the patient objects in the remove_list will be removed from the all_patients list
                    remove_list.clear() 

            return all_patients
    @classmethod
    def instantiate_from_csv(cls, filename: str): # defining a class method that will read the .csv file and create patient objects based on the data provided in the .csv file

         with open(filename, encoding="utf8") as f: # opening the .csv file and reading the data provided in it
            reader = csv.DictReader(f)
            rows_of_patients = list(reader)

            for row in rows_of_patients: # creating a patient object for each row in the .csv file based on the data provided
                    Patient( # creating a patient object based on the data provided in the .csv file
                    age_at_death = float(row['Age at Death']),
                    sex = row['Sex'],
                    highest_education_level = row['Highest level of education'],
                    known_head_injury = row['Known head injury'],
                    Amyloid_Beta42_levels = float(row['ABeta42 pg/ug']),
                    Tau_levels = float(row['pTAU pg/ug'])
                )
    @classmethod
    def get_all_patients(cls): # defining a class method that will return the list of all patient objects that have been created
        return cls.all_patients
    def __init__(self, age_at_death, sex, highest_education_level, known_head_injury, Amyloid_Beta42_levels, Tau_levels): # defining the constructor method that will create a patient object based on the data provided in the .csv file
        self.age_at_death = age_at_death
        self.sex = sex
        self.highest_education_level = highest_education_level
        self.known_head_injury = known_head_injury
        self.Amyloid_Beta42_levels = Amyloid_Beta42_levels
        self.Tau_levels = Tau_levels
        Patient.all_patients.append(self) # adding the patient object to the list of all patient objects that have been created 

    def __repr__(self): # defining the representer method that will return a string representation of the patient object that has been created
        return f"Patient(age_at_death={self.age_at_death}, sex={self.sex}, highest_education_level={self.highest_education_level}, known_head_injury={self.known_head_injury}, Amyloid_Beta42_levels={self.Amyloid_Beta42_levels}, Tau_levels={self.Tau_levels})"

    def get_age_at_death(self): # defining a method that will return the age at death of the patient
        return self.age_at_death

    def get_Amyloid_Beta42_levels(self): # defining a method that will return the Amyloid-Beta42 levels of the patient
        return self.Amyloid_Beta42_levels