def zaman_hesaplayici():
    print("\n=== Zaman Hesaplama Uygulamasına Hoş Geldiniz! ===\n")
    toplam_saat = 24  # Kullanıcıya başlangıçta verilen toplam saat
    planlar = []  # Kullanıcının planlarını saklamak için bir liste

    while True:
        print("\nToplam Süre: 24 saat")
        print(f"Kalan Süreniz: {toplam_saat:.2f} saat\n")
        print("1. Yeni bir etkinlik ekle")
        print("2. Mevcut planları görüntüle")
        print("3. Bir etkinliği kaldır")
        print("4. Uygulamadan çık")
        
        try:
            secim = int(input("Seçiminizi yapın (1-4): "))
        except ValueError:
            print("Lütfen geçerli bir sayı girin!")
            continue

        if secim == 1:
            etkinlik = input("Etkinliğin adı: ")
            try:
                sure = float(input(f"{etkinlik} için ayıracağınız saat: "))
                if sure <= 0:
                    print("Saat negatif ya da sıfır olamaz!")
                    continue
                if sure > toplam_saat:
                    print(f"Kalan {toplam_saat:.2f} saatten fazla süre ayıramazsınız!")
                else:
                    planlar.append({"Etkinlik": etkinlik, "Süre": sure})
                    toplam_saat -= sure
                    print(f"'{etkinlik}' etkinliği için {sure:.2f} saat ayrıldı.")
            except ValueError:
                print("Lütfen geçerli bir saat değeri girin!")

        elif secim == 2:
            print("\n=== Mevcut Planlar ===")
            if not planlar:
                print("Hiçbir etkinlik planlanmamış.")
            else:
                for idx, plan in enumerate(planlar, 1):
                    print(f"{idx}. {plan['Etkinlik']} - {plan['Süre']:.2f} saat")

        elif secim == 3:
            if not planlar:
                print("Hiçbir etkinlik planlanmamış, silinecek bir şey yok.")
                continue

            try:
                print("\n=== Mevcut Planlar ===")
                for idx, plan in enumerate(planlar, 1):
                    print(f"{idx}. {plan['Etkinlik']} - {plan['Süre']:.2f} saat")
                silinecek = int(input("Silmek istediğiniz etkinliğin numarasını girin: "))
                if silinecek < 1 or silinecek > len(planlar):
                    print("Geçerli bir numara girin!")
                else:
                    silinen = planlar.pop(silinecek - 1)
                    toplam_saat += silinen["Süre"]
                    print(f"'{silinen['Etkinlik']}' etkinliği silindi ve {silinen['Süre']:.2f} saat geri eklendi.")
            except ValueError:
                print("Lütfen geçerli bir sayı girin!")

        elif secim == 4:
            print("Zaman Hesaplama Uygulamasından çıkılıyor. İyi günler!")
            break

        else:
            print("Lütfen 1 ile 4 arasında bir seçim yapın!")

# Uygulamayı başlat
zaman_hesaplayici()
