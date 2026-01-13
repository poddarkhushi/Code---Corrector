from flask import Flask, render_template, request
import requests
import os
app = Flask(__name__)

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

def correct_code_openai(code, lang):

    url = "https://api.openai.com/v1/chat/completions"

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {OPENAI_API_KEY}"
    }

    data = {
        "model": "gpt-4o-mini",   
        "messages": [
            {"role": "system", "content": f"You are a code correction assistant. The user is writing in {lang}."},
            {"role": "user", "content": f"Fix this {lang} code.You will receive code. Fix it and give a short explaination for all the changes that you have made in the form of comments. Return ONLY the corrected code. Do NOT include markdown or ```python``` type of blocks.  Output ONLY raw corrected code and nothing else.\n\n.'{code}"}
        ]
    }

    response = requests.post(url, json=data, headers=headers)
    result = response.json()

    print("DEBUG OPENAI RESPONSE:", result)

    if "choices" not in result:
        return f"OPENAI API ERROR:\n{result}"

    return result["choices"][0]["message"]["content"]


@app.route("/", methods=["GET", "POST"])
def index():
    output = ""
    input_code = ""
    selected_lang = "Python"  

    if request.method == "POST":
        input_code = request.form.get("code", "")
        selected_lang = request.form.get("lang", "Python")

        output = correct_code_openai(input_code, selected_lang)

    return render_template(
        "index.html",
        output=output,
        input_code=input_code,
        selected_lang=selected_lang
    )

if __name__ == "__main__":
    app.run(debug=True)







