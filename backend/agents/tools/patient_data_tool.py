import json
import logging

def get_patient_data(name: str):
    try:
        with open("data/patients_json_data/patient_data.json") as f:
            patients = json.load(f)
        matches = [p for p in patients if p["patient_name"].lower() == name.lower()]
        
        if len(matches) == 1:
            logging.info(f"✅ Found patient: {name}")
            return matches[0]
        elif len(matches) > 1:
            return {"error": "Multiple patients with the same name"}
        else:
            return {"error": "Patient not found"}
    except Exception as e:
        logging.error(f"Error retrieving patient data: {e}")
        return {"error": str(e)}

if __name__ == "__main__":
    # Example usage
    patient_name = "Noah Bennett"
    result = get_patient_data(patient_name)
    print(result)
