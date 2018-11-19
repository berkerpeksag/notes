## Event sourcing

* Don't save the current state of objects
* Save the events that lead to the current state
* Create an event for every state change of the object:

  ```
  <BankAccountCreated: id=23 owner=John Doe>
  <DepositPerformed: accountId=12 amount=12 EUR>
  ```

  Then subsequently apply the events from the respective
  `EventStream` to a "blank" object instance.

### Advantages

* Complete log of every state change ever
* Unmatched traceability and debugability
* Very good performance characteristics
* No more mapping objects to tables

### Problems

* Event Sourcing & Command Sourcing confusion:

  **Event Sourcing:**

  - Persist only changes in state
  - Replay can be side-effect free

  **Command Sourcing:**

  - Persist Commands
  - Replay may trigger side-effects

* Side-effects on event replay

  - We don't want side-effects to be replayed: E-Mails sent twice, orders
    placed etc.

* Reporting and queries

  - The persisted event stream does not allow for database queries and reports

* Evolving events

  How to evolve (immutable) events?

  **Reasons for change:**

  - Event no longer relevant (delete)
  - Event fields change (edit)
  - Event names change (rename)

* Concurrent writes

  How to resolve race conditions that occur due to concurrent writes?

  Simple solution: Optimistic locking (e.g. increase the value of the `version`
  field)

---

**Resources**

* https://ookami86.github.io/event-sourcing-in-practice/
* https://microservices.io/patterns/data/event-sourcing.html
* https://community.risingstack.com/when-to-use-cqrs/
* https://sookocheff.com/post/architecture/what-is-cqrs/
* https://martinfowler.com/eaaDev/EventSourcing.html
