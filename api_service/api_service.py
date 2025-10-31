from flask import Flask, request, jsonify
from flask_cors import CORS
import psycopg2
import os

# --- Uygulama Yapılandırması ---
app = Flask(__name__)
CORS(app)
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://clooud2_2_dp_user:lT7t7P1OWoTiIINtSuPoE3VrRF8IAGBr@dpg-d3ub82re5dus739hupo0-a.oregon-postgres.render.com/clooud2_2_dp"
)

# --- Veritabanı Fonksiyonu ---
def connect_db():
    return psycopg2.connect(DATABASE_URL)

# --- Rota Tanımlaması ---
@app.route("/ziyaretciler", methods=["GET", "POST"])
def ziyaretciler():
    conn = connect_db()
    cur = conn.cursor()

    # İYİLEŞTİRME: Sütun adını küçük harf 'sehir' olarak kullan
    cur.execute("CREATE TABLE IF NOT EXISTS ziyaretciler (id SERIAL PRIMARY KEY, isim TEXT, sehir TEXT)")
    # (Eski tabloyu silmeniz veya 'ALTER TABLE' ile sütun adını 'sehir' yapmanız gerekebilir)

    if request.method == "POST":
        isim = request.json.get("isim")
        
        # DÜZELTME 1: Frontend'den gelen 'sehir' (küçük harf) bekleniyor
        sehir = request.json.get("sehir")
        
        if isim and sehir: # Kontrol 'sehir' (küçük harf) ile yapılıyor
            # Sütun adı 'sehir' (küçük harf) olarak güncellendi
            cur.execute("INSERT INTO ziyaretciler (isim, sehir) VALUES (%s, %s)", (isim, sehir,))
            conn.commit()
            
            # (GET isteği POST'tan sonra veriyi çekeceği için buradan yanıt döndürmek daha iyi olabilir)
            # cur.close()
            # conn.close()
            # return jsonify({"mesaj": "Eklendi"}), 201

    # Veritabanından 'sehir' (küçük harf) sütunu çekiliyor
    cur.execute("SELECT isim, sehir FROM ziyaretciler ORDER BY id DESC LIMIT 10")
    
    # DÜZELTME 2: Döngü değişkeni 'sehir' (küçük harf) f-string içinde kullanılıyor
    isimler = [f"{isim} ({sehir})" for isim, sehir in cur.fetchall()]

    cur.close()
    conn.close()
    return jsonify(isimler)

# --- Uygulama Başlatma ---
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True) # Hata takibi için debug modu açıldı
