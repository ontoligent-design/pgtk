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

To install it, do these things:

* Clone this repo somewhere on your system and mnove the file `pgtk` to a location where it can be called from the command line, e.g. in a `bin` directory that is in your system path.
  * You may also just link `pgtk` in `/usr/local/bin` or create an alias in your bash profile.
* Create a directory to put the database that `pgtk` needs to create.
* Set `PGTK_HOME` to this directory. In `.bash_profile` enter:
  * `export PGTK_HOME="/where/you/put/pgtk"`
* Run `pgtk` in your working directory.

To use it, do these things:

* You first need to download Gutenberg's RDF catalog and import it into the local database. Do:
   * `pgtk download-cache` or `pgtk getcat`
* Then:
   * `pgtk populate-database` or `pgtk mkdir`
   
To find and download content, follow this pattern:
* 
