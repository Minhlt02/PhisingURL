import pandas as pd
import numpy as np

# Đọc dữ liệu
train_df = pd.read_csv("train_features.csv")  # 28 feature từ tập huấn luyện
pred_df = pd.read_csv("predict_features.csv") # 28 feature từ dữ liệu dự đoán

# Đảm bảo đúng thứ tự cột
train_df = train_df.iloc[:, :28]
pred_df = pred_df.iloc[:, :28]

# Hàm tính drift
def check_feature_drift(train, pred):
    results = []
    for col in train.columns:
        train_mean = train[col].mean()
        pred_mean = pred[col].mean()
        train_std = train[col].std()
        pred_std = pred[col].std(ddof=0) if len(pred) > 1 else 0


        # So sánh tỷ lệ chênh lệch trung bình
        mean_diff_ratio = abs(pred_mean - train_mean) / (abs(train_mean) + 1e-8)
        std_diff_ratio = abs(pred_std - train_std) / (abs(train_std) + 1e-8)

        results.append({
            "Feature": col,
            "Train Mean": train_mean,
            "Pred Mean": pred_mean,
            "Train Std": train_std,
            "Pred Std": pred_std,
            "Mean Diff %": mean_diff_ratio * 100,
            "Std Diff %": std_diff_ratio * 100
        })
    return pd.DataFrame(results)

# Chạy kiểm tra
drift_df = check_feature_drift(train_df, pred_df)

# Sắp xếp theo mức độ chênh lệch trung bình
drift_df = drift_df.sort_values(by="Mean Diff %", ascending=False)

# Xuất kết quả
pd.set_option("display.float_format", lambda x: f"{x:.4f}")
print(drift_df)

# Lưu ra file để xem chi tiết
drift_df.to_csv("feature_drift_report.csv", index=False)
