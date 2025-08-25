from flask import Flask, request, render_template
import numpy as np
import pickle
import warnings
from feature import FeatureExtraction
from gpt_url_checker import check_with_openrouter

warnings.filterwarnings('ignore')
app = Flask(__name__)

# ==== Load mô hình RF đã train với 14 features ====
rf_model = pickle.load(open('pickle/model_rf_new.pkl', 'rb'))

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        url = request.form["url"]

        # ==== 1. Trích xuất 14 features từ URL ====
        
        obj = FeatureExtraction(url)
        features = np.array(obj.get_features_list()).reshape(1, -1)  # 14 features

        # ==== 2. Dự đoán với RF ====
        rf_pred = rf_model.predict(features)[0]
        predicted_class = "Safe" if rf_pred == 0 else "Phishing"

        # ==== 3. Kết hợp với AI checker ====
        ai_result = check_with_openrouter(url)

        print(rf_model.classes_)


        if predicted_class == "Phishing" and ai_result == "Phishing":
            final_result = "Phishing"
        elif predicted_class == "Safe" and ai_result == "Safe":
            final_result = "Safe"
        else:
            final_result = f"Suspicious (RF says {predicted_class}, AI says {ai_result})"

        return render_template(
            'index.html',
            xx=final_result,
            url=url,
            model="RF + AI",
            ml_result=predicted_class,
            ai_result=ai_result
        )

    return render_template("index.html", xx=-1)


if __name__ == "__main__":
    app.run(debug=True)
