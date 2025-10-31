from flask import Flask, render_template_string, request, redirect
import requests
import os

# --- Uygulama Yapılandırması ---
app = Flask(__name__)
API_URL = os.getenv("API_URL", "https://cloud3-d9ds.onrender.com")

# --- HTML Şablonu (DÜZELTİLMİŞ) ---
HTML_SABLONU = """
<!doctype html>
<html>
<head>
<title>Mikro Hizmetli Selam!</title>
<style>
body { font-family: Arial; text-align: center; padding: 50px; background: #eef2f3; }
h1 { color: #333; }
input { padding: 10px; font-size: 16px; margin: 5px; }
button { padding: 10px 15px; background: #4CAF50; color: white; border: none; border-radius: 6px; cursor: pointer; }
li { background: white; margin: 5px auto; width: 250px; padding: 8px; border-radius: 5px; list-style: none; }
</style>
</head>
<body>
<h1>Mikro Hizmetli Selam!</h1>
<p>Adınızı ve şehrinizi yazın</p>

<form method="POST">
    <input type="text" name="isim" placeholder="Adınızı yazın" required>
    
    <input type="text" name="sehir" placeholder="Şehrinizi yazın" required>
    
    <button type="submit">Gönder</button>
</form>

<hr>
<h3>Ziyaretçiler:</h3>
<ul>
{% for ad in isimler %}
<li>{{ ad }}</li>
{% endfor %}
</ul>
</body>
</html>
"""

# --- Rota Tanımlaması (DÜZELTİLMİŞ) ---

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # Formdan veriler (küçük harfle) alınıyor
        isim = request.form.get("isim")
        
        # HATA 2 DÜZELTİLDİ: 'request.form' kullanıldı ve değişken adı 'sehir' oldu
        sehir = request.form.get("sehir") 
        
        # Hem isim hem de şehir varsa API'ye gönder
        if isim and sehir:
            # HATA 3 DÜZELTİLDİ: API'ye hem 'isim' hem de 'sehir' JSON olarak gönderiliyor
            payload = {
                "isim": isim,
                "sehir": sehir  # API'nizin beklediği anahtar (key) 'sehir' olmalı
            }
            try:
                # Arka uçtaki "/ziyaretciler" rotasına POST isteği gönderir
                requests.post(API_URL + "/ziyaretciler", json=payload)
            except requests.exceptions.RequestException as e:
                print(f"API'ye POST isteği gönderilemedi: {e}")
                # Kullanıcıya hata göstermek de iyi bir fikir olabilir
                
        # Başarılı veya başarısız (şimdilik) her durumda ana sayfaya yönlendir
        return redirect("/")

    # --- GET isteği: Ziyaretçi listesini çeker ---
    try:
        resp = requests.get(API_URL + "/ziyaretciler")
        isimler = resp.json() if resp.status_code == 200 else []
    except requests.exceptions.RequestException:
        isimler = ["Bağlantı hatası: Arka uç API'sine ulaşılamadı."]
        
    return render_template_string(HTML_SABLONU, isimler=isimler)

# --- Uygulama Başlatma ---

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
