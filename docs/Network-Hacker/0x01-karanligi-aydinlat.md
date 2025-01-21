# Network Hacker 0x01 - Karanlığı Aydınlat /w @Barknkilic

Herkese merhaba, bu eğitim serisi boyunca sevgili Mehmet Hocam ve Barkın Hocam'ın [Network Hacker](https://www.twitch.tv/collections/vDZ1memoFhZB7w) playlistindeki eğitim videolarını yazılı hale getireceğim. Aynı zamanda seri boyunca hocalarımın yapmamızı önerdiği toolları geliştireceğim.

## **0x00 : Giriş**
### Network Hacker eğitimi boyunca neler öğreneceğiz?
Ağ güvenliği ve sızma testlerinde kullanılabilecek taktik ve teknik detaylardan bahsedeceğiz.

## **0x01 : OSI**
OSI, genellikle referans modeli olarak kullanılır ve bu yüzden başlangıçta hep bu konuya değinilir. Bu durum, bazı insanların bu konudan soğumasına neden olmuştur. OSI katmanlarına erişmek için [tıklayın](/img/0x01/2.png).

- **Fiziksel Katman:** Kablolar ve donanımların kendilerini ifade ettiği katmandır. Bu sebeple, bu eğitim serisi boyunca bu konulara fazla değinmeyeceğiz. Benim gibi lisans eğitiminde Data Communications dersinde bu kabloların hesaplamalarıyla uğraşmış olanlar, bu katmanın ne kadar tatsız olduğunu anlayacaklardır.
- **Data Link:** Bu katmanda bir ağı keşfetmek istiyorsak kullanacağımız en temel protokol nedir?
  - Katman 2'de, özellikle ethernet ağlarından bahsediyorsak, en temel protokollerden biri `arp` protokolüdür.
  - Fiziki lokasyonlu sistemler, birbirleriyle iletişim kurabilmek için bu protokolü kullanırlar. Örneğin, adresini bildiğiniz bir sisteme paket ulaştırmak istiyorsanız, bu sistemin fiziki konumunu tespit etmeniz gerekir ki paket düzgünce teslim edilebilsin. Katman 2'deki fiziki donanımlar, bu iletişimi kendi içlerinde sağlarlar. Ortada herhangi bir ağ cihazı olmadan, iki bilgisayarı doğrudan bağlayıp haberleşmelerini sağlamak istediğimizde bu protokoller kullanılır.

## **0x02 : Ağ Topolojisi**
![Topoloji](/img/0x01/1.png)
### Kabaca yukarıda bulunan görseli ifade edelim:
R1 router ve sağ tarafındaki kısımlarda yer alan sistemler, kendi içlerinde belirli VLAN (sanal ağlar) tanımlamış olan diğer alt sistemleri ifade eder.

- Çeşitli VLAN'lar vardır. Kurum içerisinde farklı erişim yetkilerine sahip, farklı sistemleri barındırabilecek VLAN tanımları yapılmıştır. 10, 20, 30 gibi ve bunları kabaca bir bina içerisinde konumlanmış, kurumun her katında yer alan farklı departmanlarda çalışması için tanımlanmış sistemler olarak düşünebiliriz.
- Pentest ya da saldırı gerçekleştirecek kişinin ağa dahil olduğu noktadan itibaren nasıl ulaşabildiği, ulaşmak için kullandığı yöntemleri ve bu yöntemler sonucunda hangi sistemlerde neler gözlemleniyor veya neleri bu sistemler içerisinde gözlemleyebiliyor olacağız.

> **Not:** Ağa dahil olduğunuzda, otomatik olarak 10.0.40.2 IP'sine sahip sistem, 10.0.30.4 makinesine erişmek istiyorsa sadece IP adresini biliyor olacaktır. Eğer aynı alt ağ içerisindelerse, yapacakları iş fiziki lokasyon tespitine girmek, yani ARP protokolü üzerinden teslimatı yapmak olacaktır. Ama farklı alt ağlar içerisindelerse, bunların birbirleriyle konuşabilmesi için ARP'ın üzerine diğer katmanlarda yer alan protokollerle iletişimin sağlanması gerekecektir.

## **0x03 : Arp & Wireshark**

![arp](/img/0x01/3.png)

Yukarıda hem ARP başlık bilgisini hem de Ethernet başlık bilgisini görüyoruz. 
Bir ARP paketi içerisinde, fiziki olarak hangi gönderen MAC adresinin olduğu ve hangi hedefteki MAC adresine gönderileceği bilgisi Ethernet başlığında yer alır.
Bunu görmek için bir Kali, bir de Ubuntu'yu sanalda ayağa kaldıracağım ve bir adet ping paketi gönderip Wireshark'tan yakalayacağım.

```bash
ping -c 1 192.168.50.130
```

![wireshark](/img/0x01/4.png)
Burada 192.168.50.129 kaynağından 192.168.50.130 hedefine gönderilmek istenen bir echo request paketini görüyorsunuz. Bu, haberleşmek istediğim diğer bir sisteme göndereceğim mesaj olarak düşünebilirsiniz. 
Öncesinde aslında ben bu sisteme ulaşabilmek için çözmem gereken bir fiziki lokasyon var. Bu lokasyonu da ARP protokolü ile karşı tarafa sorarak gerçekleştirdiğim bir süreç. 
Yani diyorum ki: 
Ben 192.168.50.129 ile haberleşmek istiyorum. Bana fiziki lokasyonunu söylersen, sana ileteceğim bir mesajım var gibi bir süreç ortaya çıkıyor.  

![arp-a](/img/0x01/5.png)

Bunun sonucunda da kendi tarafımda, fiziki lokasyonunu bildiğim bir IP adresinin kaydı oluşuyor. 
Daha sonrasında tekrardan bu isteği, mesajı göndermek istediğimde fiziki lokasyon çözme sürecine yeniden girmiyorum. Beklentim Wireshark'ta ARP protokollerini görmemek.
![wiresharkwithoutarp](/img/0x01/6.png)
Görmeme sebebim, benim artık bu sisteme x gibi bir IP'ye mesaj göndermek için fiziki bir lokasyonunu çözme gibi bir durum söz konusu değil. T0 anında haberleşmek istediğim sistemin fiziki lokasyonunu bilmiyordum, sadece kendisine ait IP adresini biliyordum ve paketi göndermek istediğimde fiziki lokasyondaki ARP'ı kullanarak bu IP adresine sahip olan kim bana bilgisini söylesin, benim de ona göndereceğim mesaj var sorusunu ilettiğimde karşı taraf bana cevap veriyor. Benim fiziki lokasyonum yani MAC adresim budur diyerek cevap veriyor ve fiziki lokasyonu kendi tablom üzerine kaydettiğim zaman bu tablo üzerinden bu soruları sormadan süreçleri atlayarak iletişim kurabiliyoruz. Bu bilgi de tabii ki kalıcı değil, belirli bir süre zarfınca sisteme kayıt oluyor. Bundan sonrasında bu sisteme bir paket gönderdiğimde sistemin IP adresi, MAC adresi veya fiziki lokasyonu değişirse başka bir yere takılırsa bu sistemin baştan sağlanması gerekiyor. Dinamik olarak işlenen bir protokol sonucunu çıkarabiliyoruz. ARP statik olarak işletilebildiği gibi dinamik olarak da işletilebilmesi söz konusu.

## **0x04 : Yapılandırma**
Barkın Hoca'nın tavsiyesi: Özellikle Windows sistemlerde, kendi içerisine ağa dahil olur olmaz otomatik başlattığı ve konuştuğu bir takım protokoller var. Bilgi toplama kısmında da değineceğiz. Eğer bir ağa dahil oluyorsanız, ARP ve IP süreçleri gibi kısımların gerçekleşerek kendinizi o ağın içinde dahil olduğunuzu belirtmeyecek yapıyı sisteminize ayarlamanız lazım. Yapacağımız işlem, TCP/IP protokollerini kapatıp kendi sisteminize hardcore kendi paketlerinizi oluşturarak networkte konuşmak ve mümkün mertebe içeride varlığınızı belli etmeden içeriye bir şekilde dahil olmak ve içeriyi keşfetmeye çalışmak. Ben bunları sanal makinede Kali üzerinden yapıyor olacağım.

Barkın Hocanın Network Pentest Metodolojisi: 
Kendi hostunu, kendi donanımını hiçbir şekilde ağa dahil etmiyor. Bunun sebebi, test yaptığı makine ile kendi makinesinin farklı işletim sistemleri koşturması. İhtiyacı olan işletim sisteminde mümkün mertebe gizli kalırken, kendi hostumda çok alakasız yapmış olduğu trafiklerin ağın içerisinde keşfedilebilir olması, izlenebiliyor olması ve bununla beraber yeri geldiğinde de çeşitli engellemeler varsa bu engellemelere takılmasına sebebiyet verdiği için ağa dahil etmiyor.

Kendi Hostunu susturma işlemi için Linux'ta 
```bash
ip addr
sudo ip addr flush dev <arayüz_adı> // IPv4
sudo sysctl -w net.ipv6.conf.<arayüz_adı>.disable_ipv6=1 // IPv6
```
Sistem, 802.1X protokolünü kullanarak kendini doğrulamaya çalışabiliyor, onu da devre dışı bırakmamız gerekiyor.
 ```bash
nmcli connection show
nmcli connection modify <bağlantı_adı> 802-1x.auth no
nmcli connection down <bağlantı_adı>
nmcli connection up <bağlantı_adı>
```

Bu şekilde hostumu o ağ içerisinden izole etmiş oluyoruz. Şimdi VMware üzerinden network ayarlarından bağlayacağım cihazı izole etmiş olduğum arayüz ile belirttiğim zaman VMware'in bridge protokolü çalışıyor.

Bu sistemi de bir T0 anında ağa dahil ettiğimde iletişimini sınırlamam lazım, bunu sağlayan çeşitli servisler var. Bunlardan birisi networkmanager. Kali üzerinde sistemi ilk çalıştırdığımız andan itibaren otomatik bağlantıyı sağlama ve arka planda çeşitli protokolleri kendi adına konuşup ayarlamaya görevlendirilmiş bir servis vaziyetinde çalışıyor. Bunu da kapatmamız gerekir. Kali ağa dahil olduğunda otomatik olarak IP almaya çalışıp diğer taraflardaki sistemlere kendini belli etmeye başlamasın, bunu da aşağıdaki görseldeki komut ile yapabiliriz. Kapatsak bile bazen DHCP istemcisi kalmış olabilir, dikkat etmek gerekiyor. Aynı şekilde WPA'yı kontrol etmekte fayda var. Çalışıyor olsaydı da killall ile son 2 komutta da görüldüğü üzere öldürüyor olacaktık.

![networking](/img/0x01/7.png)

> **Özet:** 
> 
> Ana işletim sistemini herhangi bir ağa bağladığımızda, herhangi bir şekilde işletim sisteminin ağda otomatik paket üretmesini istemiyoruz. Ben doğrudan fiziksel olarak ana hostumun üzerindeki ethernet kartım veya wifi kartım üzerinden bridge mode ile kullandığım sanal makineye aktarıyorum, aktardığım kısım da bir işletim sistemi olduğu için onda da otomatik olarak paket üreten kısımları kapatmam gerekiyor. Bütün bunları yaparkenki amacım, dahil olduğum ağda keşfedilmemek çünkü kurumsal bir ağda bilgisayarı bağladığın anda işletim sistemim diyor ki bana elektrik geldiği an itibariyle ortamı discover edeceğim, broadcast mesajları gönderiyorum gibi bir network implementasyonu var. Eğer o kurumda gelen ARP protokolündeki MAC adreslerine göre bilgisayarını bağladığın switchin 5. portundan senin MAC adresin gitti ama adamlar MAC'leri real-time takip ediyor, hiç tanımlı olmayan kurumun envanter listesinde bulunmayan bir cihaza denk geldiğinde sen faka basmış olursun.

Bir tane bash betiği yazarak bütün bu süreci tek komutla da yapabilirsiniz.

IP konfigrasyonu silmek için 
```bash
ip addr del 10.0.40.2/24 dev eth0
```

IPv6 kapatmak için : 
```bash
echo 1 > /proc/sys/net/ipv6/conf/eth0/disable_ipv6
```
## **0x05 : Keşif**

Bundan sonra topolojinin başındaki Windows Server konuştuğunda, bizle aynı subnette bir makineyse şayet hangi subnette yer aldığını anlama şansım olacak. Makine gelene kadar switch ile konuşuyor olacağım. CISCO cihazlarının üzerinde kullandıkları bir protokol discovery protokolü, bu protokol sayesinde dahil olmuş olduğumuz ağdaki anahtarlama cihazlarının bilgilerini görüntüleyebiliyor, hangi IOS sürümünün koştuğunu görebiliyoruz. IP konfigrasyonu varsa bunların hangileri olduğunu görebiliyor, hangi porta bağlıysa onu görebiliyorum.

![discovery](/img/0x01/8.png)

Şimdi switchin ürettiği trafikleri anladıysak, bir de sunucunun ürettiği trafiklere bakmak adına Windows Server'ı yeniden başlatalım.

![reboot](/img/0x01/9.png)

Windows açılır açılmaz, ilk etapta ARP ile bir şeyler çözmeye çalışmış. Broadcast basmış, 
10.0.40.3 IP'sini çözmeye çalışmış. Bunu neden yapmaya çalışmıştır? 
Kendisi üzerinde statik bir IP konfigrasyonu girdik, üzerindeki statik IP'nin başka bir IP üzerinde olup olmadığını kontrol etmek için kullanılıyor. ARP üzerinden diyor ki 10.0.40.3 IP'sine sahip olan bir makine var mı bana söylesin.
IP çakışmasını önlemek için. Giden paketin detaylarına bakalım:

![arp](/img/0x01/A.png)

- Gönderen MAC adresi, kendi MAC adres bilgisi üzerinden paketi üretiyor ve oraya ilgili kendi MAC adresi bilgisini yerleştiriyor. 
- Gönderen IP adresi olarak yazdığı değer 0.0.0.0, bu bir hosta atanabilecek IP adresi değil. 
Sebebi ise, bütün internet ağı içerisindeki IP adres havuzunu ifade eden özel bir adres değeri olması. Dolayısıyla bunu herkesle konuşmak için kendisinde IP konfigrasyonu olmadığı zaman bir değer olarak atayabileceği, protokol içerisinde yer alan tanımdan alarak buraya yerleştiriyor.  
- Hedef MAC adresinde de herkesle konuşmak istiyor, bu yüzden hepsi 0. 
Eğer ben kendi MAC adres bilgimi kullanmak istemeseydim ve rastgele herhangi bir MAC adresi yerine generic bir MAC adresi edinmek isteseydim, kaynak kısmına ne yazmam gerekecekti? 
Tamamını f ile doldurması gerekecekti. 
- Hedef IP adresindeki IP de orada keşfetmeye çalıştığı adresten kaynaklı olarak karşımıza çıkıyor. 

Hiç TCP/IP protokolü konuşmayarak, eğer bir ARP paketi üretmek istesem sırayla o an hangi sistemler varsa bunları keşfetmek için ne yapmam gerekir? 
- 10.0.40.3 için yazdıysa, bir sonraki pakette 10.0.40.4'ü, 10.0.40.5'i, o alt ağın genişliği ne kadarsa, hangi IP adresleri bunun içerisinde işaretlenebiliyorsa hepsini sırayla bu paketin benzeri şekilde oluşturup ağ içine gönderiyor olsak, broadcast olduğu için ilgili bana paket üretmesi gerekiyor, dolayısıyla hangi sistemlerin canlı olduğunu bununla keşfetme şansı doğuyor. Dolayısıyla ARP'ı hem keşif için hem de MITM gibi trafiği kendi üzerimizden geçirdiğimiz saldırılarda ele alıyoruz.

## **0x06 : Scapy**
Scapy, bilgisayar ağları için bir paket manipülasyon aracıdır. Ağ paketlerini taklit edebilir veya kodlarını çözebilir, bunları ağa gönderebilir, yakalayabilir ve istekler ile yanıtları eşleştirebilir. Ayrıca tarama, ağ yolu izleme, sondajlama, birim testleri, saldırılar ve ağ keşfi gibi görevleri de yerine getirebilir.

Dahil olduğumuz ağ üzerindeki diğer sistemleri keşfetmeye çalışıyoruz. Scapy'den paketleri oluşturalım:

![scapy](/img/0x01/B.png)
![scapy](/img/0x01/C.png)
![scapy](/img/0x01/D.png)

Topolojiye yeniden dönelim. Kali makine bir switche bağlı ve bu switch'e bağlı bir adet Windows Server'ımız da var. Bunlar bu senaryoda aynı alt ağ olarak da ele alınıyorlar. Hem fiziki olarak aynı sunucuda olmaları hem de alt ağ olarak aynı ağda yer almalarından ötürü bunları ARP üzerinden herhangi bir gateway, router sistemine geçiş yaparak keşfetmeye gerek duymadan fiziki bağlantı kısmından keşif işlemini yapabiliyoruz. 
Ağa dahil olduk ve o ağ içerisinde hangi sistemlerim var sorusunu
Katman 2'de göndereceklerimizi sendp, katman 2 sonrasındakiler için send ile gönderiyoruz.

Şimdi biz ne yaptık? 
Bizim klasik kullandığımız toollar var. arp-scan gibi, netdiscover gibi, ağdaki diğer IP'leri bulmamızı sağlar. Bu toollar arka planda çok fazla IP gönderir, cevap dönen IP'leri toplar ve bu IP'ler canlı olarak karşında der. Bu tool arka planda nasıl çalıştığını görmüş olduk. ARP paketinin ve Ethernet paketinin hangi alanlarına sırayla neler yazıyor ve dönen cevapları nasıl topladığı toolunun mantığını kavramış oluyoruz. 

Ben de daha iyi anlamak adına ufak bir tool yazdım. [ARPDiscover.py](tools/ARPDiscover.py) tıklayarak kaynak koda erişebilirsiniz. 
