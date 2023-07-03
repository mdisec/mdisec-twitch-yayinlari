<h1 align="center">SSL Temelde Nedir?</h1>

#### Bütün browserların DB'i: http://hostpreload.org/

## MITM hangi layerda iş yapar?
![image](https://github.com/grealyve/MDISec-Web-Security-and-Hacking-Notes/assets/41903311/b680042e-ca08-4bbd-a8d5-8c727d105bc1)

- Soldaki adam SSL’e geçiş yapamayacak.
- Bütün olay aslında Browser’da yatıyor. Kurban https ile gitse bile, [x.com](http://x.com) SSL sertifikasını Browser’a göstermesi lazım ki Browser onu kontrol edebilsin.
- Bir site için SSL sertifikası üretebilirsin. Ortadaki heçkır, sertifikayı kendisi için üretsin ve ürettiği sertifikayı geri Kurban’a yollasın.
- Browser’ın sertifikayı doğruladığı yer : Certificate Authorities (CA) (Browser’ların domainlerin sertifikalarını imzaladığı yer) (Adam da imzalı sertifikasını kendi sunucusuna yüklüyor)

![image](https://github.com/grealyve/MDISec-Web-Security-and-Hacking-Notes/assets/41903311/3052a3da-9c1c-44f9-93e0-99ea9c28c092)

- Sertifika Otoriteleri (CA) bu imzalamayı nasıl yapıyorlar?
    - Adam parayı veriyor, CA da cevap olarak ben sertifikayı sana hemen vermicem gidip [info.x.com](http://info.x.com) mailine postaladım diyor. (CA’lardan bir tanesi)
    - Bir [x.com/cokgizli.txt](http://x.com/cokgizli.txt) diye dosya oluştur koy oraya ben GET ile gelem, girebilirsem SSL senindir diyor. iqless
- Birisi senin adına sertifika alırsa diye : Http Public Key Pinning mevzusu var.
- SSL Strip mevzusu : Kurbanımız http ile çıkıyor, heçkır o isteği iletiyordu dönen linklerin tamamını http’ye çevirip geri Kurbanımıza veriyordu. Eskiden bu çalışıyordu.
    - Günümüzde bunu çözmenin yolu isteklerin default olarak https olarak çıkması. Bunun da yolu HTTP Strict Transport Securtiy Header’ı.
- Bir web sitesine ortada adam yokken HSTS ile gittiğinde Browser’a kaydedilir o. İkinci defa o siteye gittiğinde http ile bile gitsen Browser sana “307 Internal Redirect” verir. Ve bu HSTS olayını 1 yıl boyunca saklar o browser. Sonrasında ortada adam olsa bile adamın sertifikası CA tarafından onaylanmadığı için seni http olarak yönlendiremeyecek. (Daha önce hiç gitmediysen de 307 verir.)
- Ortadaki adam sahte sertifikayı verir, browser kontrol eder ve DB’de olmadığını görünce adam patlar.

![image](https://github.com/grealyve/MDISec-Web-Security-and-Hacking-Notes/assets/41903311/bef07dd8-1e91-4175-b3af-a2e390ea1fac)

- HSTS varken(yani daha önceden o siteye https ile gitmediysen bile) ve kendisine sunulan SSL sertifikası trusted authorities tarafından onaylanmamışsa Browser ADVANCED butonunu çıkartmıyor.
![image](https://github.com/grealyve/MDISec-Web-Security-and-Hacking-Notes/assets/41903311/5a842b71-b9be-4876-9032-f22f602ecfd0)
