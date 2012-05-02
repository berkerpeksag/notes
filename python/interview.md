## Tail recursion nedir?

Tail recursion yöntemi kullanılmadığında, değerin rekürsif olarak hesaplanabilmesi için her zaman son dönen değere ihtiyaç olduğundan fonksiyon her çalıştığında tekrar stack’e atılır. Bu da yüksek sayılı hesaplamalarla karşılaşıldığında, hafıza kullanımının artmasına ve Stack Overflow gibi hatalara sebep olur. Tail recursion yöntemi ile, fonksiyon her çalıştığında dönen değer, bir argüman olarak gönderilir ve böylece fonksiyon sadece ilk çalıştığında stack’e atılır.

Python tarafından varsayılan olarak desteklenmediği için aşağıdakine benzer bir teknikle uygulanabilir.

**Faktoriyel hesaplama örneği:**

```python
def factorial(n, f=1):
   if n == 0:
       return f
   else:
       return factorial(n - 1, f * n)
```

#### Kaynaklar

* http://c2.com/cgi/wiki?TailRecursion

## Pass-by-value nedir?

Python’da mutable ve immutable olmayan veri tiplerine göre değişir. Örneğin string, immutable olduğu için pass-by-value idir. List ise, append metodu ile pass-by-reference olabilece gibi `x = [1, 2, 3]` şeklinde tekrar tanımlanarak pass-by-value de olabilir.

```python
>>> a = 'Berker'
>>> b = a
>>> print a, b
>>> Berker Berker
>>> a = 'Merve'
>>> print a, b
>>> Merve Berker
```

#### Kaynaklar

* http://stackoverflow.com/questions/986006/python-how-do-i-pass-a-variable-by-reference/986145#986145
* http://javadude.com/articles/passbyvalue.html

## List comprehensions

Haskell’den alınmış bir özellik.

**PHP way:**

```python
results = []
for i in range(20):
   if i % 2 == 0:  # Is even?
       results.append(i)
```

**Python way:**

```python
results = [x for x in xrange(20) if x % 2 == 0]
```

## Generators

Haskell'deki **lazy evaluation**'ın karşılığıdır. `()` arasındaki işlemleri sadece atandığı değişken ya da fonksiyon çağırıldığında üretip, hafızaya atar ve işi bittiğinde siler.

#### Kaynaklar

* https://groups.google.com/forum/#!msg/comp.lang.python/rhW_rIYY5HM/WDOqW02UbRcJ
* http://stackoverflow.com/questions/2573135/python-progression-path-from-apprentice-to-guru/2576240#2576240
* http://www.quora.com/What-are-good-Python-interview-questions
* http://docs.python.org/tutorial/datastructures.html
* http://en.wikipedia.org/wiki/Python_syntax_and_semantics#Generators
* http://python.net/~goodger/projects/pycon/2007/idiomatic/handout.html
* http://stackoverflow.com/questions/101268/hidden-features-of-python

## Fonksiyonel programlama nedir?

> In functional programming, 'functions' are "first class citizens"; like data, they can be manipulated. Functions can work on functions and return a resulting function. Functions that manipulate functions are called functors or higher-order functions.

Bir programı yazmak için, nesneler ve prosedürlerin(procedures) yerine fonksiyonların kullanıldığı programlama dilleridir.

**Kısa notlar:**

* Değişkenler bir kere tanımlandığında ve değer aldıklarında, değerleri bir daha değiştirilemez.

**Çoğu fonksiyonel programlama dili aşağıdaki teknikleri ve özellikleri varsayılan olarak içerir:**

* First class functions
* High order functions
* Lexical closure
* Pattern matching
* Single assigment
* Lazy evaluation
* Garbage collection
* Type inference
* Tail call optimization
* List comprehensions
* Monads

#### Artıları

* Daha kısa programlar
* Daha doğru ve hatasız kodlar
* Diğer dillere göre fonksiyonel programlama dilleriyle çalışmak daha eğlencelidir

#### Kaynaklar

* http://devlicio.us/blogs/christopher_bennage/archive/2010/09/06/what-is-functional-programming.aspx
* http://www.cs.nott.ac.uk/~gmh/faq.html
* http://www.haskell.org/haskellwiki/Functional_programming
* http://projects.tmorris.net/public/how-to-learn-fp/artifacts/0.1/chunk-html/index.html
* http://vimeo.com/13558699
* http://c2.com/cgi/wiki?FunctionalProgramming
* http://c2.com/cgi/wiki?OoVsFunctional
* Interesting read: [The Calculi of Lambda Conversion](http://books.google.com/books?id=KCOuGztKVgcC&lpg=PP1&dq=The%20Calculi%20of%20Lambda%20Conversion&pg=PP1#v=onepage&q&f=false)
