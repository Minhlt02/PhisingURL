from flask import Flask, request, render_template
import numpy as np
import pickle
import keras
import warnings
import pandas as pd
from feature import FeatureExtraction
from gpt_url_checker import check_with_openrouter

warnings.filterwarnings('ignore')
app = Flask(__name__)

# ==== Load mô hình & thông tin huấn luyện ====
# Danh sách 28 đặc trưng đã chọn lúc train
selected_features = pickle.load(open('pickle/selected_features.pkl', 'rb'))

# Scaler đã fit trên tập huấn luyện
scaler = pickle.load(open('pickle/scaler1.pkl', 'rb'))

# Model con
rf_model = pickle.load(open('pickle/model_rf1.pkl', 'rb'))
dl_model = keras.saving.load_model('pickle/model_dl1.keras')
meta_model = pickle.load(open('pickle/model_meta1.pkl', 'rb'))  # Meta model

def get_dl_probs(model, X):
    """Lấy xác suất từ Deep Learning model."""
    probs = model.predict(X, verbose=0)
    return probs.flatten()

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        url = request.form["url"]

        # ==== 1. Trích xuất toàn bộ feature ====
        obj = FeatureExtraction(url)
        all_features = np.array(obj.get_features_list()).reshape(1, 50)

        # ==== 3. Chuẩn hóa ====
        features_scaled = scaler.transform(all_features)


        # ==== 4. Dự đoán từng model con ====
        rf_probs = rf_model.predict_proba(features_scaled)[:, 1]  # RF prob
        dl_probs = get_dl_probs(dl_model, features_scaled)        # DL prob

        # ==== 5. Meta model ====
        combined_features = np.vstack([rf_probs, dl_probs]).T
        meta_probs = meta_model.predict_proba(combined_features)[:, 1]
        y_pred = meta_model.predict(combined_features)[0]

        predicted_class = "Safe" if y_pred == 0 else "Phishing"

        # ==== 6. Kết hợp với AI checker ====
        ai_result = check_with_openrouter(url)

        if predicted_class == "Phishing" and ai_result == "Phishing":
            final_result = "Phishing"
        elif predicted_class == "Safe" and ai_result == "Safe":
            final_result = "Safe"
        else:
            final_result = f"Suspicious (ML says {predicted_class}, AI says {ai_result})"

        return render_template(
            'index.html',
            xx=final_result,
            url=url,
            model="Ensemble (RF + DL + Meta)",
            ml_result=predicted_class,
            ai_result=ai_result
        )

    return render_template("index.html", xx=-1)

if __name__ == "__main__":
    app.run(debug=True)
