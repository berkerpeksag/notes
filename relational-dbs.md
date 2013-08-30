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


### Self Referencing Relationships

This is used when a table needs to have a relationship with itself.

For example, let’s say you have a referral program. Customers can refer other
customers to your shopping website. The table may look like this:

```
# CUSTOMERS

customer_id | customer_name | referrer_customer_id
101           John Doe        0
102           Brune Wayne     101
103           James Smith     101
```

This actually can also be similar to “one to many” relationship since one
customer can refer multiple customers.


### Foreign Keys

These keys are used to create relationships between tables.

#### Defining the Foreign Key Explicitly

```sql
CREATE TABLE customers (
    customer_id INT AUTO_INCREMENT PRIMARY KEY,
    customer_name VARCHAR(100)
);

CREATE TABLE orders (
    order_id INT AUTO_INCREMENT PRIMARY KEY,
    customer_id INT,
    amount DOUBLE,
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
);

-- Create some data

INSERT INTO `customers` (`customer_id`, `customer_name`) VALUES
(1, 'Adam'),
(2, 'Andy'),
(3, 'Joe'),
(4, 'Sandy');

INSERT INTO `orders` (`order_id`, `customer_id`, `amount`) VALUES
(1, 1, 19.99),
(2, 1, 35.15),
(3, 3, 17.56),
(4, 4, 12.34);
```

**Note:** Also the Foreign Key column is indexed automatically, unless you
specify another index for it.


### Natural Join

```sql
SELECT * FROM customers NATURAL JOIN orders;
```


### Inner Join

```sql
SELECT * FROM customers JOIN orders
WHERE customers.customer_id = orders.customer_id;
```

The results are the same except a small difference. The `customer_id` column is
repeated twice, once for each table. The reason is, we merely asked the database
to match the values on these two columns. But it is actually unaware that they
represent the same information.

```sql
SELECT * FROM customers JOIN orders
WHERE customers.customer_id = orders.customer_id
AND orders.amount > 15;
```


### ON Clause

This is useful for putting the JOIN conditions in a separate clause.

```sql
SELECT * FROM customers JOIN orders
ON (customers.customer_id = orders.customer_id)
WHERE orders.amount > 15;
```

Now we can distinguish the JOIN condition from the WHERE clause conditions.


### USING Clause

USING clause is similar to the ON clause, but it's shorter. If a column is the
same name on both tables, we can specify it here.

```sql
SELECT * FROM customers JOIN orders
USING (customer_id)
WHERE orders.amount > 15;
```

In fact, this is much like the NATURAL JOIN, so the join column (customer_id) is
not repeated twice in the results.


### Left (Outer) Join

In these queries, if there is no match found from the second table, the record
from the first table is still displayed.

```sql
SELECT * FROM customers
LEFT OUTER JOIN orders
USING (customer_id);
```

This is also useful for finding records that do not have relationships. For
example, we can search for customers who have not placed any orders.

```sql
SELECT * FROM customers
LEFT OUTER JOIN orders
USING (customer_id)
WHERE orders.order_id IS NULL;
```

**Note:** The OUTER keyword is optional. You can just use LEFT JOIN instead of
LEFT OUTER JOIN.


## Right (Outer) Join

A RIGHT OUTER JOIN works exactly the same, but the order of the tables are
reversed.

### Referential Integrity

Referential integrity is a database concept that ensures that relationships
between tables remain consistent. When one table has a foreign key to another
table, the concept of referential integrity states that you may not add a record
to the table that contains the foreign key unless there is a corresponding
record in the linked table.

It also includes the techniques known as cascading update and cascading delete,
which ensure that changes made to the linked table are reflected in the primary
table.


#### Resources

* http://net.tutsplus.com/tutorials/databases/sql-for-beginners-part-3-database-relationships/
