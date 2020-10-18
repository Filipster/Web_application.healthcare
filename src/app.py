import os
import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from PIL import Image

from src import view_pras_analysis
from src import view_diabetes


def main():
    # -------------------------------- Sidebar -------------------------------
    img = Image.open('src/imgs/logo.png')
    st.sidebar.image(img, use_column_width=True)
    
    page = st.sidebar.radio(
        '', 
        ('PRAS Analysis', 'Diabetes Model', 'Heart Disease Model', 'Image Diagnosis'))
    
    if page == 'PRAS Analysis':
        view_pras_analysis.main()
    elif page == 'Diabetes Model':
        view_diabetes.main()

