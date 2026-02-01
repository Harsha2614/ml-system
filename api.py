from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import pandas as pd
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse


# Load model and features
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

model = joblib.load(os.path.join(BASE_DIR, "model/loan_model.pkl"))
features = joblib.load(os.path.join(BASE_DIR, "model/features.pkl"))


app = FastAPI(title="Loan Approval API")
# Serve frontend files
app.mount("/frontend", StaticFiles(directory="frontend"), name="frontend")


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # Allow frontend
    allow_credentials=True,
    allow_methods=["*"],  # Allow OPTIONS, POST, GET, etc.
    allow_headers=["*"],
)


# Input schema
class LoanInput(BaseModel):
    Gender: str
    Married: str
    Dependents: str
    Education: str
    Self_Employed: str
    ApplicantIncome: float
    CoapplicantIncome: float
    LoanAmount: float
    Loan_Amount_Term: float
    Credit_History: float
    Property_Area: str


@app.get("/")
def serve_frontend():
    return FileResponse("frontend/index.html")



@app.post("/predict")
def predict(data: LoanInput):

    # Convert to DataFrame
    input_df = pd.DataFrame([data.dict()])

    # One-hot encoding
    input_df = pd.get_dummies(input_df)

    # Align with training features
    input_df = input_df.reindex(columns=features, fill_value=0)

    # Predict
    prediction = int(model.predict(input_df)[0])


    result = "Approved" if prediction == 1 else "Rejected"

    return {"prediction": result,"value":prediction}
    
