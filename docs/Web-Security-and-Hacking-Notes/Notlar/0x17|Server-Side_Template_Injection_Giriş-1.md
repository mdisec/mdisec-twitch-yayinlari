<h1 align="center">Server-Side Template Injection</h1>

#### Template engine’ler sandbox yapısına sahiptirler genelde ve burda çalışırlar.
- Uygulamalarda MVC(Model View Controller) yaklaşımı işin içerisine girdiği zaman, elimizde bir controller() var ve bunun da return(view) edeceği bir view var.
  - View yeni bir atak vektörü oluşturmuş oluyor bize.
- HTML implementasyonu değil de, bir template implementasyonu yapmaya başlıyoruz. Özelleşmiş HTML gibi.
- Backend DB’den veya kullanıcıdan gelen bir inputu name olarak buraya yerleştiriyor. Burda bir ***dinamik kullanım*** oluşuyor.
![image](https://github.com/grealyve/MDISec-Web-Security-and-Hacking-Notes/assets/41903311/d8aba6e4-a703-4dca-8cce-9e88ce1b25b8)
- Ama bu konu ise, dinamik olarak bir HTML oluşturmanı gerektiren bir konu. Mesela sahibinden’de ilanların açıklama kısımları gibi. Ya da “sendgrid” gibi.
  - User’dan template’in kendisini alıyorsun artık.
![image](https://github.com/grealyve/MDISec-Web-Security-and-Hacking-Notes/assets/41903311/4f036ff4-f6ec-4c65-a540-190b329da802)
- Bu template’in içerisinde bir obje varsa ve fonksiyonları çağırmaya başlarsa neler olabilir? Sunucu içerisindeki fonksiyonlara erişirsin belki? 
![image](https://github.com/grealyve/MDISec-Web-Security-and-Hacking-Notes/assets/41903311/38d71ac9-0fcb-467a-8089-9bd847bbd6c1)
- Kaynak koda erişimimiz olmadan nasıl tespit edebiliriz?
![image](https://github.com/grealyve/MDISec-Web-Security-and-Hacking-Notes/assets/41903311/70ea9450-2377-4925-93cd-1321fd471a05)
## Lab: Basic server-side template injection
- Zafiyetin nerde olduğunu tespit edebilmek için gezindi. Sonra bir ürün listeleme isteğine baktı, 1.satıdaki parametreyi kurcalamaya başladı.
  - Geçerli olmayan bir integer değer girdi “Not found” hatası geldi.
  - String ifade yazdı, bu sefer de invalid hatası geldi. Demek ki buna göre kontrol ediyor.
- Sonra gitti 1 yazdı productId olarak. 302 döndü ve follow deyince bir sayfa geldi, parametre olarak da bizden “Unfortunately… “ mesajı almış ve cevaptaki sitede de bu mesajı yerleştirmiş.
- İlk olarak aklına reflected XSS gelebilir.
![image](https://github.com/grealyve/MDISec-Web-Security-and-Hacking-Notes/assets/41903311/e0d3e6cc-2763-42b4-b915-8183b4c47506)
- Template’e bizden gelen parametreleri koyuyor olabilir django, laravel gibi kütüphanelerde render methodu oluyormuş. Arkadaki Template Engine’i tespit etmek için ise, XSS taglarinin peşinden
  - { {xx} } % {yyy} %${zzz}
  - Ya da { {7*7} } deneyip sonuçta da 49 olarak görmeyi beklersin. Kesin olarak Template Injection var diyebilirsin.
  - Bunun aynısı geliyor ise birtakım problemler var demektir.
- Bilmediği bir template engine var. Lab sayfasında ERB template yazıyor. Araştrma zamanı:
![image](https://github.com/grealyve/MDISec-Web-Security-and-Hacking-Notes/assets/41903311/50b41306-9f8f-43a5-8fd1-0637f0dd3c3c)
![image](https://github.com/grealyve/MDISec-Web-Security-and-Hacking-Notes/assets/41903311/2519a44b-8a4f-4509-8291-defdf9bde699)
- Artık ERB ile bir işletim sistemi komutu çalıştırabilir miyiz?
  - Backend’de komut çalıştırabildiğin zaman, sunucuda da komut çalıştırabiliyorsun zaten en büyük etki de böyle oluyor.
- Ruby ERB template injection araştırılıyor.
![image](https://github.com/grealyve/MDISec-Web-Security-and-Hacking-Notes/assets/41903311/884291e4-0ec2-4c9f-a913-480a83527249)
- Pek çok payload kodu var işte.
![image](https://github.com/grealyve/MDISec-Web-Security-and-Hacking-Notes/assets/41903311/0917b063-a514-4e0a-a3f9-1c6b1676ee15)

- Sistem komutu da çalıştırılabiliyormuş. Burdan sonra reverse shell’e gidersin.
![image](https://github.com/grealyve/MDISec-Web-Security-and-Hacking-Notes/assets/41903311/7e271383-a292-4fd2-92d6-e991b10bfe2a)
## Lab: Basic server-side template injection (code context)
- Kullanıcı girişi yapıyorsun, my account tarafında.
![image](https://github.com/grealyve/MDISec-Web-Security-and-Hacking-Notes/assets/41903311/0c2d1c7a-8f93-4089-a420-5b7ba1cf761e)
- Ayarlarda kullanıcının hangi ismiyle forumda gözükeceğeine karar veriyorsun.
- Tonardo engine {{}} şeklinde kullanıyor diye öyle yazdı ama adam zaten onun içerisine koyuyor parametreyi o yüzden gerek yok.
![image](https://github.com/grealyve/MDISec-Web-Security-and-Hacking-Notes/assets/41903311/81ee291c-8fdd-437e-ac18-73b1c094fe00)
- object yazınca objeyi direkt bastı yoruma. Objeyi enumerate edebilir
- python komutları denedi, code evaluation var diyor.
- asfasjhd yazınca da hata aldı buna da normal dedi çünkü string bir şey oluşturuyor, sonra gitti kaynak koda baktı.
- import os yapmaya çalışıyor, \n falan denedi, {%import os%}
  - importun farklı bir yöntemini bulmak lazım.
- doğrudan bir python kodu yazmak lazım.
- en son şunu yazdı: __import__(”os”)
  - farklı bir import şekli
  - __import__(”os”).system(”rm -rf
  - /home/carlos/morale.txt”)
- Bu template engine, oluşacak template’i satır satır ayırıyor ve aldığı inputu string olarak evaluate ediyor ama sandbox içinde çalışmıyor sorun orda.
## Lab: Server-side template injection using documentation
- Rich-text’i kullanıcıdan alıyor, bu uygulama da java.
![image](https://github.com/grealyve/MDISec-Web-Security-and-Hacking-Notes/assets/41903311/52b8f3b1-9092-4ede-8313-8a5019fe4312)
- Öncelikle ${Object} deniyor hepsinde. Bu örnekte FreeMarker template engine varmış.
- illa gidip ${asfsa} bu şekilde devam etmen gerekmiyor. Bütün taglere, macrolara falan erişim var.
- İnternetten bu template injectionu için döküman inceliyor.
- Kendi localinde böyle bir ortam oluşturmak lazım, break point markerlar ile dökümantasyondan inceleyerek ilerlersin. Bir sınıf nasıl initiate(oluşturulur) edilir ona bakmak lazım. Bu iş öyle ilerliyor.
- Exec class’ını oluşturmayı öğrenmek lazım sonra exec fonksiyonlarını kullanarak çözecek.
- Backend’de objectconstructor set edilmiş. Sonra assign edilmiş bu obje.
![image](https://github.com/grealyve/MDISec-Web-Security-and-Hacking-Notes/assets/41903311/e714abfc-c885-4864-9e6f-900f112a53e7)
- Google’dan da bakıp çözülebilir ama bakış açısını göstermek için sağ sol yapıyor. Class oluşturma yöntemlerine bakıyordu.
- Bir rapordan bunu buldu. Execute adında bir sınıf var(full ismini yazmışlar oraya) yeni bir sınıf oluşturuluyor ondan. İşletim sisteminde komut execute ediyor bu sınıf.
![image](https://github.com/grealyve/MDISec-Web-Security-and-Hacking-Notes/assets/41903311/37592f5b-2602-448a-bf47-f536dc47edb8)
---
![image](https://github.com/grealyve/MDISec-Web-Security-and-Hacking-Notes/assets/41903311/44b2125c-a934-4ef1-a90b-e1ecdcb53b0b)
Gelen eposta içeriğini Server side render etmiş Uber. Tabiki render edecek ki oluşan içeriği mailin içerisine yazsın.
---
## Lab: Server-side template injection with a custom exploit
- Giriş yapıldı, avatar gelmiş bu sefer.
- Resim yükledikten sonra kaynak koda baktı bu resim nerden geliyor gibisinden.
- Böyle bir path’den çekiyormuş avatarı. Weiner’ı değiştirse orada bir template injection olabilir.
![image](https://github.com/grealyve/MDISec-Web-Security-and-Hacking-Notes/assets/41903311/4b84e5ae-cd6f-4c7d-a246-d9a59f1bb9c6)
- Bir gönderiye gidip yorum yazdı ve orada da kaynak koda baktı.
- Change email kısmında template injection denedi.
- Avatar yüklediği paketi inceliyor. Resim olarak göndermeyeyim dedi sonra username’i bizden aldığını gördü şunu denedi ve “Unauthorized” hatası geldi.
![image](https://github.com/grealyve/MDISec-Web-Security-and-Hacking-Notes/assets/41903311/d1c5517d-d224-4c7d-a318-6c5ed335c5b1)
- Resim yerine asfasfas yazdı ve istek gitti. Resim isteğini çağırınca asfasjagsjd{7*7} falan geldi çok saçma…
- resim yükleme paketinde Content-Type’ı text/html yaptı. Önceden image/jpeg di ve response olarak da text/html döndüğünü görünce kafası karıştı sonra resim paketine bakınca kafası yerine geldi.
- text/html yazınca php kodu geldi oraya evalution yapmaya çalışıyor. Şunu denedi ama başaramadı.
![image](https://github.com/grealyve/MDISec-Web-Security-and-Hacking-Notes/assets/41903311/6eec1948-65cf-4efc-8101-326819e9b083)
- Bir resmi gidip o klasörün altına kaydetme fonksiyonuymuş bu ve gidip tekrardan çağırtıyor sonra image olarak kaydettiriyor.
![image](https://github.com/grealyve/MDISec-Web-Security-and-Hacking-Notes/assets/41903311/99df9a61-8ad5-41ef-b8e4-4483d14196cb)
- Sonra resim isteğini tekrar yollayınca asfasjagsjd{7*7} geliyor olmadı yani 🙂
- Yine bir okumama vakası…
- setAvatar’ı çağırmamıza gerek yok
![image](https://github.com/grealyve/MDISec-Web-Security-and-Hacking-Notes/assets/41903311/00d1df7e-f5ad-4833-b4a1-7116d7b61d1a)
- En son çözüme baktı :(
