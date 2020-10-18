import streamlit as st
import pickle
import numpy as np


def main():
    # Load the model
    load_model = open('src/models/diabetes_log_reg_v1.pkl', 'rb')
    log_regression = pickle.load(load_model)

    st.title('DATAFLOW - Diabetes Probability')
    st.markdown("""> This example shows how a model can predict the probability of diabetes diagnostic.""")

    st.header('Diabetes Prediction')
    st.subheader('This model was built for FEMALES above 21 years.')

    # Obrigatory Fields
    pregnancy = st.slider(
        'How many times were/is pregnant',
        min_value=0,
        max_value=20,
        step=1
    )

    glucose = st.slider(
        'Plasma Glucose Concentration',
        min_value=0,
        max_value=250,
        step=1
    )

    bp = st.slider(
        'Diastolic blood pressure (mm Hg)',
        min_value=40,
        max_value=220,
        step=1
    )

    skin = st.slider(
        'Triceps skin fold thickness (mm)',
        min_value=1,
        max_value=99,
        step=1
    )

    insulin = st.slider(
        '2-hour serum insulin (mm U/ml)',
        min_value=0,
        max_value=999,
        step=1
    )

    bmi = st.slider(
        'Body mass Index',
        min_value=0,
        max_value=70,
        step=1
    )

    dpf = st.slider(
        'Diabetes Pedigree Function',
        min_value=0.0,
        max_value=3.0,
        step=0.1
    )

    age = st.slider(
        'Age (in years)',
        min_value=0,
        max_value=99,
        step=1
    )

    submit = st.button('Predict')

    if submit:
        result = log_regression.predict_proba(np.array([pregnancy, glucose, bp, skin, insulin, bmi, dpf, age]).reshape(1, -1))
        st.markdown('Probability of Diabetes: {:.2f}%'.format(result[0][0] * 100))
