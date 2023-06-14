<h1 align="center">File Upload</h1>

## File Upload Zafiyeti Nedir?
- Security’nin kalbi olan konulardan bir tanesi. Uygulama sunucusunun çalıştığı sunucu üzerine birtakım dosyalar yükleme anlamına geliyor bu zafiyet. Eski geleneksel uygulama mimarilerinden kalan bir zafiyet aslında bu.
- Virtual hostlarda, HTTP isteği geldiğinde önde çalışan Nginx servisinde hangi hosta gideceksen HTTP isteğinin host alanında yazan domainden hangi Virtual hosta geldiğini ve dosya sisteminde hangi pathe map edileceğinin kuralı bulunmakta.
  - /var/www/mdi.com/index.php
- Bu pathin altındaki phpnin çalıştığı işlem ve bu işlemde bir güvenlik zafiyeti çıkması sonucu ortaya çıkar File Upload Zafiyetleri.
- Developerlar, /var/www/mdi.com/public_html/index.php pathini Nginx servisine map ettirirler.
  - /vendor, /controller, /app gibi pathlerin dış dünyadan HTTP aracılığı ile erişilmesini engellerler. Dış dünyadan gelen insanları engellemek için.
- Eski mimaride bir dosya yükleme işlemi yapmak için public_html dosyasının altına “/upload/” şeklinde bir folder tutmak zorunda kalıyordunuz. Çünkü kullanıcıya tekrar sunulabilmesi için, kullanıcının yüklediği dosyalar burada tutulur.
- Bu işin güvenlik kısmı: Kullanıcıdan bir file alınıyor ve birtakım işlemler yapılmakta.
  - Mesela belirlediğin dosya tipleri vardır onları kontrol ediyorsundur. Dosya tipi nasıl belirleniyor?
      - Magic bytes
      - Mimtype : HTTP requestindeki browserın sunucuya gönderdiği dosyanın tipinin ne olduğunu düşünüyorsa onunla alakalı bir konu. Ya da sunucu browsera söylerken
  - Dosya uzantılarını kontrol ediyorsundur.
  - Dosyanın dosya olduğunu kontrolünü sağlıyorsundur.
- File upload zafiyetleri hocanın aklında ikiye ayrılır genellikle:
  - 1- Backdoor : C99, r57
  - 2- Stored XSS : Dosya uzantısını .php gibi şeyler yapamıyor olabiliriz ama .html yaparsak kullanıcının browserına gidecek bir HTML içeriği belirlemiş oluyoruz.
- Günümüzde bu iş ne oluyor? Web serverına gelen bir HTTP isteğinin içerisinde dosya var ise bu dosyayı alıp internal bir API aracılığı ile “minio servisine” ya da “S3 Bucket”a bunu gönderiyor. Bunun karşılığında bir URL alıyor ve bu URLi kendi database sistemine kaydediyor. Yani file sisteme hiç dokunmuyor bile.
  - Kullanıcıya “s.mdi.com” gibi bir Url döndüğü için kullanıcıya ne kadar süreyler buraya erişeceği gibi kısıtları vermek için kullanıcıya özel “Key”ler ürettirme gibi mevzular ortaya çıkıyor.
  - Böyle bir yapı içerisinde File Upload zafiyetini sömüremezsin belki ama düzgün konfigüre edilememiş S3 bucketlarında tüm dosyaları listeleyebileceğin farklı zafiyetler bulabilirsin ama bunun da file upload ile hiçbir alakası yoktur.
## Lab: Remote code execution via web shell upload
- /home/carlos/secret hedefimiz bu dosyayı okumak.
- Sunucuda komut çalıştıran shell execler yapmaktansa bu dosyanın içeriğini okuyan kod yazarız.
- Backend tarafına Content-Disposition headerı gitmesi lazım ki bunun bir file upload olduğunu anlasın.
  - Altında da contentini falan yazmış
![image](https://github.com/grealyve/MDISec-Web-Security-and-Hacking-Notes/assets/41903311/483d5c6c-a63e-4d94-902b-15727a92d2f5)
- Burada dosyanın pathini bulmak gibi bir sıkıntı çıkar.
  - Bu labda direkt vermiş pathi burp interceptionu kapatınca gelen sayfadan okundu: The file avatar/test.php has been uploaded.
- My account kısmından resime ters tıklayıp copy adres dedikten sonra bu sayfaya gidince dosyanın içeriği de gelmiş oluyor. Bu sayede tam pathi öğrenmiş olduk : /files/avatars/test.php
  - Ayrıca bizden aldığı dosyanın adını aynı şekilde değiştirmeden saklıyor.
- Sonra dosya yüklediğimiz istek üstünde aşağıdaki değişiklikleri yaparak farklı bir dosya yüklüyoruz.
![image](https://github.com/grealyve/MDISec-Web-Security-and-Hacking-Notes/assets/41903311/8088cb0d-bfb4-4b61-a944-2621b5003d5c)
## Lab: Web shell upload via Content-Type restriction bypass
- Browser HTTP isteğini sunucuya gönderirken requestin içerisine dosyanın tipi bilgisini yazar. Bu bilgiyi browser, dosyanın magic bytelarına bakarak kendi karar verir. Sunucu da bu bilgiye %100 güvenir ise geçmiş ola.
- Dosya yükleme isteği üstünde değişiklikler yaptı, Content-Type kısmını image/jpeg yazdı. Ayrıca aynı php kodunu tekrar yazdı.
![image](https://github.com/grealyve/MDISec-Web-Security-and-Hacking-Notes/assets/41903311/27848fc7-52f4-4e26-9a61-128972159a6a)
- /files/avatars/test.php pathine gidince flagin geldiği gözüküyor.
## Lab: Web shell upload via path traversal
- Nginx kuralı olarak hiçbir .php dosyası falan kaydettirmeme kuralı oluşturulabilir ve dosya adını bizden aldığının aynısını kaydettiğini biliyoruz bu yüzden dosyanın başına ../ koyunca bir üst dizine gidip kaydedecektir. Fakat bu lab için olmadı.
- Bu kuralı aşmanın diğer bir yöntemi ise bu kuralı bypass edecek .htaccess dosyası yüklemektir. Ön taraftaki Apache’nin davranışını değiştirebilirsiniz bu şekilde. Avatars pathinin altına .htaccess dosyasını böyle yazdığımızda Apache’nin konfigürasyonu htaccessi overwrite ediyor.
  - Şu şekilde bir konfigürasyon yazıp yolluyorsun ve sonrasında .mdisec uzantılı bir dosya oluşturup içine de php kodu yazdığında aynı şekilde çalışacağını göreceksin.
![image](https://github.com/grealyve/MDISec-Web-Security-and-Hacking-Notes/assets/41903311/a743b342-8161-4559-b659-2cb94c9eb6bb)
  - Bir de Apache’nin konfigürasyon dosyasında şöyle bir olay da olabilir; dosya uzantısı şu uzantılarla eşleşenleri php ye ver şeklinde bir kural yazmış olabilir.
- Sonradan şunu kontrol etti; dosya yüklendikten sonra pathini söylediği sayfada “avatars/test.php” şeklinde olduğunu gördü ama bizim payloadın işe yaraması için “avatars/../test.php” şeklinde olması gerekiyordu. Burada bir blacklisting yapılmış olabilir. Tüm slash işaretlerine kızıyor arkadaş.
- URL encoding yaparak dosyayı yüklediğimizde çalıştı.
## Lab: Web shell upload via extension blacklist bypass
- Az önce anlattığı mevzu geldi.
- php uzantılı dosyaları izin vermiyor, tek tek bu şekilde izin verilen dosya uzantısı denencek
  - php5 yüklendi dedi fakat php kodunu çalıştırmadı
  - phtml uzantılı yüklendi ve php payloadı da çalıştı aynı şekilde.
## Lab: Web shell upload via obfuscated file extension
- Dosyanın kesinlikle resim olmasını isteyip, uzantısıyla ilgilenmediği bir durum olabilir. Bu durumda dosyanın metadatasına yazarsın description gibi.
- Dosya uzantısını istediğimiz yapabiliriz ama magic byte gibi değerleri değiştirmemiz gerekebilir.
- Uzantıyı değiştirip yüklemeye çalıştığımızda sadece JPEG ve PNG dosyası yükleyebilirsin diye bir hata verdi. Sonunda Null byte denendi fakat başarılı olunamadı: at%00.png
- Acaba resimin içeriğine bakıyor mu diye kontrol edince kontrol etmediğini öğrenmiş olduk.
- Dosya uzantısında sıkı bir kontrol yapıyor. Dosyanın uzantısını .png ile devam ettirip deneyebilirsiniz. Sonra hangi uzantıyı alıyor diye [at.png.xxx](http://at.png.xxx) şeklinde yazıp kontrol ederseniz sonuncuyu aldığını öğrenmiş olursunuz.
- Null byte olayını tekrar denedi, filenamedeki validationı yaparken en son noktadan sonraki sonucu alıp valide ediyor. Ama Null byte’ın işe yaradığı yer ise string concatenation kısmı. Yani örnek kod şu şekilde olur ve en sondaki .jpg kısmı eklenmez: filename=”/home/application/files/avatars”.$filename
  - Şu şekilde: at.php%00.png deneyince dosyamız yüklendi.
  - İçeriğine de istediğiniz payloadı yerleştirebilirsiniz.
## Lab: Remote code execution via polyglot web shell upload
- Uzantıyı .php ile değiştirip dosyayı yükleyebiliyoruz fakat içeriğine farklı şeyler yazınca hata vermeye başlıyor.
- Php interpreteri, php taglerinin haricinde kalan kısımlarla ilgilenmez. Biz de bunu avantajımıza kullanıcaz.
- Eğer bu sunucu magic byte kontrolü yapıyorsa (ilk 10 byte ya da 20 byte gibi) ilk paragraftan sonrasında ne yazdığı ile ilgilenmeyecektir bu yüzden o kısımları değiştirip dosyayı tekrar yükleme paketini yollayınca kabul etti arkadaş. Buraya php kodumuzu eklediğimizde mis gibi çalışacaktır.
  - Bazı web uygulamaları bu mevzunun yapıldığını bildiği için resmin bütünlüğünden emin olabilmek amacıyla “image resize” ederler. Bu durumda bizim yaptığımız çalışmayacaktır. Bunu atlatmak için ise exiftoolu kullanırsın böylece resmin bütünlüğünü de bozmamış olursun.
  - exiftool -overwrite_original -DocumentName=”selam<?php echo 123;?>” at.png
## Lab: Web shell upload via race condition
- Kodlar line by line çalışır ve kodun başında dosyayı yaz(writing) diyip sonunda da sil(delete) diyebilir. Ama kodun ortasında bir yere kısa bir süreliğine Cache yazıyor olabilir. Burada iki tane thread açacaksın, threadlerden biri Writing requestini hayvan gibi spamleyecek diğeri de Cache pathine GET isteği atacak. Sen öyle bir durum yakalaman lazım ki HTTP sunucusu dosya kaydetme requestini aldıktan sonra delete gelmeden senin requestini çalıştırıp backdoor gelmeli. Race condition budur. Kaynak kod olmadan bunu bilmek zordur ve ayrıca internet üstünden exploit etmesi de zordur.
- Tek tek sunucunun dosya yüklerken ne kontrolleri yaptığına baktı önce. Php dosyası yüklemeye çalıştı olmadı, Content-Type headerını değiştirip dosyanın uzantısına .jpeg ekleyince burada başka bir şey var dedi. Null byte denedi olmadı.
- Dosyayı kaydedip validation yaptıktan sonra siliyor olabilir mi? Normal bir resim yükledikten sonra resim duruyor öyle değilmiş.
- Burada farklı durumlar da olabilir race condition için.
- PHP interpreterine siz bir HTTP POST requesti ile dosya gönderdiğiniz zaman dosyayı adam geçici olarak “/tmp/var/php” gibi pathe kaydeder webden erişilebilen bir yer değildir ve dosyanın adı da random olur. Bu labda eğer dosyayı yine /files/avatars altına aynı isim ile koyup ardından file name üzerinden validation yapıp, validation uymuyorsa dosyayı siliyorsa bu challange bu şekilde çözülebilir. Fakat gerçek hayat senaryosu değildir bu. “at.jpg” dosyasının içeriğinin validationını yapmaması gerekiyor bu durumda ki sistem mantıklı otursun. Bunu da içeriği 1111111 olan dosya yükleyip curl ile kontrol etti.
- Burada içinde php payloadı yüklenmiş bir at.jpg dosyası yükledik duruyor. Sonra aynı içerikli at.php dosyasını interpretera yükletmeye çalışacaz bunu da POST isteğine gereksiz bir parametre ekleyerek yapıcaz. Sonra GET isteği ile bu yüklenecek /files/avatars/at.php dosyasını çekeceğiz ve flagi kapıcaz.
