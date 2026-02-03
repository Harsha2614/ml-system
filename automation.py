import requests
import json
from datetime import datetime

API_URL = "https://ml-system-r7yk.onrender.com/predict"
HEALTH_URL = "https://ml-system-r7yk.onrender.com"

TEST_DATA = {
    "Gender": "Male",
    "Married": "Yes",
    "Dependents": "0",
    "Education": "Graduate",
    "Self_Employed": "No",
    "ApplicantIncome": 5000,
    "CoapplicantIncome": 15000,
    "LoanAmount": 140000,
    "Loan_Amount_Term": 360,
    "Credit_History": 1,
    "Property_Area": "Urban"
}

LOG_FILE = "automation_log.txt"


def check_health():
    try:
        r = requests.get(HEALTH_URL, timeout=10)
        return r.status_code == 200
    except:
        return False


def run_test():

    log = {
        "time": datetime.now().isoformat()
    }

    if not check_health():
        log["status"] = "SERVER_DOWN"
    else:
        try:
            res = requests.post(API_URL, json=TEST_DATA, timeout=15)
            log["status"] = "OK"
            log["response"] = res.json()
        except Exception as e:
            log["status"] = "FAILED"
            log["error"] = str(e)

    with open(LOG_FILE, "a") as f:
        f.write(json.dumps(log) + "\n")

    print("Run:", log["status"])


if __name__ == "__main__":
    run_test()
