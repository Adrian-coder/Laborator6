from flask import Flask, request, jsonify
import psycopg2

app = Flask(__name__)

def get_connection():
    return psycopg2.connect(
        host="db",
        database="postgres",
        user="postgres",
        password="postgres"
    )

@app.route("/", methods=["GET"])
def index():
    return "Aplicația Flask rulează!"

@app.route("/mesaj", methods=["POST"])
def add_message():
    content = request.json["mesaj"]
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO mesaje (continut) VALUES (%s)", (content,))
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({"status": "Mesaj adăugat!"})

@app.route("/mesaj", methods=["GET"])
def get_messages():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT continut FROM mesaje")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify([r[0] for r in rows])

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)