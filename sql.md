# SQL Integrity Constraints

Available contraints are Primary Key, Foreign Key, Not Null, Unique, Check.

Column-level definition :The constraints can be specified immediately after the
column definition.

Table-level definition: The constraints can be specified after all the columns
are defined.

### PRIMARY KEY

This constraint defines a column or combination of columns which uniquely
identifies each row in the table.

```sql
id number(5) PRIMARY KEY

-- or

id number(5) CONSTRAINT emp_id_pk
```

### FOREIGN KEY

This constraint identifies any column referencing the `PRIMARY KEY` in
another table. It establishes a relationship between two columns in the same
table or between different tables.

For a column to be defined as a `FOREIGN KEY`, it should be a defined as a
`PRIMARY KEY` in the table which it is referring.

```sql
CONSTRAINT pd_id_fk FOREIGN KEY(product_id) REFERENCES product(product_id)
```

### NOT NULL

This constraint ensures all rows in the table contain a definite value for the
column which is specified as `NOT NULL`.

### UNIQUE

This constraint ensures that a column or a group of columns in each row have a
distinct value. A column(s) can have a null value but the values cannot be
duplicated.

### CHECK

This constraint defines a business rule on a column. All the rows must satisfy
this rule.

```sql
gender char(1) CHECK (gender in ('M', 'F')),

-- or

CONSTRAINT gender_ck CHECK (gender in ('M', 'F'))
```


## Articles

* [Fun with SQL constraints](http://www.anserinae.net/fun-with-sql-constraints.html)
