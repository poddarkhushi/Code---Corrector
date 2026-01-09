from flask import Flask, render_template, request
import requests
import os
app = Flask(__name__)
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

@app.after_request
def add_header(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    return response


def correct_code_openai(code, lang):
    url = "https://api.openai.com/v1/chat/completions"

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {OPENAI_API_KEY}"
    }

    data = {
        "model": "gpt-4o-mini",
        "messages": [
            {
                "role": "system",
                "content": f"You are an expert {lang} developer. Only correct {lang} code."
            },
            {
                "role": "user",
                "content": f"Correct this {lang} code. You will receive code. Fix it and give a short explaination for  all the changes that you have made in the form of comments. Return ONLY the corrected code. Do NOT include markdown or ```python``` blocks.  Output ONLY raw corrected code and nothing else.{code}"
            }
        ]
    }

    response = requests.post(url, json=data, headers=headers)
    result = response.json()

    if "choices" not in result:
        return f"OPENAI API ERROR:\n{result}"

    return result["choices"][0]["message"]["content"]

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        input_code = request.form["code"]
        output = correct_code_openai(input_code)
        return render_template("index.html", input_code=input_code, output=output)

    return render_template("index.html", input_code="", output=None)


if __name__ == "__main__":
    app.run()

