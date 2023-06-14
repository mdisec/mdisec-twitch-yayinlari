<h1 align="center">OAuth Zafiyetleri</h1>

## Lab: Stealing OAuth access tokens via an open redirect
- OAuth servisi veren providerlar validationlar yapıyor. Burası çok karmaşık
    - Burdaki URL parser logic bugs konusu buraya girer.
- Belki sadece domain validation yapıyordur. saçma olur bu           .com.hacker.net
- Open-redirection zafiyeti aramaktayız. Ürünlerde “next product” gibi bir şey varsa ve bu da redirection yapıyorsa VE path parametresini de gidip olduğu gibi Response içine yazıyorsa burda open redirection zafiyeti vardır.
![image](https://github.com/grealyve/MDISec-Web-Security-and-Hacking-Notes/assets/41903311/5258b2c5-a00d-4ed5-912c-6b9fe1d77757)
- Giriş yapma requesti bu olacak ama olmadı çünkü path e kadar validation yapmış adamlar.
![image](https://github.com/grealyve/MDISec-Web-Security-and-Hacking-Notes/assets/41903311/6e16a9bc-4079-42a8-b1da-f443f07c3c03)
- /oauth-callback e kadar validation yapmışlar bundan sonrasını kontrol etmiyor. İster yeni parametre ekle path ekle buraya
```python3
https://acOf1f8c1eOae093802e1c3b0075006b.web-security-academy.net/oauth-callback/../../../../post/next?path=http://hacker.com
```
### Bu üst pathe çıkmayı gören server side kısmında(nginx) üst pathe çıkarır ve  “oauth-callback/../../” şu kısmı silerek algılar. Client side’da browser kontrol ediyorsa zaten “oauth-callback/../../” e gitmiş oluruz.
- Doğrudan [hacker.com](http://hacker.com) a gitti yani sunucu tarafına gitmeden Browserdaki bir davranış oluyor.
- Bu istek ile gitti giriş yaptı falan ama olmadı
![image](https://github.com/grealyve/MDISec-Web-Security-and-Hacking-Notes/assets/41903311/15e0d1c9-c8d0-47d7-9fa2-0307274dbc59)
- Bu adam tokenı location hash’e set ederek yolluyor redirecti. Bu browserda kalır sunucuya ve loglara gelmez. JS kodu ile tokenı dızlyabiliriz. 
![image](https://github.com/grealyve/MDISec-Web-Security-and-Hacking-Notes/assets/41903311/253afb74-6410-485d-a283-60439e9748ef)
- iframe ihtiyacı çıktı şimdi. Ama bu iframe içine erişemezsin o yüzden redirectiona ihtiyacımız var. Yapı gereği event message ile data dönüyorsa belki datayı leak edebilirsin
1) MDI kendi web sitesine bir içerik koyuyor, bu içerik iframe ile service provider’a yönlendirme gerçekleştiriyor.
2) Ama bu sayfada bir script var ki sayfadaki location hash bilgisini alıp tekrar kendisine request gönderen ve bu sayede access loguna yazabilme imkanı sağlıyor.
3) MDI web sitesinin linkini kurbana yolluyor ve service provider sayfasını iframe ile açıyor.
4) Provider’da halihazıra giriş yapmış olan kurban, ben seni geri yönlendiriyorum diyor.
5) Sayfadaki open-redirect zaafiyetini kullanarak kendi web sitemize geliyor ve kendi sitemizde(exploit server) adamın tokenını dızlamış oluyoruz.
![image](https://github.com/grealyve/MDISec-Web-Security-and-Hacking-Notes/assets/41903311/eed5c272-d425-4a8c-a1b9-8772a9908d62)
![image](https://github.com/grealyve/MDISec-Web-Security-and-Hacking-Notes/assets/41903311/cd8b2c66-83a7-47c5-b356-d6e34b26364e)
- Sonra çalıntı token ile gidip giriş yaparken /me isteğinde Bearer ile taşıyor. Gelen response’da API key var.
## Lab: Stealing OAuth access tokens via a proxy page
- Giriş yapma isteğinde yine redirect_uri kısmının en sonunu değiştirebiliyoruz eklemeler yapılır.
- Loginden bir şey çıkmadı gibi ama, bir ürün sitesine gittiğimizde aşağıda yorum falan yapabildiğin için comment-form sitesi geldi böyle.
- Bu sayfa yüklendiğinde POST message alıyor ve data olarak windows.location.href basıyor yani URIdan geliyor .
  - Bu sayfa için iframe açarım ve postmessage listener yazarım
![image](https://github.com/grealyve/MDISec-Web-Security-and-Hacking-Notes/assets/41903311/93a78bac-7c8a-4ce6-832d-73192c5e5f9e)
- En son tokenı nasıl dönüyor onu anlamak çokomelli. En son iş bittiğinde location ile bir URI a redirection yapıyor
![image](https://github.com/grealyve/MDISec-Web-Security-and-Hacking-Notes/assets/41903311/fec826c2-06ca-4706-bb0f-ac493fc56b5a)
- Şu tokenı çalarsa yerine geçerim diye düşünüyor, bunun cevabı olarak da redirection gelmiş
![image](https://github.com/grealyve/MDISec-Web-Security-and-Hacking-Notes/assets/41903311/1d27f968-620a-4543-804b-654f66fc207c)
- yine sonrasında Bearerdan token ile gelmiş istek ve API key falan dönüyor buda.
- Tüm redirectionların sonucunda yukardaki postMessage olayına getirmek gerekiyor. (postMessage xss poc)
  - Fetch requesti gönderirken location hashden ötürü browserda kalıyor token kayboluyor.
  - Olay yukarıdakiyle aynı ama JS kodları uğraştırdı. Form kısmı??
- comment-form endpointinde data: “window.location.href” event cevabı döndüğünü görünce bu tokendan gelen şeyi alabiliriz diye düşündü.
- Hemen burdan yürüyüp iframe oluşturdu ve üst satıra çıkıp bu iframeler arası iletişim kurmak için
  - Bir sayfayı iframe ile açtığında “postMessage” ile o iframe ile iletişim kurabiliyorsunuz. Ve bu adam comment-form endpointi de kendisini iframe içinde açanlara hrefi gönderiyor. Bu satır olmasa bi bok yapılamazdı.
  - ![image](https://github.com/grealyve/MDISec-Web-Security-and-Hacking-Notes/assets/41903311/20167b36-8807-4c29-9b3f-8046ed11e9ff)
  - Gidip birisine bu sayfayı iframe ile açtırtıyoruz, açan kişi de zaten authentication providerda aktif bir sessionu olduğu için comment-form endpointine gelecek. Ama bu comment-form iframe’e postMessage gönderdiği için eventListener yazdık.
![image](https://github.com/grealyve/MDISec-Web-Security-and-Hacking-Notes/assets/41903311/3e40e252-bc67-44c7-ad88-b4180f8a3994)
- Tokenı dızladıktan sonra /me den yine API keyi aldık.
- Şu kodda # dan sonrası sunucuya gitmez 😀
![image](https://github.com/grealyve/MDISec-Web-Security-and-Hacking-Notes/assets/41903311/7b4c8dbd-0be0-41b3-921d-90bfe8bc1e75)
