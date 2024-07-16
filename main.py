import json
import random
from datetime import date
import sys

#This algorithm is not optimized for any other group sizes, for now it should be 5
GROUP_SIZE = 5
SUBJECTS = 'subjects'

def read_json(file):
    try:
        with open(file, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Error: File '{file}' not found.")
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON in file '{file}'. {str(e)}")
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error while reading file: {str(e)}")
        sys.exit(1)

def mass_grouping(data):
    subject_dict = {}
    for student in data:
        if student['opt'] == 1:
            for subject in student[SUBJECTS]:
                if subject not in subject_dict:
                    subject_dict[subject] = []
                subject_dict[subject].append(student['uid'])
    return subject_dict

def group_amount(subject_dict):
    group_calc = {}
    for subject, students in subject_dict.items():
        full_groups = len(students) // GROUP_SIZE
        remainder = len(students) % GROUP_SIZE
        group_calc[subject] = {"full_groups": full_groups, "remainder": remainder}
    return group_calc

def distribute_remainder(groups, remainder, full_groups):
    if remainder == 0:
        return groups
    
    if remainder == 1:
        if full_groups == 1:
            groups[0].append(remainder[0])
        else:
            random_group = random.choice(groups)
            random_group.append(remainder[0])
    
    elif remainder == 2:
        if full_groups == 1:
            groups[0].extend(remainder)
        else:
            random_groups = random.sample(groups, 2)
            for i, group in enumerate(random_groups):
                group.append(remainder[i])
    
    elif remainder == 3:
        if full_groups == 1:
            groups.append(remainder[:2])
            groups.append(remainder[2:])
        elif full_groups == 2:
            groups[0].extend(remainder[:2])
            groups[1].append(remainder[2])
        else:
            random_groups = random.sample(groups, 3)
            for i, group in enumerate(random_groups):
                group.append(remainder[i])
    
    elif remainder == 4:
        if full_groups <= 3:
            groups.append(remainder)
        else:
            random_groups = random.sample(groups, 4)
            for i, group in enumerate(random_groups):
                group.append(remainder[i])
    
    return groups

def generate_study_groups(subject_dict, group_calc):
    study_groups = {}
    today = date.today().strftime("%d/%m/%Y")
    study_groups[today] = {}

    for subject, students in subject_dict.items():
        full_groups = group_calc[subject]["full_groups"]
        remainder = group_calc[subject]["remainder"]
        
        if full_groups == 0 and remainder < 3:
            continue 
        
        random.shuffle(students)
        groups = [students[i:i+GROUP_SIZE] for i in range(0, len(students) - remainder, GROUP_SIZE)]
        
        if remainder > 0:
            remaining_students = students[-remainder:]
            groups = distribute_remainder(groups, remaining_students, full_groups)
        
        study_groups[today][subject] = {f"group {i+1}": group for i, group in enumerate(groups)}

        total_students = len(students)
        study_groups[today][f"{subject} (Total Students: {total_students})"] = {f"group {i+1}": group for i, group in enumerate(groups)}

    return study_groups

def main():
    file_path = "testdata.json"  
    data = read_json(file_path)
    subject_dict = mass_grouping(data)
    group_calc = group_amount(subject_dict)
    study_groups = generate_study_groups(subject_dict, group_calc)
    
    print(json.dumps(study_groups, indent=1))

if __name__ == "__main__":
    main()
