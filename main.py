


import json

# Load trials from file
def load_trials(filename):
    with open(filename, "r") as f:
        return json.load(f)

# Manual input for patient
def get_patient_input():
    name = input("Enter your name: ")
    age = int(input("Enter your age: "))
    gender = input("Enter your gender (male/female): ")
    location = input("Enter your city: ")
    conditions = input("Enter your medical conditions (comma separated): ").split(",")

    return {
        "id": "input_001",
        "name": name,
        "age": age,
        "gender": gender.lower(),
        "conditions": [c.strip().lower() for c in conditions],
        "location": location
    }

def is_eligible(patient, trial):
    age = patient["age"]
    gender = patient["gender"]
    conditions = patient["conditions"]

    inc = trial["inclusion"]
    exc = trial["exclusion"]

    if not (inc["min_age"] <= age <= inc["max_age"]):
        return False
    if inc["gender"] != "any" and inc["gender"] != gender:
        return False
    if not any(cond in conditions for cond in inc["conditions"]):
        return False
    if any(cond in conditions for cond in exc["conditions"]):
        return False
    return True

def compute_score(patient, trial):
    score = 0
    if patient["location"].lower() == trial["location"].lower():
        score += 50
    score += len(set(patient["conditions"]) & set(trial["inclusion"]["conditions"])) * 10
    return score

def match_trials(patient, trials):
    matches = []
    for trial in trials:
        if is_eligible(patient, trial):
            score = compute_score(patient, trial)
            matches.append((trial["title"], score))
    matches.sort(key=lambda x: x[1], reverse=True)
    return matches

if __name__ == "__main__":
    trials = load_trials("clinical_trials.json")
    patient = get_patient_input()

    results = match_trials(patient, trials)

    print("\n🔍 Matching Clinical Trials for:", patient['name'])
    if results:
        for title, score in results:
            print(f"✅ {title} (Match Score: {score})")
    else:
        print("❌ No matching trials found based on your profile.")
