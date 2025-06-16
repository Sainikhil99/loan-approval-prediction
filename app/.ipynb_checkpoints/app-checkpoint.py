import streamlit as st
import pandas as pd
import pickle

# Load trained model
with open("loan_model.pkl", "rb") as file:
    model = pickle.load(file)

# App title
st.title("🏦 Loan Approval Prediction App")
st.write("### Fill in the applicant's details to check loan eligibility:")

# Input fields
gender = st.selectbox("Gender", ['Male', 'Female'])
married = st.selectbox("Married", ['Yes', 'No'])
dependents = st.selectbox("Dependents", ['0', '1', '2', '3+'])
education = st.selectbox("Education", ['Graduate', 'Not Graduate'])
self_employed = st.selectbox("Self Employed", ['Yes', 'No'])
applicant_income = st.number_input("Applicant Income", min_value=0)
coapplicant_income = st.number_input("Coapplicant Income", min_value=0)
loan_amount = st.number_input("Loan Amount (in thousands)", min_value=0)
loan_term = st.selectbox("Loan Amount Term (in days)", [360, 180, 120, 84, 60, 36, 12])
credit_history = st.selectbox("Credit History", [1.0, 0.0])
property_area = st.selectbox("Property Area", ['Urban', 'Semiurban', 'Rural'])

# Encoding
gender = 1 if gender == 'Male' else 0
married = 1 if married == 'Yes' else 0
dependents = 3 if dependents == '3+' else int(dependents)
education = 0 if education == 'Graduate' else 1
self_employed = 1 if self_employed == 'Yes' else 0
property_area_map = {'Urban': 2, 'Semiurban': 1, 'Rural': 0}
property_area = property_area_map[property_area]

# Final feature vector
input_data = pd.DataFrame([[gender, married, dependents, education,
                            self_employed, applicant_income, coapplicant_income,
                            loan_amount, loan_term, credit_history, property_area]],
                          columns=['Gender', 'Married', 'Dependents', 'Education',
                                   'Self_Employed', 'ApplicantIncome', 'CoapplicantIncome',
                                   'LoanAmount', 'Loan_Amount_Term', 'Credit_History', 'Property_Area'])

# Predict button
if st.button("Predict Loan Approval"):
    prediction = model.predict(input_data)
    result = "✅ Loan Approved!" if prediction[0] == 1 else "❌ Loan Rejected."
    st.subheader(result)
