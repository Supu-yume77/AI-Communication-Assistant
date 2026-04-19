from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

API_KEY = "your_api_key_here"

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/analyze", methods=["POST"])
def analyze():
    data = request.get_json()
    user_text = data.get("text")

    try:
        response = requests.post(
            url="https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": "openai/gpt-3.5-turbo",
                "messages": [
                    {"role": "system", "content": """
You are a professional communication trainer.

Rules:
- First decide: Is the sentence already polite and professional?
- If YES → clearly say: "This sentence is already polite and appropriate." DO NOT suggest changes.
- If NO → explain briefly and suggest a better version.
- DO NOT unnecessarily improve already good sentences.
- DO NOT repeat the same suggestion for every sentence.
- Be accurate and context-aware.

Keep answers short and precise.
"""},
                    {"role": "user", "content": f"""
Evaluate this sentence:

"{user_text}"

Tell clearly:
1. Is it polite or not?
2. If yes → say it's already good.
3. If no → give improved version.
"""}
                ]
            }
        )

        result = response.json()
        reply = result["choices"][0]["message"]["content"]

        return jsonify({"result": reply})

    except Exception as e:
        return jsonify({"result": "Error: " + str(e)})

if __name__ == "__main__":
    app.run(debug=True)
