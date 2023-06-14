<h1 align="center">CS253 vs MDISEC</h1>

- Session Hijack :
  1) Bir kullanıcının cookiesini çalarak hijack edebilirsin
  2) Cookiesini tahmin ederek hijack edebilirsin
  3) XSS exploit edip HTTP-ONLY set edilmemişse oturum anahtarını çalarak da session hijack yapabilirsin.

- HTTP Response’da neden detaylı error infosu vermek yanlıştır?
  - Runtime env variable expose olabilir
  - local path bilgisi ifşa olabilir
  - kullanılan library versions info leak olabilir.
  - partial source code leak olabilir
## Soru 6:
![image](https://github.com/grealyve/MDISec-Web-Security-and-Hacking-Notes/assets/41903311/09e3ef8c-ea24-4f16-8a85-f7cfdb7f3ae8)
- Bu da cevabı:
![image](https://github.com/grealyve/MDISec-Web-Security-and-Hacking-Notes/assets/41903311/f2bd1b8f-f877-4b10-bb43-9466063998d0)

## Soru 8:
![image](https://github.com/grealyve/MDISec-Web-Security-and-Hacking-Notes/assets/41903311/e03f8b41-9f51-45f6-9241-96a7749ffeea)

- unsafe-inline yazmayınca aktif oluyormuş zati
- Cevabı:
![image](https://github.com/grealyve/MDISec-Web-Security-and-Hacking-Notes/assets/41903311/8aae7e9d-9ebe-426c-ac29-acb7a0f35d71)
## Soru 9:
![image](https://github.com/grealyve/MDISec-Web-Security-and-Hacking-Notes/assets/41903311/f074a993-09c2-4bab-b928-999f5d26b949)

- Cevabı:
![image](https://github.com/grealyve/MDISec-Web-Security-and-Hacking-Notes/assets/41903311/10de68f4-cecd-4543-9544-0a3ae83d29f2)

## Soru 10:
![image](https://github.com/grealyve/MDISec-Web-Security-and-Hacking-Notes/assets/41903311/924e455e-aac2-4e0d-80e5-fbfce2fea394)

- Captcha rate limiting tetiklenince çalışır zaten.
- Cevabı:
![image](https://github.com/grealyve/MDISec-Web-Security-and-Hacking-Notes/assets/41903311/440b3383-db3f-4ce2-bb7c-7832590aa664)
## Soru 11:
![image](https://github.com/grealyve/MDISec-Web-Security-and-Hacking-Notes/assets/41903311/242c038b-f2e3-4257-ba66-f7caa70ae954)

# Free Response
## Soru 1 - Same Origin Policy
![image](https://github.com/grealyve/MDISec-Web-Security-and-Hacking-Notes/assets/41903311/421a1b25-dee6-4a06-9f40-e896bd46c558)
## Soru 3 - CORS Preflight
![image](https://github.com/grealyve/MDISec-Web-Security-and-Hacking-Notes/assets/41903311/69f82108-21af-4d7b-a4c3-3f2eba9d3f92)
- Cevap: JS ile bir API’den data alman ile alakalıdır. API’ler genellikle REST-API standartlarına göre ayarlandığı için, bana bu resource ile ilgili ayarları ver dediğin bir request gönderirisin. Ben gerçek bir request göndericem, bundan öncesinde bu kaynak ile konuşabiliyor muyum ona bakarsın.
## Soru 4 - Cookies:
![image](https://github.com/grealyve/MDISec-Web-Security-and-Hacking-Notes/assets/41903311/59994150-22d1-43dd-9241-9ad7e902f997)
![image](https://github.com/grealyve/MDISec-Web-Security-and-Hacking-Notes/assets/41903311/a59c3917-b9cf-44be-b0f7-d6b867ed3052)
- Cevap: CORS aynı olduğu için attacker hedef siteyi iframe içerisinde açıp, contentine erişim sağlayabilmekte. Çünkü CORS için scope yani path’in bir önemi yok.
## Soru 5 - More Cookies:
![image](https://github.com/grealyve/MDISec-Web-Security-and-Hacking-Notes/assets/41903311/43c329fb-0ff0-4596-b650-4d3b3eb8cfcf)
- Banka, tespiti referer ile yapıyor. Browser otomatikman referer headerı ekler img’deki isteğe ve  banka uygulaması da bu bilgiyi kontrol eder kendi kaynağından mı gelmiş bu istek diye acaba?
- Cevap:
![image](https://github.com/grealyve/MDISec-Web-Security-and-Hacking-Notes/assets/41903311/9157a79c-ca31-4a04-bb0c-46afb8809092)
## Soru 6 - XSS:
![image](https://github.com/grealyve/MDISec-Web-Security-and-Hacking-Notes/assets/41903311/869fd096-b060-4cb4-a173-1e629510252e)
- query string’de GET parametresi ile giden source’u alıp header’a koymuş. HTML context XSS var.
- Cevap:
![image](https://github.com/grealyve/MDISec-Web-Security-and-Hacking-Notes/assets/41903311/3737c833-c609-44b5-b72d-8beb507c8060)
- username alanında XSS payloadını yazacaksın. Aşşağıda script tagine koyuyor senin username’ini, tek tırnak ile (’) escape edip koyabilirsin encode edilmediyse. Eğer tek tırnak encode edildiyse script tagini kapatıp payloadı yazarsın.
- Alert’in içinde de XSS case var.
```javascript
</script><svg onload=alert(1)>
```
![image](https://github.com/grealyve/MDISec-Web-Security-and-Hacking-Notes/assets/41903311/dc796733-1bfa-43e3-8e33-0ce06fb6b47b)
## Soru 7 - More XSS
- Cevap:
![image](https://github.com/grealyve/MDISec-Web-Security-and-Hacking-Notes/assets/41903311/6c1041d9-4528-4e1c-8bdd-b5052ff22c08)
- back-slash, back-slash’i escape ettiği için tek tırnak escape edilemiyor
![image](https://github.com/grealyve/MDISec-Web-Security-and-Hacking-Notes/assets/41903311/02be2e7c-cc75-4be0-845b-4ab95f38654a)
## Soru 8 - CSP:
- Soru: Bu CSP kuralına göre aşağıdakilerden hangisi yüklenir/yüklenmez?
![image](https://github.com/grealyve/MDISec-Web-Security-and-Hacking-Notes/assets/41903311/07f0a369-e0a5-4662-bb53-fba47e98d440)
- style-src sadece self yazdığı için 2.si F olur yüklenmez.
- script-src self olduğu için alert çalışır.
![image](https://github.com/grealyve/MDISec-Web-Security-and-Hacking-Notes/assets/41903311/f5f925c2-3e72-46d3-82a3-baaab9236e38)
- Cevap:
![image](https://github.com/grealyve/MDISec-Web-Security-and-Hacking-Notes/assets/41903311/5480ef9c-7559-4d8f-90b7-7a47072aacd8)
- Daha önceki kafa karışıklığına sebep olan unsafe-inline muhabbeti yüzünden yanlış.
## Soru 9 - HSTS Preload:
![image](https://github.com/grealyve/MDISec-Web-Security-and-Hacking-Notes/assets/41903311/08a643a1-600a-4ba8-a920-089addb876cc)
- Preload list’e koyduğun zaman tüm browserlarda HTTP request gitse bile 307 Internal Redirect ile bu request HTTPS’e yükseltilir ve trusted auth. tarafından doğrulama yapılır falan..
- Cevap:
![image](https://github.com/grealyve/MDISec-Web-Security-and-Hacking-Notes/assets/41903311/4e679a01-d285-4548-bf93-82314d285929)
## Soru 10 - Command Injection:
![image](https://github.com/grealyve/MDISec-Web-Security-and-Hacking-Notes/assets/41903311/7dfa1e94-f6c2-43c9-8c15-a40aa67a0181)
- Cevap:
![image](https://github.com/grealyve/MDISec-Web-Security-and-Hacking-Notes/assets/41903311/803d00c2-2aba-4e13-ae91-c9bc150331db)
## Soru 11 - Fingerprinting:
![image](https://github.com/grealyve/MDISec-Web-Security-and-Hacking-Notes/assets/41903311/a7f9cc9e-a105-49dd-a3a5-908b5f16b8f6)
- Cevap:
![image](https://github.com/grealyve/MDISec-Web-Security-and-Hacking-Notes/assets/41903311/db18cf16-d8ab-4abf-952a-3a0ed9860fed)
## Soru 12 - Logic Bug:
![image](https://github.com/grealyve/MDISec-Web-Security-and-Hacking-Notes/assets/41903311/7329b517-09dc-4a9f-be62-df36c8078034)
1) CSRF,
2) no return/exit : kullanıcı adı parola vermesen bile çalışır. Çalıştıktan sonra fonksiyon kapanmaz, sadece ekrana bir şey yazar.
- kritik metodlar GET ile gelmemeli diyor.
![image](https://github.com/grealyve/MDISec-Web-Security-and-Hacking-Notes/assets/41903311/9cee206b-6ef2-48d5-bda8-3a1435952d3e)
