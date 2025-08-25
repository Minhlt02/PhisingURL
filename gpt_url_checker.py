import requests

def check_with_openrouter(url_to_check):
    API_KEY = "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"

    response = requests.post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json",
        },
        json={
            "model": "deepseek/deepseek-r1-0528-qwen3-8b:free",
            "messages": [
                {"role": "system", "content": """
You are a cybersecurity classifier.
Your task: Given a URL, respond with only ONE of the following words:
- "Phishing"
- "Safe"
Do not explain, do not add anything else.
"""}, 
                {"role": "user", "content": f"Check this URL: {url_to_check}"}
            ],
            "temperature": 0
        }
    )

    try:
        data = response.json()
        print("DEBUG:", data)  # để kiểm tra nếu lỗi

        if "choices" in data and len(data["choices"]) > 0:
            result = data["choices"][0]["message"]["content"].strip().lower()
            if result == "phishing":
                return "Phishing"
            elif result == "safe":
                return "Safe"
        return "Error"
    except Exception as e:
        print("Exception:", e)
        print("Raw response:", response.text)
        return "Error"