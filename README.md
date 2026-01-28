# Oyun Kütüphanesi Backend

Bu proje, oyunların listelenebildiği, eklenebildiği, güncellenebildiği ve silinebildiği (CRUD) bir RESTful API servisidir. Python programlama dili ve FastAPI çerçevesi kullanılarak geliştirilmiştir. Veritabanı olarak SQLite ve ORM için SQLAlchemy kullanmaktadır.

## Kullanılan Teknolojiler

* **Python 3.12+**
* **FastAPI**: Web API çerçevesi.
* **SQLAlchemy**: Veritabanı işlemleri (ORM).
* **SQLite**: Yerel dosya tabanlı veritabanı.
* **Uvicorn**: ASGI sunucusu.
* **Pydantic**: Veri doğrulama ve şema yönetimi.

## Kurulum ve Çalıştırma

Projeyi yerel makinenizde çalıştırmak için aşağıdaki adımları izleyin.

1.  **Projeyi Klonlayın**
    ```bash
    git clone [https://github.com/Kalyanamkara/oyun-kutuphanesi-backend.git](https://github.com/Kalyanamkara/oyun-kutuphanesi-backend.git)
    cd oyun-kutuphanesi-backend
    ```

2.  **Sanal Ortamı Oluşturun ve Aktifleştirin**
    Windows için:
    ```powershell
    python -m venv venv
    .\venv\Scripts\activate
    ```
    MacOS/Linux için:
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

3.  **Gerekli Kütüphaneleri Yükleyin**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Sunucuyu Başlatın**
    ```bash
    uvicorn main:app --reload
    ```

Sunucu `http://127.0.0.1:8000` adresinde çalışmaya başlayacaktır.

## API Dokümantasyonu

API'nin interaktif dokümantasyonuna ve test arayüzüne (Swagger UI) şu adresten ulaşabilirsiniz:
`http://127.0.0.1:8000/docs`

### Endpoint Listesi

* **GET /oyunlar**: Kayıtlı tüm oyunları listeler.
* **POST /oyun-ekle**: Yeni bir oyun kaydı oluşturur.
* **PUT /oyun-guncelle/{id}**: Var olan bir oyunun bilgilerini günceller (Kısmi güncelleme destekler).
* **DELETE /oyun-sil/{id}**: Belirtilen ID'ye sahip oyunu siler.

## Veritabanı Yapısı

Proje çalıştırıldığında ana dizinde otomatik olarak `oyunlar.db` dosyası oluşturulur. Veritabanı tablosu (oyunlar) şu sütunları içerir:
* `id` (Integer, Primary Key): Benzersiz kayıt numarası.
* `isim` (String): Oyunun adı.
* `tur` (String): Oyunun türü.
* `puan` (Integer): Oyunun puanı.
