<h1 align="center">Burp DOM Invader</h1>

## DOM Based XSS Nedir?
- XSS dünyası browser ve JS tarafında dönüyor. En önemli konu DOM Based XSS. Browser HTML içeriği alıp bir DOM tree oluşturduktan sonra özellikle client side JS implementasyonu manipülasyonları gerçekleştiriliebiliyor. Eğer bu DOM’un içerisinde JS’in kullandığı birtakım metodların parametrelerine müdahale etme imkanımız varsa bu DOM updati sürecinde bir XSS zafiyeti çıkartabiliyoruz.
![image](https://github.com/grealyve/MDISec-Web-Security-and-Hacking-Notes/assets/41903311/81c7a902-b7ca-4656-92ba-4b4edcbb6ccc)
- Bir sayfada binlerce JS çalışmakta ve belli durum/yapılarda DOM’u güncellemekte. Bunu track etmek çok zor çünkü içeride binlerce JS çalışıyor.
- Source’dan gelen datalar Sink’e gidiyor ve bunlar nereye gidiyor bunu insan gözüyle takip etmesi çok zor.
![image](https://github.com/grealyve/MDISec-Web-Security-and-Hacking-Notes/assets/41903311/9a11665e-344f-4e6e-af72-d84bdecf9116)
- input alanlarına token belirleyecez, DOM oluşunca bu token nerelerde tetiklendiyse[Hangi JS kodlarını tetiklediyse] oralarda gözükecek.
![image](https://github.com/grealyve/MDISec-Web-Security-and-Hacking-Notes/assets/41903311/5d5141d1-ff5a-4362-86f2-ec998edc6e39)
## DOM Based XSS
- “trigger” fonksiyonuna gelen parametre “eval” fonksiyonuna gidiyor. Burası sink oluyor.
- Source ise “document.cookie”
![image](https://github.com/grealyve/MDISec-Web-Security-and-Hacking-Notes/assets/41903311/6a35566e-bac5-4040-ab09-b77eaae8d4af)
