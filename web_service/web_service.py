from flask import Flask, render_template_string, request, redirect
import requests
import os # Bu kütüphaneyi ortam değişkeni kullanımı için ekledim (API_URL'i env'den almak için pratik)

# --- Uygulama Yapılandırması ---

app = Flask(__name__)

# Arka uç (backend) mikro hizmetinin adresi. 
# Genellikle ortam değişkenlerinden (environment variables) alınması önerilir.
API_URL = os.getenv("API_URL", "https://cloud3-d9ds.onrender.com")

# --- HTML Şablonu (Front-End Görünümü) ---

HTML_SABLONU = """
<!doctype html>
<html>
<head>
<title>Mikro Hizmetli Selam!</title>
<style>
body { font-family: Arial; text-align: center; padding: 50px; background: #eef2f3; }
h1 { color: #333; }
input { padding: 10px; font-size: 16px; }
button { padding: 10px 15px; background: #4CAF50; color: white; border: none; border-radius: 6px; cursor: pointer; }
li { background: white; margin: 5px auto; width: 200px; padding: 8px; border-radius: 5px; list-style: none; } /* list-style: none ekledim */
</style>
</head>
<body>
<h1>Mikro Hizmetli Selam!</h1>
<p>Adını yaz</p>
<p>ŞEHİR yaz</p>
<form method="POST">
<input type="text" name="isim" placeholder="Adını yaz" required>
<input type="text" name="ŞEHİR" placeholder="ŞEHİR yaz" required>
<button type="submit">Gönder</button>
</form>
<h3>Ziyaretçiler:</h3>
<ul>
{% for ad in isimler %}
<li>{{ ad }}</li>
{% endfor %}
</ul>
</body>
</html>
"""

# --- Rota Tanımlaması ---

@app.route("/", methods=["GET", "POST"])
def index():
    """
    POST: Ziyaretçi adını arka uca (API_URL) gönderir ve ana sayfaya yönlendirir.
    GET: Arka uçtan (API_URL) ziyaretçi listesini çeker ve HTML şablonunu gösterir.
    """
    if request.method == "POST":
        isim = request.form.get("isim")
        # Arka uçtaki "/ziyaretciler" rotasına POST isteği gönderir
        if isim:
            requests.post(API_URL + "/ziyaretciler", json={"isim": isim})
        return redirect("/")

    # GET isteği: Ziyaretçi listesini çeker
    try:
        resp = requests.get(API_URL + "/ziyaretciler")
        # Eğer istek başarılıysa (200), JSON verisini alır. Başarısızsa boş liste kullanır.
        isimler = resp.json() if resp.status_code == 200 else []
    except requests.exceptions.RequestException:
        # İstek sırasında bir hata oluşursa (örneğin, bağlantı hatası)
        isimler = ["Bağlantı hatası: Arka uç API'sine ulaşılamadı."]
        
    return render_template_string(HTML_SABLONU, isimler=isimler)

# --- Uygulama Başlatma ---

if __name__ == "__main__":
    # Uygulamayı 5000 portunda tüm arayüzlerde çalıştırır
    app.run(host="0.0.0.0", port=5000)
