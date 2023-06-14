<h1 align="center">Deserialization</h1>

## Deserialization Zafiyeti Nasıl Oluşur?
- Untrusted source’dan aldığı datayı valide etmediği için böyle bir açık oluşuyor.

- Bu zaafiyet için illaki class olmasına gerek yok, array kullanarak da ortaya böyle bir şey çıkabilir.
- Request response cycle’ı içerisinde ihtiyacın olup ürettirdiğin nesneler(hashtable, arrayler) cycle bittikten sonra yok oluyor. Garbage collecter geliyor silip götürüyor bunları. Ama sen bir daha ziyaret ettiğinde bunlara tekrar gerekiyor. Bu arrayleri, nesneleri bir yerde tutman gerekiyor tekrar erişmek için yoksa çok maaliyetli olur git DB’e tekrar tekrar nesneleri oluştur…
- Bir veriyi serialize ediyorsun. Programlama dilinde bir sınıfın var, bu verileri temsil eden bir string ifade oluşturup, stringi bir yere saklayıp daha sonra ihtiyacın olduğunda string’den obje’ye dönebileceksin.
![image](https://github.com/grealyve/MDISec-Web-Security-and-Hacking-Notes/assets/41903311/057b5105-09fa-45ef-927b-71b270ceee63)
- PHP koduyla bir class oluşturdu ve bir de User nesnesi oluşturdu.
    - O : 4 karakterli bir class var adı da “User”
    - :2: bu classın 2 class properties’i var. firstname ve lastname olarak 2 tane yapmıştı.
    - s:9: ilk property’nin uzunluğu 9 karakter ve ismi “firsname”. Bu property’nin değeri 6 karakter uzunluğunda olan “Mehmet”tir.
    - s:8: ikinci property’nin uzunluğu 8 karakter ve ismi de “lastname”. Bunun değeri s:4: 4 karakter uzunluğunda olan “INCE”.
    - Bu ifade string’tir. ÇOKOMELLİ!
- unserialize metoduyla tekrar string ifadeye çevirildi. Namespace’de olmayan sınıfı bulamazsın çoğu dilde böyledir. Deserialize edilecek sınıfın namespace’de olması lazım.
![image](https://github.com/grealyve/MDISec-Web-Security-and-Hacking-Notes/assets/41903311/bff56664-e71f-49e7-8c42-c5ad517aff5a)
- O:4:”User”’dan gitti User sınıfını buldu ve tıpkı serialize ederken yaptığı gibi new User(”Mehmet”, “INCE”)  komutunu çalıştıracak ama firstname ve lastname kısımlarını gitti otomatik olarak doldurdu. Gidip sıfırdan User isimli objeyi oluşturuyor, sık erişebilecek bir şey ise serialize ediyorsun ve saklıyorsun
- Sakladın yer ise ya DB’e insert edeceksin. Sık erişilen veriler session’a yazılır denir, obje ise objeyi yazacaksın oraya. Session’ı da Redis’te tutacaksın, orada tutabilmek için de serialize edip koyabilirsin.
- Bu 2 metodu bir class oluşturulduğunda çağırır. Magic method denir bunlara. Önce wakeup çağırılır.
![image](https://github.com/grealyve/MDISec-Web-Security-and-Hacking-Notes/assets/41903311/ef861954-0695-4686-b21f-e816ca7f0c42)
- Sonrasında payloadı unserialize ettirmeye çalışacağız.
![image](https://github.com/grealyve/MDISec-Web-Security-and-Hacking-Notes/assets/41903311/ff5e8a61-5cb0-4667-a892-f16aa3381fc9)
##### Arkadaki tüm cache mekanizmalarında serialization yapıyor. Frameworkler bu şekilde cache alır ve cache storage’a yazar. Cache storage’ı manipüle edebilirsen tüm hikaye değişir. Eğer DB’de tutuyorsa cacheleri SQLi bulup, adamın cache’i yazdığı DB’e kendi serialize stringini yazıp adamın deserialize komutunu tetikletmeye çalışabilirsin.
```php
$payload = 'O:6:"MDISEC":2:{s:9:"firstname";s:6:"Mehmet";s:8:"lastname";s:4:"INCE";}';
```
- Lenght kısmını da ayarla ama böyle bir sınıf bulamayacağı için hata verecektir.
- Yani sen istediği sınıfa eşleyebiliyorsun bu datayı
- Ya da bu string datayı istediğin şekilde değiştirebiliyorsun.
- istediğin datayı değiştirebilir hale geliyorsun. kendini admin yaparsın...
- Başka bir class ın içindeki metodları hedeflemekteyiz.
