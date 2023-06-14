<h1 align="center">XSS Güvenlik Zafiyeti Part - 2</h1>

Buradan [*XSS Çalışma Tahtası*](https://public-firing-range.appspot.com/) XSS talimlerinizi gerçekleştirebilirsiniz.

## XSS Nedir?
- User input’unun developer’ın JS kodu tarafından kullanılması.
- XSS’in nerede oluştuğunu anlaman çok önemli. innerHTML kodu gidip oraya yerleştiriyor ve Browser bunu tekrar parse ediyor böyle olunca da XSS ortaya çıkıyor. Yani username kısmına```<svg onload=alert(1)>```  yazdığında olay olmuyor.
![image](https://github.com/grealyve/MDISec-Web-Security-and-Hacking-Notes/assets/41903311/9b94408e-dd81-4b71-a634-f3f565f96dbc)
- DOM’u hangi JS fonksiyonları update ediyor bunları bilmek gerekli. Insecure jquery functions:
```javascript
.html()
.append*()
.insert*()
.prepend*()
.wrap*()
.before()
.after()
```
- window.postMessage() :
    - Bir web sitesi başka bir window’u iframe içinde açarsa bu iki iframe’in güvenli bir şekilde iletişim kurmasını sağlayan hikaye. Çok sık kullanılır. (gmaildeki açılan e-postalar)
    
- Bunu sömürmek için başka bir web sitesi kurup, bu web sitesini iframe ile çağıracak. JS ile kendisini iframe ile açan adamın gönderdiği cross mesajları dinleyip aksiyon alan bir JS kodu var aşşağıda.
![image](https://github.com/grealyve/MDISec-Web-Security-and-Hacking-Notes/assets/41903311/fdb0ac0f-b5f2-4b6a-bbd0-ca3335e6c891)
- Yeni web sitesinden bu iframe içerisine POST message ile bir Json göndericez. Bunu aldıktan sonra Json’ı parse ediyor, parse ettiğinin içindeki datayı html kısmını alıp innerHTML olarak yeni bir div açıyor. Div’in içeriğine senden aldığı datayı yazıyor.
  - innerHTML için tehlikeli kısım, window.addEventListener gelen mesajı postMessageHandler fonksiyonuna yönlendiriyor…
![image](https://github.com/grealyve/MDISec-Web-Security-and-Hacking-Notes/assets/41903311/b41a75bf-e08d-4f74-86aa-eb777f06ed72)
- JS bu innerHTML’i alıp DOM’un içine ekliyor.
![image](https://github.com/grealyve/MDISec-Web-Security-and-Hacking-Notes/assets/41903311/093651a9-7e37-4290-8a5d-71706038dccc)
- Böyle bir web sitesi oluşturuyoruz.  Önce iframe yüklenmesini bekliyor, yüklendikten sonra “postMessage” fonksiyonu ile iframe içine Json payloadı yolluyoruz. 
- Senin browser bütün cookie’leri isteğin içine de ekliyor.
```javascript
var payload = {’html’ : ‘<svg onload=alert(1)>’}

var payload = {’html’ : ‘<img src=x onerror=alert(1)>’}
```
bu payload karşıdaki(iframe içindeki) websitesinde çalışır bunu da şu şekilde anlarsın:
```
var payload = {’html’ : ‘<img src=x onerror=alert(document.domain)>’}
```
Bu websitesinin asıl amacı kendi iframeleri arasında iletişim sağlamak. Başka bir iframe içinden gelen istekleri kontrol etmeleri gerekirdi. postMessage()’ların güvenli kaynaktan gelmesi ve innerHTML yerine de sayfanın tüm içeriğini yeniden oraya vermektense(browser’a tekrar yorumlatıyor) data() metodu ile sayfanın datasını değiştirmesi daha iyi olurdu.
