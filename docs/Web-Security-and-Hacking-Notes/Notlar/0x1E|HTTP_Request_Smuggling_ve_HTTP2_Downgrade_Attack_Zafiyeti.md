<h1 align="center">HTTP Request Smuggling</h1>

## HTTP Request Smuggling ve HTTP/2 Downgrade Attack Zafiyeti Nedir?
- HTTP desync attack olarak geçiyor ****HTTP Request Smuggling. Buradaki zafiyet burda direkt Web ile ilgili(web app. ile değil).****
  - Webin bir tanımı var ve mezhepler bunu farklı tanımlıyor.
- Normal bir akış şeması budur.
  - Load balancer : F5, Amazort Elastic LB, Cloudflare, Cloudfront. 80,443 portunda çalışan bir kod yazılımı.
  - Ngnix de aynı şekilde bir kod ve http’nin bu ikisinde de tanımı aynı. Fakat yorumlama şekilleri farklı bunların. Öyle bir şekilde hazırlıyorsun ki isteği, LB X anlıyor Nginx Y anlıyor.
![image](https://github.com/grealyve/MDISec-Web-Security-and-Hacking-Notes/assets/41903311/249e0ffd-d23e-4e8c-90f4-1e84dff9b08a)
- Three way handshake tamamlandıktan sonra bu TCP oturumu içerisinde HTTP isteği göndereceksin. Aşağıda da bir sürü tcp isteği gidip duruyor tüm paketler gidene kadar da karşı taraf bekleyecek. Tüm gelen dataları karşı taraf yazdıktan sonra ve 2 tane new line gördüğü zaman artık TCP’yi transportation katmanı olarak kullanıp yukarı çıkıyorsun ve 1 adet HTTP requesti göndermeyi başarıyorsun.
  - Karşıdaki HTTP protokolünü anlayan kütüphane  bu serviste işlerini yaptıktan sonra sana cevap dönüyor. Sen bu cevabı alana kadar 2. bir isteği bu TCP sessionu üstünden gönderemezsin. TCP 1’de böyle.
  - HTTP bir text transper protokolüdür. Doğal olarak text gitmesi gerekiyor.
  - HTTPS de ise SSL işin içine giriyor, paket şifreli halde gidiyor ve karşı tarafta decrypt edildikten sonra cevap geliyor falan akış aynı yeni.
- Bu datada http kütüphanesinin dikkat ettiği 2 tane header var. 1-Content Lenght, 2-Transfer Encoding. Bu headerlardaki değere göre LB’da HTTP sunucusu davranışı gerçekleştirir.
  - HTTP’nin tanımında çok net bir kural yok. Content Lenght varsa transfer encodingi kale alacak mıyım almayacak mıyım? İkisi bir arada varsa nasıl olacak? Hal böyle olunca LB’da çalışan HTTP servisini implemente eden adam kendi kurallarını üretiyor, arkada çalışan nginx de kendi kurallarını üretiyor. Bu kurallar arasında da farklılık olursa sıçanzi.
      - Mesela LB content Lenght’e göre bir ayırım yapıyorsa altta kalan kısmı yeni bir HTTP isteği olarak farz ediyor. Ama arkada Nginx farklı bir yorumlama yapıyor buna.
      - ![image](https://github.com/grealyve/MDISec-Web-Security-and-Hacking-Notes/assets/41903311/6547afe5-aecb-455d-938d-cc452dd1913d)
### HTTP 1.0/1.1/2 her zaman alt katmanda TCP protokolünü kullanırlar. 
### HTTP 1.0/1.1 için en kritik şey, sen günün sonunda bir TCP oturumu elde ediyorsun ve bu hat üstünden requesti gönderiyorsun.
### Buradaki asıl mesele zaten bu HTTP paketini ilk karşılayan servisin nasıl bu kuralları implemente ettiğidir.
![image](https://github.com/grealyve/MDISec-Web-Security-and-Hacking-Notes/assets/41903311/f3c2de63-bda0-4b93-a55a-4ca73d18a2d5)
- Başka bir request injection yapmış oluyorsun. 
- LB bir dünya insanın requestini alıyor ve burda konu diğer insanların responselarını alma veya onların responselarına müdahale etmeye kadar gidebiliyor.
  - Nasıl fixlenir? Önde ve arkadaki servislerin kural tanımları aynı olması gerekiyor. Ya da vendor araştırması yapıyorsun. Aynı kişiden bu hizmetleri alacaksın.
- En temel nokta HTTP 1.0 ve 1.1 için “Transfer Encoding” ve “Content-Lenght” headerlarının protokol için bir anlamı var.

- Ama HTTP 2.0 da bunun hiçbir önemi yok. Böyle bir header yok. Artık binary bir protokol ile karşı karşıyayız. 
- İsteklerin içine id yerleştiriyorlar artık ve adam da bu id değerine göre cevap üretiyor. Yani tek bir iletişim kanalın yok istediğin kadar istek atabiliyorsun. Asenkronizasyon kazandırıyor.
- Binary bir protokol olduğu için requestin nerde bittiğini kontrol etmek için Content-Lenght e bakmana gerek yok. Protokollerin alt katmanında Frame’ler var, frameler içerisinde bitwise kaç bite olacağı yazıyor. Bunun da çok katı bir şekilde validationı yapılması gerektiği söyleniyor. Bu bahsedilen güvenlik açığı böyle bir güvenlik açığı doğrudan yok.
---
![image](https://github.com/grealyve/MDISec-Web-Security-and-Hacking-Notes/assets/41903311/a4296b58-1928-4ea0-a23f-ea581fb0b982)
- HTTP/2: Ttrsequd is Always emeLJarnes Kettle (altimwax)
- Bu adamın farklı bir yaklaşımı varmış :
  - Load balancer HTTP 2.0 ı destekliyorsa, arka taraftaki adama hangi HTTP protokol versiyonuyla yollayacak? Fark etmez.
![image](https://github.com/grealyve/MDISec-Web-Security-and-Hacking-Notes/assets/41903311/0a90a201-3faa-406e-853d-97db87701bcf)
  - Bu da developer açısından şöyle bir sorunu getiriyor: 2.0 ı 1.1 e convert edecek ve arkadaki servis hayatına devam edecek.
  - Ön taraf için hile hurda yapamıyor olabiliriz ama öyle bir HTTP 2.0 paketi yollıcaz ki bu requesti alan yazılım 1.1e döndürdüğü zaman KAFASINDAN duman çıksın.
![image](https://github.com/grealyve/MDISec-Web-Security-and-Hacking-Notes/assets/41903311/efc8df32-cd29-4109-b8c2-5bc0d2f962c6)
![image](https://github.com/grealyve/MDISec-Web-Security-and-Hacking-Notes/assets/41903311/4774380f-486c-41a1-9fa0-1ce73dc30b0a)
![image](https://github.com/grealyve/MDISec-Web-Security-and-Hacking-Notes/assets/41903311/7acb932a-1690-4ac6-b90d-83adcf68b573)
![image](https://github.com/grealyve/MDISec-Web-Security-and-Hacking-Notes/assets/41903311/84866b00-2af0-4d96-a442-2c16d8d060bb)
  - Load balancer ve Web server arasındaki TCP sessionını nasıl yaşattığına bakıyor her şey.
    - Her bir isteği sıfırdan bir TCP bağlantısı kurarak oluşturuyorsa zafiyetlerin hiçbiri olmuyor.
![image](https://github.com/grealyve/MDISec-Web-Security-and-Hacking-Notes/assets/41903311/b7eb5569-e518-427e-b2b6-0d1dda627537)
