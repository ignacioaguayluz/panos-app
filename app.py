from flask import Flask, render_template, request, jsonify
from google.oauth2.service_account import Credentials
import gspread
import os
from datetime import datetime
import json
app = Flask(__name__)
port = int(os.environ.get("PORT", 5000))

scope = [
"https://www.googleapis.com/auth/spreadsheets",
"https://www.googleapis.com/auth/drive"
]
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
creds = Credentials.from_service_account_file(
os.path.join(BASE_DIR, "credentials.json"),
scopes=scope
)
client = gspread.authorize(creds)
sheet = client.open_by_key("1720qM4F1TVsNS81JMOnwQ0juOhhgAHUnCJhYzRSpKHE").sheet1

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/tomar")
def tomar():
    return render_template("tomar.html")

@app.route("/devolver")
def devolver():
    return render_template("devolver.html")

@app.route("/accion", methods=["POST"])
def accion():
    try:
        data = request.json
        tipo = data.get("tipo") # "entregar" o "recibir"
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        if tipo == "tomar":
            row = [timestamp, "Se dio un paño", "-"]
        elif tipo == "devolver":
            row = [timestamp, "-", "Se devolvio un paño"]
        else:
            return jsonify({"error": "Tipo inválido"}), 400

        sheet.append_row(row)

        return jsonify({"message": "ok"})

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
if __name__ == "__main__":
    app.run(debug=True, port=5001)