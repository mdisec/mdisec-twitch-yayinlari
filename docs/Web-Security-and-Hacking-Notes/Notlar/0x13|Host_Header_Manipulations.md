<h1 align="center">Host Header Manipulations</h1>

- Domain sayısı > IP adresi, bu yüzden shared hosting diye bir mevzu var. Apache, tomcat, nginx gibi web servislerinin önünde bulunan reverse proxy servislerinin tüm ilgi alanı HOST ile ilgilidir.
- Atak yüzeyleri de arkadaki frameworkler olmaya başlıyor.
![image](https://github.com/grealyve/MDISec-Web-Security-and-Hacking-Notes/assets/41903311/45bda1e2-610b-4c16-95f6-213fee594eb0)
- Arkadaki frameworkler URI veya URL yapısını istemektedir.
  - Request.Url.ToString() metodu gibi fonksiyonlar framework tarafından çokça kullanılır. Özellikle statik dosyalarının full URL’lerinin template engine lerde generate edilmesi ile alakalı mevzu dönüyor.
![image](https://github.com/grealyve/MDISec-Web-Security-and-Hacking-Notes/assets/41903311/b668a3c0-988d-4bab-8cdf-29643a11452a)
  - Bu yardımcı metodlar HTTP requestinin içindeki host headerının içindeki bilgiyi alırlar.
- Ön tarafta reverse proxy i aşacak, arkada tomcati aşacak, bu iki noktadan sorunsuz geçtikten sonra burdaki requesting Map edilmesini sağlarsan ve bu uygulamada Host alanını kullanarak bir şeyler print ediyorsa XSS ortaya çıkar.
- Hatta uygulamadan kullanıcıya dönen HTML içerik, Cache mekanizmalar tarafından cache leniyor ise böylece aynı içerik birden fazla kullanıcıya sunuluyor ise sen Cache’i poison ederek Stored XSS çıkartabilirsin
- Nginx, Host’a göre uygulamaları map ettiği için sen gidip localdeki uygulamaları yazarsan, yanlış konfigüre edilmiş bir reverse proxy i sömürürsün dışarıdan erişimi olmayan bir uygulamaya erişebilme imkanı sunulmuş olur.
## Lab: Basic password reset poisoning
- Uygulama bir e-posta göndereceği zaman bir HTML’i render eder. HTML’in içerisinde full URL oluşturması gerekmektedir.
- Parola sıfırlama alanının host kısmı buradan alınır.
![image](https://github.com/grealyve/MDISec-Web-Security-and-Hacking-Notes/assets/41903311/3dc0e01c-63e1-46c3-a70f-dabfdf85de07)
- Buradaki domain alanını manipüle edip, kendi domainimiz ile değiştirmek istiyoruz. Böylece bizim web siteye gelicek ve tokenı da elde etmiş olacağız.
- Önemli: Bir web uygulamasının testing, paging süreçleri falan farklı domainlerde gerçekleşebileceği için hard coded yazamaz bu host alanını, o yüzden dinamik bir şekilde oluşturulmalı. Framework üstünde de ona göre oluşturulur.
- Biz de bu şifre sıfırlama isteğini proxy ile kesip, Host alanına kendi domainimizi yazıcaz.
- Normalde carlos dış dünyadaki domainimize gelebilir, ama bu labda öyle tasarlamamışlar kendi exploit server oluşturmuşlar onun üstünden yürünecek.
- Adam linke tıkladığında Access logdan toplayacaksın veriyi.
- Adamların oluşturduğu exploit serverının sonuna ? koyup Host’a yazdığında loglara düştüğünü göreceksin. Normalde Host kısmında / falan geçmemesi lazım.
  - ? işaretini ise, geri kalan kısmı query string’e dönsün, adamların sunucuda kafalar karışmasın diye. Normalde bir doman yazarsın yürür gidersin.
  - Router ile farklı controllera gitmesin diye.
## Lab: Password reset poisoning via dangling markup (kapanmamış tag, havada kalmış)
- Bu labda adam token falan vermiyor, gidiyor yeni password veriyor.
![image](https://github.com/grealyve/MDISec-Web-Security-and-Hacking-Notes/assets/41903311/d9480033-48d5-4aeb-802c-1f4ff5dc5492)
- Domain kısmına öyle bir şey yazmamız gerekiyor ki “href”, parolayı taşıyan bir URL’e dönüşsün.
  - Click here’a tıkladığında otomatik gidecek oraya zaten, linki görmüyor.
- önce
  - ‘></a> tagını kapatıyor
  - img tagi açıyor ve “ koyarak başlatıyor ama kapatmıyor, oradan sonra gelen her şeyi e-posta istemcisinin HTML Parser’ına oynuyoruz ve o gösterecek bize. (e-postayı alan şey, outlook)
  - tek tırnak işaretini beğenmiyor bu iş iptal, URL parserlara gidecez
![image](https://github.com/grealyve/MDISec-Web-Security-and-Hacking-Notes/assets/41903311/d8798005-9f95-478b-9e76-19db8657558e)
- Ön taraftaki reverse proxy(gateway) host alanını parse ediyor, ondan sonra applicationda bu host alanını kullanıyor.
  - URL parse olayını kral bildiği için :80’ koyup  deniyor ve sonuç 200 dönüyor. Heralde :80 den sonrasına bakmıyor. : olan kısma kadar domain olarak kabul edip ona göre MAP ediyor.
![image](https://github.com/grealyve/MDISec-Web-Security-and-Hacking-Notes/assets/41903311/6509a7d8-5327-4e15-af48-ce89374e18a7)
  - Arka taraftaki Web app bu Host taginin tamamını kullanacağı(FULL URL IDENTIFIER) için sonrasında kendi payloadımızı çakabiliriz.
![image](https://github.com/grealyve/MDISec-Web-Security-and-Hacking-Notes/assets/41903311/531fc9ff-c4a4-4a31-9a71-7d0cd278909d)
  - Burada context based encoding yapması lazım.
- Sonrasında loglara parola düşüyor.
