from collections import deque
import random
import tkinter as tk
from tkinter import messagebox
import customtkinter as ctk

# CustomTkinter genel tema ayarları
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")


class AdamAsmacaApp:

  def __init__(self, root):
    self.root = root
    self.root.title("Modern Türkçe Adam Asmaca")
    self.root.geometry("650x780")
    self.root.resizable(False, False)

    # Genel Skor ve Seri Değişkenleri
    self.toplam_puan = 0
    self.galibiyet_serisi = 0

    # Türkçe karakterler içeren kelime havuzu (Doğrudan büyük harfle tanımlıyoruz)
    self.kelimeler = [
    # 3 Harfli
    "ADA", "ÇAY", "DAĞ",
    "DERE", "GÖL", "KAR",
    "KUM", "TAŞ", "VADİ", "YOL",
    # 4 Harfli 
    "AKIL", "BALIK", "BİBER", "BULUT",
    "ÇAYIR", "DOLU", "DOSYA", "EKRAN",
    "ELMA", "HAVA", "KAPI", "KEDİ",
    "MASA", "MUZ", "RUH", "SAAT",
    "ŞANS", "TAVUK", "UYDU", "ÖLÜM",
    "BARDAK", "TABAK"
    # 5 Harfli
    "ARMUT", "AYRAN", "AZİM", "ÇORAP",
    "ÇORBA", "DENİZ", "DOLAP", "FIRÇA",
    "GÜNEŞ", "GÜVEN", "GURUR", "HALI",
    "HAYAT", "KADER", "KALEM", "KAVUN",
    "KİTAP", "KORKU", "LAMBA", "MEYVE",
    "NEHİR", "PERDE", "PİKSEL", "ROBOT",
    "SABUN", "SEBZE", "SEVGİ", "ŞİFRE",
    "TARAK", "TOPRAK", "TREN", "UMUT",
    "UZAY", "YATAK", "ZAMAN",
    # 6 Harfli
    "ADALET", "ANALİZ",
    "ARABA", "BELLEK",
    "BİLGİ", "ÇEKMECE",
    "ÇİÇEK", "ÇİLEK",
    "DEPREM", "DOST",
    "DOSTLUK", "ENERJİ",
    "FİZİK", "GALAKSİ",
    "GEZEGEN", "HAVLU",
    "HÜZÜN", "KAHVE",
    "KARPUZ", "KİMYA",
    "KLASÖR", "KLAVYE",
    "MAVİ", "MANTIK",
    "MERAK", "MİMARİ",
    "ORMAN", "ÖZGÜRLÜK",
    "PATATES", "PEYNİR",
    "PİRİNÇ", "SADAKAT",
    "SALATA", "SARIMSAK",
    "ŞELALE", "ŞİMŞEK",
    "SİNYAL", "SOĞAN",
    "VOLKAN", "YAĞMUR",
    "YAPRAK", "YILDIZ",
    "ZEYTİN",
    # 7 Harfli
    "BAŞARI",
    "BİYOLOJİ",
    "ÇİKOLATA",
    "DONANIM",
    "FIRTINA",
    "İNOVASYON",
    "İŞLEMCİ",
    "KÜTÜPHANE",
    "LİMONATA",
    "MAKARNA",
    "MATEMATİK",
    "MUTLULUK",
    "PENCERE",
    "PİYANO",
    "RÜZGAR",
    "SABIR",
    "ŞEMSİYE",
    "TEKNOLOJİ",
    "UÇAK",
    "YAZILIM",
    # 8 ve Daha Uzun Harfli Kelimeler
    "ALGORİTMA",
    "BİSİKLET",
    "DOMATES",
    "DÜŞÜNCE",
    "GEMİ",
    "GÖKKUŞAĞI",
    "GÜVENLİK",
    "HEYECAN",
    "İLETİŞİM",
    "İNTERNET",
    "KAVUN",
    "KELİME",
    "LAHMACUN",
    "LİMON",
    "MENEMEN",
    "MERDİVEN",
    "MOTOSİKLET",
    "MÜHENDİSLİK",
    "OTOBÜS",
    "PORTAKAL",
    "PROGRAMLAMA",
    "SANDALYE",
    "TELEFON",
    "TELEVİZYON",
    "VERİ",
    "VERİTABANI",
    "BİLGİSAYAR",
    "LABORATUVAR",
    "SALATALIK",
]


    # Son çıkan kelimeleri saklayacak kuyruk (Maksimum 25 kelime)
    self.son_cikanlar = deque(maxlen=25)

    self.yeni_oyun_kur()
    self.arayuz_olustur()

    # Fiziksel Klavye Bağlantısı
    self.root.bind("<Key>", self.klavye_tus_yakala)

  def turkce_buyuk_yap(self, metin):
    return (
        metin.replace("i", "İ")
        .replace("ı", "I")
        .replace("ş", "Ş")
        .replace("ğ", "Ğ")
        .replace("ü", "Ü")
        .replace("ö", "Ö")
        .replace("ç", "Ç")
        .upper()
    )

  def yeni_oyun_kur(self):
    # Son 25 oyunda çıkmayan kelimeleri filtrele
    musait_kelimeler = [
        k for k in self.kelimeler if k not in self.son_cikanlar
    ]

    # Eğer tüm kelimeler tükendiyse (veya liste çok küçükse) havuzu sıfırla
    if not musait_kelimeler:
      self.son_cikanlar.clear()
      musait_kelimeler = self.kelimeler

    self.secilen_kelime = random.choice(musait_kelimeler)

    # Seçilen kelimeyi son çıkanlar listesine ekle (en fazla 25 tutulur)
    self.son_cikanlar.append(self.secilen_kelime)

    self.kalan_hak = 6
    self.tahmin_durumu = ["_"] * len(self.secilen_kelime)
    self.denenen_harfler = set()

  def arayuz_olustur(self):
    # --- ÜST SKOR VE SERİ PANELI ---
    self.stats_frame = ctk.CTkFrame(self.root, fg_color="transparent")
    self.stats_frame.pack(pady=10, fill="x", padx=30)

    self.puan_label = ctk.CTkLabel(
        self.stats_frame,
        text=f"Puan: {self.toplam_puan}",
        font=ctk.CTkFont(family="Helvetica", size=14, weight="bold"),
        text_color="#2ecc71",
    )
    self.puan_label.pack(side="left")

    self.seri_label = ctk.CTkLabel(
        self.stats_frame,
        text=f"Seri 🔥: {self.galibiyet_serisi}",
        font=ctk.CTkFont(family="Helvetica", size=14, weight="bold"),
        text_color="#e67e22",
    )
    self.seri_label.pack(side="right")

    # --- BAŞLIK ---
    self.baslik_label = ctk.CTkLabel(
        self.root,
        text="🎮 TÜRKÇE ADAM ASMACA",
        font=ctk.CTkFont(family="Helvetica", size=20, weight="bold"),
    )
    self.baslik_label.pack(pady=5)

    # --- CANVAS (ÇİZİM) ---
    self.canvas = tk.Canvas(
        self.root,
        width=250,
        height=180,
        bg="#242424",
        highlightthickness=0,
    )
    self.canvas.pack(pady=5)
    self.daragaci_ciz()

    # --- KELİME GÖSTERGESİ ---
    self.kelime_label = ctk.CTkLabel(
        self.root,
        text=" ".join(self.tahmin_durumu),
        font=ctk.CTkFont(family="Courier", size=26, weight="bold"),
        text_color="#f1c40f",
    )
    self.kelime_label.pack(pady=10)

    # --- DURUM / KALAN HAK ---
    self.durum_label = ctk.CTkLabel(
        self.root,
        text=f"Kalan Hak: {self.kalan_hak}",
        font=ctk.CTkFont(family="Helvetica", size=14),
        text_color="#bdc3c7",
    )
    self.durum_label.pack(pady=2)

    # --- HARF BUTONLARI (KLAVYE) ---
    self.klavye_frame = ctk.CTkFrame(self.root, fg_color="transparent")
    self.klavye_frame.pack(pady=5)

    self.butonlar = {}
    alfabe = "ABCÇDEFGĞHIİJKLMNOÖPRSŞTUÜVYZ"

    row = 0
    col = 0
    for harf in alfabe:
      btn = ctk.CTkButton(
          self.klavye_frame,
          text=harf,
          width=45,
          height=38,
          font=ctk.CTkFont(family="Helvetica", size=12, weight="bold"),
          fg_color="#1f538d",
          hover_color="#14375e",
          command=lambda h=harf: self.harf_tahmin_et(h),
      )
      btn.grid(row=row, column=col, padx=3, pady=3)
      self.butonlar[harf] = btn

      col += 1
      if col > 7:
        col = 0
        row += 1

    # --- ALT KONTROL BUTONLARI ---
    self.alt_buton_frame = ctk.CTkFrame(self.root, fg_color="transparent")
    self.alt_buton_frame.pack(pady=10)

    self.ipucu_btn = ctk.CTkButton(
        self.alt_buton_frame,
        text="💡 İpucu Al (-1 Hak)",
        font=ctk.CTkFont(family="Helvetica", size=12, weight="bold"),
        fg_color="#8e44ad",
        hover_color="#6c3483",
        width=140,
        command=self.ipucu_ver,
    )
    self.ipucu_btn.pack(side="left", padx=5)

    self.yeniden_btn = ctk.CTkButton(
        self.alt_buton_frame,
        text="🔄 Yeni Oyun",
        font=ctk.CTkFont(family="Helvetica", size=12, weight="bold"),
        fg_color="#d35400",
        hover_color="#a04000",
        width=140,
        command=self.oyunu_sifirla,
    )
    self.yeniden_btn.pack(side="right", padx=5)

  def daragaci_ciz(self):
    self.canvas.delete("all")
    self.canvas.create_line(20, 160, 180, 160, width=4, fill="#a6a6a6")
    self.canvas.create_line(60, 160, 60, 20, width=4, fill="#a6a6a6")
    self.canvas.create_line(60, 20, 140, 20, width=4, fill="#a6a6a6")
    self.canvas.create_line(140, 20, 140, 40, width=3, fill="#7f8c8d")

  def adam_parcasi_ciz(self):
    hak = self.kalan_hak
    if hak == 5:
      self.canvas.create_oval(125, 40, 155, 70, width=3, outline="#e74c3c")
    elif hak == 4:
      self.canvas.create_line(140, 70, 140, 110, width=3, fill="#e74c3c")
    elif hak == 3:
      self.canvas.create_line(140, 80, 115, 95, width=3, fill="#e74c3c")
    elif hak == 2:
      self.canvas.create_line(140, 80, 165, 95, width=3, fill="#e74c3c")
    elif hak == 1:
      self.canvas.create_line(140, 110, 115, 140, width=3, fill="#e74c3c")
    elif hak == 0:
      self.canvas.create_line(140, 110, 165, 140, width=3, fill="#e74c3c")

  def klavye_tus_yakala(self, event):
    tus = self.turkce_buyuk_yap(event.char)
    if tus in self.butonlar and self.butonlar[tus].cget("state") != "disabled":
      self.harf_tahmin_et(tus)

  def ipucu_ver(self):
    gizli_indeksler = [i for i, h in enumerate(self.tahmin_durumu) if h == "_"]
    if not gizli_indeksler:
      return

    if self.kalan_hak <= 1:
      messagebox.showwarning(
          "Uyarı", "İpucu almak için yeterli hakkınız kalmadı!"
      )
      return

    secilen_idx = random.choice(gizli_indeksler)
    harf = self.secilen_kelime[secilen_idx]

    for i, h in enumerate(self.secilen_kelime):
      if h == harf:
        self.tahmin_durumu[i] = h
        if (
            harf in self.butonlar
            and self.butonlar[harf].cget("state") != "disabled"
        ):
          self.denenen_harfler.add(harf)
          self.butonlar[harf].configure(
              state="disabled", fg_color="#555555", text_color="#aaaaaa"
          )

    self.kelime_label.configure(text=" ".join(self.tahmin_durumu))
    self.kalan_hak -= 1
    self.durum_label.configure(text=f"Kalan Hak: {self.kalan_hak}")
    self.adam_parcasi_ciz()

    if self.kalan_hak == 0:
      self.galibiyet_serisi = 0
      self.seri_label.configure(text=f"Seri 🔥: {self.galibiyet_serisi}")
      messagebox.showerror(
          "Oyun Bitti",
          f"İpucu kullanırken hakkınız tükendi!\nDoğru Kelime:"
          f" {self.secilen_kelime}",
      )
      self.butonlari_kilitle()
      return

    if "_" not in self.tahmin_durumu:
      kazanc = (self.kalan_hak + 1) * 10 + len(self.secilen_kelime) * 5
      self.toplam_puan += kazanc
      self.galibiyet_serisi += 1
      self.puan_label.configure(text=f"Puan: {self.toplam_puan}")
      self.seri_label.configure(text=f"Seri 🔥: {self.galibiyet_serisi}")
      messagebox.showinfo(
          "Tebrikler!",
          f"Kazandınız! Kelime: {self.secilen_kelime}\nKazanılan Puan:"
          f" {kazanc}",
      )
      self.butonlari_kilitle()

  def harf_tahmin_et(self, harf):
    if harf in self.denenen_harfler:
      return

    self.denenen_harfler.add(harf)
    self.butonlar[harf].configure(
        state="disabled", fg_color="#555555", text_color="#aaaaaa"
    )

    if harf in self.secilen_kelime:
      for i, h in enumerate(self.secilen_kelime):
        if h == harf:
          self.tahmin_durumu[i] = harf

      self.kelime_label.configure(text=" ".join(self.tahmin_durumu))

      if "_" not in self.tahmin_durumu:
        kazanc = self.kalan_hak * 10 + len(self.secilen_kelime) * 5
        self.toplam_puan += kazanc
        self.galibiyet_serisi += 1

        self.puan_label.configure(text=f"Puan: {self.toplam_puan}")
        self.seri_label.configure(text=f"Seri 🔥: {self.galibiyet_serisi}")

        messagebox.showinfo(
            "Tebrikler!",
            f"Kazandınız! Kelime: {self.secilen_kelime}\nKazanılan Puan:"
            f" {kazanc}",
        )
        self.butonlari_kilitle()
    else:
      self.kalan_hak -= 1
      self.durum_label.configure(text=f"Kalan Hak: {self.kalan_hak}")
      self.adam_parcasi_ciz()

      if self.kalan_hak == 0:
        self.galibiyet_serisi = 0
        self.seri_label.configure(text=f"Seri 🔥: {self.galibiyet_serisi}")
        messagebox.showerror(
            "Oyun Bitti",
            f"Hakkınız tükendi!\nDoğru Kelime: {self.secilen_kelime}",
        )
        self.butonlari_kilitle()

  def butonlari_kilitle(self):
    for btn in self.butonlar.values():
      btn.configure(state="disabled")

  def oyunu_sifirla(self):
    self.yeni_oyun_kur()
    self.daragaci_ciz()
    self.kelime_label.configure(text=" ".join(self.tahmin_durumu))
    self.durum_label.configure(text=f"Kalan Hak: {self.kalan_hak}")

    for harf, btn in self.butonlar.items():
      btn.configure(state="normal", fg_color="#1f538d", text_color="white")


if __name__ == "__main__":
  root = ctk.CTk()
  app = AdamAsmacaApp(root)
  root.mainloop()