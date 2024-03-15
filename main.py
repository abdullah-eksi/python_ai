import json  # JSON veri işleme için gerekli kütüphane
import requests  # API istekleri için gerekli kütüphane
from difflib import get_close_matches  # Yakın eşleşmeleri bulmak için difflib kütüphanesinden get_close_matches fonksiyonu
import os  # İşletim sistemi işlemleri için gerekli kütüphane

# Gemini AI'dan cevap almak için Fonksiyon
def get_gemini_ai_answer(soru):
    API_KEY = ""  # API Key
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.0-pro:generateContent?key={API_KEY}"  # API isteği için URL

    # API isteği için gereken veri yapısı
    data = {
        "contents": [
            {
                "role": "user",
                "parts": [
                    {
                        "text": soru  # Kullanıcı tarafından girilen metin
                    }
                ]
            }
        ],
        "generationConfig": {
            "temperature": 0.9,
            "topK": 1,
            "topP": 1,
            "maxOutputTokens": 2048,
            "stopSequences": []
        },
        "safetySettings": [
            {
                "category": "HARM_CATEGORY_HARASSMENT",
                "threshold": "BLOCK_MEDIUM_AND_ABOVE"
            },
            {
                "category": "HARM_CATEGORY_HATE_SPEECH",
                "threshold": "BLOCK_MEDIUM_AND_ABOVE"
            },
            {
                "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
                "threshold": "BLOCK_MEDIUM_AND_ABOVE"
            },
            {
                "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
                "threshold": "BLOCK_MEDIUM_AND_ABOVE"
            }
        ]
    }

    # API isteği gönderme
    response = requests.post(url, json=data)
    if response.status_code == 200:
        return response.json()  # API'dan gelen cevabı JSON formatında döndür
    else:
        return None #bir yanıt alamazsa none döndür

# Tanımlı soruları yüklemek için işlev
def tanimli_soru_yukle(file_path):
    with open(file_path, 'r', encoding='utf-8') as file: # Dizinden JSON  dosyasını oku ve file olarak ata
        data = json.load(file) #yüklenen  verileri data adlı değişkene ata
    # JSON veri yapısından soruları çıkarıp bir sözlüğe dönüştürme
    return {list(item.keys())[0]: list(item.values())[0] for item in data["sorular"]}

# Cevapları dosyaya kaydetmek için işlev
def cevapi_kaydet(dosya_adi, cevap):
    desktop_path = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')  # Kullanıcının masaüstü yolunu bulma
    klasor_yolu = os.path.join(desktop_path, "aexp_ai_answer")  # Yeni klasör yolu oluşturma
    dosya_yolu = os.path.join(klasor_yolu, dosya_adi + ".txt") # dosya yolunu olusturma

    # Eğer "aexp_ai_answer" klasörü yoksa oluşturma
    if not os.path.exists(klasor_yolu):  #klasor yolunu kontrol etme
        os.makedirs(klasor_yolu) #eger yoksa klasor yolunu olusturma

    # Dosyayı açma 
    with open(dosya_yolu, "a") as f:
        f.write(cevap + "\n")  # Cevabı dosyaya yazma
    print(f"{dosya_adi}.txt dosyasına cevap kaydedildi.")
    return dosya_yolu

# sorulara cevap verme işlevi
def oto_cevap(params, message):
    tanimli_sorular = tanimli_soru_yukle("defined_answer.json")  # Tanımlı soruları yükle

    text = message['text'].lower().strip()  # Gelen mesajı küçük harflere çevirme ve boşlukları temizleme
    best_match = get_close_matches(text, tanimli_sorular.keys(), n=1, cutoff=0.7)  # En yakın eşleşmeyi bulma

    if best_match:
        return tanimli_sorular[best_match[0]]  # En yakın eşleşme varsa tanımlı cevabı döndürme
    else:
        # Yapay zeka yanıtı al
        ai_response = get_gemini_ai_answer(text)
        response = ai_response["candidates"][0]["content"]["parts"][0]["text"] if ai_response else None

        if response:
            return response  # Yapay zeka yanıtını döndürme
        else:
            return "Üzgünüm, bu konuda bir bilgim yok."  # Yanıt yoksa hata mesajı döndürme

# Ana Fonksiyonumuz
def main():
    
    
    print("\n\n----------- AeXp Ai Hoşgeldiniz ------------\n\n")

    while True:
        user_input = input("Sorunuzu Giriniz  (Yardım İçin [ aexp help ] komutunu kullanınız): ")

        if  user_input.lower() == 'aexp logout' or user_input.lower() == 'logout' or user_input.lower() == 'Logout' : # Kullanıcı logout girerse uygulamadan çık
            print("Çıkış Yapılıyor ...")
            break
        elif user_input.lower() == 'aexp help' or user_input.lower() == 'help': # Kullanıcı aexp help girerse yardım mesajını göster
            print("\n AeXp Ai Kullanımı: \n")
            print(" - Soru veya mesajınızı girin.")
            print(" - Cevabı Bekleyiniz")
            print(" - Gelen Yanıtı Masaüstündeki aexp_ai_answer klasöründen ilgili konuya ait dosyadan kontrol edebilirsiniz ")
            print(" - Uygulamadan Çıkmak için Logout Komutunu Kullanınız \n")
           
            continue # Döngünün başına dön
        print("\nSorunuz cevaplandırılıyor...\n") 
        response = oto_cevap({}, {'text': user_input})  # Otomatik cevap alma
     
        print("\n İşte Sorunuzun Cevabı : ",response,"\n")  # Cevabı yazdırma

        if response:
            dosya_adi = user_input.replace(" ", "_")  # Dosya adını oluşturma
            dosya_yolu = cevapi_kaydet(dosya_adi, response)  # Cevabı dosyaya kaydetme
            print(f"\n \n Sevgili Kullanıcı Sorunuzun Cevabı {dosya_adi}.txt dosyasına kaydedildi. Dosyanın Kaydedildi Yer: {dosya_yolu}\n \n")



if __name__ == "__main__":
    main()  # Ana işlevi çağırma
