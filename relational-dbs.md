## Types of Database Relationships

There are three different types of database relationships, *each named according
to the number of table rows* that may be involved in the relationship.

* One-to-one
* One-to-many
* Many-to-many


### One-to-one

* One-to-one relationships occur when each entry in the first table has one, and
  only one, counterpart in the second table.
* One-to-one relationships are rarely used because it is often more efficient to
  simply put all of the information in a single table.


### One-to-many

**Django example:** https://docs.djangoproject.com/en/dev/topics/db/examples/many_to_one/

* One-to-many relationships occur when each record in the first table
  corresponds to one or more records in the second table but each record in the
  second table corresponds to only one record in the first table.

  **Example:** The relationship between a Teachers table and a Students table in
  an elementary school database would likely be a one-to-many relationship,
  because each student has only one teacher, but each teacher may have multiple
  students.
* They are the most common type of database relationship.


### Many-to-many

* Many-to-many relationships occur when each record in the first table
  corresponds to one or more records in the second table and each record in the
  second table corresponds to one or more records in the first table.

  **Example:** For example, the relationship between a Teachers and a Courses
  table would likely be many-to-many because each teacher may instruct more than
  one course and each course may have more than one instructor.



### Foreign Keys

These keys are used to create relationships between tables.

### Referential Integrity

Referential integrity is a database concept that ensures that relationships
between tables remain consistent. When one table has a foreign key to another
table, the concept of referential integrity states that you may not add a record
to the table that contains the foreign key unless there is a corresponding
record in the linked table.

It also includes the techniques known as cascading update and cascading delete,
which ensure that changes made to the linked table are reflected in the primary
table.
