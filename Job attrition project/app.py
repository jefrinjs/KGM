from flask import Flask, render_template, request
import pickle
import pandas as pd
import numpy as np

# Load model & encoders
model = pickle.load(open("model.pkl", "rb"))
encoders = pickle.load(open("encoder.pkl", "rb"))

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/predict", methods=["POST"])
def predict():
    if request.method == "POST":
        # Collect form data
        education = request.form["education"]
        joining_year = int(request.form["joining_year"])
        city = request.form["city"]
        payment_tier = int(request.form["payment_tier"])
        age = int(request.form["age"])
        gender = request.form["gender"]
        ever_benched = request.form["ever_benched"]
        exp_domain = int(request.form["exp_domain"])

        # Create DataFrame
        new_data = pd.DataFrame([{
            "Education": education,
            "Joining year": joining_year,
            "City": city,
            "Payment tier": payment_tier,
            "Age": age,
            "Gender": gender,
            "Ever benched": ever_benched,
            "Experience in current domain": exp_domain
        }])

        # Handle unseen labels safely
        for col in encoders:
            if new_data[col].iloc[0] not in encoders[col].classes_:
                # add unseen label to classes_
                encoders[col].classes_ = np.append(encoders[col].classes_, new_data[col].iloc[0])
            new_data[col] = encoders[col].transform(new_data[col])

        # Predict
        prediction = model.predict(new_data)[0]
        result = "Employee will LEAVE ❌" if prediction == 1 else "Employee will STAY ✅"

        return render_template("result.html", result=result)


if __name__ == "__main__":
    app.run(debug=True)
