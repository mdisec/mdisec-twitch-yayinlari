<h1 align="center">SSRF Giriş</h1>

#### İşinize yarayabilecek bazı eklentiler: hackvertor, hackbar
#### Okuyabileceğiniz makaleler:
1) https://github.com/swisskyrepo/PayloadsAllTheThings/tree/master/Server%20Side%20Request%20Forgery#bypassing-filters
2) https://www.blackhat.com/docs/us-17/thursday/us-17-Tsai-A-New-Era-Of-SSRF-Exploiting-URL-Parser-In-Trending-Programming-Languages.pdf
3) https://github.com/swisskyrepo/PayloadsAllTheThings/tree/master/Server%20Side%20Request%20Forgery#bypassing-filters

## Lab: SSRF with blacklist-based input filter
- Bir ürüne gidip “Stock Check” yap. Parametre olarak bir URL gönderiyor bunu da decode et.
![image](https://github.com/grealyve/MDISec-Web-Security-and-Hacking-Notes/assets/41903311/99f922e1-34bd-429c-87f9-53fc2f77deee)
- Öncelikle götürmek istediğimiz domaini çözmesi gerekiyor vatandaşın.
### Deneyebileceğin Yaklaşımlar:
1) Blacklisting yaklaşımlı SSRF çözmek için ilk olarak DNS çözdürmeyi deneyebilirsin(localhostpentest.pentes.blog/admin).
2) İp adresini HEX karşılığında verebilirsin ya da domaini HEX karşılığında verebilirsin.
3) Portu yazarsan arka tarafta backending URL parser’ı ile ilgeliniyorsun demek.
![image](https://github.com/grealyve/MDISec-Web-Security-and-Hacking-Notes/assets/41903311/b60fa392-b76f-471e-b0a5-7efd355f322a)
- [localtest.me](http://localtest.me) yapmasının sebebi arka tarafta 127.0.0.1’e çözümlemesini sağlamak. Bunu başka bir sürü kodla da yapabilirsin(nslookup ile de sağlamasını yaparsın.) github linkinde var.
- Burada anlamaya çalıştığı şey, string.contains() metodu gibi bir şey mi var arkada ona göre güvenlik önlemi almış yoksa URL’i parse edip mi bakıyor?
  - bunu anlamak için “admin”i alıp http://localtestadmin.me/ yapıp öyle deneyince security reasons hatası geldi yine demek ki burda string kontrolü var.
![image](https://github.com/grealyve/MDISec-Web-Security-and-Hacking-Notes/assets/41903311/d44a28a9-cbb3-4d1e-ac06-6510797f328c)
- ADMIN’i büyük yazıp denedi, “CouLd not connect to external check service” hatası geldi. Case sensitive mi diye kontrol etti yani
- “admin” i 2 kere URL encode edip yolladı. İlkinde öndeki engeli atlayacak admini göremediği için, bu URL’i ikinci encode halinde de bir backend’e(Java) tekrardan HTTP requesti göndertecek. Ama şuanki backend Java galiba ve bu isteği atarken otomatik decoding yapmıyor bu yüzden hata alındı.
![image](https://github.com/grealyve/MDISec-Web-Security-and-Hacking-Notes/assets/41903311/684d7a41-7e22-4e93-91f8-2ca870ed4aab)
- İlk decodingi Nginx, apache gibi önde duran uygulamalar yapar. Sonra 2. web uygulamasının gördüğü değer de encoded bir şey, burada bulunan nginx, apache, tomcat gibi uygulamalar tekrar bunu decode ediyor.
![image](https://github.com/grealyve/MDISec-Web-Security-and-Hacking-Notes/assets/41903311/7425812f-c403-4a58-a4a7-2dc00d46654c)
- 127.1 yazınca oldu. gerisi /admin encoded şeklinde.
- Sonra carlosu tekrar istek atarak sildi.
## Lab: SSRF with whitelist-based input filter
- Whitelisting yöntemleri : domain şu olması gerekli, port olarak bu olmalı ve path olarak da bu olmalı diyerek sıkılaştırılabilir.
- Bunu atlatmanın da tek yöntemi backend’in URL parser function’ını buglaman gerekli.
![image](https://github.com/grealyve/MDISec-Web-Security-and-Hacking-Notes/assets/41903311/57147ce6-db48-47a7-a5e0-23de7240c57d)
- Normal şartlarda x:y# kullanıcı adı parola demek URL şemasında. Ama # den sonrasını location hash olarak görüp bundan sonrasını kale alma diyebilir. Burdaki logic bugı kullanman lazım. URL parser stock.weliketoshop . net i domain sanacak ama full URL’i HTTP kütüphanesine verince ben z.com’a gidicem benim domain bu diyecek, oraya da localhost’u yerleştireceksin.
- Hangi parametreleri whiteliste almış onu dene.
![image](https://github.com/grealyve/MDISec-Web-Security-and-Hacking-Notes/assets/41903311/a56d43fa-dddd-4631-8231-ef4ecd89c500)
- Parametresini (storeId) silince kızıyor. & URL encoding yaptı.
- productId yi de görmek istiyor
- pathi değiştirince kızmıyor, admin yazınca kızmaz.
- Port’u değiştirince “CouLd not connect to external check service” hatası verdi yani buna da kızmıyormuş.
- domain’i değiştirince kızıyor. [stock.weliketoshop.net](http://stock.weliketoshop.net) olmalı diyor. sonuna .asd falan yazınca anlaşılıyor bu. URL’i parse ettikten sonra comparasion yapıyor
- Parse olayını daha detaylı incelemeye al.
![image](https://github.com/grealyve/MDISec-Web-Security-and-Hacking-Notes/assets/41903311/d3aec516-6826-42e8-8c9c-c3d8b4aa899d)
- username:paswd kısmına burp collabrator koydu, pek mantıklı bir yaklaşım değil ama kızmadı yine.
- boş @ işareti yolladı. invalid URL döndü
- @ işaretinden önce # koydu, kafası karışmaya başladı.
    - URL parse edip denedi.
- 2 tane @ koydu.
![image](https://github.com/grealyve/MDISec-Web-Security-and-Hacking-Notes/assets/41903311/0810bdfb-caea-45a6-be85-65d5bf87ab6e)
- Protokol ile de ilgilenmiyor arkadaş
- Diyez # koyunca olmuş dendi, ama kafası karışıyor.
![image](https://github.com/grealyve/MDISec-Web-Security-and-Hacking-Notes/assets/41903311/d96d4000-e3bb-4434-bbf0-284fdbe06428)
- @ den sonrasını parse etse, whitelist hatası verecek zaten.
![image](https://github.com/grealyve/MDISec-Web-Security-and-Hacking-Notes/assets/41903311/f1b52154-33a4-40ca-b24c-f5542b5f7d6b)
- Buna fuzzing yapıyormuş reis. Ama Parser kızdı zaten. Sitede, altındaki tabloda fuzzingi göstermiş zaten
![image](https://github.com/grealyve/MDISec-Web-Security-and-Hacking-Notes/assets/41903311/d775b7d6-204f-4fa9-be56-eecdd72192fe)
- Double encoding yaptı / işaretine ve oldu.
  - Payload, 127.0.0.1:80/admin@stock…..
![image](https://github.com/grealyve/MDISec-Web-Security-and-Hacking-Notes/assets/41903311/145872d3-7c86-412a-be0c-2f77e0d9785e)
- Parser @ den öncesini kul adı ve parola olarak görüyor yani çalışıyor o kısımda sıkıntı yok. Ama / işaretini koyunca burdan sonrasi itibariyle benim için path’dir diyor URL parser. 127.0.0.1 i algılamış oluyor.
- Öndeki URL parser diyor ki @ den öncesi kullanıcı adı, parola ben @ den sonrasına giderim aga.
- Sonra tam URL HTTP req. yapan fonksiyona gidince, URL decoding yapıyor ki parametreleri görebilsin. HTTP librarylerinin GET metodları default olarak URL decoding yapar. Sonra decode olmuş tam URL arka tarafa gidiyor o da bir kere daha decoding yapınca **/admin** ile karşılaşıyor.
  - Normade bunun böyle çalışmaması lazım çünkü @ işaretinden sonra orayı path algılayıp kafası karışmalı. Bunu çözümü de /admin?@ şeklinde yazmaktır ki ? den sonra query string olsun ve geri kalan her şey GET parametresine dönüşsün. ? ini de encode etmen lazım.
![image](https://github.com/grealyve/MDISec-Web-Security-and-Hacking-Notes/assets/41903311/2aa06c7d-3ccf-488d-8fb3-2d5a336f51e3)
- Özetle, HTTP web server bunu decode etti ve şuna dönüştü:
![image](https://github.com/grealyve/MDISec-Web-Security-and-Hacking-Notes/assets/41903311/f411eba9-5572-4993-ba00-3c211b69961b)
- backend(/product/stock endpointi)
![image](https://github.com/grealyve/MDISec-Web-Security-and-Hacking-Notes/assets/41903311/879b729b-a9ae-4d97-b5c4-375e86f84092)
- URL’i parse ettiğinde, /admin? encoded olduğu için 127.0.0.1:80 kullanıcı adı, paroladır. stock.weliketoshop.net benim domainimdir. Bu URL’i HTTP Client Library’sine verdi ve destination URL olarak bunu SET etti. Bu kütüphaneler de URL’den hangi host’a gitmeleri gerektiğini tespit etmek için bir daha URL parsing yaparlar ama yapmadan önce decode ederler ki “query stringleri “bulabilsin. Decode edince de parser, /admin ile karşılaşıyor ve destination 127.0.0.1 e dönüyor. ? sonrasını query stringe çevirmek için önemlidir.
![image](https://github.com/grealyve/MDISec-Web-Security-and-Hacking-Notes/assets/41903311/191ae15d-5375-4556-90d0-eb46a210fbcb)
- :80/admin/delete falan o kısımları sildik çünkü diğer /admin parametresi admin sayfasını getiriyor. Ona da /delete parametresini ekleyince ve username’i de en sona eklediğinde çözülmüş oluyor.
![image](https://github.com/grealyve/MDISec-Web-Security-and-Hacking-Notes/assets/41903311/d2a82038-45ac-4f8c-9488-220d197ae79d)
![image](https://github.com/grealyve/MDISec-Web-Security-and-Hacking-Notes/assets/41903311/2491ccb1-451b-4761-b931-023ec7562420)
- Öndeki uygulamaya giden payloadı şu şekilde görüyor:
![image](https://github.com/grealyve/MDISec-Web-Security-and-Hacking-Notes/assets/41903311/feb10b0a-4da7-44db-832d-28bb067a1cc8)
![image](https://github.com/grealyve/MDISec-Web-Security-and-Hacking-Notes/assets/41903311/33165b1e-1480-406e-a3c6-cea9b3acbec9)
- 127.0.0.1 den sonra / koymayınca işler değişiyor:
![image](https://github.com/grealyve/MDISec-Web-Security-and-Hacking-Notes/assets/41903311/0da15674-f202-4b3e-8463-2dab24e32edb)

