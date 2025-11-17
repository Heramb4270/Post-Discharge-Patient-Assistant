import json
import random
from datetime import datetime, timedelta
from typing import List, Dict, Any
import uuid
from faker import Faker
import numpy as np

fake = Faker()

class MedicalDataGenerator:
    def __init__(self):
        self.diagnoses = [
            "Chronic Kidney Disease Stage 3",
            "Congestive Heart Failure (CHF), NYHA Class II",
            "Community-acquired Pneumonia", 
            "Type 2 Diabetes Mellitus with hyperglycemia",
            "Type 1 Diabetes - DKA resolved",
            "Acute Exacerbation of COPD",
            "Acute Kidney Injury on CKD",
            "Ischemic Stroke (Left MCA territory) - stable",
            "Hip Fracture - post operative",
            "Acute Myocardial Infarction (STEMI) - post PCI",
            "Severe Urinary Tract Infection (UTI)",
            "Deep Vein Thrombosis (left leg)",
            "Rheumatoid Arthritis flare",
            "Acute Cholecystitis - treated conservatively",
            "Major Depressive Disorder - stabilized on medication",
            "Hypertensive urgency",
            "Gastroenteritis - dehydration",
            "Anemia due to iron deficiency",
            "Acute Pancreatitis - resolved",
            "Transient Ischemic Attack (TIA)",
            "Cellulitis of right lower leg",
            "Acute Appendicitis - post appendectomy",
            "Chronic Liver Disease - compensated",
            "Migraine with status resolved",
            "Chronic Obstructive Pulmonary Disease - exacerbation",
            "Peptic Ulcer Disease - stable",
            "Acute Otitis Media - resolved"
        ]
        
        self.medications = {
            "Chronic Kidney Disease Stage 3": ["Lisinopril 10mg daily", "Furosemide 20mg twice daily"],
            "Congestive Heart Failure (CHF), NYHA Class II": ["Carvedilol 6.25mg twice daily", "Furosemide 40mg daily"],
            "Community-acquired Pneumonia": ["Amoxicillin-Clavulanate 875/125mg twice daily", "Albuterol inhaler PRN"],
            "Type 2 Diabetes Mellitus with hyperglycemia": ["Metformin 500mg twice daily", "Insulin glargine 10 units nightly"],
            "Type 1 Diabetes - DKA resolved": ["Insulin as per diabetes plan (basal-bolus)", "Glucagon emergency kit"],
            "Acute Exacerbation of COPD": ["Prednisone 40mg daily x5 days", "Tiotropium inhaler once daily", "Salbutamol inhaler PRN"],
            "Acute Kidney Injury on CKD": ["Amlodipine 5mg daily", "Oral sodium bicarbonate 500mg twice daily"],
            "Ischemic Stroke (Left MCA territory) - stable": ["Aspirin 81mg daily", "Atorvastatin 40mg nightly"],
            "Hip Fracture - post operative": ["Oxycodone 5mg PRN for pain", "Enoxaparin 40mg daily (anticoagulation)"],
            "Acute Myocardial Infarction (STEMI) - post PCI": ["Aspirin 81mg daily", "Clopidogrel 75mg daily", "Atorvastatin 80mg nightly", "Metoprolol 50mg twice daily"],
            "Severe Urinary Tract Infection (UTI)": ["Ciprofloxacin 500mg twice daily x7 days", "Phenazopyridine PRN for dysuria"],
            "Deep Vein Thrombosis (left leg)": ["Rivaroxaban 20mg daily"],
            "Rheumatoid Arthritis flare": ["Methotrexate 15mg weekly", "Prednisone 10mg daily (short taper)"],
            "Acute Cholecystitis - treated conservatively": ["Ibuprofen 400mg PRN", "Ondansetron 4mg PRN"],
            "Major Depressive Disorder - stabilized on medication": ["Sertraline 50mg daily"],
            "Hypertensive urgency": ["Lisinopril 20mg daily", "Hydrochlorothiazide 12.5mg daily"],
            "Gastroenteritis - dehydration": ["Oral rehydration solution", "Ondansetron 4mg PRN"],
            "Anemia due to iron deficiency": ["Oral ferrous sulfate 325mg once daily", "Vitamin C 500mg daily to aid absorption"],
            "Acute Pancreatitis - resolved": ["Pancrelipase PRN for steatorrhea", "Acetaminophen 500mg PRN"],
            "Transient Ischemic Attack (TIA)": ["Aspirin 81mg daily", "Atorvastatin 40mg nightly"],
            "Cellulitis of right lower leg": ["Cephalexin 500mg four times daily x10 days", "Ibuprofen PRN"],
            "Acute Appendicitis - post appendectomy": ["Acetaminophen 500mg PRN", "Cephalexin 500mg twice daily x5 days"],
            "Chronic Liver Disease - compensated": ["Propranolol 40mg twice daily", "Spironolactone 50mg daily"],
            "Migraine with status resolved": ["Sumatriptan 50mg PRN", "Propranolol 20mg nightly"],
            "Chronic Obstructive Pulmonary Disease - exacerbation": ["Prednisone 20mg daily x5 days", "Formoterol inhaler twice daily", "Salbutamol inhaler PRN"],
            "Peptic Ulcer Disease - stable": ["Omeprazole 20mg daily", "Sucralfate 1g four times daily PRN"],
            "Acute Otitis Media - resolved": ["Amoxicillin 500mg three times daily x7 days", "Acetaminophen PRN"]
        }
        
        self.dietary_restrictions = {
            "Chronic Kidney Disease Stage 3": "Low sodium (2g/day), fluid restriction (1.5L/day)",
            "Congestive Heart Failure (CHF), NYHA Class II": "Low sodium (1.5g/day), fluid restriction (1.5L/day)",
            "Community-acquired Pneumonia": "No specific dietary restrictions",
            "Type 2 Diabetes Mellitus with hyperglycemia": "Carbohydrate-controlled diet, avoid sugary drinks",
            "Type 1 Diabetes - DKA resolved": "Consistent carbohydrate intake; avoid missed meals",
            "Acute Exacerbation of COPD": "No smoking; avoid respiratory irritants",
            "Acute Kidney Injury on CKD": "Low potassium, low sodium, fluid restriction 1.2L/day",
            "Ischemic Stroke (Left MCA territory) - stable": "Heart-healthy diet, low sodium",
            "Hip Fracture - post operative": "High-protein diet encouraged for healing",
            "Acute Myocardial Infarction (STEMI) - post PCI": "Low saturated fat, low sodium",
            "Severe Urinary Tract Infection (UTI)": "Increase fluid intake unless fluid-restricted",
            "Deep Vein Thrombosis (left leg)": "Avoid dehydration; maintain balanced diet",
            "Rheumatoid Arthritis flare": "No alcohol while on methotrexate; maintain folate intake",
            "Acute Cholecystitis - treated conservatively": "Low-fat diet until surgical follow-up",
            "Major Depressive Disorder - stabilized on medication": "None specific",
            "Hypertensive urgency": "Low sodium (2g/day)",
            "Gastroenteritis - dehydration": "BRAT diet initially; avoid dairy until recovery",
            "Anemia due to iron deficiency": "Increase dietary iron (lean meats, legumes); avoid tea/coffee with meals",
            "Acute Pancreatitis - resolved": "Low-fat diet; avoid alcohol",
            "Transient Ischemic Attack (TIA)": "Heart-healthy diet, low sodium",
            "Cellulitis of right lower leg": "None specific",
            "Acute Appendicitis - post appendectomy": "Light diet initially; advance as tolerated",
            "Chronic Liver Disease - compensated": "Low sodium (2g/day); avoid alcohol",
            "Migraine with status resolved": "Avoid known dietary triggers (aged cheese, red wine)",
            "Chronic Obstructive Pulmonary Disease - exacerbation": "No smoking; maintain adequate hydration",
            "Peptic Ulcer Disease - stable": "Avoid NSAIDs and alcohol; small frequent meals",
            "Acute Otitis Media - resolved": "None specific"
        }
        
        self.follow_ups = {
            "Chronic Kidney Disease Stage 3": "Nephrology clinic in 2 weeks",
            "Congestive Heart Failure (CHF), NYHA Class II": "Cardiology clinic in 1 week",
            "Community-acquired Pneumonia": "Primary care in 7-10 days",
            "Type 2 Diabetes Mellitus with hyperglycemia": "Diabetes clinic in 2 weeks",
            "Type 1 Diabetes - DKA resolved": "Diabetes educator and endocrinology in 3 days",
            "Acute Exacerbation of COPD": "Pulmonology clinic in 2 weeks",
            "Acute Kidney Injury on CKD": "Nephrology clinic in 1 week",
            "Ischemic Stroke (Left MCA territory) - stable": "Stroke clinic / Neurology in 2 weeks",
            "Hip Fracture - post operative": "Orthopedics clinic in 2 weeks",
            "Acute Myocardial Infarction (STEMI) - post PCI": "Cardiology outpatient in 1 week",
            "Severe Urinary Tract Infection (UTI)": "Primary care in 5-7 days",
            "Deep Vein Thrombosis (left leg)": "Hematology / Vascular clinic in 1 week",
            "Rheumatoid Arthritis flare": "Rheumatology clinic in 2 weeks",
            "Acute Cholecystitis - treated conservatively": "Surgery clinic in 2 weeks",
            "Major Depressive Disorder - stabilized on medication": "Psychiatry clinic in 1 week",
            "Hypertensive urgency": "Primary care in 3 days",
            "Gastroenteritis - dehydration": "Primary care in 1 week if not improved",
            "Anemia due to iron deficiency": "Hematology clinic in 4 weeks",
            "Acute Pancreatitis - resolved": "Gastroenterology clinic in 2 weeks",
            "Transient Ischemic Attack (TIA)": "Neurology clinic in 1 week",
            "Cellulitis of right lower leg": "Wound clinic / Primary care in 3 days",
            "Acute Appendicitis - post appendectomy": "Surgical follow-up in 7-10 days",
            "Chronic Liver Disease - compensated": "Hepatology clinic in 2 weeks",
            "Migraine with status resolved": "Neurology clinic in 4 weeks",
            "Chronic Obstructive Pulmonary Disease - exacerbation": "Pulmonology clinic in 2 weeks",
            "Peptic Ulcer Disease - stable": "Gastroenterology in 4 weeks",
            "Acute Otitis Media - resolved": "Primary care in 1 week if persistent symptoms"
        }
        
        self.warning_signs = {
            "Chronic Kidney Disease Stage 3": "Swelling, shortness of breath, decreased urine output",
            "Congestive Heart Failure (CHF), NYHA Class II": "Rapid weight gain, worsening shortness of breath, chest pain",
            "Community-acquired Pneumonia": "High fever, worsening cough, difficulty breathing",
            "Type 2 Diabetes Mellitus with hyperglycemia": "Symptoms of hypoglycemia, persistent hyperglycemia, polyuria",
            "Type 1 Diabetes - DKA resolved": "Ketones in urine, nausea/vomiting, high blood sugar despite insulin",
            "Acute Exacerbation of COPD": "Increased breathlessness, blue lips, confusion",
            "Acute Kidney Injury on CKD": "Reduced urine output, swelling, nausea/vomiting",
            "Ischemic Stroke (Left MCA territory) - stable": "New weakness, severe headache, slurred speech",
            "Hip Fracture - post operative": "Increased wound drainage, fever, calf swelling",
            "Acute Myocardial Infarction (STEMI) - post PCI": "Chest pain, fainting, new shortness of breath",
            "Severe Urinary Tract Infection (UTI)": "Fever, flank pain, persistent vomiting",
            "Deep Vein Thrombosis (left leg)": "Increased leg swelling, sudden shortness of breath (PE signs)",
            "Rheumatoid Arthritis flare": "New infections, persistent fever, unusual bleeding",
            "Acute Cholecystitis - treated conservatively": "Persistent abdominal pain, fever, jaundice",
            "Major Depressive Disorder - stabilized on medication": "Suicidal thoughts, worsening depression, severe anxiety",
            "Hypertensive urgency": "Severe headache, vision changes, chest pain",
            "Gastroenteritis - dehydration": "Inability to tolerate fluids, high fever, bloody stools",
            "Anemia due to iron deficiency": "Persistent fatigue, palpitations, shortness of breath",
            "Acute Pancreatitis - resolved": "Severe abdominal pain, fever, persistent vomiting",
            "Transient Ischemic Attack (TIA)": "Recurrent weakness, speech difficulty, loss of vision",
            "Cellulitis of right lower leg": "Spreading redness, fever, increasing pain",
            "Acute Appendicitis - post appendectomy": "Fever, increasing abdominal pain, wound redness/drainage",
            "Chronic Liver Disease - compensated": "Jaundice, abdominal swelling, confusion (encephalopathy)",
            "Migraine with status resolved": "Increased frequency or severity of headaches, visual changes",
            "Chronic Obstructive Pulmonary Disease - exacerbation": "Increased breathlessness, blue lips, fever",
            "Peptic Ulcer Disease - stable": "Black stools, severe abdominal pain, vomiting blood",
            "Acute Otitis Media - resolved": "High fever, severe ear pain, discharge from ear"
        }
        
        self.discharge_instructions = {
            "Chronic Kidney Disease Stage 3": "Monitor blood pressure daily",
            "Congestive Heart Failure (CHF), NYHA Class II": "Daily weight monitoring and record",
            "Community-acquired Pneumonia": "Complete full course of antibiotics",
            "Type 2 Diabetes Mellitus with hyperglycemia": "Check blood sugars before meals and at bedtime",
            "Type 1 Diabetes - DKA resolved": "Carry glucometer and ketone strips; sick-day action plan provided",
            "Acute Exacerbation of COPD": "Use inhalers as demonstrated and carry rescue inhaler",
            "Acute Kidney Injury on CKD": "Weigh daily and report >2kg gain in 48 hours",
            "Ischemic Stroke (Left MCA territory) - stable": "Begin prescribed physiotherapy program and speech exercises",
            "Hip Fracture - post operative": "Keep wound clean and dry; gradual weight-bearing as instructed",
            "Acute Myocardial Infarction (STEMI) - post PCI": "Cardiac rehab referral and activity guidelines provided",
            "Severe Urinary Tract Infection (UTI)": "Complete antibiotic course and obtain urine culture if symptoms persist",
            "Deep Vein Thrombosis (left leg)": "Keep leg elevated and avoid long immobilization",
            "Rheumatoid Arthritis flare": "Monitor for side effects of medications and have labs in 1 week",
            "Acute Cholecystitis - treated conservatively": "Return to ER for severe abdominal pain or vomiting",
            "Major Depressive Disorder - stabilized on medication": "Maintain follow-up and continue therapy; seek crisis help if needed",
            "Hypertensive urgency": "Home BP log twice daily and bring to appointment",
            "Gastroenteritis - dehydration": "Maintain adequate oral fluids and electrolytes",
            "Anemia due to iron deficiency": "Take iron on empty stomach if tolerated; expect several weeks to improvement",
            "Acute Pancreatitis - resolved": "Gradual return to oral intake as tolerated",
            "Transient Ischemic Attack (TIA)": "Avoid driving until cleared by neurology",
            "Cellulitis of right lower leg": "Keep area elevated and clean; complete antibiotics",
            "Acute Appendicitis - post appendectomy": "Avoid heavy lifting for 2 weeks; wound care instructions given",
            "Chronic Liver Disease - compensated": "Daily weights and monitor for swelling; vaccines reviewed",
            "Migraine with status resolved": "Maintain headache diary; avoid overuse of acute medications",
            "Chronic Obstructive Pulmonary Disease - exacerbation": "Use inhalers as instructed; seek urgent care for worsening symptoms",
            "Peptic Ulcer Disease - stable": "Take acid suppression as prescribed and avoid irritants",
            "Acute Otitis Media - resolved": "Complete antibiotics and return if symptoms worsen"
        }

    def generate_patient_record(self) -> Dict[str, Any]:
        """Generate a single patient discharge record"""
        diagnosis = random.choice(self.diagnoses)
        
        # Generate discharge date within last 6 months
        start_date = datetime.now() - timedelta(days=180)
        end_date = datetime.now() - timedelta(days=1)
        discharge_date = fake.date_between(start_date=start_date, end_date=end_date)
        
        return {
            "patient_name": fake.name(),
            "patient_id": str(uuid.uuid4())[:8].upper(),
            "discharge_date": discharge_date.strftime("%Y-%m-%d"),
            "primary_diagnosis": diagnosis,
            "medications": self.medications.get(diagnosis, ["No medications prescribed"]),
            "dietary_restrictions": self.dietary_restrictions.get(diagnosis, "None specific"),
            "follow_up": self.follow_ups.get(diagnosis, "Primary care in 1-2 weeks"),
            "warning_signs": self.warning_signs.get(diagnosis, "Contact provider for concerns"),
            "discharge_instructions": self.discharge_instructions.get(diagnosis, "Follow up as directed"),
            "age": random.randint(25, 85),
            "gender": random.choice(["Male", "Female"]),
            "phone": fake.phone_number(),
            "email": fake.email(),
            "emergency_contact": fake.name(),
            "emergency_phone": fake.phone_number()
        }

    def generate_follow_up_report(self, patient_record: Dict[str, Any], days_after: int = None) -> Dict[str, Any]:
        """Generate a follow-up report for a patient"""
        if days_after is None:
            days_after = random.randint(1, 30)
        
        discharge_date = datetime.strptime(patient_record["discharge_date"], "%Y-%m-%d")
        report_date = discharge_date + timedelta(days=days_after)
        
        # Generate random symptoms/concerns
        symptom_templates = [
            "Patient reports mild {symptom}",
            "Experiencing {symptom} since yesterday",
            "No issues with {symptom}",
            "Improvement in {symptom}",
            "Concerns about {symptom}"
        ]
        
        symptoms = ["pain", "swelling", "fatigue", "nausea", "breathing", "appetite", "sleep"]
        
        return {
            "report_id": f"RPT-{str(uuid.uuid4())[:8].upper()}",
            "patient_name": patient_record["patient_name"],
            "patient_id": patient_record["patient_id"],
            "report_date": report_date.strftime("%Y-%m-%d"),
            "days_post_discharge": days_after,
            "primary_diagnosis": patient_record["primary_diagnosis"],
            "current_medications": patient_record["medications"],
            "reported_symptoms": random.choice(symptom_templates).format(symptom=random.choice(symptoms)),
            "medication_adherence": random.choice(["Excellent", "Good", "Fair", "Poor"]),
            "follow_up_compliance": random.choice(["Attended", "Missed", "Rescheduled"]),
            "vital_signs": {
                "blood_pressure": f"{random.randint(110, 160)}/{random.randint(70, 100)}",
                "heart_rate": random.randint(60, 100),
                "temperature": round(random.uniform(97.0, 99.5), 1),
                "weight": round(random.uniform(50, 120), 1)
            },
            "notes": f"Patient follow-up {days_after} days post-discharge. " + 
                    random.choice(["Recovering well.", "Some concerns noted.", "Stable condition.", "Improvement noted."])
        }

    def generate_symptom_queries(self, n: int = 100) -> List[Dict[str, Any]]:
        """Generate realistic patient symptom queries for training"""
        symptom_patterns = [
            "I'm experiencing {symptom} in my {body_part}",
            "I have {severity} {symptom} that started {timeframe}",
            "Is it normal to have {symptom} after {procedure}?",
            "My {symptom} is getting {progression}",
            "I'm worried about {symptom} and {secondary_symptom}",
            "Can my medication cause {symptom}?",
            "Should I be concerned about {symptom}?",
            "The {symptom} is {severity} today",
            "I've noticed {symptom} since {timeframe}",
            "Is {symptom} related to my {condition}?"
        ]
        
        symptoms = ["pain", "swelling", "nausea", "dizziness", "fatigue", "shortness of breath", 
                   "headache", "chest pain", "abdominal pain", "leg pain", "back pain"]
        body_parts = ["chest", "abdomen", "legs", "arms", "back", "head", "stomach"]
        severities = ["mild", "moderate", "severe", "sharp", "dull", "throbbing"]
        timeframes = ["yesterday", "this morning", "a few days ago", "last week", "since discharge"]
        progressions = ["worse", "better", "the same", "more frequent"]
        procedures = ["surgery", "my procedure", "discharge", "treatment"]
        conditions = ["kidney disease", "heart condition", "diabetes", "COPD"]
        
        queries = []
        
        for i in range(n):
            pattern = random.choice(symptom_patterns)
            query = pattern.format(
                symptom=random.choice(symptoms),
                body_part=random.choice(body_parts),
                severity=random.choice(severities),
                timeframe=random.choice(timeframes),
                progression=random.choice(progressions),
                procedure=random.choice(procedures),
                condition=random.choice(conditions),
                secondary_symptom=random.choice(symptoms)
            )
            
            queries.append({
                "query_id": f"Q-{str(uuid.uuid4())[:8].upper()}",
                "query": query,
                "intent": "symptom_inquiry",
                "urgency": random.choice(["low", "medium", "high"]),
                "category": random.choice(["pain", "medication", "follow-up", "general"]),
                "generated_date": fake.date_time_between(start_date='-30d', end_date='now').isoformat()
            })
        
        return queries

    def generate_medication_data(self, n: int = 50) -> List[Dict[str, Any]]:
        """Generate medication database for drug interactions and information"""
        medication_names = [
            "Lisinopril", "Furosemide", "Metformin", "Insulin", "Aspirin", 
            "Atorvastatin", "Metoprolol", "Amlodipine", "Prednisone", 
            "Ciprofloxacin", "Omeprazole", "Sertraline", "Carvedilol"
        ]
        
        medication_classes = [
            "ACE Inhibitor", "Diuretic", "Antidiabetic", "Hormone", "Antiplatelet",
            "Statin", "Beta-blocker", "Calcium Channel Blocker", "Corticosteroid",
            "Antibiotic", "Proton Pump Inhibitor", "SSRI", "Beta-blocker"
        ]
        
        medications = []
        
        for i, med_name in enumerate(medication_names):
            medications.append({
                "medication_id": f"MED-{str(uuid.uuid4())[:8].upper()}",
                "name": med_name,
                "generic_name": med_name.lower(),
                "drug_class": medication_classes[i % len(medication_classes)],
                "common_doses": [f"{random.randint(5, 100)}mg", f"{random.randint(1, 4)} times daily"],
                "side_effects": random.sample([
                    "nausea", "dizziness", "headache", "fatigue", "diarrhea", 
                    "dry cough", "muscle pain", "sleep disturbance"
                ], k=random.randint(2, 4)),
                "interactions": random.sample(medication_names, k=random.randint(1, 3)),
                "contraindications": random.sample([
                    "pregnancy", "kidney disease", "liver disease", "heart failure"
                ], k=random.randint(1, 2)),
                "monitoring_required": random.choice([True, False])
            })
        
        return medications

    def save_to_file(self, data: List[Dict[str, Any]], filename: str, directory: str = "data/generated"):
        """Save generated data to JSON file"""
        import os
        
        # Create directory if it doesn't exist
        if not os.path.exists(directory):
            os.makedirs(directory)
        
        filepath = os.path.join(directory, filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        print(f"Generated {len(data)} records and saved to {filepath}")

def main():
    """Generate various datasets"""
    generator = MedicalDataGenerator()
    
    # Generate patient records
    print("Generating patient records...")
    patients = [generator.generate_patient_record() for _ in range(50)]
    generator.save_to_file(patients, "patient_records.json")
    
    # Generate follow-up reports
    print("Generating follow-up reports...")
    reports = []
    for patient in patients[:20]:  # Generate reports for first 20 patients
        num_reports = random.randint(1, 5)
        for _ in range(num_reports):
            reports.append(generator.generate_follow_up_report(patient))
    generator.save_to_file(reports, "follow_up_reports.json")
    
    # Generate symptom queries
    print("Generating symptom queries...")
    queries = generator.generate_symptom_queries(200)
    generator.save_to_file(queries, "symptom_queries.json")
    
    # Generate medication data
    print("Generating medication database...")
    medications = generator.generate_medication_data()
    generator.save_to_file(medications, "medication_database.json")
    
    print("\nData generation complete!")
    print(f"Generated:")
    print(f"- {len(patients)} patient records")
    print(f"- {len(reports)} follow-up reports") 
    print(f"- {len(queries)} symptom queries")
    print(f"- {len(medications)} medication entries")

if __name__ == "__main__":
    main()