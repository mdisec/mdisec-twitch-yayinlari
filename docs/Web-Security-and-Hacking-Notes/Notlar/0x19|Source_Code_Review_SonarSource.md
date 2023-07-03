<h1 align="center">Source-Code Review</h1>

#### eval her zaman sıkıntı bir fonksiyondur, bu fonksiyonun parametresinde kullanıcının kontrol edebildiği hiçbir şey olmamalıdır.
# Kod Analizi
## Command Injection
![image](https://github.com/grealyve/MDISec-Web-Security-and-Hacking-Notes/assets/41903311/5efb6748-6332-42b8-a473-f5e6a1b5838a)
- .Net yazılımı bu, IntallPackage dediğinde aklına işletim sistemi üzerinde bir paket kurulumu olacak bu da arkada background proccess oluşturacak, directorylere bir şeyler yazılacak.
![image](https://github.com/grealyve/MDISec-Web-Security-and-Hacking-Notes/assets/41903311/227c2c0e-6790-4362-8b2b-50e0b3075e70)

- Burada Command Injection zafiyeti var. Process’in Argüman’ına string concatenation yapılıyor Argüman passing yapılmamış durumda.
## Code evalution
![image](https://github.com/grealyve/MDISec-Web-Security-and-Hacking-Notes/assets/41903311/f8d6e5d9-d4b0-4a4b-8ebc-552920fccfd4)
- Bu input alanı genelde HTML oluyor. HTML templating var fonksiyonun ismi o zaten.
![image](https://github.com/grealyve/MDISec-Web-Security-and-Hacking-Notes/assets/41903311/5319bad6-fbed-4aa4-acee-bbfbe056e7ab)
- Code evalution zafiyeti var burda. Eval fonk. parametresini son kullanıcı değiştirebilir burda oynamalar yapabilir.
## SQL injection
![image](https://github.com/grealyve/MDISec-Web-Security-and-Hacking-Notes/assets/41903311/d99c1246-b013-4f58-9b19-bf6001cbc6c0)
- Bu kısım kıllandırıyormuş:
![image](https://github.com/grealyve/MDISec-Web-Security-and-Hacking-Notes/assets/41903311/1bc2caa9-42dc-4816-a2cd-35e2b5c50c6f)
- “nodeParm” kodu genel olarak incelediğinde, GET ve POST requestleri ile birlikte gelen ve userın kontrol edebildiği bir parametre.
- Java kodu olduğu için, Java’da sqlRestriction kodunu gidip okuduğunda SQLi’dan kaçınman için gereken bir fonksiyon. “sqlRestriction” fonksiyonu virgülden sonraki nodeParmValue gibi parametreleri kontrol eder. Fakat burada “nodeParameterName” query template’dir ve kullanıcı manipüle edebildiği için SQL injection çıkar.
### NOT: if else kısımlarını okumazmış, neyi trace edeceğine bakar eğer o parametre if else te geçiyorsa bakarmış.
## KeySize
![image](https://github.com/grealyve/MDISec-Web-Security-and-Hacking-Notes/assets/41903311/2dde179c-21ac-42ad-b6ce-b63a2d2aaf85)
- Burada yönetilebilen parametre tokendır. Direkt token’a odaklandır reis. Token’ı manipüle edemiyorsa okumazmış.
- KeySize sen gidip 4096 yazdığında gidip değiştirmezmiş. Setter ve getter lar ile değiştirmek lazım diyor.
![image](https://github.com/grealyve/MDISec-Web-Security-and-Hacking-Notes/assets/41903311/7a81694a-3332-452b-a219-fe987343eb25)
## Local File Inclusion(LFI)
![image](https://github.com/grealyve/MDISec-Web-Security-and-Hacking-Notes/assets/41903311/aa6f3e10-61a8-46ac-a86a-679ea83f1cd6)
- Regex gördüğün anda şüphe uyandırır.
- require_once dediğin anda burada Local File Inclusion vaar.
- cookie ile bir şeyler geliyor. Regexi kontrol ettiğinde 46-122 arası karakterleri yasaklamış ama işte $ ile başlayan bir şey koyarak yine LFI yapılabilirmiş.
![image](https://github.com/grealyve/MDISec-Web-Security-and-Hacking-Notes/assets/41903311/1f66155a-7323-4805-bd91-7616aa737b8c)
```sh
$../../../../../../../../etc
```
## XXE
![image](https://github.com/grealyve/MDISec-Web-Security-and-Hacking-Notes/assets/41903311/d2d1d0b2-6f77-4b4a-8651-76ee104571f3)
- XXE varmış burda
    - .odt dosyası
- SAXBuilder ile aşağıda dox.getContent çalışınca, content.xml ‘i parse ediyor ve DTD lerin disable edilmesi yokmuş.
## Log Forging Vulnerability
![image](https://github.com/grealyve/MDISec-Web-Security-and-Hacking-Notes/assets/41903311/d2358258-2a9d-4363-9873-846e507982f8)
- _create_export bir file oluşturuyo, bid ne işe yarıyor ona  bir bakmak lazım hem input alanı zaten. Bu fonksiyonlar ne iş yapıyor bilemediği için gitti üsttekilere baktı
- business_id ile log injection yapabiliyorum dedi. Devamını görmek lazım işte…
- Jsonify outputu content type olarak json verirsen bile, body’i kontrol edebilsen bile browser render ettirtmiyor dedi
![image](https://github.com/grealyve/MDISec-Web-Security-and-Hacking-Notes/assets/41903311/22428575-be4b-4d3f-bb31-a878b1ea0032)
- Line 22’dee geçici log dosyası oluşturuluyor ardından siliniyor, buna injection yapılabilir. Bunu da söyledi
## Deserialization
![image](https://github.com/grealyve/MDISec-Web-Security-and-Hacking-Notes/assets/41903311/197bbc6e-a9c9-43b5-b06d-388b0cda1e06)
- Untrusted source’dan aldığın datayı deserialize ediyosan .Net, Java gibi OOP dillerinde ciddi problem.
- String’den direkt objeye dönme işi var burda.
- “textReader” Deserialize ediliyor, bu da zaten input alanında var ayrıca stringi XML ‘e çeviriyor.
## XSS
![image](https://github.com/grealyve/MDISec-Web-Security-and-Hacking-Notes/assets/41903311/a7f1ddd3-5f66-455e-a775-eb24b3b54d59)
- $upload_name kısmında XSS varmış.
- 21. satır upload_name kullanıcıdan alınıyor ama sanitize ediliyor fakat sanitize etmenin hiçbir önemi yok. Burada HTML encoding yapman lazım.
- 13. satırda echo veriyor burda da XSS varmış
- Ayrıca 19..satırda upload_name kısmında hiçbir validation yok, burda da File Upload vuln. var.
## Arbitrary File Overwrite
![image](https://github.com/grealyve/MDISec-Web-Security-and-Hacking-Notes/assets/41903311/cb661dda-96dc-4e9c-9d45-67caa58a71ca)
- installRepository diyor, bir şeyler yüklenecek.
- Arbitrary file overwriting
- mode’u benden alıyor, repHome’u benden alıyor, repHome’u istallConfig’e yolluyor yani “dest” kontrol ediyoruz. Gidip config dosyası üstüne başka dosya yazır falan yani
## Regular expression Denial of Service(ReDoS)
![image](https://github.com/grealyve/MDISec-Web-Security-and-Hacking-Notes/assets/41903311/39cd7688-e23a-4f27-a889-477e092bb84e)
- ReDoS var burda.
- 36.satırda Regex(search) var.
- Non-Deterministic Finite Automaton
![image](https://github.com/grealyve/MDISec-Web-Security-and-Hacking-Notes/assets/41903311/4f956211-91d2-42ce-952c-b7f47a985142)
- Recursive inner call’a girer bu da DOS’a sebep olur. a ile başlıyor b ile bitmesi gerekiyor, aa ile başlayıp a ile devam ediyor b ile bitiyor…..
- .Net ile yazılıp NFA kullanan motorlarda bu sebep olabilir.
## LDAP Injection
![image](https://github.com/grealyve/MDISec-Web-Security-and-Hacking-Notes/assets/41903311/2f0e756c-a4df-419b-86c4-c8564f9ddb8e)
- LDAP search injection.
- 28.satırda ldapSearchFiler alıyor, filterın içine atyıor, 33te de ldap_seatch ediyor işte. 30.satıda req ile envvar alıyor.
## ZIP Slip
![image](https://github.com/grealyve/MDISec-Web-Security-and-Hacking-Notes/assets/41903311/e979a9b3-e2d3-41f9-9b43-d6add49152be)
- Zip’i decomprise ederken programlama tarafında, çok dikkatli olunmalı. Zip’in içerisindeki syn-linkler ile dosyayı çıkardığında *path traversal check* yapmak lazım
- Yani içerden ../../../ dosyası falan çıkarsa ne bok yiyecen??
## Arbitrary File Deletion
![image](https://github.com/grealyve/MDISec-Web-Security-and-Hacking-Notes/assets/41903311/bc809ed3-fa41-489f-9a51-5c4ccc7bd8dc)
- get_addon_path adından belliymiş
- gidip token alınıyor, temporarily bir path oluşuyor, bu dosya geçerli mi diye bakılıyor, sonra gidip o siliniyor.
- Arbitrary file deletion.
- tmp_token kullaınıcıdan alınıyor ve artık pathi o kontrol ediyor falan…
## XSS
![image](https://github.com/grealyve/MDISec-Web-Security-and-Hacking-Notes/assets/41903311/751b6bca-54cb-419f-ab92-29cd848bb0b4)
- XSS var.
- Html.Raw, Razor template engineinde default context encoding yapmaz. Default contex encodingi HTML ve attribute encoding için yapıyor.
##  Command Injection
![image](https://github.com/grealyve/MDISec-Web-Security-and-Hacking-Notes/assets/41903311/0decf6a2-4723-44d5-bd92-1949a3919d9b)
- Şu patterni gördüğün zaman renkli hikayeler dönüyor demektir. File’a “name” attribute’u atanması lazım burda da 8.satırda bütün alanlarına koymuş zaten
## CORS Bypass
![image](https://github.com/grealyve/MDISec-Web-Security-and-Hacking-Notes/assets/41903311/a681f212-1adc-4cf7-bd30-e61d9e1aa528)
- Cors bypass var:
  - referer header’ı parametre olarak alınıyor
![image](https://github.com/grealyve/MDISec-Web-Security-and-Hacking-Notes/assets/41903311/10967471-05b8-4bb1-8b1c-1aab371b5e44)
- 14.satırda referer değil origin header’ı tarafından check edilmesi lazımmış CORS konusu.
- Origini kontrol edip spoof edemiyoruz fakat referer’ı kontrol edebiliyoruz
## Account Takeover
![image](https://github.com/grealyve/MDISec-Web-Security-and-Hacking-Notes/assets/41903311/68d06b22-ce86-4b4c-bdec-fa93967c0ab5)
- Account takeover…
  - password reset veya acount oluşturma olayı var  bruda
- Sana doğrualam epostası geliyor ya, bu token’ı offline olarak hesaplarsam sıkıntı
- tokenı oluşturma fonksiyonu tahmin edilebilir.
- CSPRNG
## Path Traversal
![image](https://github.com/grealyve/MDISec-Web-Security-and-Hacking-Notes/assets/41903311/f15a910c-d7e5-47aa-a769-f597e57927a9)
- \ ile de bakman lazım…
- image’dan LFI yaparsın akarsın
## XPath Injection
![image](https://github.com/grealyve/MDISec-Web-Security-and-Hacking-Notes/assets/41903311/c1baa1d6-782d-42f0-b9eb-f766c274a42c)
- Kullaınıcdan alınan inputu direkt olmasa da query kısmına yapıştırıyor.
- XPath injection
## SSRF
![image](https://github.com/grealyve/MDISec-Web-Security-and-Hacking-Notes/assets/41903311/7c9d1aa3-9f2a-494e-adbe-099793fb9a06)
## Open Redirect
![image](https://github.com/grealyve/MDISec-Web-Security-and-Hacking-Notes/assets/41903311/f7a32fa1-68b5-496c-98df-e66b227de3d8)
- Django kullanılmış.
- get_success_url returnüne redirect verilmiş
- "next"e [google.com](http://google.com) yazarım akarım
