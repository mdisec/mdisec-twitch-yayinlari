<h1 align="center">Deserialization</h1>

#### Deserialization için kullanabileceğiniz bir browser eklentisi: Cookie Quick Manager

- Import ettiği classları da oluşturabilir hale geliyoruz.
![image](https://github.com/grealyve/MDISec-Web-Security-and-Hacking-Notes/assets/41903311/c58c8df7-fbe3-48a8-a15b-5941e92b9492)
- Yazılım aslında “is_admin” değerini int olarak kullanırken sen diyorsun ki bu bir obje. Permission objesini de alıp başka bir objeye point ettirebilirsin.
![image](https://github.com/grealyve/MDISec-Web-Security-and-Hacking-Notes/assets/41903311/98a4ebb2-be57-4dd8-afa1-e8e47a9ac90e)
- Bir objenin propertie’lerini başka bir sınıfa point ettirmek :  property oriented programming
- İçinde wakeup, destruct bulunduran sınıfları kullanarak mesela cache sınfları dosya içine yazma işini yapar
![image](https://github.com/grealyve/MDISec-Web-Security-and-Hacking-Notes/assets/41903311/47f26045-2ff0-4d18-b311-baf02af0787e)
- Permission’a da git bunu kullan dersin ve backdoor’u kaparsın.
[No-CMS CodeIgniter Encryption Vulnerability Exploit](https://www.youtube.com/watch?v=YYsisTQcxls)

## Lab: Modifying serialized objects [*Lab Linki*](https://portswigger.net/web-security/deserialization/exploiting/lab-deserialization-modifying-serialized-objects)
- giriş yaparken gelen datayı Burp ile intercept yapıp gelen sessionı decode edip, kullanıcıyı admin yaptıktan sonra tekrar encode edip
yolladı isteği. Sessionı kopyalayıp amelece bütün isteklere yapıştırıp çözdü olayı.

## Lab: Modifying serialized data types [*Lab Linki*](https://portswigger.net/web-security/deserialization/exploiting/lab-deserialization-modifying-serialized-data-types)
- https://medium.com/swlh/php-type-juggling-vulnerabilities-3e28c4ed5c09
- Kullanıcıdan gelen access_token ı if karşılaştırmasına sokuyor. If comparasion da loose type check olduğu için phpde, zaafiyet çıkıyor.
- 3 tane = koymazsan string ile int karşılaştırdığında True dönüyor mesela kafayı yiyor php.
![image](https://github.com/grealyve/MDISec-Web-Security-and-Hacking-Notes/assets/41903311/991bb550-28d7-4e44-9e20-cfe61223749e)
- access_token’ı 0 yapıyor sonra encode edip yollayınca gerisi geliyor.

#### Kralından okuyabileceğin bazı makaleler:
- https://www.mehmetince.net/codeigniter-based-no-cms-admin-account-hijacking-rce-via-static-encryption-key/
- https://www.mehmetince.net/drupal-coder-zafiyet-analizi-metasploit-modulu-gelistirilmesi/
  - https://github.com/rapid7/metasploit-framework/pull/7115
