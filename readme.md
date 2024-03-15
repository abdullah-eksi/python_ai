# Python İle Gemini Altyapısı İle Yapay Zeka Oluşturma


# AeXp AI

AeXp AI, kullanıcıların sorularına cevap veren bir yapay zeka uygulamasıdır. Bu uygulama, tanımlı sorulara önceden belirlenmiş cevaplar verir ve ayrıca Google Gemini AI API'sini kullanarak kullanıcıların diğer sorularına cevaplar üretebilir.

## Kullanım

1. **AeXp AI'ı Başlatma:**
   - `main.py` dosyasını çalıştırarak AeXp AI uygulamasını başlatabilirsiniz.

2. **Soru Sorma:**
   - Soru veya mesajınızı girmek için komut istemine istenen soruyu yazın ve ENTER tuşuna basın.

3. **Cevapları Kontrol Etme:**
   - AeXp AI, sorunuza cevap verdiğinde, cevabı komut istemine yazdıracaktır. Ayrıca, cevaplar `aexp_ai_answer` klasöründe dosyalar halinde kaydedilir.

4. **Yardım Alma:**
   - Yardım almak için `aexp help` komutunu kullanabilirsiniz. Bu komut size AeXp AI'nın kullanımı hakkında kısa bir kılavuz sağlar.

5. **Çıkış Yapma:**
   - Çıkış yapmak için `aexp logout` veya `logout` komutunu kullanabilirsiniz.

## Dosya Yapısı

- **main.py:** AeXp AI uygulamasını çalıştırmak için ana Python betiği.
- **defined_answer.json:** Tanımlı soruların ve cevaplarının bulunduğu JSON dosyası.
- **aexp_ai_answer:** Kullanıcının sorduğu sorulara verilen cevapların kaydedildiği klasör Masaüstünüzde Otomatik Oluşcaktır.

## Gereksinimler

- Python 3.x
- requests kütüphanesi
- difflib kütüphanesi


