<h1 align="center">OAuth Zafiyetleri</h1>

#### Client application : X web sitesi

## OAUTH Nedir?
- Başka bir web sitesine bilinen sosyal medya hesaplarıyla giriş yapmadır aslında. Bir kişinin iznini(consent) başka bir web sitesindeki bilgilerine erişim sağlamaktır.
  - consent: provider kullanıcıya ben senin şu şu bilgilerini paylaşıcam diyor. Tamam deyince birtakım bilgiler dönüyor ve arkadaş token ile birlikte X web sitesine gitmesi gerekiyor.
- Bir web sitesinde bir kullanıcıya bir dünya form doldurtmak yerine, facebooktaki bilgilerini kullanarak(artık facebook hangi bilgilerini paylaşmak istiyorsa, ismini cismini epostasını…) kullanıcı oluşturma işlemi sağlar. Eposta onaylatmadır falandır o süreçleri hiç yaşamamak için.
- Gelen kullanıcıyı provider her kim ise ona sektirip, geri sektiğinde sana birtakım bilgiler ile gelmiş oluyor.
- Peki birtakım bilgiler paylaşabiliyorsak ben bu kullanıcı adı, parola falan kendi tarafımda tutmayayım her benim sayfama giriş yapmak istediğinde gitsin facebooktan authentication sağlasın ve geri geldiğinde valide olduğunu bileyim.
  - OAuth kullanma şekillerine göre arka tarafta farklılık gösteriyor. [Flows]

- OAuth’da HTTP yi düşündüğünde birtakım sorunlarla karşılaşacaksın. Bir web sitesiyle kullanıcı konuşuyor ve onu valide etmek için başka siteye yönlendiriyor. Bu web siteleri kendi arasında  bilgi paylaşımı yapamıyor CORS mevzuları girer, iki ayrı tab bunlar zaten. Provider bu adamı doğruladıktan sonra geri *X web sitesine yönlendirmesi gerekiyor(browser’a söylemesi lazım)* ve o paketin içerisine de birtakım  bilgiler yazması gerkeiyor(*code*). Bu kodu(token) X web sitesi gidip provider’a sorduğunda işte bu kişi Joseph Stalin diyebilir. Bu 2FA olabilir başka bir şey olabilir..
  - Bunu cookie bazlı yapamaz, başka bir domain için cookie set etmesi gerekiyor ayrıca cookie’nin doğruluğu ne?
![image](https://github.com/grealyve/MDISec-Web-Security-and-Hacking-Notes/assets/41903311/eb80499e-6b2a-4932-bf3c-cef6b466abf4)
- Her çeşit providerdan çıkan token farklıdır.
## Lab: Authentication bypass via OAuth implicit flow
- Logine tıkladığında bir tane endpointine gidiyor web sitesinin.
![image](https://github.com/grealyve/MDISec-Web-Security-and-Hacking-Notes/assets/41903311/ded6bd5a-1343-44e5-b8bb-9607d44ada02)
- Scope’da sizin OAuth service provider’dan hangi bilgilere erişim sağlayacağınızın kapsamını belirttiğin alan oluyor.
- redirect_url : Authentication tamamlandığında ben tekrar bu web sitesine geri gelmek istiyorum.
- nonce : CSRF zafiyetinin OAuth flowlarını engellemek için konulmuş kod.
- Gerçek hayatta Redirect edip  başka bir web sitesine götürmeli.
  - !!! Bu isteği birden fazla gönderince interaction tokenını (response tarafında) değiştiriyor mu??
- Gidip login olduk.
![image](https://github.com/grealyve/MDISec-Web-Security-and-Hacking-Notes/assets/41903311/84fb8a42-9dbc-49c8-9f5d-8ef5632bdbb2)
- Kullanıcı adı parola doğruysa geldiğimiz siteye geri yönlendirmeli. Başlangıçta ürettiğimiz kodla redirection yaşadık
![image](https://github.com/grealyve/MDISec-Web-Security-and-Hacking-Notes/assets/41903311/dfa851c0-9a9d-4231-b768-980e7af787b9)
- Provider, senin şu bilgilerini paylaşıcam diye bilgilendirme yapıyor. OK dedik
- En sonda callback parametresine götürdü bizi. Cookie ile session oluşturmuş. OPTIONS ile değerler var. me parametresine gitti.
- Veee arada /authenticate diye POST requesti çıktı karşımıza.
  - provider kullanıcıya ben senin şu şu bilgilerini paylaşıcam diyor. Tamam deyince birtakım bilgiler dönüyor ve arkadaş token ile birlikte X web sitesine gitmesi gerekiyor.
  - Ama bu işlem, vatandaş gidip username passwd ve token gibi değerlerini alıp provider’dan alıp, tekrar X web sitesine POST req. olarak yollarsa işte o requesti tutabiliyor
  - Bu tasarımda token, adam gidip tekrar provider’dan bilgilerini almak için kullanılıyor.
![image](https://github.com/grealyve/MDISec-Web-Security-and-Hacking-Notes/assets/41903311/71cfc98b-ad7b-41e8-aa2d-24a29ccb3517)
- Ameleliği vatandaşa yüklüyor ama spoof da edilebiliyor bu iş.
- Burda da e maili değiştir.
## Lab: Forced OAuth profile linking
- “nonce” gibi CSRF engelleyici token yok ise, ben gidip birine OAuth linki verdiğimde ya da bu linke yönlendiren bir web sitesine çekebilirsem ve sen gidersen sonra da authentication tamamlanıp gerisin geri redirection callback URL’in neyse o web sitesine gideceksin.
- Web sitesinin hangi bilgileri isteyeceği scope’da belli oluyor.
- client_id : Provider hangi web sitesi için auth sağladığını bilmek için.
![image](https://github.com/grealyve/MDISec-Web-Security-and-Hacking-Notes/assets/41903311/b98db784-2474-434f-9072-8e4ccba62ad3)
- Provider kısmına gidip login olunuyor. Halihazırda login olmuş olunsaydı belki kul. adı parola sormayabilirdi.
  - Ters tıklayıp responselara da bakıyor.
- Burda bir kod ile redirect ediliyoruz. Bu kod 1 kere mi kullanılıyor acep?
![image](https://github.com/grealyve/MDISec-Web-Security-and-Hacking-Notes/assets/41903311/be2da893-2661-4c15-8610-d8e3f712bd96)
- Bu kodla ana uygulamaya geri gelmedik. Bu istek ile orjinal siteye geri dönüş yapılıyor. CSRF token da yok.
![image](https://github.com/grealyve/MDISec-Web-Security-and-Hacking-Notes/assets/41903311/b4dbd639-db80-4ea9-a33e-0f46e66c0439)
- Bu URL’i admine bu sosyal medya hesabını bağlıyacağız. Bu istekle birlikte bizim sosyal medya hesabımız adminin hesaba  bağlanacak. Sonra biz de sosyal medya hesabımızla siteye giriş yapıcaz.
![image](https://github.com/grealyve/MDISec-Web-Security-and-Hacking-Notes/assets/41903311/3ad0ab6d-868b-44df-8ae4-0bed6457de3b)
- MDI reisin social medya kodu buymuş hacı diyor amaa CSRF token yok buradaa
![image](https://github.com/grealyve/MDISec-Web-Security-and-Hacking-Notes/assets/41903311/7b1268b9-9eef-4c44-8573-65a072514367)
## Burası Çokomelli!!
- Burada başka zafiyetler de çıkabilir.
![image](https://github.com/grealyve/MDISec-Web-Security-and-Hacking-Notes/assets/41903311/451933c4-8c16-415c-8a0b-a9ae6881c4ed)
- Client_id niye var? Çünkü bir providerdan OAuth servisi almak istediğinde adam sana hangi adrese geri redirect edileceğini veya trusted-domain listesi gibi özellikler ister ki bu id ile gittiğinde provider kayıtlarından bakıp redirect edilebilir izinli domainler görebilsin ve seni geri yönlendirebilsin.
  - Birden fazla domainde OAuth servisi kullanmak isteyebilirsin. O yüzden bu redirect_uri üstünde validationlar yapılır. Validationı atlatırsan ne olacak? Validationı atlatamadın, gittin bu domain üstünde open-redirect zafiyeti keşfettin ve kendi web sitene redirect ettirdin ve adamın kodunu çaldın.
![image](https://github.com/grealyve/MDISec-Web-Security-and-Hacking-Notes/assets/41903311/14c0b6b8-3378-41de-839b-cc0288c15f13)
## Lab: OAuth account hijacking via redirect_uri
- Eğer Return URL üstünde itlik kopukluk yapacaksak ilk istek üstünde durulmalı
- redirect_uri kısmına istediğini yazıp isteği yolladığında sana hala geçici bir token vermeye çalışıyor adam. Yani burada hem senden alıyor URI ve validation yapmıyor bunun üstünde.
- collaborator URLi verdi oraya
- Sonra o HTTP requestini gitti admine tıklattırmak için exploit servera yazdı.
- Sonra sosyal medya ile giriş yaptı ve en son paketi yakalayarak Collaboratora gelen çalıntı istek kodu ile isteği iletti ve admin oldu.
