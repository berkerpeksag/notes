# "Modern JavaScript" kitabı incelemesi

Kitap genel olarak JavaScript'e hızlı girişten ziyade, "JavaScript ağırlıklı
front-end geliştirmeye hızlı giriş" gibi. Eğer lise ya da üniversitede iseniz
ya da ilk işinize girme arifesindeyseniz ve İngilizcenizi yeterli bulmuyorsanız
bu kitabı gözü kapalı önerebilirim. Ayrıca, tecrübeli bir front-end
geliştiricisi iseniz, takıma yeni katılan genç yeteneklere okuması için bu
kitabı önerebilirsiniz. Bu kitabı bitirdikten sonra, herhangi bir ölçekteki
projeye zorluk çekmeden adapte olacaklardır.

Notlarıma geçmeden önce, kitabın hedef kitlesi için içerik olarak çok çok
doyurucu olduğunu ama yayınevinden kaynaklanan epey eksiklikler olduğunu da
söylemeliyim.


## İçerikli ilgili notlar

* CoffeScript bölümü örnekle de pekiştirilmiş ama bence son bölüm olarak
  konulabilirdi.
* Kitabın adı *modern* ancak `document.querySelector()` gibi bazı modern
  API'lar ve JavaScript'in olası geleceği ECMAScript 6'nın tarayıcı
  geliştiricileri tarafından şimdiden implemente edilen özelliklerinden kısaca
  bahsedilebilirdi.
* Referans olarak W3CSchools gibi bir facia gösterilirken Mozilla Developer
  Network'ten sadece XPath gibi normalde de pek kaynağın olmadığı konularda
  bahsedilmesine içerledim :P
* QUnit'in tanıtıldığı kısımdaki örnek direkt QUnit belgelerinden alınma.
  Resmi belgelerdeki örnekler eğer gerçekten iyi ise kullanılmasında problem
  yok ama en azından kitap boyunca takip edilen kod yazma biçimine ve Türkçe
  değişken, yorum ve method isimleri kullanacak şekilde düzenlenebilirdi.
  Kitaptaki hali jQuery takımının kod standartlarını takip ediyor :)


## Genel notlar

* Bazı cümleler düşük ve birkaç kalıp çok fazla tekrar ediliyor. Mesela çoğu
  kod örneğinin ardından *"Gördüğünüz gibi..."* ile başlayan cümleler var.
* Genel olarak Türkçe kelimelerin anlamlı karşılıkları kullanılmaya dikkat
  edilmiş ancak kitap genelinde tutarlı değil. Bir bölümde *implementasyon*
  kelimesi kullanılırken, diğer bölümde Türkçe karşılığı *uyarlama*
  kullanılmış.
* Kodlar düzenlenip biraz daha az yer kaplar hale getirilebilirmiş. Örneğin
  aşağıdaki kod daha kısa olarak yazılabilir:

  :::html
  <!-- ... -->
  <div class="hede">
      <p>
          Lorem ipsum dolor sit amet.
      </p>
  </div>
* Yeni başlayanlar ve internet erişimi olmayanlar için 3-4 sayfa uzunluğundaki
  kodların kitapta yer alması faydalı olabilir ancak Backbone ile Twitter
  uygulaması yapılan bölümde Twitter'ın döndürdüğü koca bir JSON çıktısı da
  eklenmiş :) En azından ilgili kısım biraz daha kırpılarak gösterilebilirdi.
