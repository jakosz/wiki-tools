### wiki-tools 
 
Scripts for processing Wikipedia data dumps

**Warning**: this is a work in progress, poorly documented and not much tested.
Someday I'll integrate these scripts into more high-level tools and document them properly.

---

### Abbreviations:
* p2c: pages-to-categories
* pmh: pages-meta-history
* u2c: users-to-categories
* u2p: users-to-pages
* u2u: users-to-users

### Description, Usage and Examples:

pmh / pages-meta-history

Transforms ..wiki-pages-meta-history.xml.bz2 dumps to (uncompressed) csv tables

$ python pmh.py input_file [output_file]
