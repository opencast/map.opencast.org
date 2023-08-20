Generate Map of Opencast Adopters
=================================

This tool is meant to automatically generate a map of Opencast adopters based
on the submitted via the optional adopter registration.


Interesting Database Parts
--------------------------

The following parts of the database may be interesting for creating the
map.

Make sure to get the latest version of the adoper registration database before running this tool:

```
❯ scp register.opencast.org:/opt/oc_adopter_reg/instance/app.db .
❯ python generate-map.py
```
