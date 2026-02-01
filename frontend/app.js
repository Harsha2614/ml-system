const form = document.getElementById("loanForm");
const resultDiv = document.getElementById("result");

form.addEventListener("submit", async (e) => {
    e.preventDefault();

    const data = {
        Gender: document.getElementById("Gender").value,
        Married: document.getElementById("Married").value,
        Dependents: document.getElementById("Dependents").value,
        Education: document.getElementById("Education").value,
        Self_Employed: document.getElementById("Self_Employed").value,
        ApplicantIncome: Number(document.getElementById("ApplicantIncome").value),
        CoapplicantIncome: Number(document.getElementById("CoapplicantIncome").value),
        LoanAmount: Number(document.getElementById("LoanAmount").value),
        Loan_Amount_Term: Number(document.getElementById("Loan_Amount_Term").value),
        Credit_History: Number(document.getElementById("Credit_History").value),
        Property_Area: document.getElementById("Property_Area").value
    };

    resultDiv.innerText = "Checking...";

    try {
        const res = await fetch(
            "http://127.0.0.1:8000/predict",
            {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify(data)
            }
        );

        const result = await res.json();

        resultDiv.innerText = `Result: ${result.prediction}`;

    } catch (err) {
        resultDiv.innerText = "Error connecting to server";
        console.error(err);
    }
});
