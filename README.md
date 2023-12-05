# Dosya Güvenliği ve Yönetim Sistemi

Bu proje, istemcinin sunucuya dosya yüklemesini, şifreleme algoritmalarını seçmesini ve dosya güvenliğini sağlamak için bir dizi özellik sunmaktadır. Ayrıca, sunucu tarafında dosya yönetimi ve istemcinin dosyaları indirme özellikleri bulunmaktadır.

## Özellikler

1. **Dosya Yükleme**
    - İstemci, sunucuya istediği dosyayı seçebilir.
    - Şifreleme algoritmasını (Des, Aes, Blowfish) ve anahtar değerini seçerek dosyayı yükleyebilir.
    - İstemesi durumunda şifresiz yükleme de mümkündür.

2. **Anahtar Değerinin Güvenliği**
    - İstemci, dosyalar için seçtiği anahtar değerini, kullanıcı tarafından belirlenen bir parola ile güvende tutabilir.
    - Anahtarlar, RC4 algoritmasıyla güvenli bir dosyada saklanır.

3. **Dosya Yönetimi**
    - İstemci, sunucudaki dosyaları dizinsel olarak gözlemleyebilir.
    - Dosya seçme, silme, yeni klasör oluşturma, dosyaları klasöre taşıma ve klasör/dosya silme gibi işlemleri gerçekleştirebilir.

4. **Dosya İndirme ve Deşifreleme**
    - İstemci, sunucudan dosyayı gerektiğinde indirebilir.
    - İndirilen dosya, lokaldeki anahtarları içeren dosyadaki anahtar kullanılarak otomatik olarak deşifre edilebilir.

5. **Çeşitli Dosya Türleri**
    - Herhangi türdeki dosya, sunucuya yüklenebilir.

6. **Şifresiz Dosya Listeleme**
    - Sunucu tarafında, istemcinin istemesi durumunda şifresiz dosyaların listesi görüntülenebilir.

## Kullanım

1. **Projeyi İndirme**
    ```bash
    git clone https://github.com/kullanici/proje.git
    cd proje
    ```

2. **Gereksinimleri Yükleme**
    ```bash
    pip install -r requirements.txt
    ```

3. **Proje Çalıştırma**
    ```bash
    python manage.py runserver
    ```

🔐 Güvenli dosya yönetimi ve şifreleme algoritmaları ile dosyalarınızı koruyun! 🚀


