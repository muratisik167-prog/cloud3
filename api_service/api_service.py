from flask import Flask, request, jsonify

from flask_cors import CORS

import psycopg2, os


app = Flask(__name__)

CORS(app)


DATABASE_URL = os.getenv(

"DATABASE_URL",

"postgresql://clooud2_2_dp_user:lT7t7P1OWoTiIINtSuPoE3VrRF8IAGBr@dpg-d3ub82re5dus739hupo0-a.oregon-postgres.render.com/clooud2_2_dp"

)


def connect_db():

return psycopg2.connect(DATABASE_URL)


@app.route("/ziyaretciler", methods=["GET", "POST"])

def ziyaretciler():

conn = connect_db()

cur = conn.cursor()

cur.execute("CREATE TABLE IF NOT EXISTS ziyaretciler (id SERIAL PRIMARY KEY, isim TEXT)")


if request.method == "POST":

isim = request.json.get("isim")

if isim:

cur.execute("INSERT INTO ziyaretciler (isim) VALUES (%s)", (isim,))

conn.commit()


cur.execute("SELECT isim FROM ziyaretciler ORDER BY id DESC LIMIT 10")

isimler = [row[0] for row in cur.fetchall()]


cur.close()

conn.close()


return jsonify(isimler)


if __name__ == "__main__":

app.run(host="0.0.0.0", port=5001)
