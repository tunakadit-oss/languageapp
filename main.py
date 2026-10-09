# =====================================================================
# 🎮 PROJE: "DOĞRU KONUŞ" - SESLİ TELAFFUZ OYUNU
# =====================================================================
# Oyun nasıl çalışıyor?
#   1. Ekranda Türkçe bir kelime çıkıyor.
#   2. Sen o kelimenin İNGİLİZCESİNİ mikrofona söylüyorsun.
#   3. Program sesini yazıya çeviriyor ve doğru mu diye kontrol ediyor.
#   4. Doğruysa +1 puan, yanlışsa hata. 3 hatada oyun biter!
#
# NASIL ÇALIŞACAKSIN?
#   - Aşağıda "✏️ GÖREV" yazan yerleri bulup boşlukları dolduracaksın.
#   - Kodunu yazdıktan sonra o satırdaki "pass" kelimesini SİL.
#   - Her görevden sonra programı çalıştırıp test et!
#
# 📦 Gerekli kütüphaneler (terminale yaz):
#   pip install sounddevice scipy numpy SpeechRecognition googletrans==4.0.0-rc1
# =====================================================================

try:
    import sounddevice as sd
    import scipy.io.wavfile as wav
    import speech_recognition as sr
    from googletrans import Translator
except ModuleNotFoundError:
    sd = None
    wav = None
    sr = None
    Translator = None

import random
import time


# === Ayarlamalar ===
# ✏️ GÖREV 1: Oyunun ayarlarını yap.
#   - sample_rate  -> ses kalitesi, 44100 yaz.
#   - duration     -> mikrofonun kaç saniye dinleyeceği, 4 yaz.
#   - max_errors   -> oyuncunun hakkı olan hata sayısı, 3 yaz.
#   - skor         -> oyuna 0 puanla başlıyoruz.
#   - errors       -> oyuna 0 hatayla başlıyoruz.
sample_rate = 44100
duration = 4
max_errors = 3 
skor = 0
errors = 0


# === Seviyelere göre kelimeler ===
# ✏️ GÖREV 2: Sözlüğü (dictionary) tamamla.
#   "kolay" seviyesi örnek olarak yazıldı. Sen de "orta" ve "zor"
#   seviyelerine 5'er kelime ekle. Zor kelimeler daha uzun olsun!
seviyelere_göre_kelimeler = {
    "kolay": ["kedi", "köpek", "elma", "süt", "güneş", "ev", "aile"],
    "orta": ["başarmak", "mevcut", "çevre", "sonuç", "seçenek", "gözlemlemek", "eşsiz"],
    "zor": ["bağımlılık", "terk etmek", "genişletmek", "uyum sağlamak", "suçlamak", "itiraf etmek"]
}


# === Araçların başlatılması ===
# ✏️ GÖREV 3: Programın araçlarını hazırla.
#   - recognizer -> sesi yazıya çeviren araç:  sr.Recognizer()
#   - translator -> Türkçeyi İngilizceye çeviren araç:  Translator()
recognizer = sr.Recognizer() if sr is not None else None
translator = Translator() if Translator is not None else None


# === Skora göre geri bildirim ===
def geri_bildirim(skor, toplam):
    # ✏️ GÖREV 4: Oyuncunun başarı oranını hesapla.
    #   İPUCU: oran = doğru sayısı BÖLÜ toplam kelime sayısı
    oran = skor / toplam if toplam else 0

    # ✏️ GÖREV 5: Orana göre farklı mesajlar döndür (return).
    if oran == 1:
        return "Mükemmel! Tüm kelimeleri doğru telaffuz ettin."
    elif oran >= 0.7:
        return "Çok iyi! Biraz daha pratikle harika olacak."
    elif oran >= 0.4:
        return "İyi gidiyorsun ancak biraz daha pratik yapmalısın."
    else:
        return "Üzülme, pratik yaptıkça gelişeceksin. Çalışmaya devam!"


def main():
    if sd is None or wav is None or sr is None or translator is None or recognizer is None:
        print("⚠️ Gerekli kütüphaneler eksik. Lütfen: pip install sounddevice scipy numpy SpeechRecognition googletrans==4.0.0-rc1")
        return

    # === Ana program ===
    print("🎮 'Doğru Konuş' oyununa hoş geldiniz!")

    # ✏️ GÖREV 6: Oyunun tekrar oynanmasını sağlayan döngüyü kur.
    #   - oyna değişkenine "e" değerini ver (e = evet).
    #   - while döngüsü, oyna değişkeni "e" olduğu sürece dönsün.
    oyna = "e"
    while oyna == "e":
        skor = 0
        errors = 0

        # === Zorluk seçimi ===
        print("\nZorluk seviyesini seçin: kolay / orta / zor")
        level = input(">>> ").strip().lower()

        # ✏️ GÖREV 7: Yanlış seviye yazılırsa tekrar sor.
        #   Kullanıcının yazdığı "level" sözlükte YOKSA:
        #     - "❗ Seviye bulunamadı. Tekrar deneyin." yazdır
        #     - tekrar input al
        #   İPUCU: while level not in seviyelere_göre_kelimeler:
        while level not in seviyelere_göre_kelimeler:
            print("❗ Seviye bulunamadı. Tekrar deneyin.")
            level = input(">>> ").strip().lower()

        # ✏️ GÖREV 8: Seçilen seviyenin kelimelerini hazırla.
        #   - kelime_list  -> sözlükten seçilen seviyenin listesini al: [:] ile kopyala
        #   - kelimeleri karıştır (random.shuffle) ki her oyun farklı olsun
        #   - toplam_kelime -> listede kaç kelime var? (len kullan)
        kelime_list = seviyelere_göre_kelimeler[level][:]
        random.shuffle(kelime_list)
        toplam_kelime = len(kelime_list)

        print(f"\n🟢 Zorluk seviyesi: {level.capitalize()}")
        print("🧠 Türkçe bir kelime göreceksiniz. İngilizce çevirisini telaffuz etmeye çalışın.")
        time.sleep(2)

        # === Ana oyun döngüsü ===
        # ✏️ GÖREV 9: Listedeki her kelime için sırayla dön.
        #   İPUCU: for kelime in kelime_list:
        for kelime in kelime_list:
            print(f"\n📣 Kelime: {kelime}")

            # 🎙 Konuşma kaydı
            print("🎙 Şimdi konuşun...")
            recording = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=1, dtype="int16")
            sd.wait()
            wav.write("output.wav", sample_rate, recording)
            print("✅ Kayıt tamamlandı, tanımlanıyor...")

            try:
                with sr.AudioFile("output.wav") as source:
                    audio = recognizer.record(source)

                # ✏️ GÖREV 10: Kaydedilen sesi İngilizce yazıya çevir.
                #   İPUCU: recognizer.recognize_google(audio, language="en").lower()
                tanimlanan = recognizer.recognize_google(audio, language="en").lower()
                print("📝 Şunu söylediniz:", tanimlanan)

                # ✏️ GÖREV 11: Türkçe kelimenin İngilizce karşılığını bul.
                #   İPUCU: translator.translate(kelime, src="tr", dest="en").text.lower()
                ceviri = translator.translate(kelime, src="tr", dest="en").text.lower()
                print("🔤 Çeviri:", ceviri)

                # Cevabı karşılaştırma (söylenenin içinde çeviri geçiyorsa doğru say)
                # ✏️ GÖREV 12: Cevabı kontrol et.
                #   EĞER ceviri, tanimlanan'ın içinde geçiyorsa VEYA tersi doğruysa:
                #     - skor'u 1 artır
                #     - "✅ Doğru! +1 puan" yazdır
                #   DEĞİLSE:
                #     - errors'u 1 artır
                #     - şunu yazdır:
                #       f"❌ Tam olarak değil. Beklenen: {ceviri}. Hatalar: {errors}/{max_errors}"
                #   İPUCU: if ceviri in tanimlanan or tanimlanan in ceviri:
                if ceviri in tanimlanan or tanimlanan in ceviri:
                    skor += 1
                    print("✅ Doğru! +1 puan")
                else:
                    errors += 1
                    print(f"❌ Tam olarak değil. Beklenen: {ceviri}. Hatalar: {errors}/{max_errors}")

                # ✏️ GÖREV 13: Hata sayısı max_errors'a ulaştıysa oyunu bitir.
                #   - "\n💀 Oyun bitti. 3 hata yaptın." yazdır
                #   - döngüden çık (break)
                if errors >= max_errors:
                    print("\n💀 Oyun bitti. 3 hata yaptın.")
                    break

            except sr.UnknownValueError:
                # ✏️ GÖREV 14: Ses hiç anlaşılmadıysa ne olacak?
                #   - errors'u 1 artır
                #   - f"😕 Konuşma tanınamadı. Hatalar: {errors}/{max_errors}" yazdır
                #   - hata sayısı dolduysa "\n💀 Oyun bitti. 3 hata yaptın." yazdır ve break yap
                errors += 1
                print(f"😕 Konuşma tanınamadı. Hatalar: {errors}/{max_errors}")
                if errors >= max_errors:
                    print("\n💀 Oyun bitti. 3 hata yaptın.")
                    break

            except sr.RequestError as e:
                print(f"❗ Hizmet hatası: {e}")
                break

        # === Sonuçlar ===
        # ✏️ GÖREV 15: Oyun bitince sonuçları göster.
        #   - f"\n🏁 Oyun bitti! Puanınız: {skor}/{toplam_kelime}" yazdır
        #   - geri_bildirim fonksiyonunu skor ve toplam_kelime ile çağırıp sonucunu yazdır
        print(f"\n🏁 Oyun bitti! Puanınız: {skor}/{toplam_kelime}")
        print(geri_bildirim(skor, toplam_kelime))

        # ✏️ GÖREV 16: Tekrar oynamak isteyip istemediğini sor.
        #   - "\nTekrar oynamak ister misiniz? (e/h)" yazdır
        #   - cevabı oyna değişkenine kaydet
        #   İPUCU: input(">>> ").strip().lower()
        print("\nTekrar oynamak ister misiniz? (e/h)")
        oyna = input(">>> ").strip().lower()

    print("\n👋 Oynadığınız için teşekkürler, görüşmek üzere!")


if __name__ == "__main__":
    main()


# =====================================================================
# 🌟 BİTİRDİN Mİ? EKSTRA GÖREVLER (isteyenler için)
# =====================================================================
# 1. Sözlüğe "çok zor" diye 4. bir seviye ekle.
# 2. Her doğru cevapta 1 yerine 2 puan ver.
# 3. Oyuncunun adını başta sorup mesajlarda kullan.
# 4. En yüksek skoru bir değişkende tutup oyun sonunda "Rekor: ..." yazdır.
# =====================================================================
