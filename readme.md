Generate Map of Opencast Adopters
=================================

[![Build Status](https://travis-ci.com/opencast/map.opencast.org.svg?branch=master)
](https://travis-ci.com/opencast/map.opencast.org)

*This is still work in progress*

How to use the toolchain
------------------------

This tool is meant to automatically generate a map of Opencast adopters based
on the data submitted when registering for the package repository.


1.Getting the Source Code
-------------------------

You can get the Opencast adopters' map code by cloning the Git repository.

Cloning the Git repository:
git clone git@github.com:opencast/map.opencast.org.git
 

2.Install Dependencies
----------------------

Please make sure to install the following dependencies.
Required:
python>= 3.
geopy>=1.18.1
npm>=6.9.0


3.Build and Start the Script
----------------------------

Start the build process with the following command:
npm run build

run the script: 
python generate-map.py


4.View the map
--------------

use the webpack-dev-server to run the server on port 8080 using npm:

npm run start-dev


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