import requests

def check_with_openrouter(url_to_check):
    API_KEY = "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"  # Thay bằng key bạn lấy ở bước 1

    response = requests.post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json",
            "HTTP-Referer": "http://localhost",
            "X-Title": "My Phishing Checker",
        },
        json={
            "model": "openai/gpt-oss-20b:free",
            "messages": [
                {"role": "system", "content": """You are a cybersecurity expert specialized in detecting phishing websites. Analyze the given URL and return only "Phishing" or "Safe"."""},
                {"role": "user", "content": f"Check if this URL is safe: {url_to_check}"}
            ],
            "temperature": 0.3
        }
    )

    try:
        data = response.json()
        if "choices" in data and len(data["choices"]) > 0:
            result = data["choices"][0]["message"]["content"].strip().lower()
            if "phishing" in result:
                return "Phishing"
            elif "safe" in result:
                return "Safe"
        return "Error"
    except Exception:
        return "Error"

