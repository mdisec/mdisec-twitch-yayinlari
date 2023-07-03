<h1 align="center">Business Logic Vulnerebilities</h1>

### Oluşturulan kuklanın(uygulamanın) tanımlarında yani yapabileceği şeyler arasındaki birtakım eksiklikleri kullanarak zafiyet tespit edebilmek amaçlanıyor. 

## Lab: Excessive trust in client-side controls
- Senin 100$’ın var bu ürünü sepetine ekleyebiliyorsun, fakirlikle yüzleşiyormuşsun, ürünü silebiliyormuşsun.
- Ürünü sepete ekle dediğimizde giden request şu:
![image](https://github.com/grealyve/MDISec-Web-Security-and-Hacking-Notes/assets/41903311/5c1a289a-8c23-461a-b939-cd8a61e8548d)
- Nomalde price DB’de bulunan bir değerdir, enayiler son kullanıcıdan alıyor. ProductID’yi alırsın, quantityi alırsın yeter.
- 100 dolar yazdı oraya, 1.00$ olarak gitti ama. Demek ki sondaki 2 haneyi . dan sonra kabul ediyor.
- Order tamamlandı.
- Alınan price çok da önemli değil ama bunu kontrol edilmemesi sıkıntı.
  - product i &redir=PRODCT&quantity=1&price=133700
      - Mesela burda quantitiyi 0.1 yapınca ne olacak? Price ile çarpmış bu quantityi
  - ya da mesela order tamamlandığında  1.satıra order completed gibi bir şey yazıyordu o requeste gitseydik ne olacaktı?
### Bu olay aslında daha karmaşık yapılarda da gözlemlenebiliyor. 1.adımda alınan formu 3. adımda da kullanan yapılarda mesela sıkıntı çıkartabilir.
## Lab: High-level logic vulnerability
- Yine aynı ceketi sepete ekle, place order yaptı olmadı
- Miktarını arttırdı, o requesti incele. 0.1 artır desek sevmedi isteği.
- Miktarı azalttı, -0 yazdı requeste ve hata vermedi.
- Tekrar her şeyi sıfıradı ve terkardan ekledi ceketi. Bu sefer quantitye önce sakfhgja yazdı hata aldı sonra, 00 yazdı hata almadı 302 Found ama sepet boştu.
- Quantity’e 1,00 yazdı hata verdi. Sonra 1 yazdı(normal değeri) Content-Lenght: 0 döndü. Tekrar yaptı 2 tane sepette oldu. Sonra negatif sayıda denedi o da oldu. -3 tane var, place order yaptı ama total price 0’dan aşşağı olamaz diye hata verdi
- Sonra gitti farklı ürün koydu sepete pozitif olsun diye.
![image](https://github.com/grealyve/MDISec-Web-Security-and-Hacking-Notes/assets/41903311/5e73ed7b-2c51-4615-a42a-8108bcf12220)
- Satın al deyince satın aldı. Ama lab çözülmedi - miktarını tam tersi üründen yapmak lazım.
## Lab: Low-level logic flaw
- Gitti ceketi ekledi, giden paketi inceledi.
![image](https://github.com/grealyve/MDISec-Web-Security-and-Hacking-Notes/assets/41903311/84e6bd06-7a3d-45da-9349-c07e0c82900b)
- Kupon eklemeyi denedi. Hazır kupon formatlarına bakıyor.
- Sonra sıfırdan gitti -1 tane ceket eklemeyi denedi 302 found ama eklemiyor. 1 tane ekledi, sonra -1 tane ekledi elde var 0, tekrardan -1 ekle dediğinde yine eklemedi. 1 tane varken direkt -3 ekle dediğnide yine olmadı.
- Şöyle bir sıkıntı varsa zaten SQL injectiona gidiyor mevzu
![image](https://github.com/grealyve/MDISec-Web-Security-and-Hacking-Notes/assets/41903311/6af7fa94-f3ac-4fac-888b-c468e8679a28)
- Max kaç tane sepete ekleyebiliyor onu denedi. 00 denedi.
- Yeni bir parametre ekledi backend bunu umursamayacak, bu sayıyı 1’den 100000e kadar arttıracak birer birer.
![image](https://github.com/grealyve/MDISec-Web-Security-and-Hacking-Notes/assets/41903311/46136a05-0e28-487c-ab95-c2f3c52e7dbd)
- F5 atınca para kısmı bir artıyor bi eksiye düşüyor. Aynı isteği sürekli atıyor sürekli 99 tane eklenmiş oluyor. Eksideyken place order denedi ama para - olduğu için hata verdi.
- Marketten gidip başka en pahalı eşya için aynısını yaptı.  Sonra place order paketi için de aynısını yaptı.
- Bu sayılar integer değerinde çıkmazsa overflow olduğu için negatif bir değer ortaya çıkıyor.
- Bu iki ürünü 100$ ın altına getirebilecek kadar değer ürettiğinde place ordera basacak şekilde denedi.
- Sayıları hesaplayıp denesen olabilir
