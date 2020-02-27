# Project Gutenberg Toolkit

## Overview

`pgtk` is a command line utility, written in Python, to make it easier to search and acquire resources from Project Gutenberg.

It has the following commands:

```
NAME
    pgtk

SYNOPSIS
    pgtk COMMAND

COMMANDS
    COMMAND is one of the following:

     getcat
       Download RDF catalog from Project Gutenburg

     mkdb
       Create db with downloaded RDF data

     query
       Run a query to the catalog table in the database. Don't use a LIMIT clause; instead pass argument.

     search
       Search catalog by fields:  title (ti), creators (cr), and subjects (su). Also: languages (la) defaults to 'EN', types (ty) defaults to 'TEXT', and formats (fo) defaults to '%TEXT/PLAIN%'.

     getpubs
       Download epubs from a list of files generated from a search

     rmcat
       Remove RDF cache from file system
 ```

To install it, do something like this:

* Clone this repo somewhere on your system.
* Create a directory to put `pgtk` resources, i.e. the executible file `pgtk` and the local database that `pgtk` needs to create.
* Set `PGTK_HOME` to this directory. So, in `.bash_profile` enter:
  * `export PGTK_HOME="/where/you/put/pgtk"`
* Run `chmod +x pgtk` to make the file executible and then symlink to an alias in `/usr/local/bin`. Or, you create an alias statement for it in your bash profile to the file.
* Source your bash profile file.
* Your are ready to run `pgtk`.

To use it, do these things:

* Get into a working directory where you want to download content.
* You will first need to download Gutenberg's RDF catalog and import it into the local database. Do this:
   * `pgtk getcat`
* Then:
   * `pgtk mkdir`
   
To find and download content, follow this pattern:
* Search for something
  * `pgtk search au 'Austen'`
* View results
```
31100|AUSTEN, JANE|THE COMPLETE PROJECT GUTENBERG WORKS OF JANE AUSTEN A LINKED INDEX OF ALL PG EDITIONS OF JANE AUSTEN|https://www.gutenberg.org/ebooks/31100.txt.utf-8
42078|AUSTEN, JANE|THE LETTERS OF JANE AUSTEN SELECTED FROM THE COMPILATION OF HER GREAT NEPHEW, EDWARD, LORD BRADBOURNE|https://www.gutenberg.org/ebooks/42078.txt.utf-8
37431|AUSTEN, JANE MACKAYE, STEELE, MRS.|PRIDE AND PREJUDICE, A PLAY FOUNDED ON JANE AUSTEN'S NOVEL|https://www.gutenberg.org/ebooks/37431.txt.utf-8
17797|AUSTEN-LEIGH, JAMES EDWARD|MEMOIR OF JANE AUSTEN|https://www.gutenberg.org/ebooks/17797.txt.utf-8
22536|AUSTEN-LEIGH, WILLIAM AUSTEN-LEIGH, RICHARD ARTHUR|JANE AUSTEN, HER LIFE AND LETTERS: A FAMILY RECORD|https://www.gutenberg.org/ebooks/22536.txt.utf-8
# 5 items returned
```
