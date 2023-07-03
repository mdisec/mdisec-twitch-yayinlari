<h1 align="center">Web Cache Poisoning Zafiyeti</h1>

## Web Cache Nedir ?
- Cache dediğinde birçok kişinin aklına “Browser Cache” ve “DNS cache” gelir.
  - DNS cache: işletim sisteminizin cache yapması ve DNS serverının da cache yapmasıdır TTL değerleri falan vardır.
  - Browser cache: ctrl+f5 :D
- Server-side caching, modern frameworklerin template enginelerinin sağladığı caching yöntemleri.
  - Laravel, related template engine var. Her seferinde template sıfırdan üretmektense bunu bir ara cache formatında tutar ve diske kaydeder. Lazım olduğunda ise cache den alır ki aynı işlemleri ve maaliyetleri tekrarlamamak için.
- Bizim konuşacağımız template engineler ile alakalı değil. Web cache bunlarla alakalı değil spesifik olarak.

- İki kişi aynı sayfaya geldiğinde sürekli aynı şeyleri tekrar tekrar üretmektense bunu direct cache de tutarlar ve burdan serve edilir. Bunların hepsi HTTP katmanında oluyor.
![image](https://github.com/grealyve/MDISec-Web-Security-and-Hacking-Notes/assets/41903311/28991905-dac8-4db9-825f-bbdf665c7ac3)
1) Bu sistemde hangi adreslerin cache leneceğine kim karar veriyor?
2) Bir requesting cache den mi döneceği yoksa sunucuya mı iletileceği nasıl karar veriyoruz?
- Her cache edilen şeylerin bir key-value değerleri olması gerekiyor. Value zaten sunucudan dönen content.
  - Key ise, web servisi kendisi üretiyor. Protokol, domain, path ve query stringi baz alarak üretiyor.
    - in memory çalışır bu DB falan kullanmaz.

- Elimizde böyle bir key yoksa gelen HTTP requestlerini sunucuya göndermek zorunda. Gider sunucu bir response üretir ve sonrasında sunucu cache ile ilgili esktra bir bilgiyi ortadaki Web-cache servisine söylemesi lazım. Bunu da header valuelar ile söyleyebiliyor. Cache=True
  - Bu content cashlenebilir mi cashlenemez mi onu söylemesi lazım /private-key ya da /settings gibi her usera özgü farklılık gösterecek endpointlerdir bunlar.
  - Query stringler çok kritiktir bu cache mevzusunda.

- Bir istek gönderiyoruz, Serverdan Web-cache mekanizmasına dönen cevapta bizim isteğimiz cache lenebilir ise buraya(response un body kısmına) bir şey injekte etmeyi başarabilirsek ve benden sonraki gelen kişinin contentin içeriğine istediğimizi yazabiliyoruz.
  - Peki ya request gönderdiğinde sana gelen cevabın Web-cache mekanizmasından dönüp dönmediğini nasıl anlayacaksın?
### “              Göremiyorsan delay koy.          “
![image](https://github.com/grealyve/MDISec-Web-Security-and-Hacking-Notes/assets/41903311/78b29b8a-0c2c-44cb-b07c-742feb3981a8)
### İLK TENKİK : query stringe rastgele bir değer yaz. İlk gönderdiğinde ve ikinci gönderdiğinde zaman farkı varsa anlayabilirsin.
![image](https://github.com/grealyve/MDISec-Web-Security-and-Hacking-Notes/assets/41903311/2367e900-cd66-4ea5-b5ae-ab9e8c009c03)
### İKİNCİ TEKNİK : Cache sunucular sana söyler.  OK ya da MISS yazar. Bazıları cache keyini yazar(kısa bir key). 
- Responsedaki headera bakarsın 200 OK 404 fark etmez.
![image](https://github.com/grealyve/MDISec-Web-Security-and-Hacking-Notes/assets/41903311/9770e248-28c6-449d-8458-aed6ba43ad84)
- Bir endpoint parametresi almıyordur yani ?selam=kelam yaz yolla
  - Caching yaparken spesifik bir query stringe bakmaz sistemler.

## Response Contentine nasıl bir şeyler injecte edeceğiz? (Lab: Web cache poisoning with an unkeyed header)
- Query stringler key’in belirlenmesi için anahtarlanıyor burada.
  - Key value - Unkeyed value  diye 2 tane hikaye var. Key’de kullanılan valuelar var, keyde kullanılmayan valuelar var. Query stringin neredeyse tamamı keyde kullanılır. Burda caching yapmak çok zordur. Çünkü onu değiştirdiğin zaman key değişecektir, başka bir kullanıcının contentine injection yapamazsın.
- Modern frameworkler işin içerisine giriyor burada. Ana sayfaya gelen herkes aynı cachei görmektedir. Yazılımcı açısından debugging için bunu görmesi gerekebilir falan ama bu zafiyet açığı değildir.
- Cache poisoning için arka tarafı da biraz bilmek gerekiyor.
![image](https://github.com/grealyve/MDISec-Web-Security-and-Hacking-Notes/assets/41903311/2f6c704a-e1b4-4919-a332-162b47c935b1)
- Template engine 2.satırı alıp aslında 5.satıra çeviriyor. Peki buradaki protokol, domain, port nereden geliyor?
  - Modern frameworkler bunları hesaplarken Request Headerından yararlanırlar.
    - Mesela http isteği geliyorsa protokol olarak onu yazar, X yerine gider Hostu yazar, port tanımı olmadığı için otomatik 80 alır. Link üretirken bunları kullanırlar işte.
![image](https://github.com/grealyve/MDISec-Web-Security-and-Hacking-Notes/assets/41903311/8a57e95b-2e81-4be0-a69a-4f08cd50e4eb)
- Mesela gidip host alanını ordan direkt çekiyormuş. (Değiştirmeyi denedik başaramadık abi)
![image](https://github.com/grealyve/MDISec-Web-Security-and-Hacking-Notes/assets/41903311/8979bfaf-e461-4e50-840e-6d7d7e9c2a33)
- Host alanına dokunamadık, ön taraftaki Nginx Host tanımına göre çalışır ama arka taraftaki web application framework X-Forwarded-Host headerı yazarsan buna göre çalışır. Link üretirken helper functionları bunu baz alabilir mesela.
![image](https://github.com/grealyve/MDISec-Web-Security-and-Hacking-Notes/assets/41903311/b2396ecd-cb27-4141-bb41-ea7d8b9df709)
- X-Cache : miss yazıyor ama tekrar isteği yollayınca Hit oldu. Caching key üretirken  X-Forwarded-Host headerına  bakıyor demekki.
![image](https://github.com/grealyve/MDISec-Web-Security-and-Hacking-Notes/assets/41903311/540b9f77-78f7-4f04-9f24-f0f8934dd52f)
- Cache counterı belli bir sınırdan sonra keyi silebiliyormuş silmesi için sürekli denedik ama olmadı gibi.
- Sonra şunu repeaterda üstüne oynamak için aldık. **“Unkeyed bir value bulduk ve bu valuenun responsta görev aldığını gördük.”**
  - Temiz bir ortamda çalışmak için ?a=a yazıp o ortamda test yaptı:
![image](https://github.com/grealyve/MDISec-Web-Security-and-Hacking-Notes/assets/41903311/800e407e-e3ec-4070-a735-dff02224f3fa)
- Böyle bir XSS payloadı injecte edebiliyoruz. Aynı cache keyini başkalarında hit ettirebildiğimizde Stored XSS olacak. Yani ana sayfanınkini de böyle yapmamız lazım. Yukarda da yazdığım gibi sürekli istek giderse o cache invalide olabiliyor. Burada query string içerisinde bunu yaptık ama zor gibi. 
![image](https://github.com/grealyve/MDISec-Web-Security-and-Hacking-Notes/assets/41903311/3b432068-c897-4ea0-b589-948b259882b3)
- böyle yolladı sadece query stringi sildi. Ama arada bu injection kodu kayboluyor, sürekli bu paketi yolluyor ta ki Miss gelene kadar:
![image](https://github.com/grealyve/MDISec-Web-Security-and-Hacking-Notes/assets/41903311/6a25a86c-63fc-4547-92c9-28dc96ee4831)
![image](https://github.com/grealyve/MDISec-Web-Security-and-Hacking-Notes/assets/41903311/1ed4d737-dd73-48bb-84be-1f59d89fcf90)
## Gerçek hayattan örnekler
- Bazen Web-appler asenkron şekilde JS contenti generate etmesi gerekir dinamik şekilde.
  - User’ın sessionına göre alıp buradaki birtakım HTML içeriklerini değiştirmeniz gereken bir endpoint. Backendde bir kodu var. Dinamik bir single page sayfası olduğunu düşün.
      - Herkes home page e geliyor ve dönen content de JS. Sen Cache server tarafından keylenmeyen bir değer bulursan patlatırsın. SANA ÖZGÜN BİR CONTENT ÜRETMESİ LAZIM. Bu case olma olasılığı çok düşüktür.
![image](https://github.com/grealyve/MDISec-Web-Security-and-Hacking-Notes/assets/41903311/20753647-d36f-440e-8bad-cbf92cfe0f49)
- tracking.js full path üstünden çağırılmış
  - // tricki ise senin isteğin http iste http, https ise https üzerinden çağırması için kullanılır.
![image](https://github.com/grealyve/MDISec-Web-Security-and-Hacking-Notes/assets/41903311/dccf8fcf-79d5-4c52-8be3-b15ec1721f6e)
- Javascript contentini cache hitliyor. Buradan da o case çıkabilir.
  - Header kısmına X-Forwarded-Path : /selam yazdı bir cacık olmadı. X-Forwarded-Port : 1 yazdı olmaıd.
  - Extender “Param Miner” kuruyosun. Sağ tıkla guess header diyosun.
![image](https://github.com/grealyve/MDISec-Web-Security-and-Hacking-Notes/assets/41903311/e73fbafd-5da2-48a7-b6de-5589e41d3536)
- real lifeta görsem geçerim diyor :)
