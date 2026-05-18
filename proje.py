import sqlite3

def dosya_yaz(mesaj):
    dosya=open("hastane.txt","a")
    dosya.write(mesaj+"\n")
    dosya.close()

def veritabani_kur():
    vt=sqlite3.connect("hastane.vt")
    imlec=vt.cursor()
    imlec.execute("""CREATE TABLE IF NOT EXISTS randevu 
                     (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                      hasta_ad TEXT,tc TEXT,yas INTEGER,bolum TEXT)""")
    vt.commit()
    vt.close()

def yeni_randevu_al():
    ad=input("Hasta Ad Soyad:")
    tc=input("TC No:")
    yas=input("Yaş:")
    bolum=input("Poliklinik:")
    vt=sqlite3.connect("hastane.vt")
    imlec=vt.cursor()
    imlec.execute("INSERT INTO randevu (hasta_ad,tc,yas,bolum) VALUES (?,?,?,?)",(ad,tc,yas,bolum))
    vt.commit()
    vt.close()
    dosya_yaz("Yeni kayıt alındı")
    print("Kayıt başarıyla tamamlandı.")

def rapor_listele(kullanici_yetkisi):
    if kullanici_yetkisi=="Yönetici":
        vt=sqlite3.connect("hastane.vt")
        imlec=vt.cursor()
        imlec.execute("SELECT * FROM randevu")
        kayitlar=imlec.fetchall()
        print("GÜNCEL LİSTE")
        for satir in kayitlar:
            print("Hasta:",satir[1]," Bölüm:",satir[4])
        vt.close()
    else:
        print("Bu listeyi görme yetkiniz yok!")

veritabani_kur()
dosya_yaz("Sistem Girişi Yapıldı.")
yetkiler={
    "admin": {"sifre": "123", "rol": "Yönetici"},
    "doktor": {"sifre": "456", "rol": "Doktor"}
    }
print("Hastane Randevu Sistemi")
kullanici=input("Kullanıcı Adı:")
sifre=input("Şifre:")
if kullanici in yetkiler and yetkiler[kullanici]["sifre"]==sifre:
    rol=yetkiler[kullanici]["rol"]
    print("Hoş geldiniz\n")
    while True:
        print("1.Randevu Oluştur")
        print("2.Hasta Listesi ve Analiz (Yönetici)")
        print("3.Çıkış")
        secim=input("İşlem seçiniz:")
        if secim=="1":
            yeni_randevu_al()
        elif secim=="2":
            rapor_listele(rol)
        elif secim=="3":
            dosya_yaz("Sistem Kapatıldı.")
            break
        else:
            print("Yanlış giriş!")
else:
    print("Giriş bilgileri hatalı.")
