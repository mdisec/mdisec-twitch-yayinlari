<h1 align="center">Session ve CSRF Zaafiyeti</h1>

# Protokollerin Durumu Nedir?
- TCP handshake karşıdaki kullanıcıyı doğrulamanı sağlıyor. Karşındaki insanı doğrulabiyor olması en büyük artısı.
- HTTP’nin en büyük eksikliklerinden biri karşındakini doğrulayamıyor olman.
- HTTP’nin diğer en büyük eksikliği State/Stateless durumları.
- HTTP’de önemli bilgiler “header” kısmında gider; host, cookie, bağlantının devamı gibi… Body kısmında data gider.
![image](https://github.com/grealyve/MDISec-Web-Security-and-Hacking-Notes/assets/41903311/faba6055-2cd8-4b15-a356-a71b563ba059)
- Her paket gittiğinde kullanıcı adı ve parola istememesi için cookie yöntemi kullanılıyor.

## Cookie Mekanizması Nasıl Çalışıyor?
- **Bir Websitesi neye göre Cookie Set ediyor?  —→ http://www.mdisec.com:80/**
    - **Protokol**
    - **Domain(subdomain dahil değil yani değişse cookie düşer)**
    - **Port**
![image](https://github.com/grealyve/MDISec-Web-Security-and-Hacking-Notes/assets/41903311/300c981f-4ef8-4066-9d5b-50443fcb65eb)
- path : Bu cookie’nin hangi sınırlar içinde kullanalıabileceğini belirler.
### Cookie değeri senin “session”a ulaşman için gerekli anahtar. Cookie’yi alan Reverse Proxy senin hangi sunucuya(1,2,3)’e gitmen gerektiğini yönlendirmesini yapıyor.
## Cookie Nerede Saklanır?
- Cookie oluşturmak adına başlattığın sessionlar /tmp/disk’e yazılır.
    - Session : Cookie’nin bilgilerinin yazıldığı ve tutulduğu bir bilgi topluluğu. %90 sunucu tarafında gerçekleşir yani clientin kendi tarafında değiştirebileceği bir şey değil.
1) Session oluştuğunda sunucu tarafında diskte tutabilirler ama bu diskte IO işlemine sebep olur. Sistemi yavaşlatır yani.
    - Kullanıcı her istek attığında sen bu cookie’yi alacaksın
    - diskteki hangi session hangi session folder’ı bununla alakalı bulacaksın dosyayı okuyacaksın
    - Session’a bir şey yazdığında dosyayı update edeceksin
2) Web app. sayısı artarsa ve gelen requestleri dağıtmak için ön tarafa reverse-proxy(LOAD BALANCER) konursa içeride sessionu sunucu ile senkronize etmen gerekecek. Yani diskte tutulmaması gerekiyor DB’de tutulabilir.
    - DB içinde tutulmasının da dezavantajları var. Yük ve performans konusu devreye giriyor.
    - Birden fazla DB varsa SQL Proxy gerektiriyor. Bunun da yerini Mikroservisler alıyor(?)
    - Bütün web app. lerin statik dosyalarda aynı içerik olması için CDN de gerekiyor. Cloudflare gibi programlar ile bir dosyanın ya da HTTP response’unun kolaylıkla yapılabilmesi sağlanır.
3) Content Delivery Network: Hiçbir diske dokunmayan, işletim sistemi aracılığıyla memory’de key-value şeklinde veri tutan servis. CDN
    - Memory’de tuttuğu için çok hızlı oluyor.
    - Integrity’ye güvenemiyorsun. CDN patlarsa en kötü 302 Redirection alır.
    - Bunun da backupını alman lazım.
4) Cookie Based Session : Client tarafında tutmak. Cookie yi json olarak veriyor server.
    - **Yani adam sana kul. adı parola ile geldi sen bunu aldın doğruladın ve bu adamın bilgileri ve permissionlarıyla bir obje oluşturdun, bunu SYMMETRIC ENC ile şifreledin(şifrelerken application settings tarafında set ettiğin secret keyi kullandın), sonra bunun HMAC ile signiture’ını aldın, adamın eline bunu verdin. —> Single Sign On bu mantıkta çalışıyor.**
    - SUNUCU TARAFINDA CONFIG DOSYASINDA BULUNAN SYMMETRIC ENC SUPER SECRET KEY ..!
    - Set-Cookie : SESSION={’IV’:’RANDOM_DEGER’, ‘session_data’: [’email’, ’user_id’]} | CHECKSUM
        - [’email’, ’user_id’] = ENCRYPTED
        - [Hiçbir verinin değişmediğini garanti etmek için]CHECKSUM = HMAC( {’IV’:’RANDOM_DEGER’, ‘session_data’: ENC}) | + KEY
            - Signiture olmuş olur elinde bunu da BASE64 ile encode edersin.
    - Bu mevzunun geliştirilmiş hikayeleri var : Openid, OAuth aynı mantık üzerinde ama farklı şekilde çalışıyor.
## CSRF (Crosss Site Request Forgery) Zaafiyeti
1.Tab içinde 18.132.45.78 sitesinde login olmuş kullanıcı var | 2.Tab’da hacker.com açık.
![image](https://github.com/grealyve/MDISec-Web-Security-and-Hacking-Notes/assets/41903311/1adf8a18-2f7b-4b6e-9e3f-477d2a69f6f8)
- hacker.com’a gittiğinde bu resmi yüklemek için o http isteğini göndermek zorunda. O webb sitesine GET talebi gönderiyor, browser da Cookie’yi otomatikman ekliyor.Domain, protokol ve port koşulları sağlandığı için Cookie buraya da set edilecek.
- Browser, kullanıcının bu talebi isteyerek mi oluşturduğunu anlamak zorunda.
    - CSRF token oluşturup sunucuya göndermesi gerekiyor.
![image](https://github.com/grealyve/MDISec-Web-Security-and-Hacking-Notes/assets/41903311/4e295702-a989-4fad-9721-b1dc34928a12)
- Bu token bu session’a özel üretir.
- Bu tokenı http://18.132.45.78/address/delete/17/?_token=alskhfasuklhfasjlfasjdhask 

- Bu CSRF token bilgisi nerede tutuluyor?
    - Session nerede tutuluyorsa orada tutulur. Fakat token’ı illaki sessionda tutmak zorunda değilsin. User’ın kendi Cookie’sinde de tutabilirsin.
- REST API kullanılırsa?
    - Cookie diye bir şey olmaz. Origin diye bir şey olur. Doğası gereği CSRF zaafiye olamaz burda.
![image](https://github.com/grealyve/MDISec-Web-Security-and-Hacking-Notes/assets/41903311/ae0bbfac-ba4f-4b2a-a976-ad4e29a19bad)
Autharization diye bir header’ın olacak, oturum anahtarını burada taşıyacaksın
