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
