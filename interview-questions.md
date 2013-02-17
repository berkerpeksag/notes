## "Tarayıcının adres çubuğuna google.com yazdın, enterladıktan sonra sayfanın gösterilmesine kadar arka tarafta hangi teknik işlemler olur?"

* Adres yerel önbellekte var mı diye kontrol edilir
* Adresi protokol, domain ve path olarak ayırır
* Eğer cachelenmediyse domain için DNS lookup yapılır ve hazır verilebilecek durumdaysa onu verir
* Yoksa protokol, domain, port ve path diye böler ve domain için DNS lookup yapar
* Sonra ilgili protokol ve port'a göre sunucuya istek yapar ve path bilgisini verir
* Eğer header'da `Modified-after` gibi bir değer varsa ona göre **sadece şu tarihten sonra değişmişse ver** diyebilir
* Sunucudan dönen yanıta(`200`, `404` vb.) göre body kısmını alır ve eğer `200` geldiyse parse etmeye başlar
* Parse işlemi boyunca gördüğü her resource için aynı işlemi asenkron olarak yapar
* Yine duruma gerektiğinde ya re-render ya da re-flow yapar
