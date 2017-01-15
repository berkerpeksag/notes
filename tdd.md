## Test doubles

Meszaros uses the term Test Double as the generic term for any kind of
pretend object used in place of a real object for testing purposes. Meszaros
then defined four particular kinds of double:

* **Dummy** objects are passed around but never actually used. Usually they
  are just used to fill parameter lists.
* **Fake** objects actually have working implementations, but usually take
  some shortcut which makes them not suitable for production (an in memory
  database is a good example).
* **Stubs** provide canned answers to calls made during the test, usually not
  responding at all to anything outside what's programmed in for the test.
  Stubs may also record information about calls, such as an email gateway
  stub that remembers the messages it 'sent', or maybe only how many messages
  it 'sent'.
* **Mocks** are what we are talking about here: objects pre-programmed with
  expectations which form a specification of the calls they are expected to
  receive.


## Mocks vs. Stubs

* A stub uses state verification while a mock uses behavior verification.
* In order to use state verification on the stub, we need to make some extra
  methods on the stub to help with verification (e.g. add
  a `MailServiceStub.numberSent()` method)
* Mock objects always use behavior verification, a stub can go either way.

---

**Reference:** https://www.martinfowler.com/articles/mocksArentStubs.html
