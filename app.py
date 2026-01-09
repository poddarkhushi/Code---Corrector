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


def correct_code_openai(code):
    url = "https://api.openai.com/v1/chat/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {OPENAI_API_KEY}",
    }
    data = {
        "model": "gpt-4o-mini",
        "messages": [
            {
                "role": "system",
                "content": "You will receive code. Fix it and give a short explaination for  all the changes that you have made in the form of comments. Return ONLY the corrected code. Do NOT include markdown or ```python``` blocks.  Output ONLY raw corrected code and nothing else."
            },
            {"role": "user", "content": code}
        ]
    }
    r = requests.post(url, json=data, headers=headers).json()
    if "choices" in r:
        return r["choices"][0]["message"]["content"]
    return str(r)


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        input_code = request.form["code"]
        output = correct_code_openai(input_code)
        return render_template("index.html", input_code=input_code, output=output)

    return render_template("index.html", input_code="", output=None)


if __name__ == "__main__":
    app.run()
