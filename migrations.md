# Migrations

### Adding columns

* Safe for readonly models
* Safe when there are no constraints on the column

### Removing columns

* Safe for readonly models

### Renaming columns

* Not safe
* First add a new column, then remove the old one
* When the column is used on SQL queries you'll need to split this in three steps

### Creating tables

* Safe

### Removing tables

* Safe

### Creating indexes

* Safe only for readonly models
* Otherwise make sure you create indexes concurrently

### Removing indexes

* Safe

Reference: http://pedro.herokuapp.com/past/2011/7/13/rails_migrations_with_no_downtime/
