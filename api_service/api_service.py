from flask import Flask, request, jsonify
from flask_cors import CORS
import psycopg2
import os

# --- Uygulama Yapılandırması ---

app = Flask(__name__)
CORS(app)

# Veritabanı bağlantı bilgilerini ortam değişkeninden veya varsayılan değerden alır
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://clooud2_2_dp_user:lT7t7P1OWoTiIINtSuPoE3VrRF8IAGBr@dpg-d3ub82re5dus739hupo0-a.oregon-postgres.render.com/clooud2_2_dp"
)

# --- Veritabanı Fonksiyonu ---

def connect_db():
    """Veritabanı bağlantısını kurar ve döndürür."""
    return psycopg2.connect(DATABASE_URL)

# --- Rota Tanımlaması ---

@app.route("/ziyaretciler", methods=["GET", "POST"])
def ziyaretciler():
    """Ziyaretçi verilerini POST ile ekler ve GET ile son 10 ziyaretçiyi listeler."""
    
    # Bağlantıyı aç
    conn = connect_db()
    cur = conn.cursor()

    # Eğer yoksa ziyaretciler tablosunu oluştur
    cur.execute("CREATE TABLE IF NOT EXISTS ziyaretciler (id SERIAL PRIMARY KEY, isim TEXT, SEHİR TEXT)")

    if request.method == "POST":
        # İsim verisini alır
        isim = request.json.get("isim")
        SEHİR = request.json.get("SEHİR")
        
        # Veritabanına yeni ziyaretçiyi ekler
        if isim and SEHİR:
            cur.execute("INSERT INTO ziyaretciler (isim,SEHİR) VALUES (%s, %s)", (isim,SEHİR,))
            conn.commit()

    # Son 10 ziyaretçinin ismini veritabanından çeker
    cur.execute("SELECT isim,SEHİR FROM ziyaretciler ORDER BY id DESC LIMIT 10")
    isimler = [f"{isim} ({SEHİR})" for isim, sehir in cur.fetchall()]

    # Bağlantıları kapat
    cur.close()
    conn.close()

    # İsim listesini JSON olarak döndürür
    return jsonify(isimler)

# --- Uygulama Başlatma ---

if __name__ == "__main__":
    # Uygulamayı 5001 portunda tüm arayüzlerde çalıştırır
    app.run(host="0.0.0.0", port=5001)
