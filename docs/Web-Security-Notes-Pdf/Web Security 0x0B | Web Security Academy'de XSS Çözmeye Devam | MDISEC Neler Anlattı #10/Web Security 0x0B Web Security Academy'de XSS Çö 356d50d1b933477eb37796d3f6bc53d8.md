# Web Security 0x0B | Web Security Academy'de XSS Çözmeye Devam | MDISEC Neler Anlattı #10

# Lab: Clobbering DOM attributes to bypass HTML filters

> Bu lab ortamında HTMLJanitor isimli bir JavaScript kütüphanesi kullanılmaktadır. JavaScript payload’larını bulup temizleyen bir kütüphane gibi düşünebiliriz bunu. İsminden anlaşılan da budur.
> 

![Untitled](Web%20Security%200x0B%20Web%20Security%20Academy'de%20XSS%20C%CC%A7o%CC%88%20356d50d1b933477eb37796d3f6bc53d8/Untitled.png)

- HTML Filtreleme diye bir konu bulunmaktadır. Kullandığınız bir web uygulamasında gelen bazı kısımlarda içerikler HTML formatındadır. Örneğin sahibinden araç satış sitesi gibi bir uygulamada bir ürünün açıklama sayfası aslında HTML sayfası şeklindedir. Buradaki içerik ilanı oluşturan kullanıcıdan alınmaktadır. Aynı zamanda ilan başka kullanıcılara gösterilmektedir. Yani güvensiz bir kaynaktan alınan HTML içerik farklı kullanıcılara sunulmaktadır. Tam olarak bir Stored XSS ortamı oluşmaktadır burada. Dolayısıyla bu içerikte bir XSS Payload’ının olmadığına emin olmanız gerekmektedir. Kullanıcıdan alınan içerik HTML olduğu için bunun filtrelenmesi ve temizlenmesi gerekmektedir. Yani blacklist mantığıyla istenmeyen içerikler filtrelenmelidir. Bu konu için de [DOMPurify](https://github.com/cure53/DOMPurify) isimli bir araç bulunmaktadır. [https://github.com/cure53/DOMPurify](https://github.com/cure53/DOMPurify)
- Burada HTML içeriğe yazdığınız saldırı kodları silinip temizleneceği için 2 seçeneğiniz bulunmaktadır. Ya buradaki filtering blacklisting’i bypass’lamanız ya da HTML içeriğini yöneten başka bir javascript kodu ile ilerlemeniz gerekir.
- Şimdi lab ortamımıza erişip çalışmalara başlayalım.
- Bir ürünün ayrıntılarına gittiğimizde yorum yapma imkanına sahip olmaktayız. Buradaki yorum alanında hem XSS ile ilgili payload’lar yazıp hem de XSS ile bağlantılı olmayan ifadeler yazarak nelerin silinip nelerin silinmediğini test edelim.

```python
ilker'"'`< > yılmaz <script>alert(1)</script> mdisec <svg onload=alert(1)> deneme <form>
```

![Untitled](Web%20Security%200x0B%20Web%20Security%20Academy'de%20XSS%20C%CC%A7o%CC%88%20356d50d1b933477eb37796d3f6bc53d8/Untitled%201.png)

> Yorumu kaydettikten sonra sayfada bu şekilde gösterildiğini görmekteyiz.
> 

![Untitled](Web%20Security%200x0B%20Web%20Security%20Academy'de%20XSS%20C%CC%A7o%CC%88%20356d50d1b933477eb37796d3f6bc53d8/Untitled%202.png)

- Buradaki yorumu inspect element ile incelediğimizde şu yapıda olduğunu görebiliriz. Verdiğimiz data’da XSS Payload’ları silinmiş ve tamamlamadığımız <form> tag’i tarayıcı tarafından tamamlanmış durumda. Verdiğimiz özel karakterler de encode edilmiş durumda.

```python
<section class="comment"><p><a id="author" href="http://test.com"></a>test | 28-01-2024<img class="avatar" src="/resources/images/avatarDefault.svg"></p><p>ilker'"'`&lt; &gt; yÄ±lmaz  mdisec  deneme <form></form></p><p></p></section>
```

- Burada silme işlemleri backen yerine muhtemelen client’ta yapılıyordur. Bu yüzden sayfa kaynağındaki JavaScript kodlarına bakabiliriz. Sayfa kaynağını incelediğimizde bu konularla ilgili 2 adet JavaScript dosyası görmekteyiz.

![Untitled](Web%20Security%200x0B%20Web%20Security%20Academy'de%20XSS%20C%CC%A7o%CC%88%20356d50d1b933477eb37796d3f6bc53d8/Untitled%203.png)

- İkinci sıradaki dosyamızı inceleyelim ve neler olup bittiğini görelim.
- Bu dosyayı incelediğimizde şu kod satırıyla birlikte bazı tag’lerin kullanımına izin verildiğini görüyoruz. Bunlar “input, form, i,b,p” tag’leri olarak belirlenmiş durumda. Aynı zamanda buradaki tag’ler için de kullanılabilecek attribute’lar belirlenmiş durumda.

```python
let janitor = new HTMLJanitor({tags: {input:{name:true,type:true,value:true},form:{id:true},i:{},b:{},p:{}}});
```

- Kodu okumaya devam ettiğimizde bizim gönderdiğimiz data’nın geldiği kısım burasıdır;

```python
if (comment.body) {
                let commentBodyPElement = document.createElement("p");
                commentBodyPElement.innerHTML = janitor.clean(comment.body);

                commentSection.appendChild(commentBodyPElement);
            }
```

- Şimdi de kısıtlanan attribute’lar ile ilgili bir deneme yapalım, bu deneme ile aslında izin verilen attribute’lar dışında kullanılan ifadelerin silindiğini görebiliriz.
- Örneğin form tag’i için sadece id attribute’una izin verilmektedir, biz oluşturacağımız yorumda hem id hem de action attribute’larını koyarak hangisinin silineceğini görelim.

```python
mdisec <form action=selam id=x> aleykumselam
```

![Untitled](Web%20Security%200x0B%20Web%20Security%20Academy'de%20XSS%20C%CC%A7o%CC%88%20356d50d1b933477eb37796d3f6bc53d8/Untitled%204.png)

- Burada yorumu gönderdikten sonra oluşan yorumumuzu inspect element ile inceleyebiliriz. Bu kısmı incelediğimizde izin verilmeyen attribute’ların silindiğini kolaylıkla fark edebiliriz.

```python
<p>mdisec <form id="x"> aleykumselam</form></p><p></p></section>
```

- Burada farklı bir ayrıntı yöntem de mevcut. Örneğin bu şekilde bir yorum yazdığımızda işler değişmektedir.

```python
mdisec <form onfocus=alert(1)><input id=attributes>Click me
```

- Böyle bir yorum girdiğimizde de inspect element ile yorumu incelersek artık onfocus attribute’unun silinmediğini görebiliriz.

```python
<p>mdisec <form onfocus="alert(1)"><input>Click me</form></p>
```

![Untitled](Web%20Security%200x0B%20Web%20Security%20Academy'de%20XSS%20C%CC%A7o%CC%88%20356d50d1b933477eb37796d3f6bc53d8/Untitled%205.png)

- Burada yaşanan olayın nasıl olduğunu anlamamız gerekiyor. İncelediğimiz JavaScript dosyasındaki kodlara baktığımızda ilgili JavaScript kodu attribute’ları dolaşırken yanlışlıkla form elementinin attribute’unu değil de sadece input elementinin attribute’larını dolaşmaktadır. Böylece form elmentindeki onfocus attribute’una hiçbir zaman dokunmamaktadır.

```python
// Sanitize attributes
        for (var a = 0; a < node.attributes.length; a += 1) {
          var attr = node.attributes[a];
  
          if (shouldRejectAttr(attr, allowedAttrs, node)) {
            node.removeAttribute(attr.name);
            // Shift the array to continue looping.
            a = a - 1;
          }
        }
```

- Tarayıcı konsolunda da denemeler yaptığımızda id attribute’u için “attributes” değerinden başka bir değişken verdiğimizde istediğimiz sonucu alamamaktayız. Sadece “attributes” verdiğimizde silinmemektedir.

![Untitled](Web%20Security%200x0B%20Web%20Security%20Academy'de%20XSS%20C%CC%A7o%CC%88%20356d50d1b933477eb37796d3f6bc53d8/Untitled%206.png)

- Burada aslında yaşanan olay şöyledir;
id attribute’una verdiğiniz isim ne ise o isim node içerisinde yani JavaScript o tag’i node olarak değerlendirdiğinde, ilgili node’un içerisinde bir değişken adı olarak oluşmakta.
- Yani kodumuzdaki for döngüsü node’nin attribute’unu almak istediğinde form’un içerisindeki input elementinin id değeri attributes olduğundan dolayı node.attributes buna atanmış oluyor. Aslında burada for döngüsündeni node içerisinde attribute diye bir isim oluşmakta ve bunun uzunluğu bulunmamakta. Dolayısıyla bu döngüye hiç girmemektedir. Girmediği için de silme işlemi gerçekleşmemektedir.

![Untitled](Web%20Security%200x0B%20Web%20Security%20Academy'de%20XSS%20C%CC%A7o%CC%88%20356d50d1b933477eb37796d3f6bc53d8/Untitled%207.png)

- Artık bu bilgiler ışığında lab ortamını çözmeye odaklanalım. Yukarıda da gördüğümüz yorum alanında çalışmalarımıza devam edelim. Burada girdiğimiz yorum ile bir pop-up çıkartarak document.cookie değerini almamız gerekmektedir.

- Yorum olarak buradaki yapıyı girmekteyiz. Oluşturduğumuz form için id değerini x vermekteyiz. input elementi için de id değerini attributes verdiğimizde form elementindeki attribute’ların silinmesini engellemekteyiz. Form elementindeki onfocus attribute’u ile alert’i çağırmaktayız. Buraya onfocus edilmesi için de id=x verip daha sonra url’den location hash ile buradaki x’e odaklatmaktadır. Burada da iframe ile bunu sağlayıp bir delay koyarak tüm javascript kodları yüklendikten sonra uygulamalıyız.

```python
<form id=x tabindex=0 onfocus=print()><input id=attributes>
```

![Untitled](Web%20Security%200x0B%20Web%20Security%20Academy'de%20XSS%20C%CC%A7o%CC%88%20356d50d1b933477eb37796d3f6bc53d8/Untitled%208.png)

- Artık exploit server’a giderek iframe ile kurduğumuz yapıyı buraya koyabiliriz.

```python
<iframe src=https://0a69009b03868a8f81ffa70100b100a8.web-security-academy.net/post?postId=5 onload="setTimeout(()=>this.src=this.src+'#x',500)">
```

![Untitled](Web%20Security%200x0B%20Web%20Security%20Academy'de%20XSS%20C%CC%A7o%CC%88%20356d50d1b933477eb37796d3f6bc53d8/Untitled%209.png)

- Ve artık bu sayede lab’ı çözmüş olduk…

![Untitled](Web%20Security%200x0B%20Web%20Security%20Academy'de%20XSS%20C%CC%A7o%CC%88%20356d50d1b933477eb37796d3f6bc53d8/Untitled%2010.png)

# Browser Davranışları

Aşağıdaki gibi bir içeriğe sahip olan HTML dosyasını tarayıcıda açtığımızda istediğimiz alert başarıyla oluşturulacaktır. 

```python
<html>
    <svg onload=alert(1)>
</html>
```

Ancak burada yapıyı değiştirip bozduğumuzda yine de alert çalışacak mı yoksa çalışmayacak mı sorusu akıllarda bir soru işaretidir. 

```python
<html>
    <svg onload=alert(1)
</html>
```

Siz yapınızı kısmen bozmuş olsanız bile tarayıcı davranışlarıyla birlikte eksik olan parça tarayıcı tarafından tamamlanır ve HTML içeriğiniz düzeltilerek tarayıcıda çalıştırılmış olur. Siz üst  tarafta gösterdiğimiz gibi bir data gönderseniz bile tarayıcı bunu aşağıdaki hale getirecektir, aslında HTML içeriğini olması gerektiği hale getirmektedir. HTML’i parse ederek sonuçları getirmiş olur; 

```python
<html>
	<head>
	</head>
	<body>
		<svg onload="alert(1)" <="" html=""></svg>
	</body>
</html>
```

![Untitled](Web%20Security%200x0B%20Web%20Security%20Academy'de%20XSS%20C%CC%A7o%CC%88%20356d50d1b933477eb37796d3f6bc53d8/Untitled%2011.png)

# Lab: Reflected XSS into HTML context with nothing encoded

Yukarıdaki zorlu lab ortamlarından sonra artık bu lab’ın çözümü de bu kadar basit :) 

Buradaki mevzuyu da muhtemelen artık anlamış olmalıyız…

```python
<script>alert(1)</script>
```

![Untitled](Web%20Security%200x0B%20Web%20Security%20Academy'de%20XSS%20C%CC%A7o%CC%88%20356d50d1b933477eb37796d3f6bc53d8/Untitled%2012.png)

- XSS ile ilgili kapsamlı bir kaynak arayışındaysanız da bu adresi ziyaret edebilirsiniz: [https://portswigger.net/web-security/cross-site-scripting/cheat-sheet](https://portswigger.net/web-security/cross-site-scripting/cheat-sheet)

# Kaynaklar

1. [https://www.youtube.com/watch?v=Cy9qGc_A_Ic](https://www.youtube.com/watch?v=Cy9qGc_A_Ic&list=PLwP4ObPL5GY940XhCtAykxLxLEOKCu0nT&index=11)