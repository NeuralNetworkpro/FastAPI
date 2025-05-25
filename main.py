from fastapi import FastAPI,Path,HTTPException,Query
import json

app=FastAPI()

def load_data():
    # Placeholder for data loading logic
    with open("patients.json", "r") as file:
        data = json.load(file)
    return data

@app.get("/")
def hello():
    return {"mesage": "Pateint Management System API"}

@app.get("/about")
def about():
    return {"message": "A fully functional API to manage your patiemt records"}

@app.get("/view")
def view():
    data = load_data()
    return data

@app.get("/patient/{patient_id}")
def view_patient(patient_id: str=Path(..., description="The ID of the patient to view",example="P008", min_length=3, max_length=10)):
    data = load_data()
    if patient_id in data:
        return data[patient_id]
    raise HTTPException(status_code=404, detail="Patient not found")


@app.get("/sort")
def sort_patients(sort_by:str=Query(..., description="Sort patients by height,weight or bmi"),order:str=Query("asc", description="Order of sorting: 'asc' for ascending, 'desc' for descending")):
    valid_fields = ["height", "weight", "bmi"]
    if sort_by not in valid_fields:
        raise HTTPException(status_code=400, detail="Invalid sort parameter. Use 'height', 'weight', or 'bmi'.")
    if order not in ["asc", "desc"]:
        raise HTTPException(status_code=400, detail="Invalid order parameter. Use 'asc' or 'desc'.")
    data = load_data()
    sort_order = True if order == "desc" else False
   
    sorted_data = sorted(data.values(), key=lambda x:x.get(sort_by,0), reverse= sort_order)
    return sorted_data