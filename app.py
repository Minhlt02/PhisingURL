#importing required libraries

from flask import Flask, request, render_template
import numpy as np
import pandas as pd
from sklearn import metrics 
import warnings
import pickle
warnings.filterwarnings('ignore')
from feature import FeatureExtraction

app = Flask(__name__)

models = {
    '0' : "pickle/model_gbc.pkl",
    'Random Forest': "pickle/model_rf.pkl",
    'Support Vector Machine': "pickle/model_svm.pkl",
    'Gradient Boost Classifier': "pickle/model_gbc.pkl"
}

# file = open("pickle/model_rf.pkl","rb")
# rf = pickle.load(file)
# file.close()

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        select = request.form.get('model')
        model_path = models[str(select)]
        model = open(model_path, 'rb')
        pickled_model = pickle.load(model)
        model.close
        
        url = request.form["url"]
        obj = FeatureExtraction(url)
        x = np.array(obj.getFeaturesList()).reshape(1,30) 

        y_pred = pickled_model.predict(x)[0]
        #1 is safe       
        #-1 is unsafe
        y_pro_phishing = pickled_model.predict_proba(x)[0,0]
        y_pro_non_phishing = pickled_model.predict_proba(x)[0,1]
        # if(y_pred ==1 ):
        pred = "It is {0:.2f} % safe to go ".format(y_pro_phishing*100)
        return render_template('index.html',xx =round(y_pro_non_phishing,2),url=url,model=select )
    return render_template("index.html", xx =-1)


if __name__ == "__main__":
    app.run(debug=True)