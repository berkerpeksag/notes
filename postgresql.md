# Notes on PostgreSQL

### Uniqueness

* Adding a unique constraint will automatically create a unique B-tree index
  on the column or group of columns listed in the constraint.
  ([Source](https://www.postgresql.org/docs/9.4/static/ddl-constraints.html))
* The preferred way to add a unique constraint to a table is
  `ALTER TABLE ... ADD CONSTRAINT`. *The use of indexes to enforce unique
  constraints could be considered an implementation detail that should not be
  accessed directly.*

  One should, however, be aware that there’s no need to manually create
  indexes on unique columns; doing so would just duplicate the
  automatically-created index.
  ([Source](https://www.postgresql.org/docs/9.4/static/indexes-unique.html))
* To recreate a constraint, without blocking updates while the index is
  rebuilt:

  ```sql
  CREATE UNIQUE INDEX CONCURRENTLY examples_new_col_idx ON examples (new_col);
  ALTER TABLE examples
      ADD CONSTRAINT examples_unique_constraint USING INDEX examples_new_col_idx;
  ```
  ([Source](https://www.postgresql.org/docs/9.4/static/sql-altertable.html))
