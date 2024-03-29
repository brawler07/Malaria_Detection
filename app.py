from __future__ import division, print_function
import sys
import os
import glob
import re
import numpy as np

from tensorflow.keras.applications.imagenet_utils import preprocess_input, decode_predictions
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image


from flask import Flask, redirect, url_for, request, render_template  
from werkzeug.utils import secure_filename


app = Flask(__name__)

MODEL_PATH ='C:\\Users\\lenovo\\Downloads\\Mini-Project\\malaria_detector.h5'

model = load_model(MODEL_PATH)





def model_predict(img_path, model):
    img = image.load_img(img_path, target_size=(130,130,3))
    x = image.img_to_array(img)
    x = np.expand_dims(x, axis=0)
    x=x/255 

    preds = model.predict(x)
    if preds< 0.5:
        preds="The Person is Infected With malaria"
    else:
        preds="The Person is not Infected With malaria" 
    
    
    return preds


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/predict', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        f = request.files['file']

        basepath = os.path.dirname(__file__)
        file_path = os.path.join(
            basepath, 'uploads', secure_filename(f.filename))
        f.save(file_path)
        preds = model_predict(file_path, model)
        result=preds
        return result
    return None


if __name__ == '__main__':
    app.run(debug=True)
