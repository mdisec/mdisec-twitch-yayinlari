<h1 align="center">Directory Traversal</h1>

#### Bu iş RCE’ye gider
#### Bu zafiyetin çözüm noktası, okuyacağın dosyanın nihai path’inin istediğin destination ve aynı noktada olup olmadığına bakman.
#### Gerçek hayattaki uygulamalar filename inputunu alıp decode etmek gibi şeyler yapmazlar, URL decoding gibi. Senden alınan filename bir URL’in içerisine konup, backend bu URL’e HTTP req gönderip resim alan bir mekanizma varsa işte o zaman double encoding işe yarıyor.

# Bu zafiyetin varlığı nasıl tespit edilir?
- Bu adam bir path’de bulunuyor ama pathin ne olduğunu bilmiyoruz.
- Bir dosyada ../ yapıp sonra tekrar aynı dizine geldiğimizde sıkıntı olmadan dosya geliyorsa directory traversal zafiyeti var demektir.
  - **../image/24.jpg**
---
## Directory Traversal Nedir?
- Dizin gezinmece.
- Günümüzdeki web applicationları resource erişimleri sağlıyor. Diskte bulunan bir veriyi okuma gerçekleştiriyor.
- Zafiyet, web app. kullanıcıdan aldığı bir input ile yereldeki  bir dosyaya erişim sağladığı yerde sıkıntı çıkıyor.
    - Sen gidip o dizini değiştirip, daha sonra okuma, silme, değiştirme (I/O) işlemi gerçekleştirebilme.
    - file=x
- Elinde id=5 olan bir post var ve bunun içinde de bir resim var. Bu resmin full path’ini expose edersen, full path’e erişimi olan biri bu resmi görebilir. Resmin full path’ini de DB’de tutuyorsun onu kullanıcıya dönüyorsun, kullanıcı ona geldiği zaman gene Django’nun execution içerisine giren bir yapı yok yani.
![image](https://github.com/grealyve/MDISec-Web-Security-and-Hacking-Notes/assets/41903311/9764a809-2375-44b1-9142-5936ddab85d8)
- IMG resource’una HTTP talebi geldiğinde önde çalışan Nginx(reverse proxy) kuralı bunu resim olarak gördüğü için localden dosyayı okuyup sana geri sunar. Yani app. içindeki hiçbir kural permission mimarisi içerisine girmez. Doğrudan erişebilirsin.
- Bu yüzden  uygulamalar conten erişimi sağlarken DB’deki her şeye erişim kontrolü yaparken statik resource’lara bunu pek yapmıyorlar. O yüzden bir resim göstermek istediğin zaman reverse proxy kuralları ile proxy service olarak sunman gerekiyor ya da farklı modeller kuruyorsun.
  - S3 bucket içerisinde miniofile yapıları?!?
- Böyle bir fatura görme yapısı vardır 15’i 16 yapınca basic IDOR denersin ama yapamazsın. Gidip pdf’i export et dediğinde backend pdf üretip, web sunucusu içerisindeki diske koyar ve bunun linkini sana verir. Bu link de app. permission şeması içerisine girmez.
![image](https://github.com/grealyve/MDISec-Web-Security-and-Hacking-Notes/assets/41903311/af048f9e-0b0f-49b5-b9dd-f3c756c00d38)
- Arkadaki yapı şu şekilde
  - /var/www/hackerconf.stream/static/ahmet
  - ahmet’i okumaya çalışacak gidip.
  - ../../../../../../../../../../../../../../../etc/passwd Linuxta üst dizine çıkmanın sonu yoktur garanti olsun diye 500 tane koy.
![image](https://github.com/grealyve/MDISec-Web-Security-and-Hacking-Notes/assets/41903311/251316a0-7a05-41c7-88ab-d1946dabbb90)
- ~ vs. shell environment’da geçerlidir. Bir programın okuduğu path erişiminde her program bunu destekliyor olamaz. O yüzden home dizinine gitmek yanlış olur, home dizini belki yoktur vs  vs.

- Özellikle Load Balancer’ın yaptığı URL normalization ile arkadaki application serverın yaptığı URL normalizationlar farklı ise, ön taraftaki app. serverdan izniniz olmayan noktalara erişim sağlayabiliyorsunuz.
  - Uber’in SingleSignOn mekanizmasını bypasslayıp internal sistemlere erişim sağlamada. URL normalization ve parsing.
---
## Lab: File path traversal, simple case
- Gerçek hayatta böyle sorgular yapılmaz aslında.
![image](https://github.com/grealyve/MDISec-Web-Security-and-Hacking-Notes/assets/41903311/e062da67-2a4c-459c-9673-c2b03c12723b)
- Benden aldığı bir inputu bir file reading işlemi yapacak.
## Lab: File path traversal, traversal sequences blocked with absolute path bypass
- Arkadaki kod resorce contcatenation yapmıyor olabilir, direkt resource okuyor olabilir. Yani bu çalışan uygulama ile aynı dizinde bulunuyorsa gitmek istenen nokta, bu birleştirmeyi yapmaz. Üst dizine çıkmak bir şey ifade etmeyecektir bu yüzden full path vermek zorundasın.
  - /etc/passwd
![image](https://github.com/grealyve/MDISec-Web-Security-and-Hacking-Notes/assets/41903311/ebc24c4d-1938-4597-8047-41da3e047168)
## Lab: File path traversal, traversal sequences stripped non-recursively
- Genelde yazılımlarda ../ yapmana engel koyarlar.
  - ../24.jpg yaptığında hala aynı cevap geliyorsa demek ki ../ kaldırıyordur adam.
  - Bunun da çözümü ….// yapmandır
![image](https://github.com/grealyve/MDISec-Web-Security-and-Hacking-Notes/assets/41903311/42a5e5bb-3a94-4e47-9ec8-adec297d1940)
- ….//images/24.jpg altında olduğunu elimizle tespit ettik, bu pathi verse yukarı çık tekrar gel yapıp tespit edebilirdik.
- for each ile sürekli bunları siler ise Denail of Service zafiyeti ortaya çıkar.
## Lab: File path traversal, traversal sequences stripped with superfluous URL-decode
- Input validation’dan mı hata alıyoruz yoksa dosyayı gerçekten bulamadığı için mi hata alıyoruz diye kontrol sağlandı.
- Gerçek hayattaki uygulamalar filename inputunu alıp decode etmek gibi şeyler yapmazlar, URL decoding gibi. Senden alınan filename bir URL’in içerisine konup, backend bu URL’e HTTP req gönderip resim alan bir mekanizma varsa işte o zaman double encoding işe yarıyor.
- Biz de URL encoding yaparak payload deniyoruz ve dizini de bulmaya çalışıyoruz.
    - GET / image?filename=..%25fimages%25f41.jpg
        - 2 kere encoding yaptı /
    - noktalara kızsa .jpg okumaz zati
- ./ taktiğini denedik, ../ konduğunda gene okuyor, ….// gene okuyor
- / görünce delleniyor oğlan
    - % nin encoded hali %25, üst dizine çık tekrar gir yaptı
    - %2f in decoded hali / (slash) işareti.
![image](https://github.com/grealyve/MDISec-Web-Security-and-Hacking-Notes/assets/41903311/70cc4901-21ca-4876-a736-cb84e36961e5)
## Lab: File path traversal, validation of start of path
- Böyle bir şeylerle karşılaşıyorsun:
![image](https://github.com/grealyve/MDISec-Web-Security-and-Hacking-Notes/assets/41903311/e11eb875-1f25-4fd5-bb4b-967bbb64750a)
- Bazı durumlarda backend, başlangıçtaki dosya yolu ile validation sağlar.
![image](https://github.com/grealyve/MDISec-Web-Security-and-Hacking-Notes/assets/41903311/4ac1358b-d8e0-46e9-be74-5bc6de49479b)
## Lab: File path traversal, validation of file extension with null byte bypass
- Senden folder alır.
![image](https://github.com/grealyve/MDISec-Web-Security-and-Hacking-Notes/assets/41903311/8b70c615-6f33-4daa-bb44-38d422025057)
  - /var/www/hackerconf. stream/.. /.. /.. /.. /.. /.. /.. /. ./selam/liste. txt
    - SQLi yaparken # ile sağ tarafı kapatabiliyordun ama bunda yapamıyorsun.
  - PHP’de eskiden en sona %00 yazdığında string bitti sanıyordu sonradan düzeltmişler.
- Burada null byte çalışır, git en sona %00 koy.
- Ve lab sayfasında da .jpg uzantısını istediğini söylemiş
- Bunu yapmasının sebebi;
![image](https://github.com/grealyve/MDISec-Web-Security-and-Hacking-Notes/assets/41903311/b734f82f-0ac3-4916-9289-4db435dd7b1b)
- String birleştirme yapacağı zaman adam, NULL Byte’dan sonrasını kopyalamıyr adam, zafiyetin oluştuğu yer burası.
## Directory Traversal ile ilgili zaafiyetlerden nasıl yararlandım ?
- Apache solr adlı yazılımı file adlı bir dosya alıyormuş. Logları okumak için bu kod parçacığını yazmış reis. Sonra cookie çalmış RCE’ye kadar yolu var.
![image](https://github.com/grealyve/MDISec-Web-Security-and-Hacking-Notes/assets/41903311/4e0450c3-1207-40d3-a430-150f2615c666)
