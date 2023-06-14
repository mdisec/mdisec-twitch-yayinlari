<h1 align="center">Bir Hacker'ın Gözünden Modern Web Nasıl Çalışır?</h1>

#### Not: İlk kısımları bildiğim için not almayıp atlamıştım. İlerleyen zamanlarda ekleyeceğim.

- Bilgisayar ilk açıldığında 192.168.1.0 broadcast yapıyor ve ip adresi istiyor. DHCP Protokolü ile alıyor ip adresini.
- Bilgisayarlar birbiriyle konuşmak için MAC adresini öğrenecek bunun için Layer 2’de ARP protokolünü kullanıyorlar ve OS ARP Table oluşturuyor.
- Bilgisayarı açtığında DNS’i ve Gateway’i manuel olarak girmiyorsun. Bunları DHCP sağlıyor.
- Bir ip adresinin LAN içinde olduğunu anlaması Subnet Mask sayesinde oluyor. 255.255.255.0. Bilgisayar konuşmak istediği ip ile subnet mask ip’nin bit karşılıklarını yazar 1-1 işleme sokar ve çıkan sonuca göre karar verir.

- [www.google.com](http://www.google.com) ‘a gitmek istediğinde
- DNS’e koşmadan önce bilgisayar “*Host*” dosyasına bakmalıdır. /etc/hosts burada bulamayınca DNS’e soracak:
    - DNS’e(8.8.8.8) UDP protokolüyle 53 numaralı porta x.com’un ipsi ne? - Resolver DNS
- Resolver DNS bilmiyor ise, Root DNS’e gider sorar. O da bu ip adresinin kim olduğunu bilmediğini ama nereden öğrenebileceğini söyler yani Top Level Domain’e yönlendirir(TLD *.com/.net/.org).
- TLD de x.com’un kayıtlarını tutan adama yönlendirir. Authoritative DNS (Yetkili DNS) e yönlendirir. Yani kurumun DNS’i sanırsam.
    - dig NS google.com

##  Ne Gibi Riskler Var?
- Başka biri 8.8.8.8’e gittiğinde bütün süreç tekrar yaşanmayacak çünkü TTL’lere göre Cache’de tutma mekanizması var.
    1) Bu Cache’i poison edebilirsen x.com’a gidecek HTTP paketlerini istediğin gibi yönlendirirsin.
    2) Authoritative DNS sunucusunu ele geçirirsen, MX kayıtlarını değiştirirsin bütün e-postaları üstüne alırsın, Cname ağ recorlarını değiştirirsin tüm kayıtları üstüne alırsın, .txt kayıtlarını değiştirirsin sertifika issue ortaya çıkar.
    3) TLD saldırıları sıkıntı, tüm *.com cevaplarını yanlış döndürebilir sana.

## Bir IP ile Konuşmak
- Ip adresinin 80 portuna TCP SYN paketi yolluyor üçlü el sıkışma tamamlanıyor...
```
SYN —>
    <— SYN + ACK
ACK —>
```
![image](https://github.com/grealyve/MDISec-Web-Security-and-Hacking-Notes/assets/41903311/3e39b107-2cd6-4e9c-92d2-fae4b61b8f0f)
- Şimdi artık HTTP yollayabilirsin. 1 HTTP GET ve response aldığında aşşağıdaki katmanlarda 150 tane istek gidip geldiğini görebilirsin ve bu da HTTP’nin boktanlığından kaynaklanır.
## Sunucular Bölgesi (DMZ)
- 80 ya da 443 numaralı porta gittiğinde aslında sen Firewall üstünden geçiyorsun. Peki bu firewall nedir?
    - Firewall: Network management toolu. Şu sourcedan gelen şu portla konuşur/konuşamaz işini yapıyor.
    - TCP SYN Attack: TCP paketinin içinde “Source” kısmına random bir ip adresi yazarsın ve web sunucusuna yollarsın, web sunucusu da başka bir adamla konuşmaya çalışır kaynaklarını tüketir(SYN Fload). Kaynağı az olduğu için firewallun hayvan gibi bir gücü olur ve onunla üçlü el sıkışmayı yaşarsın. Firewall DDoS engeller olayını böyle düşün.
- Firewall’u geçtikten sonra web sunucusuna geliyorsun. Bu web sunucunun üstünde neler var; Apache/nginx, Php-FQM, MySQL, Static dosyalar…

## Virtual Hosting (VHOST)
- Domain sayısı ip sayısını geçtiği için böyle bir şey ortaya çıkmış.
- Host firmasının konfigürasyonuna göre hangi siteye gidiyorsan sana /var/www/… sitesine yönlendirir.
![image](https://github.com/grealyve/MDISec-Web-Security-and-Hacking-Notes/assets/41903311/41ed88da-da31-470e-b527-ddf077bf9eeb)
- Bunun bir e-ticaret sitesi olduğunu düşün çok satış yaptığı dönemlerde bu sunucu yetmiyor. Eskiden RAM eklerlermiş, günümüzde ise bir tane daha web sunucusu kurulabilir. Kod baseini, kaynak kodlarını da hepsine ekleyem sonra DBler de kurayım. Bu sistem içerisinde sana ReverseProxy(LoadBalancer)’a da ihtiyacın var.
![image](https://github.com/grealyve/MDISec-Web-Security-and-Hacking-Notes/assets/41903311/926920df-58fe-4232-8c5f-6031bbf8b554)
- Burada artık farklı sorunlar da yaşanmaya başlıyor:
    - Eğer session diskte tutuluyorsa bu adamın tüm requestlerde aynı yere gelmesi gerekiyor. Çünkü bu session ilk sunucuda bulunuyor diğerlerinde onun bilgisi yok. İlk sunucu çökerse adam log out olacak gibi sıkıntılar.
    - Cloudflare cookiesi ne işe yarıyor?: Reverse Proxy senden gelen isteği hangi sunucuya yolladığını bir cookie ile bildirip kendi üstünde tutuyor, sunucu tarafına geçmiyor. Bir sonraki gelişinde de diyor ki ben bu adamı daha önce şu sunucuya yolladım tekrar oraya gitsin.
    - Databaselerden biri düşerse ne olacak? Aktif mi pasif mi çalışacak? Birden fazla DB olursa SQL Proxy Servisine ihtiyacın var. Tüm SQL sorgularını SQL Proxy’e soruyorsun, o senin için hangi DB uygunsa ona soruyor. Günümüzde “Mikroservis” yapıları buradan ortaya çıkıyor.
    - Session nerde tutulacak peki?: Session servisleri ortaya çıkmaya başladı Redis, Memcached gibi… Yani en baştan requestimiz geldi, web sunucumuza gitti oradan SQL proxy ile DB’e soruldu ardından onaylandı, web servisi session oluşturduu veee Session servisi üstüne yazdın bunu.
    - Statik dosyalar mevzusu: Sunucuya bir dosya yüklüyorsun ve sadece birisinde kalıyormuş gibi oluyor. Bunun olmaması için CDN gerekiyor.
- Bütün web app. lerin statik dosyalarda aynı içerik olması için CDN(Content Delivery Network) de gerekiyor. Bütün millet bir resimin yüklenmesi için gelip senin CDN sunucuna istek atmaması için, Cloudflare gibi programlar ile bir dosyanın ya da HTTP response’unun kolaylıkla yapılabilmesi sağlanır(resimin cache i dönüyor adamlara). Mesela bir resimin yüklenmesi, Farklı ülkelerdeki kullanıcılara teker teker sunucu isteği atılıp gönderilmez de Cloudflare üzerinden(burada Firewall ve Reverse Proxy ikilisi oluyor) otomatik gönderilir. Tüm trafik bu CloudFlare üzerinden akıyor, Çin’deki bir adama da resimin aynı cache değeri dönüyor yani sadece güvenlik değil mesele. Ayrıca senin evinde yaşanan olayların aynısı içerideki sunucuda da yaşanıyor.
![image](https://github.com/grealyve/MDISec-Web-Security-and-Hacking-Notes/assets/41903311/3e675dff-f89b-44c6-bfb5-df8df554ac7e)
- Full text searchleri veri tabanı üzerinde yapılması sonucu ortaya çıkan maaliyetleri engellemek için : Elastic Search
- Sunucuya gelen bütün HTTP isteklerinin “Loging” ini tutan sunucular bulunur.
- Bu sunucunun da aynısının yedeğinin bulunduğu bir sunucu daha olur : DRC
    - Olur da sistemin çalıştığı data center patlarsa tüm trafik hiçbir kesinti yaşanmadan DRC hizmet verir.
- SSL Reverse Proxy kısmında sonuçlanıyor. HTTP requestini işleyip inceleyen adam reverse-proxy. HTTP Desync açığı çıkabiliyor sunucu başka görüyor, RP başka görüyor.
