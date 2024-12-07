import sqlite3


def init_db():
    conn = sqlite3.connect("books.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS books (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            author TEXT NOT NULL,
            category TEXT,
            year INTEGER
        )
    """)
    conn.commit()
    return conn


def seed_data(conn):
    cursor = conn.cursor()
    books = [
        ("Savaş ve Barış", "Lev Tolstoy", "Roman", 1869),
        ("Suç ve Ceza", "Fyodor Dostoyevski", "Roman", 1866),
        ("Karamazov Kardeşler", "Fyodor Dostoyevski", "Roman", 1880),
        ("1984", "George Orwell", "Distopya", 1949),
        ("Hayvan Çiftliği", "George Orwell", "Distopya", 1945),
        ("Kürk Mantolu Madonna", "Sabahattin Ali", "Roman", 1943),
        ("İçimizdeki Şeytan", "Sabahattin Ali", "Roman", 1940),
        ("Yabancı", "Albert Camus", "Felsefi Roman", 1942),
        ("Mutlu Prens", "Oscar Wilde", "Hikaye", 1888),
        ("Bir İdam Mahkumunun Son Günü", "Victor Hugo", "Roman", 1829),
        ("Dönüşüm", "Franz Kafka", "Roman", 1915),
        ("Şeker Portakalı", "Jose Mauro de Vasconcelos", "Roman", 1968),
        ("Fareler ve İnsanlar", "John Steinbeck", "Roman", 1937),
        ("Gazap Üzümleri", "John Steinbeck", "Roman", 1939),
        ("Bülbülü Öldürmek", "Harper Lee", "Roman", 1960),
        ("Cesur Yeni Dünya", "Aldous Huxley", "Distopya", 1932),
        ("İnsan Neyle Yaşar?", "Lev Tolstoy", "Hikaye", 1885),
        ("Simyacı", "Paulo Coelho", "Roman", 1988),
        ("Uçurtma Avcısı", "Khaled Hosseini", "Roman", 2003),
        ("Satranç", "Stefan Zweig", "Roman", 1941),
    ]
    cursor.executemany("""
        INSERT INTO books (title, author, category, year) VALUES (?, ?, ?, ?)
    """, books)
    conn.commit()


def add_book(conn):
    title = input("Kitap Başlığı: ")
    author = input("Yazar: ")
    category = input("Kategori: ")
    year = int(input("Yıl: "))
    
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO books (title, author, category, year) VALUES (?, ?, ?, ?)
    """, (title, author, category, year))
    conn.commit()
    print(f"'{title}' kitabı başarıyla eklendi!")

def list_books(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM books")
    books = cursor.fetchall()
    if books:
        print("\n--- Tüm Kitaplar ---")
        for book in books:
            print(f"{book[0]}: {book[1]} - {book[2]} ({book[3]}, {book[4]})")
    else:
        print("Henüz bir kitap eklenmedi.")


def filter_books(conn):
    print("\nFiltreleme Seçenekleri:")
    print("1. Kategoriye Göre")
    print("2. Yazara Göre")
    print("3. Yıla Göre")
    choice = int(input("Seçiminiz: "))
    
    cursor = conn.cursor()
    if choice == 1:
        category = input("Kategori: ")
        cursor.execute("SELECT * FROM books WHERE category = ?", (category,))
    elif choice == 2:
        author = input("Yazar: ")
        cursor.execute("SELECT * FROM books WHERE author = ?", (author,))
    elif choice == 3:
        year = int(input("Yıl: "))
        cursor.execute("SELECT * FROM books WHERE year = ?", (year,))
    else:
        print("Geçersiz seçim!")
        return
    
    books = cursor.fetchall()
    if books:
        print("\n--- Filtrelenmiş Kitaplar ---")
        for book in books:
            print(f"{book[0]}: {book[1]} - {book[2]} ({book[3]}, {book[4]})")
    else:
        print("Hiçbir kitap bulunamadı.")


def update_book(conn):
    list_books(conn)
    book_id = int(input("Güncellemek istediğiniz kitabın ID'sini girin: "))
    
    title = input("Yeni Kitap Başlığı: ")
    author = input("Yeni Yazar: ")
    category = input("Yeni Kategori: ")
    year = int(input("Yeni Yıl: "))
    
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE books SET title = ?, author = ?, category = ?, year = ? WHERE id = ?
    """, (title, author, category, year, book_id))
    conn.commit()
    print(f"Kitap ID {book_id} başarıyla güncellendi!")


def delete_book(conn):
    list_books(conn)
    book_id = int(input("Silmek istediğiniz kitabın ID'sini girin: "))
    
    cursor = conn.cursor()
    cursor.execute("DELETE FROM books WHERE id = ?", (book_id,))
    conn.commit()
    print(f"Kitap ID {book_id} başarıyla silindi!")


def main():
    conn = init_db()
    seed_data(conn)
    print("Kitap Yönetim Sistemi Başlatıldı!")
    
    while True:
        print("\n--- Menü ---")
        print("1. Kitap Ekle")
        print("2. Tüm Kitapları Listele")
        print("3. Kitapları Filtrele")
        print("4. Kitap Güncelle")
        print("5. Kitap Sil")
        print("6. Çıkış")
        
        choice = int(input("Seçiminiz: "))
        if choice == 1:
            add_book(conn)
        elif choice == 2:
            list_books(conn)
        elif choice == 3:
            filter_books(conn)
        elif choice == 4:
            update_book(conn)
        elif choice == 5:
            delete_book(conn)
        elif choice == 6:
            print("Çıkış yapılıyor...")
            conn.close()
            break
        else:
            print("Geçersiz seçim!")

if __name__ == "__main__":
    main()
