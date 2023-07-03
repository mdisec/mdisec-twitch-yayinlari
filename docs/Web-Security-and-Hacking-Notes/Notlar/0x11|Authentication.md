<h1 align="center">Authentication</h1>

### Öncelikle Cookie mevzusu anlatılmış, bildiğim için not almamışım fakat lablardan devam edicez.

## Lab: Username enumeration via different responses
- Bir login sitesinin backendinde şöyle bir yapı olabilir :
  - username girildiğinde (birlikte belki başka datalar da gelir) var olup olmadığını kontrol eder önce.
  - var ise parolayı gider kontrol eder. Sonra sessionu başlatır falan..
  - Yanlış olan, invalid username geldiğinde sadece “username invalid” şeklinde hata dönmesi.
- Burp içinde Grep - Extract komutu yazdırabilirsin çıktıları daha iyi filtrelemek için:
  - Invalid kısmının geçtiği yeri seçip OK dersen yeterli
- Session, daha kullanıcı ilk geldiğinde oluşturulur. Oturum açtıktan sonra Cookie’deki değer regenerate edilir.
    - Sessionda bir değişiklik olduğunda CSRF token da rotate edilir. Bazı botlar her req-response’da bu tokenı rotate ediyor.
    - CSRF token Session içerisinde barındırılır.
## Lab: Broken brute-force protection, IP block
- Hatalı deneme sayısını ölçtüğü yer Session olabilir. Cookie’yi sildikten sonra tekrar login olmayı denersin ve sana yukarıda Set-Cookie ile yeni bir cookie verir.
    - Manuel olarak kaç kere denedikten sonra blockladığını ölçmek isteyebilirsin.
    - Session olmadan brute force yaparsın
- Belki de IP tabanlı bir şey yapıyordur. Hikaye burada uygulama senin IP adresini nasıl alıyor? Nasıl hesaplıyor kısmına geliyor. (https://www.mehmetince.net/yuk-dengeleyiciler-ve-gercek-ip-adresi-karmasasi/)
    - Arka taraftaki reverse proxynin arkasında bulunan web uygulaması, bir takım headerlara bakar. Bu nedenle engeli aşmak için ilk denemen gereken şey:
        - X-Forwarded-For: 127.0.0.1 headerı ile sınırı aştıktan sonra 127.0.0.2 yapıp denersin, banlanırsan g.o
        - X-Real-Ip: 127.0.0.4 üstteki gibi denersin.
            - Param miner extensionu var, response a göre karar veriyor. Guess header
        - Ameleus yöntemi ile 2 kere yanlış deneme + 1 kere login olma şeklinde ilerlemeyi çözdü.
        - Burp Copy as Python Requests
            - username passwd seçip, sağ tıkla, Copy as request with session object
