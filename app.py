from flask import Flask, render_template, request, jsonify
from google.oauth2.service_account import Credentials
import gspread
import os
from datetime import datetime
import json
app = Flask(__name__)
port = int(os.environ.get("PORT", 10000))

def get_sheet():
    try:
        scope = [
            "https://www.googleapis.com/auth/spreadsheets",
            "https://www.googleapis.com/auth/drive"
        ]

        creds = Credentials.from_service_account_info(
            json.loads(os.environ["GOOGLE_CREDS"]),
            scopes=scope
        )

        client = gspread.authorize(creds)
        return client.open_by_key("1720qM4F1TVsNS81JMOnwQ0juOhhgAHUnCJhYzRSpKHE").sheet1

    except Exception as e:
        print("Error conectando con Google Sheets:", e)
        return None


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

        sheet = get_sheet()

        if sheet:
            sheet.append_row(row)
        else:
            print("No se pudo conectar a Google Sheets")

        return jsonify({"message": "ok"})

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=port)