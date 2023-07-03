<h1 align="center">XSS Güvenlik Zafiyeti Part - 1</h1>

## Tespit
#### XSS HTTP response’un Body kısmında gerçekleşir. Buradaki dataya odaklan. Hedef, arkadaki sistem değil onu kullanan kişiler aslında.
- Bir HTTP response’u 3’e ayrılır:
    - CSS : Kaşının, gözünün, teninin rengini verir.
    - HTML : Senin iskeletindir.
    - JavaScript : Vücudunu hareket ettirmeni sağlar. Biz de hareket kısmıyla ilgileniyoruz.
- *Response’un içerisinde kontrol edebildiğin bir değişkeni(değerini kendin belirleyebildiğin), browser’a geri gönderilen HTML içeriğin bir kısmında kullanılıyor.*
![image](https://github.com/grealyve/MDISec-Web-Security-and-Hacking-Notes/assets/41903311/3159ec38-3ae3-4ff6-9df9-b32f81f84359)
- Search kısmı olur, URL’in keywork kısımları olur, input edebildiğin her yer olabilir.

- Browser, gelen HTML’i parse ediyor ve bir tane structure oluşturuyor. JS ile ilgili kısımları JS interpreterine veriyor, CSS kodlarını çalıştırıyor ve ortaya bir tane DOM oluşturmuş oluyor.
    - Inpect yaptığında ve sayfanın kaynak kodlarına baktığında orada bulunana kodlar biribirinden farklıdır. Çünkü browser o kaynak kodundaki JS kodlarını falan işliyor ve ortaya site çıkmış oluyor. Biz inspect kısmı ile ilgilenicez.

- XSS saldırısına input olarak şöyle başlayacaksın:
```html
mdi'">< 
  yazıp dönen cevabın içinde mdi geçtiği yerlere bak.
Browser tarafına bunun data olarak kullanılması gerekirken, tag olarak kullanabilme imkanı ortaya çıkıyor.
<script>alert(1)</script>
```
- data olarak gönderdiğimiz verinin, browsera aynı şekilde geri dönmesi halinde burada anlamalısın ki < tagi browser için başka bir anlam ifade ediyor.

- Bu gönderilen yazı backend tarafında data olarak kalıyor ama tekrar browser’a response olarak geri döndüğünde browser bunu artık tag olarak yorumluyor ve XSS doğuyor.
- XSS payloadın her zaman response’da yansımaz. Yansıyorsa —> *Reflected XSS*
    - DB’e kaydedilebilir.  Diğer kullanıcılar da bu veriyi DB’den çekip browser da bunu yorumlayınca sömürülebilir.(*Stored XSS*)
    - Başka bir web servisi tarafından alınıp başka bir web application kullanıyor da olabilir.
![image](https://github.com/grealyve/MDISec-Web-Security-and-Hacking-Notes/assets/41903311/0e672841-d238-429b-9e06-90a450a0988e)
- Browserlar “textarea” içerisindeki scriptleri çalıştırmaz. Senin de bu scripleri nereye yazacağın çok önemli.
    - Saldırı kodunun textarea’yı kapatma ile başlaması gerekiyor.
- Kendinden başkasına etki ettiremiyorsan *Self XSS* olmuş oluyor
- Web sitesinin başka bir web servisinden gelen veriyi encoding yapmadan getiriyorsa orada Stored XSS çıkabilir. Facebook örneği (1:32:00)

## HTML Context
- <> tagların olabilmesi için bu işaretlerin olması gereklidir. Bunlar olmazsa asla XSS yapamazsın.
    - Encode edebilirler &lt; ve &gt; olarak.
## Attribute Context
![image](https://github.com/grealyve/MDISec-Web-Security-and-Hacking-Notes/assets/41903311/a861aa0d-e76c-405a-a5b3-f178ea0e41f3)
- Bu tagin value attribute’unda olduğun için XSS oluşmaz(Mehmet kısmı.)
- Öncelikle “ koyarak bu attributeun tanımını bitirmelisin. Sonrasında kendi tagini açıp scriptini yazabilirsin.
![image](https://github.com/grealyve/MDISec-Web-Security-and-Hacking-Notes/assets/41903311/15ceac42-7800-4363-8cac-3b35bede2f2b)
- Encode edilse bile kendi attribute unu oluşturup script çalıştırabilirsin :
    - <> encode edilmeli VE “ ‘ ` encode edilmeli!!
![image](https://github.com/grealyve/MDISec-Web-Security-and-Hacking-Notes/assets/41903311/5cbe533f-a7ea-4f31-9e7b-29fb357580f8)
#### Not: Internet Exlporer version 8-9’da HTML Parser Engine ` ` bu işareti görünce tag’i sonlandırıyor. 
## HREF Context
- a href içine USER_DATA durum ile karşılaşırsan gidip JS’in browserlarda protocol handler olduğu durumu tetikleyebiliyorsun.
![image](https://github.com/grealyve/MDISec-Web-Security-and-Hacking-Notes/assets/41903311/478fa3bb-a215-4cf5-a196-c102bbcc6648)
## JSINLINE Context
- id kısmına alert(1) göndermen yeterli olur XSS tetiklemek için.
    - Her şeyi encode etsen bile bu XSS çalışır. Burada parantezleri encode etmen gerekiyor
![image](https://github.com/grealyve/MDISec-Web-Security-and-Hacking-Notes/assets/41903311/6aba78d3-fa64-42d9-84a0-82ccfd88f1d7)
---
![image](https://github.com/grealyve/MDISec-Web-Security-and-Hacking-Notes/assets/41903311/ab4612ea-0467-477d-b264-8043bc66b74a)
- Burada Asla XSS oluşmaz ama gidip yazılımcı Command line yaparsa işi biter.
![image](https://github.com/grealyve/MDISec-Web-Security-and-Hacking-Notes/assets/41903311/dad18be3-14c4-448c-b2de-ee07ac4134c5)
- %0a new line demek
## Google XSS
- 2.Challenge Blockquote içinde script çalıştıramayacağın için svg tagini dene. Olmazsa img denersin.
![image](https://github.com/grealyve/MDISec-Web-Security-and-Hacking-Notes/assets/41903311/8213b73a-76aa-480b-8995-0a8cac772012)
---
- 4.Challenge Kullanıcının inputunu şu şekilde tutuyor —> inputa  = ’-alert(1)-’ yazdığında tetiklenecektir.
- HTTP içerisindeki + ifadeleri özellikle Query Stringde HTTP’nin ilk satırını GET’in bozduğu için boşluğu encode etmek gerek, + kullanmıyoruz da - kullanıyoruz.
![image](https://github.com/grealyve/MDISec-Web-Security-and-Hacking-Notes/assets/41903311/fda8dc26-efaa-40a8-82ce-583bf4ea4ed8)
-----
#### 6.Challenge
- Location hashden bir path alıyor sonra “includeGadget” ile bu pathi yüklüyor. Eğer verilen input http ile başlarsa hata verir. http isteklerini göndermeni engelliyor kod. 
![image](https://github.com/grealyve/MDISec-Web-Security-and-Hacking-Notes/assets/41903311/f21e2e33-6e06-4423-a0b7-e00b66c17086)
    - data:text/javascript,alert(1)
![image](https://github.com/grealyve/MDISec-Web-Security-and-Hacking-Notes/assets/41903311/dce770eb-3013-4592-b56d-4096d8441a7f)
- URL’deki # burada js’in kodu anlamlandırmasını sağlıyor. 

### Ekstra Notlar:
- Nasıl çözülür? : Input Validation VE Output Encoding
Input’u encode etmek yanlış bir yaklaşım olur. DB’e kaydederken datayı bozmuş olursun veya başka bir ekip bu datayı kullanmak için decode etmesi gerekir.
Context Based Encoding Owasp
- DOM based xsslerde hangi fonksiyonların engellendiğini filtrelendiğini kolayca anlayabilmek için url kısmında kendi fonksiyonunu yazıp bakabilirsin
