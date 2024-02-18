# 0x02 | IDOR (Insecure Direct Object Reference) Hakkında Her şey | MDISEC Neler Anlattı #3

# **GİRİŞ**

IDOR meselesine giriş yapmadan önce bir web uygulamasının temelde nasıl çalıştığını anlamalıyız öncelikle. Bir web uygulamasında siber güvenlik açısından riskleri değerlendireceksek burada en önemli nokta input’lardır. Yani bir web uygulamasının çalışması için bizden aldığı direktiflerdir.

Şöyle bir web uygulaması düşünelim; bu web uygulaması sadece üzerinde çalıştığı işletim sisteminin saatini ekrana yazıyor. Ne yaparsak yapalım sadece ekrana bu saati yazdırıyor. Yani bizden herhangi bir bilgi ya da direktif almamakta. Böyle bir web uygulamasına takdir edersiniz ki pek bir saldırı bulunmamaktadır. Ancak günümüz web uygulamalarının çoğu bunun aksi yönünde oldukça fazla input alan uygulamalardır. Application security konuştuğumuzda ise en önemli konulardan biri bu input’lardır.

Web uygulamasının çalışması için kullanıcıya bir takım bilgileeri vermesi gerekmektedir. Örneğin bir e-ticaret sitesinde adres bilgimizi kaydettiğimizi düşünelim. Birden fazla adres de yazabildiğimizi varsayalım. Ayrıca siparişimizi oluştururken de menüden adresimizi seçebilmekteyiz. Yani uygulamada sipariş tamamlama ekranına gelindiğinde, veritabanında kayıtlı olan adreslerimiz ile ilgili bilgiler alınarak karşımıza getirilmektedir.

# **IDOR (Insecure Direct Object Reference) Ne Demektir ?**

Bir web uygulaması çalışırken kullanıcıdan aldığı bilgiler ile veritabanındaki birtakım verilere erişim sağlayıp bu veriyi okuyarak kullanıcıya gösterme, güncelleme, silme ya da değiştirme gibi işlemler yapmaktadır. Ancak uygulamanın bu işlemleri yapabilmesi için birtakım kurallar bulunmaktadır.

Örneğin bu kural setlerinden biri şöyle olabilir; başka bir kullanıcının adresini görememeliyiz. Adreslerim kısmına geldiğimizde sadece kendi adreslerimizi görebilmekteyiz ve başka bir kullanıcının adresini görememekteyiz. Eğer siz bu kuralı atlatıp başkasının adresini görebilirseniz bu bizim için IDOR kategorisine giren zafiyet tipimize bir örnek olmuş olur.

Bir örnekle açıkladığımız ifadeleri ayrınntılı bir şekilde ele alalım;

Buradaki zafiyetli web uygulamamızda bazı denemeler yaparak ilerleyelim. İki adet kullanıcı oluşturalım ve bu kullanıcıların adreslerini ekleyelim.

![Untitled](0x02%204c5ab91a49e44cbe8e5a0b2b2df4bfbd/Untitled.png)

MDI-1 Kullanıcısı için adresini silmek istediğimizde şöyle bir request ile karşılaşmaktayız. Buradaki request yakalama ve manipüle etme işlemini de Burp Suite ile sağlamaktayız. Bu araç sayesinde tarayıcımızda gerçekleşen tüm işlemlerin ayrıntılarını görebilmekteyiz.

![Untitled](0x02%204c5ab91a49e44cbe8e5a0b2b2df4bfbd/Untitled%201.png)

Buradaki request’i inceleyecek olursak; address isimli bir controller’ımızın olduğunu, delete isimli bir fonksiyonumuzun var olduğunu görebilmekteyiz. 15 değeri, silme işlemini gerçekleştiren fonksiyona bir function parametresi olarak iletilmektedir. Burada 15 dğeri de veritabanında ilgili adresin ifade ettiği id değeri olarak kabul edilebilir.

```
//Veritabanı yapımızı bu şekilde düşünelim
Addressler //adresler tabosu

id AUTO INC //bu tabloya ait alanlar
user_id
title
adres_bilgisi
sehir_id

12 | MDI-2 Adresi | ?
15 | MDI-1 Adresi | dsfdfdsfs
```

Yakaladığımız bu request’te 15 değeri yerine 12 yazarsak ne olacağını inceleyelim;

![Untitled](0x02%204c5ab91a49e44cbe8e5a0b2b2df4bfbd/Untitled%202.png)

Burada gördüğünüz üzere 302 Found kodu ile cevap verildi. Uygulama arayüzüne geri geldiğimizde de bizleri bu şekilde bir mesaj karşılamaktadır;

![Untitled](0x02%204c5ab91a49e44cbe8e5a0b2b2df4bfbd/Untitled%203.png)

Uygulamamızda yer alan ifadede ise ‘Authorization Failure’ mesajı yer almaktadır. Bu mesajı görüyor olmanız veriyi silemediğiniz anlamına gelmez. Bu sebeple veriyi silip silmediğimizi tekrar kontrol etmeliyiz. Hesaptaki adresleri kontrol ettiğimizde silme işleminin gerçekleştirilemediğini görmekteyiz.

![Untitled](0x02%204c5ab91a49e44cbe8e5a0b2b2df4bfbd/Untitled%204.png)

Peki eğer veritabanında bulunmayan bir id değeri girersek ne olur?

![Untitled](0x02%204c5ab91a49e44cbe8e5a0b2b2df4bfbd/Untitled%205.png)

```php

//uygulamanın davranışlarına göre oluşturduğumuz tahmini kod yapısı

class AddressController extend Controller {
  public function delete($address_id){
     if(!AddressModel->chechaddress($address_id)){
       redirect('/',404)
     }

     AddressModel->deleteAddress($address_id);
  }
}
```

Yukarıda yaptığımız işlemler neticesinde 15 değerini girince bu adresi silebiliyor olsaydık IDOR zafiyetinden bahsedebilirdik.

## **Yani IDOR ne demektir?**

Bir obje referansına güvensiz bir şekilde doğrudan (direct) erişim ile ilgili bir husustur.

## **Bu aşamada birbiriyle çok karıştırılan Missing Function Level Access ile IDOR zafiyetinin farklarını ele alalım;**

Insecure Direct Object Reference (Veriye Yetkisiz Erişim)

Missing Function Level Access Control (Fonksiyon Seviyesinde Yetki Kontrolü Eksikliği)

Şöyle bir request üzerinden ilerleyelim;

![Untitled](0x02%204c5ab91a49e44cbe8e5a0b2b2df4bfbd/Untitled%206.png)

Buradaki request’i Burp Suite ile Intruder kısmına ilettiğimizde burada ‘delete’ olarak ifade edilen kısma farklı ifadeler koyarak sistemin bize ne gösterdiğini kontrol edelim. Çünkü bu web uygulamasında ‘delete’ fonksiyonu gibi başka fonksiyonlar da kullanılmış olabilir.

![Untitled](0x02%204c5ab91a49e44cbe8e5a0b2b2df4bfbd/Untitled%207.png)

Intruder aracılığıyla ‘delete’ ifadesi yerine başka ifadeler yazarak sistemin ne cevap verdiğini test edebiliriz. Burada fieldname’ler deneyerek ilerleyebiliriz.

![Untitled](0x02%204c5ab91a49e44cbe8e5a0b2b2df4bfbd/Untitled%208.png)

İşte yaptığımız işlemler neticesinde aldığımız sonuçlar;

![Untitled](0x02%204c5ab91a49e44cbe8e5a0b2b2df4bfbd/Untitled%209.png)

Bu sonuçları incelediğimizde ‘edit’ ifadesi için alınan değerin uzunluğu diğerlerinden farklı bir uzunluktadır. 

![Untitled](0x02%204c5ab91a49e44cbe8e5a0b2b2df4bfbd/Untitled%2010.png)

Bu yüzden sistemde kontrol edip bu ifadenin bize hangi sonuçları getirdiğini görmemiz gerekmektedir;

![Untitled](0x02%204c5ab91a49e44cbe8e5a0b2b2df4bfbd/Untitled%2011.png)

Burada veri olmasına rağmen intruder kısmında neden 404 verildiğini düşünmemiz gerekmektedir. Burada ilk deneme yapılırken ‘delete’ ifadesi ile adres silinmektedir ve diğer request’lerde böyle bir ifade olmadığı için hata alınmaktadır.

![Untitled](0x02%204c5ab91a49e44cbe8e5a0b2b2df4bfbd/Untitled%2012.png)

Dolayısıyla burada ilk deneme için ‘delete’ ifadesi yerine karşılığı olmayan bir ifade yazarak verinin silinmesini engellemeliyiz.

![Untitled](0x02%204c5ab91a49e44cbe8e5a0b2b2df4bfbd/Untitled%2013.png)

Artık bu şekilde request istekleri istediğimiz gibi gelmektedir. ‘edit’ field name’i için de 200 kodunun döndüğünü görebilmekteyiz;

![Untitled](0x02%204c5ab91a49e44cbe8e5a0b2b2df4bfbd/Untitled%2014.png)

Buraya kadar olan kısımdan yapabileceğimiz bazı çıkarımlar bulunmaktadır. İncelediğimiz web uygulamasında bize ‘edit’ ile ilgili bir fonksiyon işlemi sunulmamasına rağmen bu fonksiyona erişebildik. Bu konu Missing Function Level Access Control zafiyeti olarak kabul edilmektedir.

![Untitled](0x02%204c5ab91a49e44cbe8e5a0b2b2df4bfbd/Untitled%2015.png)

/address/edit/17

IDOR zafiyeti ise başkasına ait verileri görebildiğimiz durumlarda geçerlidir. Örneğin ‘id’ dğeri olarak 17 ifadesi yerine 5 ifadesini koyduğumuzda başkasına ait verileri görebildiğimiz için IDOR zafiyetinin varlığından da bahsedebiliriz.

![Untitled](0x02%204c5ab91a49e44cbe8e5a0b2b2df4bfbd/Untitled%2016.png)

/address/edit/5

## **Bu farkı da açıkladıktan sonra web uygulaması için başka yerlerde IDOR zafiyeti olabilir mi ona bakalım?**

Sipariş detayı sayfasına geldiğimizde adres bilgilerini görebilmekteyiz. Burası adresin kullanıldığı bir başka yer. Herhangi bir ürünü sepete ekleyip onu alacağımız esnada adres listedi gelmektedir.

![Untitled](0x02%204c5ab91a49e44cbe8e5a0b2b2df4bfbd/Untitled%2017.png)

Peki buradaki adres ifadesi için `‘id’` değerini değiştirirsek başka bir kullanıcının adres bilgisine erişebilir miyiz?

![Untitled](0x02%204c5ab91a49e44cbe8e5a0b2b2df4bfbd/Untitled%2018.png)

Bu kısımdaki address değerini 17 yerine 18 yaparak başka bir kullanıcının adres bilgileri ile değiştirebilmekteyiz. Yani burada sipariş özelliğini kullanarak başka bir kullanıcının adres bilgisine erişebilmekteyiz.

![Untitled](0x02%204c5ab91a49e44cbe8e5a0b2b2df4bfbd/Untitled%2019.png)

Bu işlemin literatürdeki tam adı da **Second Order Insecure Direct Object Reference** şeklindedir. Adresi seçtiğimiz endpoint ile değiştirdiğimiz id değerini gördüğümüz kısım farklıdır çünkü. Olay tek bir request-response döngüsü içinde yaşanmamaktadır.

# **IDOR Neden Web Dünyasındaki En Zor Zafiyettir ?**

Zafiyetler temel olarak Teknik zafiyetler ve Business Logic zafiyetler olmak üzere ikiye ayrılmaktadır. Burada Business Logic bir zafiyetten bahsetmekteyiz. Herhangi bir saldırı kodu yok. SQL Injection’da, XSS’te, SSRF’te herhangi bir payload görebilirsiniz ancak IDOR’da payload bulunmamakta. Örneğin id değeri 17 iken 15'e çevirdik. Code review’da da anlaşılıp bulunması son derece zor bir zafiyettir. Kaynak kod analizi araçlarının da bulması zor olan bir zafiyet türüdür.

Günümüzde IDOR’un En Çok Karşılaşılan ve Etkisi En Kritik Zafiyetlerden Olmasının Sebebi Nedir?

Bu konuda da developer’ların yani yazılım geliştiricilerin çok büyük yapılar içerisinde kaybolduğu gerçeği yer almaktadır. Bu yüzden de bu tür açıklar oldukça yaygındır.

# **Bu Tür Zafiyetler Nasıl ve Neden Ortaya Çıkmaktadır ? — Mikroservis Mimarilerine Bakış**

![Untitled](0x02%204c5ab91a49e44cbe8e5a0b2b2df4bfbd/Untitled%2020.png)

[https://medium.com/@OlabodeAbesin/microservice-architecture-the-complete-guide-357bf7131cf1](https://medium.com/@OlabodeAbesin/microservice-architecture-the-complete-guide-357bf7131cf1)

Günümüzde şöyle bir durum bulunmaktadır. Bir e-ticaret sitesi düşünelim. Burada user’ın bilgisi bulunmakta. User bilgisine erişimesi gereken farklı uygulamalar vardır. Bunun için user bilgilerini dönen bir service yazılır. Burada mimari düzgün bir yapıda oluşturulmalıdır. Kullanıcı yetkilendirme işlemlerinin nasıl uygulanacağı belirlenmelidir. Eğer uygun yapı oluşturulmazsa bu yanlış mimariler IDOR gibi zafiyetlere sebebiyet verebilmektedir.

Bir örnek verecek olursak buradaki yapıda farklı programlama dillerinin json’ı farklı yorumlamasından dolayı ortaya çıkan bir problem ile karşılaşmaktayız. API Gateway ile Microservice yapısındaki programlama dillerinin farklılığından dolayı bu tarz problemler ortaya çıkabilmektedir.

![Untitled](0x02%204c5ab91a49e44cbe8e5a0b2b2df4bfbd/Untitled%2021.png)

## **AuthMatrix**

İncelediğimiz bir web uygulaması için yetki ve grup tanımlamalarını oluşturarak denemeler yapmak gerekmektedir. Tüm yetki şeması simüle edilerek hangi kullanıcının neyi görebildiğini öğrenebiliriz.

![Untitled](0x02%204c5ab91a49e44cbe8e5a0b2b2df4bfbd/Untitled%2022.png)

## **autochrome**

Araştırdığımız sistemde birden fazla kullanıcı ekleyerek denemeler yapmamız gerektiği için kullanabileceğimiz bir diğer faydalı araç da autochrome aracıdır. Bu araç sayesinde istediğiniz kullanıcıları ekleyerek her kullanıcı için ayrı bir pencerede işlemlerinizi yürütebilirsiniz. Bu sayede yaptığınız işlemler birbiriyle karışmayacaktır.

![Untitled](0x02%204c5ab91a49e44cbe8e5a0b2b2df4bfbd/Untitled%2023.png)

autochrome aracı için de buradaki bağlantıdan kurulumu yapabilirsiniz;

[https://github.com/nccgroup/autochrome](https://github.com/nccgroup/autochrome)

![Untitled](0x02%204c5ab91a49e44cbe8e5a0b2b2df4bfbd/Untitled%2024.png)

Buraya kadar okuduğunuz için teşekkür ederim. Selametle …

# **KAYNAKÇA**

1. [Web Security 101 0x02 | IDOR Insecure Direct Object Reference Zafiyetleri Hakkında Her şey — Mehmet İnce — Youtube](https://www.youtube.com/watch?v=TsJ2XPuGe1k)
2. [https://medium.com/@aysebilgegunduz/everything-you-need-to-know-about-idor-insecure-direct-object-references-375f83e03a87](https://medium.com/@aysebilgegunduz/everything-you-need-to-know-about-idor-insecure-direct-object-references-375f83e03a87)