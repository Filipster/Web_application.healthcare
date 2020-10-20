import streamlit as st
import tensorflow.keras
import numpy as np
from PIL import Image, ImageOps


def main():
    st.title('DATAFLOW - Image Diagnosis')

    st.sidebar.header('Choose a Model')
    choices = ['Eye Diseases', 'COVID', 'Skin Cancer']
    menu = st.sidebar.selectbox('Menu:', choices)
    
    st.set_option('deprecation.showfileUploaderEncoding', False)
    image_input = st.sidebar.file_uploader('Choose an image: ', type=['jpg', 'png'])
    if image_input:
        img = image_input.getvalue()

        size = st.slider('Adjust image size: ', 300, 1000)
        st.image(img, width=size, height=size)
        np.set_printoptions(suppress=True)

        # Image process
        data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)
        image = Image.open(image_input)
        size = (224, 224)
        image = ImageOps.fit(image, size, Image.ANTIALIAS)
        image_array = np.asarray(image)
        normalized_image_array = (image_array.astype(np.float32) / 127.0) - 1
        normalized_image_array.resize(data.shape)
        data[0] = normalized_image_array

        if menu == 'Eye Diseases':
            load_eye_models(data)
        elif menu == 'COVID':
            load_covid(data)
        elif menu == 'Skin Cancer':
            load_skin(data)


def load_eye_models(data):
    # Buttons for predictions    
    st.header('Analyze Cataract')
    st.markdown('> Eye Diseases analyzes cataract, diabetic retinopathy and redness levels. Upload an image to get started.')

    cataract = st.button('Click to analyze', key=1)
    if cataract:
        predict_result('cataract', data)

    st.header('Analyze Diabetes Retinopathy')
    retinopathy = st.button('Click to analyze', key=2)
    if retinopathy:
        predict_result('retinopathy', data)
    
    st.header('Analyze Redness Levels')
    redness = st.button('Click to analyze', key=3)
    if redness:
        predict_result('redness', data)


def load_covid(data):
    st.header('Analyze COVID')
    st.markdown('> COVID Uses CT Scans to detect whether the patient is likely to have COVID or not. Upload an image to get started.')

    covid = st.button('Click to analyze', key=4)
    
    if covid:
        predict_result('covid', data)


def load_skin(data):
    st.header('Analyze Skin Cancer')
    st.markdown('> Detects whether the patient has benign or malignant type of cancer. Further classifications are still under testing. Upload an image to get started.')

    skin = st.button('Click to analyze', key=5)
    if skin:
        predict_result('Skin Cancer', data)


def predict_result(mdl, data):
    if mdl == 'cataract':
        model = tensorflow.keras.models.load_model('src/models/eye_models/cataract/model.h5')
    elif mdl == 'retinopathy':
        model = tensorflow.keras.models.load_model('src/models/eye_models/dr/model.h5')
    elif mdl == 'redness':
        model = tensorflow.keras.models.load_model('src/models/eye_models/redness/model.h5')
    elif mdl == 'covid':
        model = tensorflow.keras.models.load_model('src/models/covid_model/model.h5')

        preds = model.predict(data)
        class1 = preds[0,0]
        class2 = preds[0,1]

        if class1 > class2:
            st.markdown('Negative for **{}** with **{:.2f}** % of confidence.'.format(mdl.title(), class1 * 100))
        elif class2 > class1:
            st.markdown('Possibility for **{}** with **{:.2f}** % of confidence.'.format(mdl.title(), class2 * 100))
        else:
            st.markdown('This image could not be identified.')
        return ''

    elif mdl == 'Skin Cancer':
        model = tensorflow.keras.models.load_model('src/models/skin_model/model.h5')

        preds = model.predict(data)
        class1 = preds[0,0]
        class2 = preds[0,1]
        print(preds)
        if class1 > class2:
            st.markdown('Benign type for **{}** with **{:.2f}** % of confidence.'.format(mdl.title(), class1 * 100))
        elif class2 > class1:
            st.markdown('Malign type for **{}** with **{:.2f}** % of confidence.'.format(mdl.title(), class2 * 100))
        else:
            st.markdown('This image could not be identified.')
        return ''
    else:
        st.markdown('Something gone wrong.')

    preds = model.predict(data)
    class1 = preds[0,0]
    class2 = preds[0,1]

    if class1 > class2:
        st.markdown('Possbility for **{}** with **{:.2f}** % of confidence.'.format(mdl.title(), class1 * 100))
    elif class2 > class1:
        st.markdown('Negative for **{}** with **{:.2f}** % of confidence.'.format(mdl.title(), class2 * 100))
    else:
        st.markdown('This image could not be identified.')