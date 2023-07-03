<h1 align="center">IDOR (Insecure Direct Object Reference)</h1>

- Application securityde en önemli konu kullanıcıdan alınan inputlar, direktiflerdir.

# IDOR Nedir?
- Bir web sitesikullanıcıdan aldığı bilgiler ile veritabanına erişim sağlayıp bu veriyi okuyup kullanıcıya gösterme, veriyi değiştirme, silme gibi işlemler yapar. IDOR'un gerçekleşmesi için bazı kurallar gerekiyor örneğin: 
  - Ben başka bir kullanıcının adresini görememeliyim

## Uygulamalı Örnek
- Aşağıdaki burp ss i için: 
- Veritabanındaki kullanıcının ID’si 15 imiş. Bunu anlamış olduk. 15i 14 yapınca işler değişiyor. Forward etmeden önce Action kısmından “Do intercept response this request” yap ki sonucu görebilesin.

![image](https://github.com/grealyve/MDISec-Web-Security-and-Hacking-Notes/assets/41903311/beb038e4-2f81-42c7-b53f-3a7b22e2f1ed)
  - Veri tabanında adress bilgisini ifade eden id değeri 15, bu bizim başlangıç noktamız olacak.
- Normalde bir kullanıcı, başka bir kullanıcının datasını değiştiremiyor olması gerekiyor. Bu veriyi silme yetkisi var mı? Bu veri senin mi kontrollerini yapması gerekiyor?
- Gelen cevap 302 FOUND olabilir ama buna aldanma, authorization failure hatası da alıyor olabilirsin. Adres silinmiş de olabilir silinmemiş de olabilir. Gidip diğer kullanıcıyı kontrol et. 
- Sonra veritabanında var olması güç bir ID üstünde paketi yolla, sitenin backend davranışını anlamaya çalış. 
  - 404 Not Found döndürdü. ID validation yapıp ondan sonra silme işlemini gerçekleştiriyor. Eğer bu id yok ise adresi silmeyip 404 hatası döndürüyor. Kullanıcının silme yetkisini de kontrol ediyor bu arada. 
![image](https://github.com/grealyve/MDISec-Web-Security-and-Hacking-Notes/assets/41903311/fb70a74f-b9ab-49ab-8858-69716d09e0a0)
- Delete fonksiyonu yerine belki arkada update fonksiyonu vardır onun üzerinde deneme yapıyoruz. CRUD(Create-Read-Update-Delete).
- Referans noktan arkadaki fonksiyon olacak. Intruder’dan ekleyeceksin buraya popüler fonksiyon isimlerinden gireceksin. “From field names”
- Başka bir fonksiyona eriştiğinde : Missing Function Level Access Control zaafiyeti var demektir. Intruder’dan “edit” isimli bir fonksiyona eriştik. Eğer bu endpointi kullanarak başka idler ile farklı verilere erişebiliyorsan IDOR zafiyeti demektir.
------------
- Adres kısmını bu uygulamada başka nerelerde kullanılıyor onu düşünmen gerekiyor.
- Sipariş verirken adress ID sini değiştirdiğinde ve Forward yapınca sipariş tamamlanırsa IDOR var demektir. Bu fotoğraftaki address verisi bizim 17 değerini tutuyor bunu değiştirip başka adrese yollayabiliyor musun?
![image](https://github.com/grealyve/MDISec-Web-Security-and-Hacking-Notes/assets/41903311/5e3a46cf-9e02-4f40-8bcd-7b7991fade54)
- Adress ID değerini 18 yapıp yollayınca sipariş tamamlandı, başka birisinin adresine ürün gitmiş oldu. History kısmından ise başkasının adres bilgisine ulaşmış oluyoruz.
![image](https://github.com/grealyve/MDISec-Web-Security-and-Hacking-Notes/assets/41903311/e60db9b6-4d61-458c-86b2-083f6f0e5202)
- Bu adres bilgisi bu user’ın mı? Bunun kontrolü unutulmuş bu yüzden IDOR zafiyeti çıkıyor. Sadee bu adres var mı yok mu onun kontrolünü yapmış.
![image](https://github.com/grealyve/MDISec-Web-Security-and-Hacking-Notes/assets/41903311/c5ac71ce-4f8c-4080-8f37-7c90931251d9)
- Zafiyetler 2 türe ayrılıyor :
1) Teknik zafiyetler (payload var bunlarda örn. SQLi, XSS)
2) Business Logic zafiyetler(kaynak kodda bulması da zor, örn. IDOR)

- Günümüzde artık olay microservicelere kayıyor olaylar. Bir uygulamada aynı DB üstünde kendi sorgusunu çalıştıran onlarca servis var. Birisi sadece kullanıcı adını, biri sadece adresini, biri sadece kullanıcı bilgilerini gibi… Burada business logic kurallar nereye konulacak? Yani hangi user’ın adresini görebileceğin kuralını nereye implemente edeceksin? Servis mi kontrol edecek yoksa bu servisi çağıran uygulama mı?
  - Eğer servis, yetkiyi kontrol ediyorsa şöyle bir sıkıntı olacak: yarın bir gün bu servisi kullanmak isteyen başka bir web uygulaması başka bir yetki ve servis yapısı istediğinde sen microservice deploy edeceksin. 
  - Servisin görevi verilen işi yapmaktır, iş nedir = adres bilgisini getir. Adresi görebilirsin, göremezsin derse “annotation” devreye giriyor(can read gibi).
![image](https://github.com/grealyve/MDISec-Web-Security-and-Hacking-Notes/assets/41903311/46ee496c-6991-4cf2-9598-698e5415a90f)
- Ama illaki bu servis içinde kontrol edicem diyorsan “user_id”sini de alıyorsun ve SQL sorgusu içine ekliyorsun ve bu userın bu adrese erişip erişemeyeceği gibi “JOIN, WHERE” komutlarında yazması lazım. Eğer bunu unutursa parametreleri pass ediyor ama alt katmandaki servis kontrolü yapmıyor, servisteki adam bu yetkileri kontrol etmiyorsa IDOR oluşmuş oluyor. Büyük firmalarda genelde bu servisler ayrı takımlar tarafından kodlanıyor o yüzden dikkat.

- Aşağıdaki ss için: 
- API Gateway ile Servis yazılım dilleri farklı olduğu için IDOR ortaya çıkıyor.
- API Gateway 5 üzerinden işlem yapıyor fakat servis dili ben son gelen parametreyi id olarak aldığı için “6 id” li kullanıcının bilgilerini döndürüyor.
    - Kimi JSON parserlar ilk gördüğünü değer olarak kabul ederken kimisi ikinciyi değer olarak görüyor.
![image](https://github.com/grealyve/MDISec-Web-Security-and-Hacking-Notes/assets/41903311/b1f35cf3-d46c-4093-b82d-178a81691ecd)
- Web uygulamasının arka tarafında bir mikroservis yapısı varsa sen kullanıcı için cookie kullanmaya devam et. Ama API DB’e gidip user ile ilgili tüm yetki ve verileri toplayıp bir tane JWT oluşturup servislere bu JWT’yi yolladığında yetki kontrollerini servis üstünde çok daha hızlı yapabilirsin. Yani JWT oluşturup içeride onu gezdirirsin. Bu yapının da götürüsü olarak mesela kullanıcı başka bir web servisine gittiğinde JWT ile gelmediği için(cookie ile geliyor) bu API’lar için merkezi bir Database oluşturmak zorunda kalıyorsun, içeride JTW kullanmaya devam edebilirsin.
![image](https://github.com/grealyve/MDISec-Web-Security-and-Hacking-Notes/assets/41903311/677ce843-1368-4ec3-b802-a7da14e5a79c)

## Burp Suite ile IDOR'u Pentester Nasıl Bulabilir ? 
- Burp içinde Autmatrix extensionı kullanabilirsin.
![image](https://github.com/grealyve/MDISec-Web-Security-and-Hacking-Notes/assets/41903311/abce1395-e0d6-4d20-9233-545727148b05)
- Yatay ve dikey senaryolar oluşturmalısın yani kullanıcıların birbirinin verilerini görüp görememe mevzusu başka; bir kullanıcı, adminin işlerine erişebiliyor mu bu mevzu başka. Her bir senaryoyu değerlendirmen gerekiyor.
- En az 2 farklı kullanıcı ile tokenları al Autmatrix içine koy. Bunun üstünde profiller oluşturup oynamalar yaparak IDOR zafiyetini tespit edebilirsin.
- Anonim user, normal kullanıcı 1, normal kullanıcı 2, moderatör ve admin gibi. Her bir kullanıcı için ayrı cookie değerleri girebilirsin.
- Bu extensionı kullanarak kullanıcıya dönen responseları filtreleyebilir, hangi kullanıcı için hangi response döndüğünü detaylı inceleyebilirsiniz. Kimi yerde 500 gördüğün yerde IDOR vardır , her zamna 200 dönmesi lazım değil.
- Anonim bir Cookie oluşturma : XSRF-TOKEN=invalid;SESSION=INVALID

IDOR Hakkında Her Şey: https://medium.com/@aysebilgegunduz/everything-you-need-to-know-about-idor-insecure-direct-object-references-375f83e03a87
