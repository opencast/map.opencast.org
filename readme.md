Generate Map of Opencast Adopters
=================================

*This is still work in progress*

This tool is meant to automatically generate a map of Opencast adopters based
on the data submitted when registering for the package repository.


Interesting Database Parts
--------------------------

The following parts of the database may be interesting for creating the
map.

```sql
CREATE TABLE user (
  city TEXT NOT NULL,
  country TEXT NOT NULL,
  created DATETIME NOT NULL,
  department TEXT,
  organization TEXT NOT NULL,
  usage TEXT,
  ...
  PRIMARY KEY (username),
  CHECK (access IN (0, 1)),
  CHECK (admin IN (0, 1)),
  UNIQUE (email)
);
```

The file `user.db` contains a test SQLite database with a few test users around
the world.


Example Map
-----------

[Map created for the 2018 Opencast Summit in Vienna
](https://drive.google.com/open?id=1_GQmB7eKIx5G0YIGzQNhBBIpIi8&usp=sharing)
